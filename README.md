# YouTube Fila Sequencial 📺

Um sistema local desenvolvido em Python e FastAPI para contornar o algoritmo do YouTube. Ele permite extrair as inscrições, salvar os vídeos em um banco de dados SQLite local e gerar uma fila de reprodução estritamente cronológica (do mais antigo para o mais novo).

## Tecnologias Utilizadas
* Python 3
* FastAPI & Uvicorn (Servidor Web)
* SQLite3 (Banco de Dados persistente)
* Google API Client (YouTube Data API v3)
* Jinja2 (Motor de Templates HTML)

## Como rodar localmente
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv` e ative-o.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Obtenha suas credenciais OAuth 2.0 no Google Cloud Console e salve como `client_secret.json` na raiz.
5. Inicie o servidor: `uvicorn main:app`.
