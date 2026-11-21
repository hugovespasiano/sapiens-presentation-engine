---
name: web-application-security
description: Diretrizes canônicas para proteção de camadas de aplicação e navegador (OWASP Top 10): Rate Limiting em rotas críticas (login, auth, APIs), segurança estrita de cookies (HttpOnly, Secure, SameSite), controle de CORS e prevenção de CSRF, matriz canônica de Security Headers e CSP (Content Security Policy), validação de Cloudflare Turnstile no servidor (siteverify), blindagem contra SQL Injection em RPCs dinâmicas e telemetria de alertas de incidentes.
---

# SKILL: WEB APPLICATION SECURITY & OWASP HARDENING (Versão 1.0.0 FINAL)
> **Vespasiano Labs & Ecossistema Hugo Vespasiano**  
> *Padrão Canônico de Proteção de Camada Web, Sessões, Cabeçalhos e Formulários*

---

## 1. O Princípio Fundamental: Defesa em Profundidade no Navegador

> **"Proteger a infraestrutura e o banco de dados é inútil se a porta de entrada da aplicação permitir que robôs testem milhares de senhas, sequestrem sessões de usuários via scripts ou forjem ordens a partir de sites maliciosos."**

Esta skill governa os 7 vetores clássicos de vulnerabilidade em nível de aplicação e navegador (OWASP Top 10), transformando boas práticas conceituais em **padrões mandatórios de implementação e auditoria**.

---

## 2. As 7 Diretrizes Canônicas de Aplicação

```text
┌────────────────────────────────────────────────────────┐
│ NAVEGADOR / CLIENTE                                    │
│ • Envia formulário + Cookie de Sessão + Turnstile      │
└──────────────────────────┬─────────────────────────────┘
                           │ POST /api/auth/login
                           ▼
┌────────────────────────────────────────────────────────┐
│ 1. RATE LIMITING (Anti-Brute Force)                    │
│ • Mais de 5 tentativas em 15 min por IP/Conta?         │
│ • Se SIM: Retorna 429 Too Many Requests com Retry-After│
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. TURNSTILE SITEVERIFY (Anti-Robô no Servidor)        │
│ • Consulta API oficial da Cloudflare via HTTPS         │
│ • Token inválido ou expirado? Aborta imediatamente.    │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. CORS & CSRF VALIDATION (Anti-Origem Cruzada)        │
│ • O Origin/Referer bate com a whitelist estrita?       │
│ • Se NÃO: Retorna 403 Forbidden.                       │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ 4. PARAMETERIZED QUERIES (Anti-SQL Injection)          │
│ • Parâmetros sanitizados; zero concatenação de strings │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ 5. COOKIES SEGUROS (Resposta HTTP)                     │
│ • HttpOnly: true | Secure: true | SameSite: 'Lax'      │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ 6. SECURITY HEADERS & CSP (Proteção de Renderização)   │
│ • Content-Security-Policy, X-Frame-Options, HSTS       │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ 7. TELEMETRIA DE INCIDENTES (Sentry Alertas)           │
│ • Registra falhas repetidas e dispara alerta vermelho   │
└────────────────────────────────────────────────────────┘
```

---

### Diretriz 1 — Rate Limiting Operacional em Camada de Aplicação

A ausência de limitador de vazão permite ataques de força bruta (*brute-force*), enumeração de usuários e negação de serviço.

- **Endpoints de Autenticação (`/api/auth/login`, `/api/auth/signin`):**
  - **Teto Estrito:** Máximo de **5 tentativas com falha por intervalo de 15 minutos** por combinação de IP + identificador do usuário (e-mail).
  - **Ação em Excesso:** Retornar HTTP `429 Too Many Requests` com cabeçalho `Retry-After: <segundos>`.
- **Recuperação de Senha (`/api/auth/forgot-password`):**
  - **Teto Estrito:** Máximo de **3 solicitações por hora** por e-mail e por IP, evitando disparo em massa de e-mails via Resend e desgaste da cota transacional.
- **Formulários Públicos e Mutações Anônimas (`/api/contact`, `/api/quote`, `/api/lead`):**
  - **Teto Estrito:** Máximo de **10 requisições por minuto** por IP.
- **Implementação Recomendada:** Upstash Redis (Serverless/Edge), tabela PostgreSQL com limpeza automática ou Cloudflare Rate Limiting Rules no WAF.

---

### Diretriz 2 — Padrão Canônico de Cookies e Sessões

Qualquer cookie utilizado para carregar tokens JWT, identificação de sessão ou estado de autenticação deve ser emitido com os seguintes atributos:

```typescript
// Exemplo canônico de configuração de cookie em Next.js / Node
response.cookies.set('sb-access-token', token, {
  httpOnly: true,                               // PROÍBE acesso via JavaScript (mitiga roubo via XSS)
  secure: process.env.NODE_ENV === 'production', // Trafega estritamente via HTTPS criptografado
  sameSite: 'lax',                              // Impede envio automático em links externos maliciosos
  path: '/',
  maxAge: 60 * 60 * 24 * 7                      // 7 dias de expiração controlada
});
```

- **`httpOnly: true` (Obrigatório):** Impede que códigos maliciosos injetados no cliente acessem o cookie através de `document.cookie`.
- **`secure: true` (Obrigatório em Produção):** Garante que o navegador nunca transmita o cookie através de conexões `http://` abertas.
- **`sameSite: 'lax'` ou `'strict'` (Obrigatório):** `lax` é o padrão seguro para SPAs e navegação web comum; operações financeiras ou administrativas ultra-críticas devem adotar `strict`. É expressamente proibido usar `sameSite: 'none'` sem justificação formal em ADR e sem `secure: true`.

---

### Diretriz 3 — Política Restrita de CORS e Prevenção de CSRF

- **Whitelist Explícita de Origens (CORS):**
  - As rotas de API da aplicação devem ler a variável de ambiente `ALLOWED_ORIGINS` (ex: `https://app.seudominio.com.br,https://admin.seudominio.com.br`).
  - **Veto Pétreo:** É terminantemente proibido utilizar curinga `Access-Control-Allow-Origin: *` em endpoints que aceitam credenciais (`Access-Control-Allow-Credentials: true`) ou tokens de sessão.
- **Validação de Cabeçalhos Anti-CSRF:**
  - Para todas as mutações (`POST`, `PUT`, `DELETE`, `PATCH`), o servidor deve inspecionar os cabeçalhos `Origin` ou `Referer`.
  - Se o cabeçalho estiver presente e seu domínio não pertencer à lista de origens autorizadas da aplicação, o servidor deve rejeitar a requisição imediatamente com `403 Forbidden`.

---

### Diretriz 4 — Matriz Canônica de Security Headers e CSP

Toda aplicação em produção deve injetar os seguintes cabeçalhos de segurança em todas as respostas HTTP (via `next.config.js`, middleware ou Cloudflare Transform Rules):

```text
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://challenges.cloudflare.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https: blob:; font-src 'self' data:; connect-src 'self' https://*.supabase.co https://*.sentry.io https://challenges.cloudflare.com; frame-src https://challenges.cloudflare.com; frame-ancestors 'none'; object-src 'none'; base-uri 'self';
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), browsing-topics=()
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

- **`Content-Security-Policy` (CSP):** Delimita quais servidores e scripts podem ser executados pelo navegador, neutralizando injeção de scripts maliciosos de terceiros.
- **`X-Frame-Options: DENY`:** Proíbe terminantemente que a aplicação seja renderizada dentro de `<iframe>` de outros sites, eliminando qualquer risco de *Clickjacking*.
- **`X-Content-Type-Options: nosniff`:** Força o navegador a respeitar o tipo MIME declarado pelo servidor, impedindo que arquivos de texto ou imagens sejam executados como JavaScript.
- **`Permissions-Policy`:** Desativa permissões de hardware invasivas (câmera, microfone, geolocalização) que a aplicação não utiliza.
- **`Strict-Transport-Security` (HSTS):** Força conexões HTTPS durante 2 anos (`max-age=63072000`).

---

### Diretriz 5 — Protocolo de Validação de Turnstile no Servidor (`siteverify`)

A inclusão do widget visual do Cloudflare Turnstile no frontend **não garante proteção** se o backend aceitar o formulário sem conferência ativa na API da Cloudflare.

```typescript
// Padrão canônico de validação no servidor
export async function validateTurnstileToken(token: string, clientIp?: string): Promise<boolean> {
  const secretKey = process.env.CLOUDFLARE_TURNSTILE_SECRET_KEY;
  if (!secretKey) {
    console.error("ERRO CRÍTICO: CLOUDFLARE_TURNSTILE_SECRET_KEY não configurada.");
    return false; // Fail-closed
  }

  const formData = new URLSearchParams();
  formData.append('secret', secretKey);
  formData.append('response', token);
  if (clientIp) formData.append('remoteip', clientIp);

  const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: formData,
  });

  const outcome = await res.json();
  return outcome.success === true;
}
```

- **Fail-Closed:** Se a chave de secret não existir ou a chamada falhar, o cadastro/login deve ser recusado.
- **Token Descartável (One-Time Token):** O token gerado tem validade curta (até 5 minutos). O backend nunca deve processar uma requisição cujo token retorne `success: false`.

---

### Diretriz 6 — Blindagem Contra SQL Injection em RPCs Dinâmicas

Embora o Supabase e o PostgREST parametrizem consultas comuns nativamente, o risco de SQL Injection reaparece em funções PostgreSQL personalizadas (`SECURITY DEFINER` / RPCs) que utilizam SQL dinâmico.

- **Proibição de Concatenação Crua:** É TERMINANTEMENTE PROIBIDO concatenar strings de entrada diretamente em queries de banco:
  ```sql
  -- VULNERABILIDADE GRAVE (SQL Injection direto)
  EXECUTE 'SELECT * FROM clients WHERE name = ''' || user_input || '''';
  ```
- **Uso Obrigatório de Formatadores Seguros no PostgreSQL:**
  ```sql
  -- PADRÃO SEGURO: Usando %L (Literal sanitizado) ou %I (Identificador)
  EXECUTE format('SELECT * FROM clients WHERE name = %L', user_input);
  
  -- OU PADRÃO COM CLÁUSULA USING (Parâmetro posicional)
  EXECUTE 'SELECT * FROM clients WHERE name = $1' USING user_input;
  ```
- **Auditoria de Parâmetros:** Toda função RPC que recebe texto livre deve ser inspecionada sob a regra: *se contiver `EXECUTE`, exige `%L`, `%I` ou cláusula `USING`*.

---
### Diretriz 7 — Monitoramento e Alertas de Incidentes (Sentry & Brute-Force)

O monitoramento não deve ser um repositório passivo de logs de erro, mas um mecanismo ativo de disparo de alertas diante de anomalias:

- **Alerta de Força Bruta:** Mais de 10 respostas `401 Unauthorized` consecutivas para a mesma conta ou mesmo IP em menos de 5 minutos deve emitir log de alerta `CRITICAL` no Sentry e notificar a equipe.
- **Alerta de Tentativa de Invasão de Tenant / IDOR:** Qualquer resposta `403 Forbidden` disparada em rotas protegidas deve ser registrada com o `auth.uid()`, `tenant_id` solicitado e IP de origem.
- **Procedimento de Resposta a Incidentes:**
  1. Identificação do IP ou usuário abusivo.
  2. Bloqueio temporário no Cloudflare WAF (*IP Access Rules / Block*).
  3. Invalidação imediata de sessões ativas da conta suspeita no Supabase Auth.

---

### Diretriz 8 — Prevenção e Testes Rigorosos de XSS (Cross-Site Scripting)

O React e o Next.js já aplicam escape automático para strings no JSX (`<div>{variavel}</div>`). No entanto, o risco de XSS ressurge quando a aplicação interage com HTML bruto, atributos dinâmicos ou APIs do navegador:

1. **Escape Contextual Nativo em Primeiro Lugar:**
   * Nunca converta texto simples em HTML. Strings comuns devem ser sempre renderizadas diretamente no JSX, permitindo que o React neutralize `<script>`, `onerror` e outros vetores nativamente.

2. **Proibição Canônica de `dangerouslySetInnerHTML`:**
   * O uso de `dangerouslySetInnerHTML` é **PROIBIDO por padrão**.
   * *Regime de Exceção:* Só é permitido se a funcionalidade exigir intrinsecamente a renderização de HTML rico (ex: editor de texto formatado, laudos técnicos gerados com formatação externa).
   * Toda exceção deve ser obrigatoriamente documentada em comentário no código e precedida de sanitização contextual comprovada.

3. **Sanitização Obrigatória com DOMPurify (Onde HTML Rico For Inevitável):**
   * Quando HTML não confiável precisar ser renderizado, deve ser purificado com biblioteca homologada (ex: `dompurify` ou `isomorphic-dompurify` para SSR):
     ```typescript
     import DOMPurify from "isomorphic-dompurify";

     // PADRÃO SEGURO: Sanitização estrita antes da renderização
     const cleanHtml = DOMPurify.sanitize(untrustedHtml, {
       ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'ul', 'li', 'br'],
       ALLOWED_ATTR: []
     });
     ```
   * *Aviso:* A mera importação do DOMPurify não comprova segurança se a configuração permitir tags perigosas (`<script>`, `<iframe>`, `<object>`) ou atributos de eventos (`onload`, `onerror`).

4. **Sanitização de Atributos e Links Dinâmicos:**
   * URLs passadas em links (`<a href={userUrl}>`) devem ser validadas para rejeitar protocolos pseudo-URI (`javascript:`, `data:text/html`):
     ```typescript
     function isSafeUrl(url: string): boolean {
       try {
         const parsed = new URL(url, 'https://example.com');
         return ['http:', 'https:', 'mailto:', 'tel:'].includes(parsed.protocol);
       } catch {
         return false;
       }
     }
     ```

5. **Evolução da CSP (Content Security Policy):**
   * A política CSP do `next.config.ts` deve planejar a eliminação progressiva de `'unsafe-inline'` em scripts através de nonces gerados dinamicamente no Middleware ou hashes SHA-256 de scripts estáticos.

6. **Protocolo de Testes de XSS:**
   * O Auditor Cético deve testar os 3 vetores:
     - **XSS Armazenado (Stored):** Cadastrar nome de cliente ou laudo contendo `<img src=x onerror=alert(1)>` e verificar se a tela do dashboard escapa o payload.
     - **XSS Refletido (Reflected):** Passar parâmetros na URL como `?error=<script>alert(1)</script>` e conferir se a resposta trata como texto.
     - **XSS Baseado em DOM:** Inspecionar manipulações de `window.location` ou `document.write`.

---

## 3. Checklist do Security Auditor

1. [ ] Rotas de login e recuperação de senha possuem rate limit ativo no servidor?
2. [ ] Cookies de sessão contêm `HttpOnly`, `Secure` e `SameSite=Lax/Strict`?
3. [ ] A API rejeita requisições com `Origin` não autorizado (whitelist de CORS)?
4. [ ] A resposta HTTP inclui os 6 cabeçalhos de segurança canônicos (CSP, X-Frame-Options, HSTS, etc.)?
5. [ ] O token do Cloudflare Turnstile é validado no backend via endpoint `siteverify`?
6. [ ] Funções PostgreSQL dinâmicas (`EXECUTE format`) utilizam estritamente `%L` ou `USING`?
7. [ ] Tentativas anormais de login disparam alerta de incidentes no Sentry?
8. [ ] O código está livre de `dangerouslySetInnerHTML` não justificado e não sanitizado?
9. [ ] Links externos com atributos dinâmicos são validados contra `javascript:`?
10. [ ] Testes de XSS armazenado e refletido foram executados nos formulários públicos?
