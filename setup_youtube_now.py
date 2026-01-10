import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

print("=== CONFIGURAÇÃO YOUTUBE API ===")
print("Diretório atual:", os.getcwd())

# Verificar arquivos
files = os.listdir('.')
print("\nArquivos encontrados:")
for f in files:
    if 'cred' in f.lower() or 'json' in f.lower() or '.env' in f:
        print(f"  📄 {f}")

# Configuração
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CRED_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

if os.path.exists(CRED_FILE):
    print(f"\n✅ {CRED_FILE} encontrado")
    
    # Ler credenciais
    with open(CRED_FILE, 'r') as f:
        creds_data = json.load(f)
    print(f"   Client ID: {creds_data.get('client_id', '')[0:20]}...")
    
    # Obter token
    flow = InstalledAppFlow.from_client_secrets_file(CRED_FILE, SCOPES)
    print("\n⚠️  Abrindo navegador para autorização...")
    print("   Login com: darkfactory.tv@gmail.com")
    
    creds = flow.run_local_server(port=8080)
    
    # Salvar token
    with open(TOKEN_FILE, 'w') as f:
        f.write(creds.to_json())
    print(f"✅ Token salvo em {TOKEN_FILE}")
    
    # Extrair refresh token
    token_data = json.loads(creds.to_json())
    refresh_token = token_data.get('refresh_token')
    
    if refresh_token:
        print(f"\n🎯 REFRESH TOKEN OBTIDO:")
        print(f"   {refresh_token[0:50]}...")
        
        # Atualizar .env.local
        env_lines = []
        if os.path.exists('.env.local'):
            with open('.env.local', 'r') as f:
                env_lines = f.readlines()
        
        # Adicionar/atualizar refresh token
        updated = False
        for i, line in enumerate(env_lines):
            if line.startswith('YOUTUBE_'):
                env_lines[i] = f'YOUTUBE_REFRESH_TOKEN={refresh_token}\n'
                updated = True
                break
        
        if not updated:
            env_lines.append(f'\nYOUTUBE_REFRESH_TOKEN={refresh_token}\n')
        
        with open('.env.local', 'w') as f:
            f.writelines(env_lines)
        
        print("✅ .env.local atualizado")
        
        # Criar variável para GitHub Secrets
        print("\n📋 PARA GITHUB SECRETS:")
        print(f"YOUTUBE_CREDENTIALS={json.dumps(token_data)}")
        
    else:
        print("❌ Não foi possível obter refresh token")
        
else:
    print(f"\n❌ {CRED_FILE} não encontrado")
    print("   Coloque o arquivo em: C:\\devprojects\\Dark-Factory\\credentials.json")
