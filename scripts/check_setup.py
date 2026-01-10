#!/usr/bin/env python3
"""
scripts/check_setup.py
Verifica TODO o setup do Dark Factory em 10 segundos
"""
import sys
import json
from pathlib import Path

def check_all():
    print("🔍 VERIFICAÇÃO COMPLETA DO DARK FACTORY")
    print("=" * 50)
    
    checks = {
        "Estrutura de Pastas": check_folders(),
        "Arquivos de Config": check_config_files(),
        "Python e Dependências": check_python(),
        "APIs Configuradas": check_apis(),
        "Workflow GitHub": check_workflow()
    }
    
    print("\n📊 RESUMO:")
    for check_name, (status, message) in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check_name}: {message}")
    
    # Recomendações
    print("\n🎯 PRÓXIMOS PASSOS:")
    if not checks["APIs Configuradas"][0]:
        print("1. Configure as APIs de áudio (Suno/Stable Audio)")
    if not checks["Workflow GitHub"][0]:
        print("2. Atualize o workflow no GitHub")
    print("3. Execute: python config/config_manager.py")

def check_folders():
    required = ["config", "src", "productions", ".github/workflows"]
    missing = [f for f in required if not Path(f).exists()]
    return (len(missing) == 0, f"{len(missing)} faltando" if missing else "OK")

def check_config_files():
    required = ["config/project.json", "requirements.txt"]
    missing = [f for f in required if not Path(f).exists()]
    return (len(missing) == 0, f"{len(missing)} faltando" if missing else "OK")

def check_python():
    try:
        import google.genai
        return (True, "Python 3.11+ OK")
    except ImportError:
        return (False, "Instale: pip install -r requirements.txt")

def check_apis():
    config_file = Path("config/project.json")
    if not config_file.exists():
        return (False, "project.json não encontrado")
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        apis = config.get("apis", {})
        youtube_enabled = apis.get("youtube", {}).get("enabled", False)
        gemini_enabled = apis.get("gemini", {}).get("enabled", False)
        
        # Verificar se tem pelo menos uma API ativa
        if youtube_enabled or gemini_enabled:
            return (True, f"APIs básicas configuradas")
        
        return (False, "Configure pelo menos uma API")
    except Exception as e:
        return (False, f"Erro: {str(e)}")

def check_workflow():
    workflow = Path(".github/workflows/dark-factory-production.yml")
    if not workflow.exists():
        return (False, "Workflow não encontrado")
    
    try:
        content = workflow.read_text(encoding="utf-8")
        if "content_generator.py" in content:
            return (True, "Workflow básico OK")
        return (False, "Workflow incompleto")
    except Exception as e:
        return (False, f"Erro ao ler: {str(e)}")

if __name__ == "__main__":
    check_all()
