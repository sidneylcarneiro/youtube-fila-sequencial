import os
import pickle
from datetime import datetime, timedelta, timezone
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Definimos o escopo restrito: o script só tem permissão para LER dados, não para alterar ou apagar.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

class YouTubeManager:
    def __init__(self, client_secret_file='client_secret.json'):
        self.client_secret_file = client_secret_file
        self.api_service_name = "youtube"
        self.api_version = "v3"
        # Ao instanciar a classe, ele já tenta autenticar
        self.youtube = self._authenticate()

    def _authenticate(self):
        """Lida com a autenticação OAuth 2.0 e faz o cache do token."""
        creds = None
        
        # O arquivo token.pickle armazena os tokens de acesso.
        # Ele é criado automaticamente na primeira vez que você faz o login.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Se não houver credenciais válidas, exige o login.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("=> Atualizando token de acesso...")
                creds.refresh(Request())
            else:
                print("=> Solicitando nova autorização pelo navegador...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file, SCOPES)
                # Abre o navegador localmente para você aprovar o acesso
                creds = flow.run_local_server(port=8080)
            
            # Salva o token recém-adquirido para as próximas execuções
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build(self.api_service_name, self.api_version, credentials=creds)

    def get_subscriptions(self):
        """Busca TODOS os canais nos quais você está inscrito (lidando com paginação)."""
        print("=> Mapeando todos os canais inscritos...")
        canais = []
        next_page_token = None
        
        while True:
            request = self.youtube.subscriptions().list(
                part="snippet",
                mine=True,
                maxResults=50, # Limite máximo por "página" que o Google permite
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response.get('items', []):
                titulo = item['snippet']['title']
                canal_id = item['snippet']['resourceId']['channelId']
                canais.append({'titulo': titulo, 'id': canal_id})
                
            # Verifica se o Google enviou uma "próxima página"
            next_page_token = response.get('nextPageToken')
            
            # Se não tiver próxima página, sai do loop
            if not next_page_token:
                break
                
        return canais

    def get_recent_videos(self, canais, dias=21):
        """Busca vídeos recentes dos canais informados e ordena do mais antigo para o mais novo."""
        print(f"\n=> Buscando vídeos publicados nos últimos {dias} dias...")
        videos = []
        
        # A API do YouTube exige a data no formato ISO 8601 UTC (ex: 2026-03-05T00:00:00Z)
        data_limite = (datetime.now(timezone.utc) - timedelta(days=dias)).isoformat()
        
        for canal in canais:
            print(f"   Lendo canal: {canal['titulo']}")
            request = self.youtube.search().list(
                part="snippet",
                channelId=canal['id'],
                maxResults=50, # Aumentamos para o limite máximo permitido por requisição
                order="date",
                type="video",
                publishedAfter=data_limite
            )
            response = request.execute()
            
            for item in response.get('items', []):
                videos.append({
                    'video_id': item['id']['videoId'],
                    'titulo': item['snippet']['title'],
                    'canal': item['snippet']['channelTitle'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'publicado_em': item['snippet']['publishedAt']
                })
                
        # O pulo do gato: Ordenar a lista pela data, do mais antigo para o mais recente!
        videos.sort(key=lambda x: x['publicado_em'])
        
        return videos