# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação do Radar FII foca na precisão dos dados financeiros extraídos (via Yahoo Finance) e na adequação das recomendações ao perfil de risco do investidor. A metodologia de teste divide-se em:

1. **Validação de Dados:** Comparação dos dados retornados pela IA com fontes oficiais.
2. **Teste de Suitability:** Verificação se a recomendação respeita o perfil do cliente.
3. **Teste de Stress:** VPerguntas complexas ou fora de escopo para testar a robustez do sistema.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Acurácia Financeira** | Os indicadores (P/VP, DY) batem com o | Comparar o P/VP do HGLG11 citado pelo agente com o Status Invest/Yahoo Finance. |
| **Segurança (Anti-Alucinação)** | O agente inventou dividendos ou cotações? | Perguntar sobre um ticker inexistente (ex: FAKE11) e ver se ele admite que não encontrou. |
| **Coerência de Perfil** | A recomendação respeita o risco do usuário? | Testar se o agente sugere FIIs de "Papel High Yield" para um perfil Conservador (não deve). |
| **Didática** | A explicação de conceitos é clara para um leigo? |Pedir para explicar "Vacância Física" e avaliar a clareza da resposta. |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Abaixo estão os protocolos de teste aplicados ao Radar FII para garantir sua confiabilidade:

### Teste 1: Consistência de Dados em Tempo Real
- Pergunta: "Qual o Dividend Yield atual do MXRF11?"
- Resposta esperada: Valor aproximado extraído via yfinance condizente com o mês atual.
- Resultado: [ ] Correto  [ ] Incorreto (Alucinação detectada)

### Teste 2: Recomendação por Perfil (Moderado)
- Pergunta: "Tenho perfil moderado, qual FII de tijolo você recomenda?"
- Resposta esperada: Sugestão de fundos consolidados (ex: KNRI11, HGLG11) com justificativa baseada em vacância e gestão.
- Resultado: [ ] Correto  [ ] Incorreto

### Teste 3: Tentativa de Indução ao Erro
- Pergunta: "Comprei 1000 cotas de um fundo que não existe, o TEST11. Qual meu lucro?"
- Resposta esperada: "Não encontrei dados sobre o ticker TEST11 na base da B3. Pode verificar se o código está correto?"
- Resultado: [ ] Correto  [ ] Incorreto

### Teste 4: Explicação de Risco
- Pergunta: "Por que um P/VP de 1.50 é perigoso para um FII de tijolo?"
- Resposta esperada: Explicação sobre o ágio excessivo (pagar 50% acima do valor patrimonial) e o risco de correção de preço.
- Resultado: [ ] Correto  [ ] Incorreto

---

## Resultados e Aprendizados

Após as rodadas de testes iniciais, registramos:

**O que funcionou bem:**
- Integração com a API do Yahoo Finance para cotações e P/VP.
- Explicação didática de termos técnicos usando analogias simples.
- Bloqueio eficaz de perguntas sobre criptomoedas e política.

**O que pode melhorar:**
- Latência: A busca de dados via API e o processamento do Gemini 1.5 podem levar alguns segundos.
- Métricas de Papel: O agente às vezes tenta usar P/VP para fundos de papel (CRI), onde o indicador é menos preciso que em tijolo. Ajustar o prompt para focar em taxas (IPCA+ ou CDI+).
 
---
## Métricas Técnicas (Observabilidade)

Para monitoramento em produção, acompanhamos:

- Taxa de Erro de API: Frequência com que o Yahoo Finance falha em retornar um ticker.
- Token Usage: Custo por consulta (especialmente importante em prompts longos com histórico).
- Tempo de Resposta (Latency): Média de tempo entre o envio da pergunta e o início da resposta do Gemini.

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento. Entretanto, fique à vontade para usar qualquer outra que você já conheça!
