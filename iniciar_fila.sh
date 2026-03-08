#!/bin/bash
echo "Iniciando a Fila Sequencial do YouTube..."
cd /home/sidney/Dev/youtube-fila-sequencial
source venv/bin/activate
uvicorn main:app
