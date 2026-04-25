import streamlit as st
import google.generativeai as genai
import base64
import requests

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Corretor de Redação ENEM",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = ""

# ── Logo ──────────────────────────────────────────────────────────────────────
def carregar_logo_url(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode()

logo_url = "https://escolaweb.educacao.al.gov.br/uploads/01879b1d-b890-426b-af27-3d5d0b3bb2e4.jpg"
logo_base64 = carregar_logo_url(logo_url)
st.markdown(
    f"""
    <h1><img src='data:image/jpeg;base64,{logo_base64}' width="50" style="vertical-align: -12px;">
    Corretor de Redação ENEM</h1>
    """,
    unsafe_allow_html=True
)
st.write("Envie a foto da redação manuscrita para extração e correção automática pelas **5 competências do ENEM**.")
st.divider()


def obter_api_key_gemini() -> str:
    api_key = st.session_state.get("gemini_api_key", "").strip()
    if not api_key:
        raise ValueError("Informe sua API key do Gemini na barra lateral para usar o app.")
    return api_key

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("🔑 Configuração do Gemini")
    st.text_input(
        "API key do Gemini",
        type="password",
        key="gemini_api_key",
        placeholder="Cole sua chave do Google AI Studio",
        help="A chave fica disponível apenas na sessão atual do app.",
    )

    tem_api_key = bool(st.session_state["gemini_api_key"].strip())
    if tem_api_key:
        st.caption("✅ API key carregada. O app está pronto para uso.")
    else:
        st.warning("Informe sua API key do Gemini para habilitar o OCR e a correção.")

    st.divider()
    st.subheader("📤 Envie sua imagem")
    imagem_upada = st.file_uploader(
        "Selecione uma imagem (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"],
        key="file_uploader"
    )

    if imagem_upada:
        st.image(imagem_upada, caption="Imagem carregada", use_container_width=True)
        iniciar_ocr = st.button(
            "🔍 Iniciar OCR",
            use_container_width=True,
            type="primary",
            disabled=not tem_api_key,
        )
    else:
        iniciar_ocr = False

    st.divider()

    # Botão limpar — reseta tudo via query params para forçar reload limpo
    if st.button("🗑️ Limpar tudo", use_container_width=True):
        for chave in ["resultado_ocr", "texto_ocr", "resultado_correcao"]:
            st.session_state.pop(chave, None)
        st.rerun()

    st.divider()
    st.caption("📌 Modelos em uso:\n\n🔍 **OCR:** Gemini 2.5 Flash\n\n✍️ **Correção:** Gemini 2.5 Flash")


# ── Funções ───────────────────────────────────────────────────────────────────

def ocr_gemini(image_bytes: bytes) -> str:
    """Extrai texto manuscrito da imagem usando Gemini 2.5 Flash."""
    genai.configure(api_key=obter_api_key_gemini())
    model = genai.GenerativeModel("gemini-2.5-flash")
    image = {"mime_type": "image/jpeg", "data": image_bytes}
    response = model.generate_content([
        "Extraia todo o texto manuscrito da imagem com fidelidade máxima. "
        "Retorne apenas o texto extraído, sem comentários ou formatação adicional.",
        image
    ])
    return response.text


def corrigir_redacao_enem(texto_redacao: str) -> str:
    """Corrige a redação pelas 5 competências do ENEM usando Gemini 2.5 Flash."""
    genai.configure(api_key=obter_api_key_gemini())
    model = genai.GenerativeModel("gemini-2.5-flash")

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
    response = model.generate_content(prompt)
    return response.text


# ── Processamento OCR ─────────────────────────────────────────────────────────
if imagem_upada and iniciar_ocr:
    with st.spinner("🔄 Extraindo texto da imagem, aguarde..."):
        try:
            texto_ocr = ocr_gemini(imagem_upada.getvalue())
            st.session_state["texto_ocr"] = texto_ocr
            st.session_state["resultado_ocr"] = f"### Texto extraído da imagem\n\n{texto_ocr}"
            # Limpa correção anterior se existir
            st.session_state.pop("resultado_correcao", None)
        except Exception as e:
            st.error(f"❌ Erro no OCR: {e}")

# ── Botão de correção ─────────────────────────────────────────────────────────
if "texto_ocr" in st.session_state:
    if st.button("✍️ Corrigir Redação ENEM", type="primary", disabled=not bool(st.session_state.get("gemini_api_key", "").strip())):
        with st.spinner("📝 Corrigindo redação, aguarde..."):
            try:
                resultado_correcao = corrigir_redacao_enem(st.session_state["texto_ocr"])
                st.session_state["resultado_correcao"] = resultado_correcao
            except Exception as e:
                st.error(f"❌ Erro na correção: {e}")

# ── Exibição dos resultados ───────────────────────────────────────────────────
st.subheader("📄 Texto Extraído (OCR)")
if "resultado_ocr" in st.session_state:
    st.markdown(st.session_state["resultado_ocr"], unsafe_allow_html=True)
else:
    st.info("Envie uma imagem e clique em **Iniciar OCR** para ver o resultado aqui.")

if "resultado_correcao" in st.session_state:
    st.divider()
    st.subheader("✅ Correção da Redação ENEM")
    st.markdown(st.session_state["resultado_correcao"], unsafe_allow_html=True)

# ── Rodapé ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("📝 Corretor ENEM — OCR e correção com Gemini 2.5 Flash")