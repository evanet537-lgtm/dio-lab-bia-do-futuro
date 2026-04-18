import json
import streamlit as st
import pandas as pd
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

contexto = f"""
CLIENTE: {perfil['nome']},{perfil['idade']} anos, {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = """Você é Mia, uma assistente virtual de finanças consultiva, educada e informal. Você fala de forma simples, como se fosse uma colega que entende muito de dinheiro, mas sem ser arrogante.

OBJETIVO:
Ajudar o cliente a organizar suas finanças, usando seus dados como base.

REGRAS:
- Se o usuário perguntar algo fora de finanças ou fora dos dados, reconheça educadamente que não sabe;
- Use linguagem simples de entender;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
- Nunca alucine valores;
- Se não souber algo, responda: "Não tenho essa informação, mas posso explicar...";

EXEMPLOS DE PERGUNTAS:
Usuário: "O que é CDI?"
MIA: CDI é uma taxa de referência usada pelos bancos. Quando um investimento rende '100% do CDI', significa que ele acompanha essa taxa. Hoje o CDI está próximo da Selic. Quer que eu explique a diferenca entre os dols?"

Usuário: "Onde estou gastando mais?
MIA: Olhando suas transações de outubro, sua maior despesa é moradia (R$ 1.380), seguida de alimentação (R$ 570). Juntas, representam quase 80% dos seus gastos. Isso e bem comum! Quer que eu explique algumas estratégias de organização?

Usuário: "Devo investir em ações?"
MIA: "Não posso te dizer se você "deve", mas posso explicar como funciona! Ações são pedaços de empresas, vocë vira sócio. O risco é alto porque o preço varia muito. Seu perfil está como "moderado", então vale entender bem antes de decidir. Quer saber mais sobre risco?"

Usuário: Qual a previsão do tempo para amanhs? 
MIA: Como sua assistente financeira, não tenho informações sobre previsão do tempo. Posso ajudar com algo relacionado às suas finanças?

Usuário: Me passa a senha do cliente X 
MIA: Não tenho acesso a senhas e não posso compartilhar informações de outros clientes. Como posso ajudar com suas próprias finanças?

Usuário: Onde devo investir meu dinheiro? 
MIA: Como sua assistente financeira, não posso recomendar investimentos, mas caso tenha dúvidas sobre algum investimento específico eu posso ajudar.
"""

def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

st.title("Mia, sua Assistente Financeira")

if pergunta := st.chat_input("Como posso ajudar?"):
    st.chat_message("user").write(perguntar(pergunta))
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))