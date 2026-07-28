# Documentação do Agente: Assistente de Fundos Imobiliários (FIIs)

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

Muitas pessoas têm dificuldade em entender como funcionam os Fundos Imobiliários (FIIs), quais são os seus tipos (Tijolo, Papel, FoFs, Fiagros) e como escolher as melhores opções para gerar renda passiva mensal. Além disso, relatórios financeiros de FIIs costumam ser complexos e difíceis de analisar sem conhecimento técnico.

### Solução
> Como o agente resolve esse problema de forma proativa?

Um agente especialista e educativo sobre FIIs que explica conceitos básicos e avançados, analisa o mercado e fornece recomendações de ações práticas (como compra, rebalanceamento ou diversificação em FIIs) de acordo com o perfil do cliente e dados atualizados do mercado.

### Público-Alvo
> Quem vai usar esse agente?

Investidores iniciantes e intermediários que buscam gerar renda passiva com Fundos Imobiliários, mas precisam de orientação clara para tomar decisões conscientes de investimento.

---

## Persona e Tom de Voz

### Nome do Agente
Radar FII *(ou FII.bot)*

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Consultivo, analítico e educativo. O agente se comporta como um consultor financeiro acessível, que simplifica termos do mercado imobiliário sem perder o rigor analítico ao sugerir estratégias de alocação.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Acessível e profissional. Explica jargões técnicos (como *P/VP*, *Dividend Yield*, *Vacância* e *Cap Rate*) de forma didática e objetiva.

### Exemplos de Linguagem
- **Saudação:** "Olá! Sou seu assistente de Fundos Imobiliários. Quer tirar dúvidas sobre FIIs ou prefere analisar uma recomendação para a sua carteira hoje?"
- **Confirmação:** "Entendi! Vou buscar os dados mais recentes desse fundo no Yahoo Finance para avaliar a recomendação ideal para o seu perfil."
- **Erro/Limitação:** "Não consegui obter os dados mais recentes desse FII específico via API no momento, mas posso te explicar as regras gerais de análise desse tipo de fundo."

---
##C omponentes

Componente	Descrição
- Interface	-> Chatbot construído em Streamlit
- LLM	-> Google Gemini (Gemini 1.5 Flash ou Gemini 1.5 Pro via API)
- Base de Conhecimento ->	Conhecimento nativo do Gemini (para conceitos e didática) combinado com integração à API do Yahoo Finance (yfinance em Python) ou APIs públicas (HG Brasil Finance / Status Invest) para cotações, Dividend Yield e P/VP em tempo real.
- Validação -> Camada de verificação de respostas (checagem de limites de risco, adequação ao perfil de investidor e injeção de aviso legal/disclaimer)

## Segurança e Anti-Alucinação
Estratégias Adotadas
[x] Dados em Tempo Real via API: Para cotações, dividendos e métricas numéricas do fundo, o agente consulta diretamente a API do Yahoo Finance/HG Brasil em vez de confiar apenas na memória do modelo.

[x] Uso do Conhecimento Nativo do Gemini: Utiliza a capacidade explicativa do Gemini para simplificar conceitos sobre tipos de FIIs, impostos e estratégias.

[x] Admissão de Limitações: Quando a API de dados falhar ou o fundo não for encontrado, o agente informa a limitação ao usuário em vez de inventar números de cotação ou proventos.

[x] Inclusão de Disclaimer de Investimento: Todas as recomendações de ações contêm um aviso explícito informando que se tratam de sugestões educativas e que a decisão final cabe ao investidor.

[x] Trava de Segurança no Prompt: O prompt do sistema instrui explicitamente o Gemini a responder apenas sobre Fundos Imobiliários e mercado financeiro relacionado.

## Limitações Declaradas
O que o agente NÃO faz?

- Não executa ordens de compra ou venda: O agente fornece análises e sugestões de recomendação, mas não realiza transações na bolsa de valores.

- Não garante rentabilidade futura: O agente não promete retornos fixos ou garantidos, reforçando a natureza da renda variável.

- Não substitui relatórios gerenciais oficiais: O agente compila dados das APIs e relata visões gerais, mas sugere a leitura dos relatórios oficiais dos administradores dos FIIs.

- Não elabora declarações de Imposto de Renda: O agente explica as regras de tributação dos FIIs, mas não faz o preenchimento de obrigações fiscais do usuário.

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Cliente] -->|Mensagem / Carteira| B[Interface - Streamlit]
    B --> C[Gemini LLM]
    C -->|Consulta Indicadores| D[Base de Conhecimento / Yahoo Finance API]
    D -->|Retorna Cotação, P/VP, DY| C
    C --> E[Validação de Regras e Risco]
    E --> F[Resposta + Recomendação de Ação]

