"""
config/config_manager.py - Gerenciador central de configuração
VERSÃO CORRIGIDA - sem erros de sintaxe
"""
import os
import json
from pathlib import Path

class DarkFactoryConfig:
    """Configuração central do Dark Factory"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Carrega configuração - USA utf-8-sig para lidar com BOM"""
        config_path = Path("config/project.json")
        
        if not config_path.exists():
            self.config = {
                "project": {"name": "Dark Factory", "version": "2.0"},
                "apis": {},
                "features": {"content_generation": True}
            }
            return
        
        # utf-8-sig remove BOM automaticamente se existir
        try:
            with open(config_path, "r", encoding="utf-8-sig") as f:
                self.config = json.load(f)
        except json.JSONDecodeError:
            # Fallback: tentar ler como bytes e remover BOM manualmente
            with open(config_path, "rb") as f:
                content = f.read()
                # Remover BOM se existir
                if content.startswith(b'\xef\xbb\xbf'):
                    content = content[3:]
                self.config = json.loads(content.decode('utf-8'))
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            self.config = {
                "project": {"name": "Dark Factory", "version": "2.0"},
                "apis": {},
                "features": {"content_generation": True}
            }
    
    def is_feature_enabled(self, feature_name):
        """Verifica se uma feature está habilitada"""
        features = self.config.get("features", {})
        return features.get(feature_name, False)
    
    def get_api_key(self, api_name):
        """Obtém chave de API da variável de ambiente"""
        api_config = self.config.get("apis", {}).get(api_name, {})
        env_var = api_config.get("api_key_env")
        
        if env_var and api_config.get("enabled", False):
            return os.getenv(env_var)
        return None

# Instância global - SINGLETON
config = DarkFactoryConfig()

if __name__ == "__main__":
    separator = "=" * 50
    print(separator)
    print("🏭 DARK FACTORY CONFIG MANAGER")
    print(separator)
    
    print(f"\n📁 PROJETO:")
    print(f"  Nome: {config.config.get('project', {}).get('name', 'N/A')}")
    print(f"  Versão: {config.config.get('project', {}).get('version', 'N/A')}")
    print(f"  Modo: {config.config.get('project', {}).get('mode', 'N/A')}")
    
    print(f"\n📊 FEATURES:")
    features = config.config.get('features', {})
    for feature, enabled in features.items():
        status = "✅ ATIVO" if enabled else "❌ INATIVO"
        print(f"  {feature}: {status}")
    
    print(f"\n🔑 APIs:")
    apis = config.config.get('apis', {})
    for api_name, api_config in apis.items():
        enabled = api_config.get('enabled', False)
        status = "✅ PRONTO" if enabled else "⚙️  PENDENTE"
        print(f"  {api_name}: {status}")
    
    print(f"\n{separator}")
    print("✅ CONFIGURAÇÃO CARREGADA COM SUCESSO!")
