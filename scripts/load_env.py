"""
scripts/load_env.py
Carrega variáveis do .env.local para o ambiente Python
"""
import os
import sys
from pathlib import Path

def load_dotenv(env_file=".env.local"):
    """Carrega variáveis de um arquivo .env"""
    file_path = Path(env_file)
    
    if not file_path.exists():
        print(f"❌ {env_file} não encontrado")
        return False
    
    print(f"📁 Carregando {env_file}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Ignorar linhas vazias e comentários
                if not line or line.startswith('#'):
                    continue
                
                # Separar chave=valor
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remover aspas se houver
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    # Definir no ambiente
                    os.environ[key] = value
                    print(f"   ✅ {key} = {'*' * min(10, len(value))}...")
        
        print(f"✅ {env_file} carregado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar {env_file}: {e}")
        return False

def check_environment():
    """Verifica se as variáveis estão carregadas"""
    print("\n🔍 VERIFICANDO VARIÁVEIS DE AMBIENTE:")
    
    required = ['SUNO_API_KEY', 'STABLE_AUDIO_API_KEY']
    all_ok = True
    
    for var in required:
        value = os.getenv(var)
        if value:
            masked = value[:10] + "..." + value[-4:] if len(value) > 15 else "***"
            print(f"   ✅ {var}: {masked} ({len(value)} chars)")
        else:
            print(f"   ❌ {var}: NÃO DEFINIDA")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    print("🔧 CARREGADOR DE AMBIENTE DARK FACTORY")
    print("=" * 50)
    
    # Carregar .env.local
    success = load_dotenv()
    
    if success:
        check_environment()
        print("\n✅ Ambiente configurado com sucesso!")
    else:
        print("\n❌ Falha ao configurar ambiente")
        sys.exit(1)
