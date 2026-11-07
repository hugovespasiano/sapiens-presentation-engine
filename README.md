# Sapiens Presentation Engine 🎓✨

> **"Conteúdo inteligente. Visual extraordinário."**  
> Motor de geração programática de apresentações didáticas premium em PowerPoint nativo (.pptx) com animações Morph, alinhamento à BNCC e suporte à Coleção Traço & Saber da Sapiens.IA.

---

## 🏛️ Sobre o Projeto

O **Sapiens Presentation Engine** é um sistema projetado para automatizar a produção de apresentações didáticas completas, cientificamente confiáveis e visualmente consistentes.

Diferente de geradores genéricos de slides com IA (que criam arquivos estáticos ou layouts frágeis), este motor:
1. **Separa Conteúdo da Renderização:** A IA atua como roteirista pedagógica, enquanto o código Python monta os elementos de forma determinística.
2. **Preserva Animações Nativas:** Utiliza o mecanismo oficial da Microsoft (`!!` no Painel de Seleção) para transições cinematográficas **Morph** entre slides sem corromper o arquivo OOXML.
3. **Aplica a Constituição da Sapiens.IA:**
   - **Regra da Ideia Única:** 1 caixa = 1 ideia principal.
   - **Regra da Palavra-chave Contextualizada:** Conceitos ensinados naturalmente pela própria frase.
   - **Coleção Traço & Saber:** Aquarela científica sobre papel bege (`#F7F3E8`), terracota (`#C28A57`) e azul acinzentado (`#6E8A9D`), sem preto puro e sem cores neon.

---

## ⚙️ Arquitetura do Sistema

```mermaid
flowchart LR
    A[Tema / Plano de Aula] --> B[LLM Planner]
    B --> C[SlideDeckSpec JSON]
    C --> D[Motor de Montagem Python]
    D --> E[Injeção OOXML + Morph Transition]
    E --> F[PowerPoint .pptx Nativo & Editável]
```

### O Segredo Técnico do Morph (`!!`)
Para garantir transições suaves entre slides consecutivos no PowerPoint sem depender de renderizadores pesados:
- O mesmo objeto recebe o prefixo `!!` em slides adjacentes (ex: `!!CardAntes`).
- O script injeta o bloco de transição OOXML compatível com Office 2016/2019/365:
```xml
<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
  <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" p14:dur="1200">
      <p159:morph option="byObject"/>
    </p:transition>
  </mc:Choice>
  <mc:Fallback xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
    <p:transition spd="slow"><p:fade/></p:transition>
  </mc:Fallback>
</mc:AlternateContent>
```

---

## 📂 Estrutura de Arquivos

```text
sapiens-presentation-poc/
├── README.md                                  # Este documento
├── ROADMAP.md                                 # Planejamento das próximas fases
├── requirements.txt                           # Dependências Python
├── sapiens_theme.json                         # Design System oficial (Traço & Saber)
├── generate_deck.py                           # Protótipo 1 (Tema Escuro / Comparação)
├── generate_sapiens_deck.py                   # Gerador Oficial Sapiens.IA (Traço & Saber)
├── artesanato_1750_aquarela.jpg               # Imagem 1: Oficina de Tecelagem (Gemini Imagen 3)
├── mina_carvao_corte_transversal.jpg          # Imagem 2: Corte Transversal da Mina (Gemini Imagen 3)
├── Revolucao_Industrial_Antes_Depois.pptx     # Apresentação gerada (Teste 1)
└── Revolucao_Industrial_Sapiens_Oficial.pptx  # Apresentação gerada (Oficial Sapiens)
```

---

## 🚀 Como Executar em Outro Computador

### 1. Clonar o Repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd sapiens-presentation-poc
```

### 2. Instalar Dependências
Certifique-se de ter o Python 3.10 ou superior instalado:
```bash
pip install -r requirements.txt
```

### 3. Gerar a Apresentação Oficial
Execute o gerador:
```bash
python generate_sapiens_deck.py
```
O arquivo `Revolucao_Industrial_Sapiens_Oficial.pptx` será criado na pasta. Basta dar dois cliques para abrir no PowerPoint e apertar **F5** para assistir à transição Morph em ação.
