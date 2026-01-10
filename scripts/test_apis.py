"""
scripts/test_apis.py - VERSÃO FINAL FUNCIONAL
"""
import sys
import os
from pathlib import Path

# ADICIONAR ESTAS LINHAS NO INÍCIO
# =========================================
# 1. Carregar .env.local antes de tudo
env_loader = Path("scripts/load_env.py")
if env_loader.exists():
    try:
        # Importar e executar load_dotenv
        import importlib.util
        spec = importlib.util.spec_from_file_location("load_env", env_loader)
        load_env = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(load_env)
        load_env.load_dotenv()
    except:
        print("⚠️  Não foi possível carregar scripts/load_env.py")
        print("   Tentando carregar manualmente...")
        
        # Carregar manualmente
        env_file = Path(".env.local")
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
else:
    print("⚠️  scripts/load_env.py não encontrado")

# =========================================

import json

def load_config():
    """Carrega configuração do project.json"""
    config_path = Path("config/project.json")
    
    try:
        with open(config_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return None

def test_suno(config_data):
    """Testa Suno.ai"""
    print("\n🎵 TESTANDO SUNO.AI:")
    
    api_key = os.getenv('SUNO_API_KEY')
    if not api_key:
        print("   ❌ SUNO_API_KEY não encontrada no ambiente")
        print("   Verifique o conteúdo do .env.local")
        return False
    
    print(f"   ✅ API Key encontrada")
    print(f"   📏 Comprimento: {len(api_key)} caracteres")
    
    # Mostrar formato (seguro)
    if len(api_key) > 10:
        masked = api_key[:8] + "..." + api_key[-4:]
        print(f"   🔐 Formato: {masked}")
    
    # Verificar formato
    if api_key.startswith('suno-'):
        print("   ✅ Formato Suno correto")
    elif 'suno' in api_key.lower():
        print("   ✅ Chave contém 'suno'")
    else:
        print("   ⚠️  Formato não padrão")
    
    return True

def test_stable_audio(config_data):
    """Testa Stable Audio"""
    print("\n🎵 TESTANDO STABLE AUDIO:")
    
    api_key = os.getenv('STABLE_AUDIO_API_KEY')
    if not api_key:
        print("   ❌ STABLE_AUDIO_API_KEY não encontrada")
        return False
    
    print(f"   ✅ API Key encontrada")
    print(f"   📏 Comprimento: {len(api_key)} caracteres")
    
    # Mostrar formato seguro
    if len(api_key) > 10:
        masked = api_key[:8] + "..." + api_key[-4:]
        print(f"   🔐 Formato: {masked}")
    
    # Verificar formato
    if api_key.startswith('sk-'):
        print("   ✅ Formato Stable Audio correto")
    elif api_key.startswith('Bearer '):
        print("   ✅ Formato Bearer token")
    else:
        print("   ⚠️  Formato não padrão")
    
    return True

def main():
    print("🔧 TESTE DE APIS - CARREGANDO .env.local")
    print("=" * 60)
    
    # Verificar se variáveis estão carregadas
    print("\n🔍 VARIÁVEIS CARREGADAS:")
    suno_key = os.getenv('SUNO_API_KEY')
    stable_key = os.getenv('STABLE_AUDIO_API_KEY')
    
    print(f"   SUNO_API_KEY: {'✅' if suno_key else '❌'}")
    print(f"   STABLE_AUDIO_API_KEY: {'✅' if stable_key else '❌'}")
    
    if not suno_key or not stable_key:
        print("\n⚠️  Variáveis não carregadas!")
        print("   Verifique o arquivo .env.local")
        return False
    
    # Carregar configuração
    print("\n📁 CONFIGURAÇÃO DO PROJETO:")
    config_data = load_config()
    if not config_data:
        return False
    
    project = config_data['project']
    print(f"   ✅ {project['name']} v{project['version']}")
    print(f"   Modo: {project['mode']}")
    
    # Testar APIs
    results = {
        "Suno.ai": test_suno(config_data),
        "Stable Audio": test_stable_audio(config_data)
    }
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL:")
    
    ready_count = sum(1 for r in results.values() if r)
    
    for service, success in results.items():
        status = "✅ PRONTO" if success else "❌ FALHA"
        print(f"  {service}: {status}")
    
    print(f"\n🎯 APIs PRONTAS: {ready_count}/2")
    
    if ready_count == 2:
        print("\n✅ SISTEMA 100% CONFIGURADO!")
        print("   Próximo: Implementar APIs reais")
        return True
    else:
        print("\n❌ Configure as APIs primeiro")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
