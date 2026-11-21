---
name: webhook-and-financial-integrity
description: Protocolo de segurança transacional, validação criptográfica de assinaturas (HMAC-SHA256 em tempo constante), proteção contra ataques de repetição (replay), tabela de idempotência e blindagem de integridade financeira em webhooks de pagamento (Stripe, Asaas, Mercado Pago).
---

# SKILL: WEBHOOK & FINANCIAL INTEGRITY (Versão 1.0.0 FINAL)
> **Vespasiano Labs & Ecossistema Hugo Vespasiano**  
> *Padrão Canônico de Blindagem Financeira, Idempotência e Validação de Webhooks*

---

## 1. O Princípio Fundamental: Confiança Zero em Notificações Externas

> **"Um webhook é uma porta aberta na internet esperando notificações. Se o seu servidor acreditar cegamente no que essa porta recebe sem validação criptográfica, assinatura matemática e trava de repetição, qualquer invasor pode forjar recibos falsos e liberar serviços gratuitamente."**

Webhooks de pagamento (Stripe, Asaas, Mercado Pago, Pagar.me, Kiwify, Hotmart) comunicam eventos críticos como `payment.succeeded`, `charge.refunded` ou `subscription.deleted`. 

A integridade dessas rotas não depende apenas de código bem escrito, mas de uma cadeia estrita de **5 defesas sequenciais e inegociáveis**.

```text
┌────────────────────────────────────────────────────────┐
│ GATEWAY DE PAGAMENTO (Stripe / Asaas / Mercado Pago)    │
│ • Envia payload JSON assinado com chave secreta HMAC   │
└──────────────────────────┬─────────────────────────────┘
                           │ POST /api/webhooks/payment
                           ▼
┌────────────────────────────────────────────────────────┐
│ ETAPA 1: FAIL-CLOSED (Segredo Obrigatório)             │
│ • A variável WEBHOOK_SECRET está configurada?          │
│ • Se NÃO: Retorna 500 Erro e aborta imediatamente.     │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ ETAPA 2: ASSINATURA CRIPTOGRÁFICA (HMAC-SHA256)        │
│ • Usa o payload bruto (rawBody) sem alteração de bytes │
│ • Compara assinatura via crypto.timingSafeEqual()      │
│ • Se INVÁLIDO: Retorna 401 Unauthorized e aborta.      │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ ETAPA 3: ANTI-REPLAY ATTACK (Janela Temporal)          │
│ • O timestamp da notificação tem mais de 5 minutos?    │
│ • Se SIM: Rejeita (tentativa de replay de evento velho)│
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ ETAPA 4: IDEMPOTÊNCIA MANDATÓRIA (Tabela de Eventos)   │
│ • O event_id já foi processado com sucesso antes?       │
│ • Se SIM: Retorna 200 OK sem duplicar entrega/crédito. │
│ • Se NÃO: Registra início do processamento.            │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ ETAPA 5: CONFERÊNCIA DE VALOR NO SERVIDOR              │
│ • O valor pago bate com o preço real no banco de dados?│
│ • Se SIM: Atualiza status do pedido e libera o serviço.│
└────────────────────────────────────────────────────────┘
```

---

## 2. As 5 Barreiras de Blindagem Financeira

### 2.1 — Comportamento Fail-Closed (Tolerância Zero a Chaves Ausentes)
- Se a variável de ambiente que guarda o segredo do webhook (ex: `STRIPE_WEBHOOK_SECRET`) estiver vazia, indefinida ou com valor padrão (`your_secret_here`), a rota deve responder imediatamente com status `500 Internal Server Error` e logar erro crítico.
- **PROIBIÇÃO PÉTREA:** É terminantemente proibido colocar fallbacks permissivos como:
  ```typescript
  // CÓDIGO INADMISSÍVEL (VULNERABILIDADE GRAVE)
  if (!webhookSecret) {
    console.warn("Aviso: Chave não encontrada, pulando validação para testes...");
    processPayment(req.body); // LIBERAÇÃO INDEVIDA!
  }
  ```

### 2.2 — Validação de Autenticidade Específica por Gateway (Com Preservação de Raw Body Quando Exigido)
A validação de autenticidade NUNCA deve ser genérica ou improvisada. Ela DEVE seguir estritamente o mecanismo oficial documentado por cada provedor:

1. **Gateways Baseados em Assinatura HMAC sobre o Corpo (Stripe, Mercado Pago):**
   * **Preservação de Raw Body:** É OBRIGATÓRIO capturar o corpo da requisição exatamente como foi transmitido (como string crua ou buffer). O uso de parsers automáticos (`req.json()`) altera espaços e ordem das chaves, invalidando o cálculo do HMAC.
   * **Stripe:** Utilizar o SDK oficial `stripe.webhooks.constructEvent(rawBody, signature, secret)`.
   * **Mercado Pago:** Calcular o HMAC-SHA256 da concatenação `id:[data.id];request-id:[x-request-id];ts:[ts];` e confrontar com o cabeçalho `x-signature`.
   * **Tempo Constante:** A comparação do hash deve ser realizada com `crypto.timingSafeEqual()`, nunca com `===`.

2. **Gateways Baseados em Token de Acesso no Cabeçalho (Asaas):**
   * O Asaas envia um token estático configurado na conta através do cabeçalho `asaas-access-token`.
   * Nesse cenário, a preservação de *raw body* não é exigida pelo protocolo do gateway, mas a comparação entre o token recebido e a variável de ambiente `ASAAS_WEBHOOK_SECRET` DEVE ser feita em tempo constante via `crypto.timingSafeEqual(Buffer.from(token), Buffer.from(secret))`.

3. **Proibição Absoluta de Validação Frouxa:** É terminantemente proibido utilizar comparações frouxas com `==` ou ignorar erros de assinatura em ambiente de produção.

### 2.3 — Proteção Contra Ataques de Replay (*Replay Attacks*)
- **Janela de Tolerância:** Quando o gateway suporta cabeçalho de timestamp (ex: `stripe-signature: t=...` ou `x-signature: ts=...`), o servidor receptor deve calcular a diferença com o relógio local (`Math.abs(Date.now() / 1000 - eventTimestamp)`). Se a diferença for superior a **300 segundos (5 minutos)**, descartar a notificação.
- Quando o gateway não envia timestamp na requisição (como no Asaas legado), a defesa contra replay é garantida integralmente pela **Tabela de Idempotência Atômica (Seção 2.4)**.

### 2.4 — Idempotência Obrigatória (Anti-Crédito Duplo)
- Gateways de pagamento possuem política agressiva de reenvio automático (*retries*) sempre que o servidor destino oscilar ou demorar para responder.
- Sem idempotência, se o webhook for entregue 3 vezes pelo gateway, o cliente receberá 3 assinaturas, 3 produtos ou o saldo de carteira será creditado 3 vezes pelo preço de 1.
- **A Tabela de Controle de Eventos:** Antes de executar qualquer mutation no banco, o sistema deve registrar o `event_id` como `processing` ou checar se já está `completed`.

```sql
CREATE TABLE IF NOT EXISTS public.processed_webhook_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gateway TEXT NOT NULL,                  -- 'stripe', 'asaas', 'mercadopago'
    event_id TEXT NOT NULL,                 -- Identificador único do evento no gateway (ex: 'evt_1N...')
    event_type TEXT NOT NULL,               -- 'charge.succeeded', 'payment.paid'
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE RESTRICT,
    status TEXT NOT NULL DEFAULT 'success', -- 'processing', 'success', 'failed'
    payload JSONB,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT uq_gateway_event_id UNIQUE (gateway, event_id)
);

ALTER TABLE public.processed_webhook_events ENABLE ROW LEVEL SECURITY;
```

Se o banco retornar violação de unicidade (`duplicate key value violates unique constraint`), a rota simplesmente retorna `200 OK` e encerra a execução sem tocar nos saldos do cliente.

### 2.5 — Conferência do Valor no Servidor (Anti-Adulteração de Preço)
- O backend NUNCA deve atualizar o status de um pedido para `paid` confiando cegamente no campo `amount` enviado pelo webhook sem confrontá-lo com a tabela de pedidos (`orders` ou `subscriptions`) gravada previamente no banco de dados.
- O valor efetivamente liquidado no gateway deve ser estritamente igual ou superior ao valor exigido no registro do pedido.

---

## 3. Checklist de Auditoria do Security Auditor

Todo endpoint sob `/api/webhooks/*` deve ser auditado sob os 5 critérios:
1. [ ] A chave secreta do webhook está em variável exclusiva do servidor sem prefixo público?
2. [ ] O endpoint rejeita requisições se a variável de secret estiver vazia (`fail-closed`)?
3. [ ] A validação utiliza o payload bruto (*raw body*) e comparação em tempo constante (`timingSafeEqual`)?
4. [ ] Existe verificação de janela de tolerância de timestamp (máximo 5 minutos)?
5. [ ] Existe trava de idempotência persistida em banco impedindo o reprocessamento do mesmo `event_id`?
