import sqlite3

class Database:
    def __init__(self, db_name="fila.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        # Permite acessar as colunas pelo nome (essencial para o Jinja2 no HTML)
        self.conn.row_factory = sqlite3.Row 
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Cria a tabela que armazena os dados do vídeo e o status."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                video_id TEXT PRIMARY KEY,
                titulo TEXT,
                canal TEXT,
                thumbnail TEXT,
                publicado_em TEXT,
                assistido INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def salvar_videos(self, videos):
        """Salva a lista do YouTube no banco. O 'IGNORE' impede que vídeos 
        antigos (já assistidos) voltem para a fila ou sejam duplicados."""
        for video in videos:
            self.cursor.execute('''
                INSERT OR IGNORE INTO videos (video_id, titulo, canal, thumbnail, publicado_em)
                VALUES (?, ?, ?, ?, ?)
            ''', (video['video_id'], video['titulo'], video['canal'], video['thumbnail'], video['publicado_em']))
        self.conn.commit()

    def get_videos_nao_assistidos(self):
        """Retorna apenas a fila pendente, ordenada pela data."""
        self.cursor.execute('''
            SELECT * FROM videos 
            WHERE assistido = 0 
            ORDER BY publicado_em ASC
        ''')
        # Converte o retorno do banco para dicionários que o HTML consegue ler
        return [dict(row) for row in self.cursor.fetchall()]

    def marcar_assistido(self, video_id):
        """Muda o status do vídeo para 1 (assistido)."""
        self.cursor.execute('UPDATE videos SET assistido = 1 WHERE video_id = ?', (video_id,))
        self.conn.commit()
        
    def contar_nao_assistidos(self):
        """Conta quantos vídeos ainda estão pendentes na fila."""
        self.cursor.execute('SELECT COUNT(*) FROM videos WHERE assistido = 0')
        return self.cursor.fetchone()[0]

    def get_ultima_atualizacao(self):
        """Pega a data do vídeo mais recente no banco para saber quando foi a última leva."""
        self.cursor.execute('SELECT MAX(publicado_em) FROM videos')
        resultado = self.cursor.fetchone()
        
        if resultado and resultado[0]:
            data_iso = resultado[0] # Ex: 2026-03-07T15:30:00Z
            # Quebra a data e formata para o padrão brasileiro (DD/MM/YYYY)
            ano, mes, dia = data_iso[:10].split('-')
            return f"{dia}/{mes}/{ano}"
            
        return "Desconhecida"