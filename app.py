import streamlit as st
import google.generativeai as genai
import json

# Configuração da página
st.set_page_config(
    page_title="IA Personal Trainer",
    page_icon="💪",
    layout="centered"
)

# Configuração do Google Gemini
if "GOOGLE_API_KEY" not in st.secrets and "GOOGLE_API_KEY" not in st.session_state:
    api_key = st.text_input("Digite sua Google API Key:", type="password")
    if api_key:
        st.session_state["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        st.rerun()
    st.stop()
else:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else st.session_state.get("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

# Estilo personalizado
st.markdown("""
    <style>
    /* Reset e configurações base */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Fundo principal com tema de robô/IA */
    .stApp {
        background: 
            linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%),
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    /* Efeito de grade tecnológica */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 1;
    }
    
    /* Container principal */
    .main .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        position: relative;
        z-index: 2;
    }
    
    /* Título principal com efeito de robô */
    h1 {
        color: #00ffff;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 
            0 0 10px #00ffff,
            0 0 20px #00ffff,
            0 0 30px #00ffff;
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: 2px;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff; }
        to { text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff; }
    }
    
    /* Subtítulo */
    p {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
    }
    
    /* Botões com estilo de robô */
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #ff0080);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 
            0 0 10px rgba(0, 255, 255, 0.5),
            inset 0 0 10px rgba(0, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        max-width: 200px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.8),
            inset 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Campos de entrada com estilo futurista */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #00ffff;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        color: #00ffff;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus-within {
        border-color: #ff0080;
        box-shadow: 0 0 20px rgba(255, 0, 128, 0.5);
        background: rgba(0, 0, 0, 0.9);
    }
    
    /* Slider com estilo de robô */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00ffff, #ff0080);
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    /* Subtítulos com estilo tecnológico */
    h3 {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
        text-align: center;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        letter-spacing: 1px;
    }
    
    /* Separador futurista */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ffff, #ff0080, #00ffff, transparent);
        margin: 2rem 0;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    /* Loading spinner futurista */
    .stSpinner > div {
        border: 3px solid rgba(0, 255, 255, 0.3);
        border-top: 3px solid #00ffff;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Conteúdo gerado pela IA com estilo de terminal */
    .ai-content {
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #00ffff;
        border-radius: 12px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.3),
            inset 0 0 20px rgba(0, 255, 255, 0.1);
        position: relative;
    }
    
    .ai-content::before {
        content: '🤖 IA RESPONSE';
        position: absolute;
        top: -10px;
        left: 20px;
        background: #000;
        color: #00ffff;
        padding: 5px 15px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid #00ffff;
        border-radius: 5px;
    }
    
    .ai-content h1, .ai-content h2, .ai-content h3 {
        color: #00ffff;
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
    }
    
    .ai-content p, .ai-content li {
        color: #e0e0e0;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    
    /* Labels com estilo futurista */
    label {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        margin-bottom: 8px;
        display: block;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        .main .block-container {
            padding: 1rem;
        }
        .stButton > button {
            max-width: 100%;
        }
    }

    /* Spinner de robô personalizado */
    .custom-robot-spinner {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 30px 0;
    }

    .custom-robot-spinner .robot-emoji {
        font-size: 48px;
        animation: robot-bounce 1s infinite alternate;
    }

    @keyframes robot-bounce {
        0% { transform: translateY(0); }
        100% { transform: translateY(-15px); }
    }

    .custom-robot-spinner .text {
        color: #00ffff;
        margin-top: 10px;
        font-size: 1.1rem;
        text-shadow: 0 0 10px #00ffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.title("🤖 FitBot 💪")
st.markdown("Seu treino personalizado com inteligência artificial")
st.markdown("---")

# Inicialização do estado da sessão
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Função para gerar o plano de treino usando IA
def gerar_plano_treino(dados):
    prompt = f"""Atue como um personal trainer profissional experiente e crie um plano de treino detalhado em português.
    Use as seguintes informações do cliente:
    
    - Frequência: {dados['frequencia']} vezes por semana
    - Exercícios favoritos: {dados['exercicios_favoritos']}
    - Tipo de treino desejado: {dados['tipo_treino']}
    - Pontos a melhorar: {dados['pontos_melhorar']}
    
    Crie um plano de treino completo que inclua:
    1. Uma breve introdução personalizada
    2. Divisão semanal dos treinos
    3. Para cada dia de treino:
       - Lista de exercícios
       - Número de séries e repetições
       - Tempo de descanso entre séries
       - Observações técnicas importantes
    4. Dicas de execução e segurança
    5. Sugestões de progressão
    6. Recomendações de aquecimento e alongamento
    
    Use emojis para tornar o plano mais visual e organizado.
    Formate o texto usando markdown para melhor legibilidade.
    """
    
    try:
        # Configurar o modelo
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=1,
            top_k=1,
            max_output_tokens=2048,
        )

        # Inicializar o modelo com o nome correto
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        
        # Gerar resposta com configurações personalizadas
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config
        )

        # Extrair o texto da resposta
        return response.text

    except Exception as e:
        return f"""⚠️ Erro ao gerar o plano de treino: {str(e)}
        
Por favor, verifique sua conexão com a internet e sua API key do Google."""

# Interface do usuário baseada em etapas
if st.session_state.current_step == 0:
    st.markdown("### 📅 Quantas vezes por semana você pode treinar?")
    frequencia = st.slider("Selecione a frequência semanal", 1, 7, 3)
    if st.button("Próximo"):
        st.session_state.frequencia = frequencia
        st.session_state.current_step = 1
        st.rerun()

elif st.session_state.current_step == 1:
    st.markdown("### 💪 Quais são seus exercícios favoritos?")
    exercicios = st.text_area("Liste seus exercícios favoritos", height=100)
    if st.button("Próximo"):
        st.session_state.exercicios_favoritos = exercicios
        st.session_state.current_step = 2
        st.rerun()

elif st.session_state.current_step == 2:
    st.markdown("### 🎯 Qual é seu objetivo de treino?")
    tipo_treino = st.selectbox("Escolha o tipo de treino", 
                              ["Força", "Hipertrofia", "Endurance"])
    if st.button("Próximo"):
        st.session_state.tipo_treino = tipo_treino
        st.session_state.current_step = 3
        st.rerun()

elif st.session_state.current_step == 3:
    st.markdown("### 📈 Quais pontos você quer melhorar?")
    pontos_melhorar = st.text_area("Descreva os pontos que deseja melhorar", height=100)
    if st.button("Próximo"):
        st.session_state.pontos_melhorar = pontos_melhorar
        st.session_state.current_step = 4
        st.rerun()

elif st.session_state.current_step == 4:
    st.markdown("### 🤖 Gerar Plano de Treino")
    dados = {
        "frequencia": st.session_state.frequencia,
        "exercicios_favoritos": st.session_state.exercicios_favoritos,
        "tipo_treino": st.session_state.tipo_treino,
        "pontos_melhorar": st.session_state.pontos_melhorar
    }
    
    if st.button("Gerar"):
        with st.empty():
            st.markdown("""
            <div class="custom-robot-spinner">
                <span class="robot-emoji">🤖</span>
                <span class="text">A IA está gerando seu plano personalizado...</span>
            </div>
            """, unsafe_allow_html=True)
            plano = gerar_plano_treino(dados)
            st.markdown(f"""
            <div class="ai-content">
                {plano}
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("Recomeçar"):
        st.session_state.current_step = 0
        st.rerun() 