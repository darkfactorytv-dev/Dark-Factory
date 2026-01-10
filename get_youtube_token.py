import os
import json
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

print("=== OBTENDO REFRESH TOKEN DO YOUTUBE ===")

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

if not os.path.exists('credentials.json'):
    print("❌ credentials.json não encontrado")
    exit(1)

print("✅ credentials.json encontrado")

# Criar flow OAuth
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', 
    SCOPES
)

print("\n⚠️  IMPORTANTE: Use a mesma conta do YouTube Channel")
print("   Email: darkfactory.tv@gmail.com")
print("\nAbrindo navegador para autorização...")

# Executar fluxo OAuth
creds = flow.run_local_server(
    port=8080,
    success_message='✅ Autorização concluída! Você pode fechar esta aba.',
    open_browser=True
)

# Salvar token completo
with open('token_completo.json', 'w') as f:
    f.write(creds.to_json())

print(f"\n✅ Token salvo em 'token_completo.json'")

# Extrair refresh token
token_data = json.loads(creds.to_json())
refresh_token = token_data.get('refresh_token')

if refresh_token:
    print(f"\n🎯 REFRESH TOKEN OBTIDO COM SUCESSO!")
    
    # Criar objeto para GitHub Secrets
    youtube_creds = {
        "type": "authorized_user",
        "client_id": token_data.get("client_id"),
        "client_secret": token_data.get("client_secret"),
        "refresh_token": refresh_token
    }
    
    # Salvar para GitHub
    with open('youtube_credentials_github.json', 'w') as f:
        json.dump(youtube_creds, f, indent=2)
    
    print("✅ Arquivo para GitHub criado: 'youtube_credentials_github.json'")
    
    # Atualizar .env.local
    env_lines = []
    env_file = '.env.local'
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_lines = f.readlines()
    
    # Remover linhas antigas do YouTube
    env_lines = [line for line in env_lines if not line.startswith('YOUTUBE_')]
    
    # Adicionar nova
    env_lines.append(f'YOUTUBE_REFRESH_TOKEN={refresh_token}\n')
    
    with open(env_file, 'w') as f:
        f.writelines(env_lines)
    
    print("✅ .env.local atualizado")
    
    print("\n📋 PARA GITHUB SECRETS:")
    print("Nome: YOUTUBE_CREDENTIALS")
    print("Valor (copie o conteúdo abaixo):")
    print("="*50)
    print(json.dumps(youtube_creds, indent=2))
    print("="*50)
    
else:
    print("❌ Não foi possível obter refresh token")

print("\n🔧 PRÓXIMO PASSO:")
print("1. Copie o JSON acima para GitHub Secrets")
print("2. Execute: python scripts\\test_youtube.py --test-upload")
