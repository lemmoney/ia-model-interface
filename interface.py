import streamlit as st
import requests

# Configurações da interface
st.title("Opencashback IA com GPT/Gemini - Versão Beta 0.1")

st.write("""
Insira os detalhes de sua dúvida, escolha o contratante e o modelo desejado para resposta.
""")

# Lista fixa de nomes de contratantes
contractors = ["Electrolux", "Mirra", "Spicy Casa Forte", "Lojas REDE", "Lovebrands LRV", "Lemoneybr Vtex", "Bluk", "Lecadô", "Spicy", "MonteCarlo", "CamisariaFMW", "Interfarma", "Multi", "ohboy", "Dalijou", "LB SJDR", "Anfitria", "Biscoite", "Darkside", "Loja Três", "AmoBeleza", "Puket", "Fisico&Forma", "D+ Carinho", "Me Belisca", "Shopclub", "Imaginarium", "Grande Adega", "LB Patrocinio", "Opencashback", "Komfort House", "Loja3", "Alalala", "Ledur", "Clarinha", "LB Vinhedo"]  # Substitua com seus contratantes reais

# Inputs do usuário
message = st.text_area("Pergunta", value="Digite sua pergunta aqui...")
account_name = st.selectbox("Nome do Contratante", options=contractors)

# Seleção do modelo
model_option = st.selectbox("Escolha o modelo", options=["GPT-4", "Gemini"])

# Variável para armazenar a resposta gerada
response_result = None

# Botão para enviar os dados
if st.button("Enviar Pergunta"):
    if message and account_name:
        # Dados a serem enviados para a API
        payload = {
            "message": message,
            "account_name": account_name,
            "model": model_option  
        }

        # Exibir um spinner enquanto a solicitação é processada
        with st.spinner("Aguarde enquanto sua pergunta está sendo processada..."):
            try:
                # Chamada para a API FastAPI
                response = requests.post("https://us-central1-ock-test.cloudfunctions.net/ock-question", json=payload)
                response_data = response.json()
                
                if response.status_code == 200:
                    st.success("Consulta SQL gerada com sucesso!")
                    response_result = response_data["result"]
                    st.text_area("Resultado", value=response_result, height=300)
                else:
                    st.error(f"Erro: {response_data['detail']}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")
    else:
        st.warning("Por favor, preencha todos os campos antes de enviar.")

# Se uma resposta foi gerada, perguntar ao usuário se foi útil
if response_result:
    st.write("Essa resposta foi útil?")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("👍"):
            # Enviar feedback de que foi útil
            feedback_payload = {
                "account_name": account_name,
                "useful": True,  # Feedback de que foi útil
                "response": response_result,
                "question": message,
                "model": model_option
            }
            try:
                feedback_response = requests.post("https://us-central1-ock-test.cloudfunctions.net/ock-feedback", json=feedback_payload)
                if feedback_response.status_code == 200:
                    st.success("Obrigado pelo seu feedback!")
                else:
                    st.error("Falha ao enviar o feedback.")
            except Exception as e:
                st.error(f"Erro ao conectar com a API de feedback: {str(e)}")

    with col2:
        if st.button("👎"):
            # Enviar feedback de que não foi útil
            feedback_payload = {
                "account_name": account_name,
                "useful": False,  # Feedback de que não foi útil
                "response": response_result,
                "question": message,
                "model": model_option
            }
            try:
                feedback_response = requests.post("https://us-central1-ock-test.cloudfunctions.net/ock-feedback", json=feedback_payload)
                if feedback_response.status_code == 200:
                    st.success("Obrigado pelo seu feedback!")
                else:
                    st.error("Falha ao enviar o feedback.")
            except Exception as e:
                st.error(f"Erro ao conectar com a API de feedback: {str(e)}")
