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
        st.session_state.pop('file_uploader', None)
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
Você é um corretor oficial de redações do ENEM com 15 anos de experiência, profundo conhecimento da Cartilha do Participante do ENEM e dos critérios oficiais do INEP. Sua avaliação é técnica, objetiva e estritamente alinhada ao espelho de correção oficial do INEP. Você não tem medo de atribuir a nota máxima (200) em cada competência se o texto cumprir os requisitos da cartilha. Sua correção é justa e didática.
</role>

<task>
Corrija a redação abaixo avaliando cada uma das 5 competências do ENEM. Para cada competência, analise os elementos exigidos, liste as evidências do texto e, SOMENTE COMO CONCLUSÃO da sua análise, atribua uma nota seguindo obrigatoriamente os níveis oficiais (0, 40, 80, 120, 160 ou 200).
</task>

<competencias>
- **Competência 1 – Domínio da norma culta:** Avalie ortografia, acentuação, morfossintaxe, regência, concordância e pontuação. Cite trechos com erros e corrija-os. Lembre-se que a nota máxima (200) admite até dois desvios menores.
- **Competência 2 – Compreensão da proposta e aplicação de repertório:** Avalie se o participante compreendeu o tema, não fugiu da proposta, e se utilizou repertório sociocultural produtivo e legitimamente articulado ao tema. Se houver repertório legitimado, pertinente e produtivo, a nota máxima (200) deve ser atribuída.
- **Competência 3 – Organização e interpretação de informações:** Avalie a coerência e progressão temática. Verifique se há tese clara, argumentos bem desenvolvidos e ausência de contradições.
- **Competência 4 – Mecanismos de coesão:** Avalie o uso de conectivos, pronomes, conjunções e outros recursos coesivos. Identifique rupturas ou repetições desnecessárias. Presença expressiva de coesão intra e interparágrafos justifica a nota 200.
- **Competência 5 – Proposta de intervenção:** Avalie se a proposta é detalhada, respeita os direitos humanos e contém os 5 elementos obrigatórios: agente, ação, modo/meio, efeito e detalhamento. Se os 5 elementos estiverem claros e explícitos, a nota é obrigatoriamente 200.
</competencias>

<output_format>
Responda estritamente neste formato Markdown:

## Correção da Redação

### Competência 1 – Domínio da Norma Culta
**Erros encontrados:** [cite trechos com erros e corrija-os. Lembre-se: até 2 desvios menores ainda permitem nota 200]
**Análise:** [justifique o nível de domínio da norma padrão com base no texto]
**Sugestão de melhoria:** [orientação prática]
**Nota Final C1:** [0/40/80/120/160/200]

### Competência 2 – Compreensão da Proposta e Repertório
**Repertório utilizado:** [identifique o repertório e avalie se é legitimado, pertinente e produtivo]
**Análise:** [justifique detalhadamente como o tema foi abordado]
**Sugestão de melhoria:** [orientação prática]
**Nota Final C2:** [0/40/80/120/160/200]

### Competência 3 – Organização e Argumentação
**Estrutura identificada:** [descreva o projeto de texto: tese / argumentos / conclusão]
**Análise:** [avalie a progressão temática e desenvolvimento dos argumentos]
**Sugestão de melhoria:** [orientação prática]
**Nota Final C3:** [0/40/80/120/160/200]

### Competência 4 – Coesão Textual
**Recursos coesivos encontrados:** [liste os principais conectivos intra e interparágrafos usados, apontando repetições se houver]
**Análise:** [avalie a fluidez e a articulação entre as partes do texto]
**Sugestão de melhoria:** [orientação prática]
**Nota Final C4:** [0/40/80/120/160/200]

### Competência 5 – Proposta de Intervenção
**Elementos presentes:** [marque ✅ ou ❌ para: Agente, Ação, Modo/Meio, Efeito e Detalhamento]
**Análise:** [justifique a viabilidade e a presença dos elementos]
**Sugestão de melhoria:** [orientação prática]
**Nota Final C5:** [0/40/80/120/160/200]

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
- A nota 200 na Competência 1 não exige perfeição absoluta. O INEP admite até 2 (dois) desvios pontuais se o texto demonstrar excelente domínio geral. Não penalize a nota máxima por erros mínimos e isolados.
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
        max_completion_tokens=5000
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
