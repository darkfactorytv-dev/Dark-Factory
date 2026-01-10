# test_simple.py
import os
import sys

print("🔍 TESTE SIMPLES DO .env.local")

# 1. Verificar se arquivo existe
try:
    with open('.env.local', 'r') as f:
        print("✅ .env.local encontrado")
        
        # Ler e processar
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' in line:
                parts = line.split('=', 1)
                key = parts[0].strip()
                value = parts[1].strip()
                
                # Limpar aspas
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                os.environ[key] = value
                print(f"   {key} = ***{value[-4:] if len(value) > 4 else '****'}")
        
        print(f"✅ Variáveis carregadas")
        
except FileNotFoundError:
    print("❌ .env.local não encontrado")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)

# 2. Verificar
print("\n📊 VERIFICAÇÃO:")
suno = os.getenv('SUNO_API_KEY')
stable = os.getenv('STABLE_AUDIO_API_KEY')

if suno:
    print(f"✅ SUNO_API_KEY: {len(suno)} caracteres")
else:
    print("❌ SUNO_API_KEY: NÃO ENCONTRADA")

if stable:
    print(f"✅ STABLE_AUDIO_API_KEY: {len(stable)} caracteres")
else:
    print("❌ STABLE_AUDIO_API_KEY: NÃO ENCONTRADA")

# 3. Testar import do módulo
print("\n🔧 TESTANDO MÓDULO DE ÁUDIO...")
sys.path.append('src')

try:
    from audio.api_manager import AudioAPIManager
    print("✅ Módulo importado com sucesso!")
    
    # Testar instância
    manager = AudioAPIManager()
    print(f"✅ AudioAPIManager criado")
    
    # Testar conexão Suno
    print(f"\n🔗 Testando conexão Suno...")
    result = manager.test_suno_connection()
    
    if result['success']:
        print(f"✅ Conexão Suno OK (Status: {result.get('status', 'N/A')})")
    else:
        print(f"❌ Falha: {result.get('error', 'Unknown')}")
    
except ImportError as e:
    print(f"❌ Erro importação: {e}")
except Exception as e:
    print(f"❌ Erro: {e}")
