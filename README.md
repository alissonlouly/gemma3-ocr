
# Gemma3-OCR: Correção Automática de Redação Manuscrita

Este app permite extrair o texto de uma redação manuscrita (imagem) e corrigi-la automaticamente segundo as competências do ENEM, usando IA generativa (Google Gemini para OCR e OpenAI GPT para correção).

## Funcionalidades
- Upload de imagem da redação manuscrita (PNG, JPG, JPEG)
- Extração automática do texto manuscrito (OCR)
- Correção detalhada segundo as 5 competências do ENEM
- Interface simples via Streamlit

## Como usar
1. **Clone o repositório:**
	```bash
	git clone https://github.com/alissonlouly/gemma3-ocr.git
	cd gemma3-ocr
	```
2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```
3. **Instale as dependências:**
	```bash
	pip install -r requirements.txt
	```
4. **Configure as chaves de API:**
	- Crie um arquivo `.env` na raiz do projeto com:
	  ```env
	  OPENAI_API_KEY=sk-...
	  GEMINI_API_KEY=...
	  LANGUAGE_MODEL=gpt-4o
	  ```
	- As chaves podem ser obtidas em [OpenAI](https://platform.openai.com/api-keys) e [Google AI Studio](https://aistudio.google.com/app/apikey).
5. **Execute o app:**
	```bash
	streamlit run OCR.py
	```
6. **Acesse o app:**
	- O Streamlit abrirá no navegador (geralmente em http://localhost:8501)

## Segurança
- **NUNCA** suba seu arquivo `.env` para o GitHub!
- O arquivo `.env` já está no `.gitignore`.
- Se um segredo vazar, gere um novo imediatamente.

## Exemplo de uso
1. Faça upload de uma foto da redação manuscrita.
2. Clique em "Iniciar OCR" para extrair o texto.
3. Clique em "Corrigir Redação ENEM" para receber a análise detalhada.

## Tecnologias
- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [OpenAI GPT API](https://platform.openai.com/)

## Licença
MIT

---
Desenvolvido por Alisson Louly e colaboradores.
