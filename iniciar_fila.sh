#!/bin/bash
echo "Iniciando a Fila Sequencial do YouTube..."
cd LOCAL-PARA-SUA-PASTA/youtube-fila-sequencial
source venv/bin/activate
uvicorn main:app
