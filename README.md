# 🤖 Radar FII: Agente Financeiro Inteligente para Fundos Imobiliários

## Contexto

Os assistentes virtuais no setor financeiro estão evoluindo de simples chatbots reativos para **agentes inteligentes e proativos**. Neste projeto, foi desenvolvido o **Radar FII**, um agente especialista em Fundos Imobiliários (FIIs) que utiliza IA Generativa e dados em tempo real para:

- **Antecipar necessidades:** Identifica oportunidades de diversificação, rebalanceamento e foco em renda passiva mensal.
- **Personalizar recomendações:** Sugere ações de investimento em FIIs (compra, manutenção ou alocação) com base no perfil de risco e objetivos do cliente.
- **Explicar conceitos:** Ensina didaticamente o funcionamento dos FIIs, métricas (*P/VP*, *Dividend Yield*, *Vacância*) e tipos de fundos (Tijolo, Papel, FoFs, Fiagros).
- **Garantir segurança e confiabilidade:** Integra a API do Yahoo Finance e validações no prompt para evitar alucinações e dados numéricos incorretos.

---

## O Que Você Encontra Neste Projeto

### 1. Documentação do Agente
Definição do caso de uso focado em FIIs, persona consultiva, arquitetura do fluxo de dados e estratégias de segurança anti-alucinação.
📄 **Arquivo:** [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md)

---

### 2. Base de Conhecimento
Estratégia de dados combinando arquivos locais (`data/`) para o perfil do investidor e transações com a integração da API do **Yahoo Finance (`yfinance`)** para cotações e proventos atualizados.
📄 **Arquivo:** [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md)

---

### 3. Prompts do Agente
Engenharia de prompts do **Google Gemini**, contendo as regras de comportamento, diretrizes de recomendação, exemplos de diálogo e tratamento de *edge cases*.
📄 **Arquivo:** [`docs/03-prompts.md`](./docs/03-prompts.md)

---

### 4. Aplicação Funcional
Protótipo interativo construído em **Streamlit**, conectado à API do **Google Gemini** e com busca de cotações em tempo real.
📁 **Código:** [`src/app.py`](./src/app.py)

---

### 5. Avaliação e Métricas
Métricas de qualidade, assertividade dos indicadores extraídos, coerência das recomendações com o perfil do investidor e taxa de respostas seguras.
📄 **Arquivo:** [`docs/04-metricas.md`](./docs/04-metricas.md)

---

### 6. Pitch
Roteiro do pitch de 3 minutos apresentando a dor do investidor em FIIs, a solução criada com o Radar FII e o seu diferencial.
📄 **Arquivo:** [`docs/05-pitch.md`](./docs/05-pitch.md)

---

## Tech Stack e Ferramentas

| Categoria | Ferramenta / Biblioteca | Aplicação no Projeto |
|-----------|-------------------------|----------------------|
| **LLM / IA** | **Google Gemini** (1.5 Flash/Pro) | Processamento de linguagem natural, explicações e geração de recomendações |
| **Interface** | **Streamlit** | Interface de chat interativa e visualização de dados da carteira |
| **Dados / Mercado** | **Yahoo Finance (`yfinance`)** | Busca de cotações, P/VP e proventos em tempo real de FIIs da B3 |
| **Linguagem** | **Python 3.10+** | Linguagem principal do projeto |
| **Diagramas** | **Mermaid** | Modelagem do fluxo e arquitetura do agente |

---

## Estrutura do Repositório

```
📁 lab-agente-financeiro/
│
├── 📄 README.md                      # Apresentação geral do projeto Radar FII
│
├── 📁 data/                           # Dados mockados e locais
│   ├── historico_atendimento.csv     # Histórico de interações anteriores
│   ├── perfil_investidor.json        # Perfil de risco e metas do investidor
│   ├── produtos_financeiros.json     # Catálogo de FIIs analisados e categorizados
│   └── transacoes.csv                # Histórico de aportes em FIIs do cliente
│
├── 📁 docs/                           # Documentação do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso, persona, arquitetura e segurança
│   ├── 02-base-conhecimento.md       # Estratégia de integração Gemini + Yahoo Finance
│   ├── 03-prompts.md                 # System prompts e engenharia de contexto
│   ├── 04-metricas.md                # Avaliação de acurácia e anti-alucinação
│   └── 05-pitch.md                   # Roteiro do pitch de apresentação
│
├── 📁 src/                            # Código-fonte da aplicação
│   └── app.py                        # Aplicação interativa em Streamlit
│
└── 📁 assets/                         # Imagens e diagramas do projeto
```

---

## Dicas Finais

1. **Comece pelo prompt:** Um bom system prompt é a base de um agente eficaz
2. **Use os dados mockados:** Eles garantem consistência e evitam problemas com dados sensíveis
3. **Foque na segurança:** No setor financeiro, evitar alucinações é crítico
4. **Teste cenários reais:** Simule perguntas que um cliente faria de verdade
5. **Seja direto no pitch:** 3 minutos passam rápido, vá ao ponto
