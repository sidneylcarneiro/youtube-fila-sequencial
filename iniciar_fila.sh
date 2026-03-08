#!/bin/bash
echo "Iniciando a Fila Sequencial do YouTube..."

# Entra na pasta do projeto
cd /home/sidney/Dev/youtube-fila-sequencial

# Chama o Uvicorn DIRETAMENTE de dentro do ambiente virtual (Sem precisar de source)
./venv/bin/uvicorn main:app

# Se o servidor cair ou der erro, o terminal pausa aqui para você conseguir ler o que aconteceu
echo ""
echo "O servidor foi encerrado ou encontrou um erro."
read -p "Pressione [Enter] para fechar esta janela..."
