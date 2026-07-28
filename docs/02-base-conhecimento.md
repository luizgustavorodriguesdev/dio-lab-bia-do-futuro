# Base de Conhecimento do Radar FII

## Dados Utilizados
O Radar FII utiliza uma estratégia híbrida: dados locais (mockados) para entender o cliente e dados em tempo real (via API) para entender o mercado.

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `perfil_investidor.json` | JSON | Define o nível de risco (Conservador a Arrojado) para filtrar recomendações. |
| `transacoes.csv` | CSV | Registra o preço médio de compra e a quantidade de cotas que o usuário já possui. |
| `produtos_financeiros.json` | JSON | Catálogo curado de FIIs com descrições didáticas e classificação (Tijolo/Papel). |
| `historico_atendimento.csv` | CSV | Mantém o histórico de dúvidas anteriores para evitar repetições e dar continuidade. |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Para o Radar FII, os dados originais foram expandidos:

- Tickers B3: Adicionamos o sufixo .SA aos tickers em produtos_financeiros.json para total compatibilidade com a biblioteca yfinance.
- Metas de Renda: No perfil_investidor.json, incluímos um campo de "Meta de Renda Passiva Mensal" para que o agente possa sugerir quanto falta investir para atingir o objetivo.
- Indexadores: Em fundos de papel, mapeamos se o fundo é focado em IPCA+ ou CDI+ para alinhar com o cenário macroeconômico atual.

---

## Estratégia de Integração

### Como os dados são carregados?
> Os dados locais são carregados via Pandas no início da execução da aplicação Streamlit. Eles ficam armazenados no session_state para garantir rapidez nas consultas. Quando o usuário cita um ticker (ex: "MXRF11"), o agente dispara uma chamada assíncrona para a API do Yahoo Finance.


### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

O Radar FII utiliza a técnica de Injeção de Contexto Dinâmico:
- O agente identifica o usuário.
- Busca o perfil e as métricas do mercado.
- Concatena essas informações em uma string estruturada (Markdown) que é enviada como "Contexto" junto com a pergunta do usuário para o Gemini.
---

## Exemplo de Contexto Montado

Abaixo, um exemplo de como o Gemini recebe os dados antes de gerar a resposta:

```
[DADOS DO INVESTIDOR]
- Nome: Carlos Andrade
- Perfil: Moderado (Aceita oscilação em troca de dividendos)
- Carteira Atual: 100 cotas de HGLG11, 50 cotas de KNIP11.

[DADOS DE MERCADO (REAL-TIME)]
- HGLG11: Cotação R$ 165,00 | P/VP: 1.04 | DY (12m): 8.2%
- KNIP11: Cotação R$ 98,50 | P/VP: 0.99 | DY (12m): 11.5%

[PERGUNTA DO USUÁRIO]
"Vale a pena comprar mais HGLG11 hoje ou diversificar?"
...
```
