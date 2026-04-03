import os
import pickle
import webbrowser
import threading
import socket
import http.server
import urllib.parse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class GoogleAuth:
    def __init__(self, client_secret_file='client_secret.json'):
        self.client_secret_file = client_secret_file
        self.scopes = [
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
        self.token_file = 'token.pickle'
        self.flow = None
        self.auth_code = None

    def authenticate(self, callback=None):
        '''Método principal que será chamado pelo frontend'''
        def auth_thread():
            try:
                user_data = self.get_user_info()
                if callback:
                    callback(user_data)
            except Exception as e:
                if callback:
                    callback({'error':str(e)})

        threading.Thread(target=auth_thread, daemon=True).start()

    def get_user_info(self):
        """Obtém informações do usuário após autentificação"""
        creds = None

        # Verificar se já existe token salvo
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token: #read binary 'rb'
                creds = pickle.load(token)
        
        # Se não há credenciais validadas, faszer autentificação
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = Flow.from_client_secrets_file(
                    self.client_secret_file,
                    scopes=self.scopes,
                    redirect_uri='http://localhost:8080/'
                )

                # Gerar URL de autorização 
                auth_url, _ = flow.authorization_url(prompt='consent')

                # Abrir navegador para autentificação 
                webbrowser.open(auth_url)

                # Servidor local para capturar o código
                self.auth_code = self._get_auth_code_local()

                # Trocar código por token
                flow.fetch_token(code=self.auth_code)
                creds = flow.credentials

                # Salvar token
                with open(self.token_file, 'wb') as token: # write binary 'wb'
                    pickle.dump(creds, token)

        # Buscar informações do usuário
        service = build('people', 'v1', credentials=creds)
        profile = service.people().get(
            resourceName='people/me',
            personFields='names,emailAddresses,photos'
        ).execute()

        # Extrair dados
        user_data = {
            'email': profile.get('emailAddresses', [{}])[0].get('value', ''),
            'name': profile.get('names', [{}])[0].get('displayName', ''),
            'picture': profile.get('photos', [{}])[0].get('url', '')
        }
        return user_data
    
    def _get_auth_code_local(self):
        '''Servidor local para capturar o código de autorização'''
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)

                if 'code' in params:
                    self.server.auth_code = params['code'][0]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("Autenticado! Você pode fechar esta janela.".encode('utf-8')) # permice assento e coisas do tipo
                else:
                    self.send_response(400)
                    self.end_headers()

            def log_message(self, format, *args):
                pass # Suplimir logs

        server = http.server.HTTPServer(('localhost', 8080), Handler)
        server.auth_code = None

        # Timeout para não travar
        server.timeout = 300

        while server.auth_code is None:
            server.handle_request()

        server.server_close()
        return server.auth_code
    
    def logout(self):
        '''Remove o token salvo'''
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
