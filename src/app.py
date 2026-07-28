import streamlit as st
import google.generativeai as genai
import yfinance as yf
import pandas as pd
import json
import os
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Configuração da página Streamlit
st.set_page_config(page_title="Radar FII - Agente Inteligente", page_icon="🤖", layout="wide")

def load_data():
    default_perfil = {"perfil": "Não Definido", "meta_mensal": 0.0}
    
    try:
        # Carregar Perfil
        if os.path.exists('data/perfil_investidor.json'):
            with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
                perfil = json.load(f)
        else:
            perfil = default_perfil

        # Carregar Produtos
        if os.path.exists('data/produtos_financeiros.json'):
            with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
                produtos = json.load(f)
        else:
            produtos = []

        # Carregar Transações
        if os.path.exists('data/transacoes.csv'):
            transacoes = pd.read_csv('data/transacoes.csv')
        else:
            transacoes = pd.DataFrame()

        return perfil, produtos, transacoes
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return default_perfil, [], pd.DataFrame()

def get_fii_data(ticker):
    if not ticker.endswith(".SA"):
        ticker += ".SA"
    try:
        fii = yf.Ticker(ticker)
        info = fii.info or {}
        
        price = (
            info.get('regularMarketPrice') 
            or info.get('currentPrice') 
            or info.get('previousClose')
            or info.get('regularMarketPreviousClose')
        )
        
        pvp = info.get('priceToBook')
        dy = info.get('trailingAnnualDividendYield') or info.get('dividendYield') or 0
        if dy and dy < 1:
            dy = dy * 100
            
        return {
            "ticker": ticker.replace(".SA", ""),
            "preco": round(price, 2) if price else "N/D",
            "pvp": round(pvp, 2) if pvp else "N/D",
            "dy": f"{dy:.2f}%" if dy else "N/D",
            "nome": info.get('longName', ticker.replace(".SA", ""))
        }
    except Exception:
        return None

def get_gemini_response(prompt, system_instruction):
    candidate_models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
    
    last_exception = None
    raw_response = None
    
    # 1. Tenta a lista de candidatos diretos
    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            response = model.generate_content(prompt)
            if response and response.text:
                raw_response = response.text
                break
        except Exception as e:
            last_exception = e
            continue

    # 2. Se os nomes diretos falharem, consulta dinamicamente os modelos disponíveis
    if not raw_response:
        try:
            available_models = genai.list_models()
            for m in available_models:
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name.replace('models/', '')
                    try:
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=system_instruction
                        )
                        response = model.generate_content(prompt)
                        if response and response.text:
                            raw_response = response.text
                            break
                    except Exception as e:
                        last_exception = e
                        continue
        except Exception as e:
            last_exception = e

    if not raw_response:
        return f"Não foi possível obter resposta da API do Gemini. Detalhes do erro: {last_exception}"

    # Processamento pós-resposta: extrai estritamente o conteúdo após o marcador [RESPOSTA_FINAL]
    text = raw_response
    if "[RESPOSTA_FINAL]" in text:
        text = text.split("[RESPOSTA_FINAL]")[-1].strip()
    elif "RESPOSTA_FINAL" in text:
        text = text.split("RESPOSTA_FINAL")[-1].strip()

    # Filtro complementar de segurança para remover qualquer vestígio de rascunho em inglês
    lines = text.split('\n')
    filtered_lines = []
    
    english_prefixes = (
        "user asks", "user's question", "context:", "constraints:", "role:", 
        "function:", "approach:", "client specifics:", "greeting:", "core function:", 
        "application to user:", "what i can do:", "analyze specific", "suggest portfolio", 
        "evaluate dividend", "monitor market", "language rule:", "expert in fii",
        "paper fund", "hybrid/brick", "brick fund", "shopping malls", "direct answer",
        "didactic", "funded analysis", "no internal monologue", "specific disclaimer",
        "characteristics:", "nature:", "strengths:", "risks:", "metric interpretation",
        "introduction:", "analysis of the asset", "price:", "p/vp:", "dy:", "strategy:",
        "current context", "analyzing the provided data"
    )

    for line in lines:
        clean_line = line.strip().lstrip('*-•"\' ').strip()
        clean_lower = clean_line.lower()
        
        if not clean_line:
            if filtered_lines:
                filtered_lines.append(line)
            continue
            
        # Descarta linhas que contêm prefixos de raciocínio em inglês
        if any(clean_lower.startswith(prefix) or prefix in clean_lower for prefix in english_prefixes):
            continue
            
        # Descarta linhas com formato de metadado (ex: "Role: ...", "Context: ...")
        if ":" in clean_line:
            header_part = clean_line.split(":")[0].strip().lower()
            if header_part in ["role", "context", "constraints", "function", "approach", "greeting", "price", "nature", "strengths", "risks", "introduction", "asset"]:
                continue

        filtered_lines.append(line)
        
    final_text = '\n'.join(filtered_lines).strip()
    
    if final_text.startswith('* ') or final_text.startswith('• ') or final_text.startswith('- '):
        final_text = final_text[2:].strip()
        
    return final_text if final_text else raw_response

def main():
    st.title("🤖 Radar FII: Seu Agente Especialista")
    
    perfil, _, transacoes = load_data()
    
    # Barra Lateral
    with st.sidebar:
        st.header("Configurações")
        api_key = st.text_input("API Key do Gemini", type="password")
        if api_key:
            genai.configure(api_key=api_key)
            
        st.divider()
        st.subheader("Seu Perfil")
        st.write(f"**Classe:** {perfil.get('perfil', 'Moderado')}")
        st.write(f"**Meta Mensal:** R$ {perfil.get('meta_mensal', 0.0):.2f}")
        
        if not transacoes.empty:
            st.subheader("Sua Carteira")
            st.dataframe(transacoes, hide_index=True)

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ex: Vale a pena comprar MXRF11 agora?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not api_key:
                st.error("Por favor, insira sua API Key na barra lateral.")
            else:
                with st.spinner("Analisando mercado..."):
                    words = prompt.upper().split()
                    ticker_found = next((w for w in words if len(w) == 6 and w[4:6].isdigit()), None)
                    
                    market_context = ""
                    if ticker_found:
                        data = get_fii_data(ticker_found)
                        if data and data.get('preco') != "N/D":
                            market_context = (
                                f"\n\n[DADOS DE MERCADO EM TEMPO REAL - {ticker_found}]:\n"
                                f"- Preço Atual: R$ {data['preco']}\n"
                                f"- P/VP: {data['pvp']}\n"
                                f"- Dividend Yield (DY): {data['dy']}"
                            )
                    
                    system_prompt = f"""Você é o "Radar FII", um consultor especialista em Fundos Imobiliários (FIIs) e Fiagros da B3.

Sua tarefa é responder ao cliente de forma clara, amigável, didática e profissional em Português do Brasil.

Dados do Cliente:
- Perfil: {perfil.get('perfil', 'Moderado')}
- Meta Mensal: R$ {perfil.get('meta_mensal', 0.0):.2f}
{market_context}

FORMATO DE RESPOSTA OBRIGATÓRIO:
Sua resposta DEVE começar exatamente com a tag [RESPOSTA_FINAL] na primeira linha, seguida diretamente pela sua mensagem em Português do Brasil. Não escreva nada antes dessa tag.

Exemplo:
[RESPOSTA_FINAL]
Olá! Sou o Radar FII...

Ao final da sua resposta, adicione sempre o seguinte aviso legal:
*Aviso: Esta é uma sugestão baseada em análise de dados e não garante rentabilidade. A decisão final é de sua responsabilidade.*"""

                    response = get_gemini_response(prompt, system_prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()