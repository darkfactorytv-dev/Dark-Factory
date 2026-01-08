# test_final.py - Teste definitivo
import sys
import os

print("🧪 TESTE DEFINITIVO DARK FACTORY")
print("=" * 60)

# Configurar paths ABSOLUTOS
BASE = r"C:\devprojects\Dark-Factory"
PATHS = [
    BASE,
    os.path.join(BASE, "src"),
    os.path.join(BASE, "src", "utils"),
    os.path.join(BASE, "src", "core"),
    os.path.join(BASE, "src", "temas"),
]

print("📁 CONFIGURANDO PATHS:")
for p in PATHS:
    if os.path.exists(p):
        sys.path.insert(0, p)
        print(f"  ✅ {p}")
    else:
        print(f"  ❌ {p} (não existe)")

print("\n🔧 TESTANDO IMPORTS...")

# Testar logger
try:
    print("1. Importando logger...")
    # Primeiro executar o arquivo logger.py
    logger_path = os.path.join(BASE, "src", "utils", "logger.py")
    with open(logger_path, 'r', encoding='utf-8') as f:
        logger_code = f.read()
    
    # Executar em namespace separado
    logger_namespace = {}
    exec(logger_code, logger_namespace)
    
    # Obter o logger
    logger = logger_namespace.get('logger')
    if logger:
        print("   ✅ Logger carregado!")
        logger.info("Teste do sistema de logs")
    else:
        print("   ⚠️  Logger não encontrado no namespace")
        
except Exception as e:
    print(f"   ❌ Erro no logger: {e}")

# Testar theme_manager
try:
    print("\n2. Importando theme_manager...")
    theme_manager_path = os.path.join(BASE, "src", "core", "theme_manager.py")
    with open(theme_manager_path, 'r', encoding='utf-8') as f:
        theme_manager_code = f.read()
    
    # Substituir import problemático
    theme_manager_code = theme_manager_code.replace(
        'from utils.logger import logger',
        '# Import substituído\nlogger = None\n# Fim da substituição'
    )
    
    # Executar
    theme_namespace = {'logger': logger} if 'logger' in locals() else {}
    exec(theme_manager_code, theme_namespace)
    
    # Obter ThemeManager
    ThemeManager = theme_namespace.get('ThemeManager')
    if ThemeManager:
        print("   ✅ ThemeManager carregado!")
        
        # Testar
        print("\n3. Testando funcionalidade...")
        manager = ThemeManager()
        
        # Modificar para usar logger simples se necessário
        if hasattr(manager, 'logger') and manager.logger is None:
            class SimpleLogger:
                def info(self, msg): print(f"📝 {msg}")
                def success(self, msg): print(f"✅ {msg}")
                def warning(self, msg): print(f"⚠️ {msg}")
                def error(self, msg): print(f"❌ {msg}")
                def debug(self, msg): print(f"🔧 {msg}")
            manager.logger = SimpleLogger()
        
        # Selecionar tema
        theme = manager.get_random_theme()
        if theme:
            print(f"   🎯 TEMA: {theme.get('name', 'N/A')}")
            print(f"   📍 ID: {theme.get('id', 'N/A')}")
            print(f"   🏷️  Categoria: {theme.get('category', 'N/A')}")
            
            # Estatísticas
            stats = manager.get_statistics()
            print(f"\n   📊 ESTATÍSTICAS:")
            print(f"      • Total: {stats.get('total_themes', 0)}")
            print(f"      • Disponíveis: {stats.get('available_themes', 0)}")
            print(f"      • Usados: {stats.get('used_themes', 0)}")
        else:
            print("   ⚠️  Nenhum tema disponível")
            
    else:
        print("   ❌ ThemeManager não encontrado no código")
        
except Exception as e:
    print(f"   ❌ Erro no theme_manager: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("🏭 DARK FACTORY - TESTE CONCLUÍDO")
print("\n🎯 PRÓXIMOS PASSOS:")
print("1. Amanhã: Comprar chip e configurar conta Google")
print("2. Criar YouTube Channel")
print("3. Configurar APIs do Google Cloud")
print("4. Integrar Gemini Pro para roteiros reais")
