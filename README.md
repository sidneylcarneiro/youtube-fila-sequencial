# YouTube Fila Sequencial 📺

Um sistema local desenvolvido em Python e FastAPI criado para contornar o algoritmo de recomendação do YouTube. Ele varre as suas inscrições, extrai os vídeos recentes e constrói uma fila de reprodução estritamente cronológica (do mais antigo para o mais novo). 

Assista ao conteúdo na ordem exata em que foi publicado, sem distrações e sem perder nenhum vídeo por conta do algoritmo.

## 🚀 Principais Funcionalidades

* **Fila Cronológica Inteligente:** Ordena os vídeos do mais antigo para o mais recente, garantindo o consumo contínuo da linha do tempo.
* **Banco de Dados Local (SQLite):** Mantém um histórico off-line. Ao clicar em um vídeo, ele é automaticamente marcado como "assistido" e removido da sua fila para sempre.
* **Resiliência de API (Cache):** Se a cota diária gratuita do Google expirar ou você ficar sem internet, o sistema não quebra. Ele renderiza a interface instantaneamente usando o banco de dados local.
* **Filtros Dinâmicos no Frontend:** Interface fluida com botões ocultáveis e checkboxes em JavaScript puro para filtrar a visualização por canais específicos em tempo real, sem recarregar a página.
* **Integração Nativa com Linux:** Possui script e configuração de `.desktop` para rodar o servidor em segundo plano e abrir o navegador com apenas 1 clique no menu do sistema (testado no Cinnamon).

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, FastAPI, Uvicorn
* **Banco de Dados:** SQLite3
* **Integração:** Google API Client (YouTube Data API v3, OAuth 2.0)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Jinja2 (Motor de Templates)

## ⚙️ Como Instalar e Rodar

1. Clone o repositório:
    ```bash
    git clone [https://github.com/sidneylcarneiro/youtube-fila-sequencial.git](https://github.com/sidneylcarneiro/youtube-fila-sequencial.git)

    ```

2. Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate

    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

    ```

4. **Configuração da API:** 
    Obtenha suas credenciais OAuth 2.0 (App para Computador) no [Google Cloud Console](https://console.cloud.google.com/) e salve o arquivo como `client_secret.json` na raiz do projeto.

5. **Inicie o Servidor:**
    ```bash
    uvicorn main:app

    ```

*O navegador abrirá automaticamente no endereço `http://127.0.0.1:8000` na primeira execução, solicitando o login do Google para gerar o `token.pickle`.*

## 🔒 Segurança

O arquivo `.gitignore` já está configurado para não subir o seu `token.pickle`, `client_secret.json` e `fila.db`. Mantenha essas credenciais estritamente locais.
