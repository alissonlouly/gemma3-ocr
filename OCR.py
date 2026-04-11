import streamlit as st
import openai
from dotenv import load_dotenv
import os
from PIL import Image
import base64
import google.generativeai as genai

load_dotenv()
# Configuração inicial da página
st.set_page_config(
    page_title="OCR com Gemma-3",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Função para carregar e converter imagem do logo em base64 (de URL)
import requests
def carregar_logo_url(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode()


# Exibir título customizado com logo (usando imagem online)
logo_url = "https://escolaweb.educacao.al.gov.br/uploads/01879b1d-b890-426b-af27-3d5d0b3bb2e4.jpg"
logo_base64 = carregar_logo_url(logo_url)
st.markdown(
    f"""
    <h1><img src='data:image/jpeg;base64,{logo_base64}' width="50" style="vertical-align: -12px;"> OCR Inteligente</h1>
    """,
    unsafe_allow_html=True
)

st.write("Extraia textos de imagens utilizando a tecnologia do modelo **Gemma-3 Vision**.")
st.divider()

# Sidebar com upload e botões
with st.sidebar:
    st.subheader("📤 Envie sua imagem")
    imagem_upada = st.file_uploader("Selecione uma imagem (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    if imagem_upada:
        st.image(imagem_upada, caption="Imagem carregada", use_column_width=True)
        iniciar_ocr = st.button("🔍 Iniciar OCR")
        if st.button("🗑️ Limpar Resultado"):
            st.session_state.pop('resultado_ocr', None)
            st.session_state.pop('texto_ocr', None)
            st.session_state.pop('resultado_correcao', None)
            st.experimental_rerun()

# Função para OCR com modelo vision da OpenAI
def ocr_gemini(image_bytes):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash')
    image = {"mime_type": "image/jpeg", "data": image_bytes}
    response = model.generate_content([
        "Extraia todo o texto manuscrito da imagem. Apenas o texto, sem comentários.",
        image
    ])
    return response.text

# Função para correção de redação ENEM
def corrigir_redacao_enem(texto_redacao):
    api_key = os.getenv("OPENAI_API_KEY")
    language_model = os.getenv("LANGUAGE_MODEL", "gpt-5.4-mini-2026-03-17")
    client = openai.OpenAI(api_key=api_key)
    prompt = f"""
<role>
Você é um corretor oficial de redações do ENEM com 15 anos de experiência, profundo conhecimento da Cartilha do Participante do ENEM e dos critérios oficiais do INEP. Sua correção é rigorosa, justa e didática.
</role>

<task>
Corrija a redação abaixo avaliando cada uma das 5 competências do ENEM. Para cada competência, atribua uma nota seguindo obrigatoriamente os níveis oficiais (0, 40, 80, 120, 160 ou 200) e justifique com exemplos extraídos do próprio texto.
</task>

<competencias>
- **Competência 1 – Domínio da norma culta:** Avalie ortografia, acentuação, morfossintaxe, regência, concordância e pontuação. Cite trechos com erros e corrija-os.
- **Competência 2 – Compreensão da proposta e aplicação de repertório:** Avalie se o participante compreendeu o tema, não fugiu da proposta, e se utilizou repertório sociocultural produtivo e legitimamente articulado ao tema.
- **Competência 3 – Organização e interpretação de informações:** Avalie a coerência e progressão temática. Verifique se há tese clara, argumentos bem desenvolvidos e ausência de contradições.
- **Competência 4 – Mecanismos de coesão:** Avalie o uso de conectivos, pronomes, conjunções e outros recursos coesivos. Identifique rupturas ou repetições desnecessárias.
- **Competência 5 – Proposta de intervenção:** Avalie se a proposta é detalhada, respeita os direitos humanos e contém os 5 elementos obrigatórios: agente, ação, modo/meio, efeito e detalhamento.
</competencias>

<output_format>
Responda estritamente neste formato Markdown:

## Correção da Redação

### Competência 1 – Domínio da Norma Culta
**Nota: [0/40/80/120/160/200]**
**Justificativa:** [análise detalhada]
**Erros encontrados:** [cite trechos e corrija]
**Sugestão de melhoria:** [orientação prática]

### Competência 2 – Compreensão da Proposta e Repertório
**Nota: [0/40/80/120/160/200]**
**Justificativa:** [análise detalhada]
**Repertório utilizado:** [avalie qualidade e pertinência]
**Sugestão de melhoria:** [orientação prática]

### Competência 3 – Organização e Argumentação
**Nota: [0/40/80/120/160/200]**
**Justificativa:** [análise detalhada]
**Estrutura identificada:** [tese / argumentos / conclusão]
**Sugestão de melhoria:** [orientação prática]

### Competência 4 – Coesão Textual
**Nota: [0/40/80/120/160/200]**
**Justificativa:** [análise detalhada]
**Recursos coesivos encontrados:** [liste os usados]
**Sugestão de melhoria:** [orientação prática]

### Competência 5 – Proposta de Intervenção
**Nota: [0/40/80/120/160/200]**
**Justificativa:** [análise detalhada]
**Elementos presentes:** [marque ✅ ou ❌ para cada um dos 5 elementos]
**Sugestão de melhoria:** [orientação prática]

---

## Resultado Final

| Competência | Nota |
|-------------|------|
| C1 – Norma Culta | [nota] |
| C2 – Proposta e Repertório | [nota] |
| C3 – Argumentação | [nota] |
| C4 – Coesão | [nota] |
| C5 – Intervenção | [nota] |
| **TOTAL** | **[soma]** |

## Parecer Geral
[Parágrafo síntese com os principais pontos fortes e fracos da redação, e as 3 prioridades de melhoria mais importantes para o participante.]
</output_format>

<constraints>
- As notas devem ser OBRIGATORIAMENTE um dos valores oficiais: 0, 40, 80, 120, 160 ou 200.
- Nunca atribua nota fora desses valores.
- Se a redação fugir completamente do tema, a Competência 2 recebe nota 0 e as demais recebem no máximo 40.
- Se houver menos de 7 linhas, aplique as penalidades oficiais do INEP.
- Se houver desrespeito aos direitos humanos, a Competência 5 recebe nota 0.
- Cite sempre trechos reais da redação para embasar cada avaliação.
</constraints>

<essay>
{texto_redacao}
</essay>
"""
    response = client.chat.completions.create(
        model=language_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048
    )
    return response.choices[0].message.content

# Processamento do OCR se botão for clicado
if imagem_upada and iniciar_ocr:
    with st.spinner("🔄 Analisando imagem, aguarde..."):
        texto_ocr = ocr_gemini(imagem_upada.getvalue())
        st.session_state['texto_ocr'] = texto_ocr
        st.session_state['resultado_ocr'] = f"### Texto extraído da imagem\n\n{texto_ocr}"

# Botão para corrigir redação
if 'texto_ocr' in st.session_state:
    if st.button("✍️ Corrigir Redação ENEM"):
        with st.spinner("Corrigindo redação, aguarde..."):
            resultado_correcao = corrigir_redacao_enem(st.session_state['texto_ocr'])
            st.session_state['resultado_correcao'] = resultado_correcao

# Exibição dos resultados
st.subheader("📄 Resultado do OCR")
if 'resultado_ocr' in st.session_state:
    st.markdown(st.session_state['resultado_ocr'], unsafe_allow_html=True)
else:
    st.info("Envie uma imagem e clique em 'Iniciar OCR' para ver o resultado aqui.")

if 'resultado_correcao' in st.session_state:
    st.subheader("✅ Correção da Redação ENEM")
    st.markdown(st.session_state['resultado_correcao'], unsafe_allow_html=True)

# Rodapé simplificado
st.divider()
st.caption("🚀 Desenvolvido com ❤️ utilizando o modelo OpenAI Vision + GPT-4o")
