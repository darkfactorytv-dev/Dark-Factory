# config/path_setup.py
import sys
from pathlib import Path

# Adicionar src ao Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

print(f"✅ Python path configurado: {src_path}")
