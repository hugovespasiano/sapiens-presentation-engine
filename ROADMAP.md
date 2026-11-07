# 🗺️ Roadmap de Desenvolvimento — Sapiens Presentation Engine

Este roadmap define as próximas etapas de evolução, partindo da validação inicial até a fábrica editorial e a futura plataforma comercial.

---

## 📌 Fase 0: Prova de Conceito Técnica (Concluída ✅)
- [x] Teste de manipulação OOXML em Python (`python-pptx` + `lxml`).
- [x] Injeção de transição nativa **Morph** (`<p159:morph option="byObject"/>`).
- [x] Validação da regra do `!!` para sincronização de formas entre slides.
- [x] Teste do layout de **"Antes e Depois" (Comparação Visual)**.
- [x] Integração da identidade visual **Coleção Traço & Saber (v3.5)**.
- [x] Teste de geração de imagens com IA (Aquarela científica via Gemini Imagen 3: oficina artesanal e corte transversal de mina).

---

## 🚀 Fase 1: Fábrica Editorial Sapiens.IA (Próximo Passo)
**Objetivo:** Acelerar a produção das aulas do 6º ao 9º ano da Sapiens.IA para geração de receita imediata.

1. **Cardápio de 5 Arquétipos Mestres (.pptx):**
   - [ ] Abertura / Capa Editorial.
   - [ ] Conceito com Ilustração (Imagem Mestre).
   - [ ] Linha do Tempo Cronológica com Morph.
   - [ ] Antes e Depois / Comparação Visual (validado).
   - [ ] Síntese / Conclusão Pedagógica.
2. **Skill Sapiens no Antigravity (`sapiens-curriculum`):**
   - [ ] Mapeamento do currículo BNCC História (EF06 a EF09).
   - [ ] Prompts padronizados de imagem para a Coleção Traço & Saber.
3. **Pipeline de Geração em Lote:**
   - [ ] Script que recebe uma lista de 5 a 10 aulas e cospe todas as apresentações completas na pasta.

---

## 📱 Fase 2: Módulo Social (Postador Automático de Carrosséis)
**Objetivo:** Transformar o material da aula diretamente em marketing para venda no Instagram e redes sociais.

1. **Exportação Multi-Formato:**
   - [ ] Conversão automática das lâminas para formato quadrado (1:1 / 1080x1080) e vertical (4:5 / 1080x1350).
2. **Gerador de Copy Comercial:**
   - [ ] Criação de legendas automáticas com foco em professores do Fundamental II e hashtags estratégicas.
3. **Agendamento e Publicação:**
   - [ ] Integração com rotinas agendadas (via Antigravity / API de redes) para disparo automático.

---

## 🌐 Fase 3: Plataforma Comercial Web / PWA (Escala de Mercado)
**Objetivo:** Permitir que professores e escolas usem a ferramenta diretamente pelo navegador (computador, tablet ou celular).

1. **Frontend Responsivo:**
   - [ ] Aplicação Web em Next.js + Tailwind CSS + shadcn/ui.
   - [ ] PWA (Progressive Web App) instalável no celular.
2. **Fluxo de Usuário:**
   - [ ] Campo de briefing simples (Tema, Ano Escolar, Quantidade de Slides, Estilo).
   - [ ] Pré-visualização do roteiro antes da geração final.
   - [ ] Botão de download de PowerPoint (.pptx) e PDF.
3. **Monetização e Planos:**
   - [ ] Modelo de créditos ou assinatura mensal para educadores.
