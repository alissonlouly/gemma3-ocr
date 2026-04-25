
# Gemma3-OCR: Correção Automática de Redação Manuscrita

Este app permite extrair o texto de uma redação manuscrita (imagem) e corrigi-la automaticamente segundo as competências do ENEM, usando Google Gemini para OCR e correção.

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
4. **Tenha sua chave de API do Gemini em mãos:**
	- A chave pode ser obtida no [Google AI Studio](https://aistudio.google.com/app/apikey).
	- A chave é informada diretamente na sidebar do app, durante o uso.
5. **Execute o app:**
	```bash
	streamlit run OCR.py
	```
6. **Acesse o app:**
	- O Streamlit abrirá no navegador (geralmente em http://localhost:8501)

## Segurança
- A chave fica apenas na sessão atual do app quando digitada na sidebar.
- Se um segredo vazar, gere um novo imediatamente.

## Exemplo de uso
1. Informe sua API key do Gemini na sidebar.
2. Faça upload de uma foto da redação manuscrita.
3. Clique em "Iniciar OCR" para extrair o texto.
4. Clique em "Corrigir Redação ENEM" para receber a análise detalhada.

## Tecnologias
- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)

## Licença
MIT

---
Desenvolvido por Alisson Louly e colaboradores.
