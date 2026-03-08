from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import webbrowser
from googleapiclient.errors import HttpError # Importante: Biblioteca para capturar os erros do Google

from src.youtube_client import YouTubeManager
from src.database import Database

db = Database()
yt = YouTubeManager()
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Abre o navegador assim que o servidor ligar
    webbrowser.open("http://127.0.0.1:8000")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def exibir_fila(request: Request):
    """Lógica principal com proteção contra falhas da API."""
    
    nao_assistidos = db.contar_nao_assistidos()
    
    if nao_assistidos == 0:
        print("\n=> Fila zerada! Acordando a API do YouTube...")
        try:
            inscricoes = yt.get_subscriptions()
            videos_recentes = yt.get_recent_videos(inscricoes, dias=21)
            
            if videos_recentes:
                db.salvar_videos(videos_recentes)
                print("=> Banco de dados atualizado com a nova remessa.")
        except HttpError as error:
            print(f"\n❌ ALERTA DA API DO GOOGLE: {error.reason}")
        except Exception as e:
            print(f"\n❌ ERRO DE CONEXÃO: {e}")
            
    # Busca os dados do banco
    videos_fila = db.get_videos_nao_assistidos()
    
    # --- NOVIDADE AQUI: Pegamos as estatísticas para mandar pro HTML ---
    total_restantes = len(videos_fila)
    ultima_atualizacao = db.get_ultima_atualizacao()
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "videos": videos_fila,
            "total_restantes": total_restantes,       # Variável nova
            "ultima_atualizacao": ultima_atualizacao  # Variável nova
        }
    )

@app.get("/watch/{video_id}")
def assistir_video(video_id: str):
    """Salva no banco e te manda pro YouTube."""
    print(f"=> Vídeo {video_id} assistido! Removendo da fila...")
    db.marcar_assistido(video_id)
    
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    return RedirectResponse(url=youtube_url)