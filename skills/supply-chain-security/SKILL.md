---
name: supply-chain-security
description: Protocolo canônico de segurança da cadeia de suprimentos de software (Supply Chain Security): prevenção contra pacotes alucinados por IA (Anti-Slopsquatting), verificação de existência no registry oficial (npm/PyPI), inspeção de scripts de ciclo de vida (postinstall), integridade de lockfiles, auditoria de vulnerabilidades conhecidas e secret scanning no histórico Git com Gitleaks.
---

# SKILL: SUPPLY CHAIN SECURITY & DEPENDENCY GOVERNANCE (Versão 1.0.0 FINAL)
> **Vespasiano Labs & Ecossistema Hugo Vespasiano**  
> *Padrão Canônico de Proteção de Dependências, Registries e Integridade de Código*

---

## 1. O Princípio Fundamental: Dependências São Código de Terceiros Executando com Privilégios Plenos

> **"Dar `npm install` ou `pip install` é conceder permissão total de execução de código na sua máquina e no seu servidor de produção. Modelos de IA frequentemente alucinam pacotes inexistentes com nomes convincentes. Hackers monitoram essas alucinações para registrar malwares com os mesmos nomes. Nenhuma dependência entra no ecossistema sem verificação prévia de proveniência e integridade."**

Esta skill governa a aquisição, auditoria e preservação de dependências externas, neutralizando os ataques de cadeia de suprimentos e alucinações de IA (*Slopsquatting*).

---

## 2. A Regra Anti-Slopsquatting: Verificação Obrigatória Antes de Instalar

**PROIBIDO:** Executar `npm install <pacote>` ou `pip install <pacote>` diretamente por sugestão de IA sem validação no registry oficial.

### Protocolo de 4 Etapas para Adição de Novas Dependências:

```text
┌────────────────────────────────────────────────────────┐
│ 1. JUSTIFICATIVA ARQUITETURAL (Boring Technology)      │
│ • O framework nativo resolve? Se sim, não instale.     │
│ • Vale a pena adicionar um novo fornecedor ao projeto? │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. CONSULTA AO REGISTRY OFICIAL                        │
│ • npm view <pacote> / pypi.org/pypi/<pacote>/json      │
│ • O pacote EXISTE no registry oficial?                 │
│ • Quem é o mantenedor? O repositório bate com o código?│
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. INSPEÇÃO DE SCRIPTS DE CICLO DE VIDA                │
│ • Possui scripts preinstall, install ou postinstall?   │
│ • Se SIM: Inspecionar o script antes de executar!      │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 4. AUTORIZAÇÃO EXPLÍCITA DO PRODUCT OWNER              │
│ • O Agente 01 apresenta o pacote e a justificativa     │
│ • Instalação somente após o "DE ACORDO" do usuário     │
└────────────────────────────────────────────────────────┘
```

> [!WARNING]
> **Idade e Contagem de Downloads NÃO São Prova de Segurança:**  
> Um pacote antigo com milhões de downloads pode ser sequestrado por credenciais vazadas de um mantenedor. Um pacote interno novo da Vespasiano Labs pode ser 100% seguro com 0 downloads. O critério de confiança baseia-se em: proveniência verificável, inspeção de código e integridade do lockfile.

---

## 3. Integridade do Lockfile e Fixação de Versões

1. **Compulsão do Lockfile:** Todo repositório DEVE versionar no Git o seu arquivo de trava (`package-lock.json`, `pnpm-lock.yaml` ou `poetry.lock`).
2. **Checagem de Hash Criptográfico:** O lockfile armazena o checksum SHA-512 do pacote (`integrity: sha512-...`). Isso garante que o que foi testado em desenvolvimento é exatamente o mesmo binário executado no build do CI/CD.
3. **Builds de Produção via `npm ci`:** Em esteiras de integração contínua (CI/CD) e Dockerfiles, usar estritamente `npm ci` em vez de `npm install`, impedindo alterações dinâmicas de dependências na publicação.

---

## 4. Auditoria de Vulnerabilidades Conhecidas

1. **Varredura Periódica:** Antes de cada homologação de versão, rodar no terminal:
   ```bash
   npm audit --audit-level=high
   ```
2. **Tratamento de Vulnerabilidades:**
   * Vulnerabilidades de severidade **Alta** ou **Crítica** em dependências diretas de produção bloqueiam a homologação.
   * Se a vulnerabilidade residir em uma subdependência transitória profunda sem patch upstream disponível, o Agente 01 deve registrar um ADR (Architecture Decision Record) avaliando se o vetor de ataque é alcançável pelo código da aplicação.

---

## 5. Secret Scanning no Histórico Git (Gitleaks)

Segredos não devem ser verificados apenas no estado atual dos arquivos, mas também no histórico completo de commits:
1. **Regra de Ouro:** Remover uma chave de API de um arquivo e fazer um novo commit **NÃO** remove o segredo do repositório. O histórico do Git continua armazenando o token.
2. **Ferramenta Canônica:** Recomenda-se o uso do `gitleaks` para varredura do histórico local:
   ```bash
   gitleaks detect --source . --verbose
   ```
3. **Remediação de Vazamento em Histórico:** Caso uma chave tenha sido commitada no passado:
   * **Ação Primária Imediata:** Revogar e rotacionar a credencial no painel do provedor (Supabase, Asaas, Stripe).
   * **Ação Secundária:** Reescrever o histórico com `git filter-repo` ou `BFG Repo-Cleaner` caso o repositório seja público.
