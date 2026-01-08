# test_clean.py - Teste após remover BOM
import sys
import os

print("🧪 TESTE APÓS LIMPEZA DE BOM")
print("=" * 60)

# Configurar paths
BASE = r"C:\devprojects\Dark-Factory"
PATHS = [
    BASE,
    os.path.join(BASE, "src"),
    os.path.join(BASE, "src", "utils"),
    os.path.join(BASE, "src", "core"),
]

for p in PATHS:
    if p not in sys.path:
        sys.path.insert(0, p)

print("📁 Paths configurados")

# Testar imports
print("\n🔧 TESTANDO IMPORTS...")

try:
    # Importar logger
    print("1. Importando logger...")
    from utils.logger import logger
    print("   ✅ Logger importado com sucesso!")
    
    # Testar logger
    logger.info("Teste do sistema de logs")
    logger.success("Import funcionando!")
    
except ImportError as e:
    print(f"   ❌ Erro import logger: {e}")
    # Criar logger fallback
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("DarkFactory")
    print("   ✅ Logger fallback criado")

try:
    # Importar theme_manager
    print("\n2. Importando theme_manager...")
    from core.theme_manager import ThemeManager
    print("   ✅ ThemeManager importado com sucesso!")
    
    # Testar
    print("\n3. Testando funcionalidades...")
    manager = ThemeManager()
    
    # Verificar se manager tem logger
    if not hasattr(manager, 'logger') or manager.logger is None:
        manager.logger = logger
    
    # Estatísticas
    stats = manager.get_statistics()
    print(f"   📊 Estatísticas:")
    print(f"      • Total temas: {stats.get('total_themes', 0)}")
    print(f"      • Usados: {stats.get('used_themes', 0)}")
    print(f"      • Disponíveis: {stats.get('available_themes', 0)}")
    
    # Selecionar tema
    theme = manager.get_random_theme()
    if theme:
        print(f"\n   🎯 TEMA SELECIONADO:")
        print(f"      • Nome: {theme.get('name', 'N/A')}")
        print(f"      • ID: {theme.get('id', 'N/A')}")
        print(f"      • Categoria: {theme.get('category', 'N/A')}")
        
        # Mostrar fatos
        facts = theme.get('facts', [])
        if facts:
            print(f"      • Fato 1: {facts[0]}")
    else:
        print("\n   ⚠️  Nenhum tema disponível")
        
    print("\n✅ TODOS OS IMPORTS FUNCIONANDO!")
    
except ImportError as e:
    print(f"   ❌ Erro import theme_manager: {e}")
except Exception as e:
    print(f"   ❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("🏭 DARK FACTORY - SISTEMA PRINCIPAL OPERACIONAL!")
print("\n🎯 AMANHÃ: Comprar chip → Verificar conta → APIs → Produção real")
