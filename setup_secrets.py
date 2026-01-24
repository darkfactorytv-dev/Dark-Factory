#!/usr/bin/env python3
"""Sincroniza .env com GitHub Secrets - detecta automaticamente todas as chaves."""
import subprocess
import sys
from pathlib import Path

def load_env(path: Path) -> dict:
    """Carrega todas as variáveis do .env."""
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key] = value
    return env

def check_gh() -> bool:
    """Verifica se gh CLI está autenticado."""
    result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    return result.returncode == 0

def set_secret(key: str, value: str) -> bool:
    """Define secret no GitHub."""
    result = subprocess.run(
        ["gh", "secret", "set", key, "--body", value],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def main():
    env_path = Path(".env")
    if not env_path.exists():
        sys.exit("❌ .env não encontrado")

    if not check_gh():
        sys.exit("❌ gh CLI não autenticado. Execute: gh auth login")

    env = load_env(env_path)
    
    # Filtra apenas chaves com valor preenchido
    secrets_to_sync = {k: v for k, v in env.items() if v.strip()}
    
    if not secrets_to_sync:
        sys.exit("❌ Nenhuma chave com valor no .env")

    print(f"🔐 Sincronizando {len(secrets_to_sync)} secrets...")
    
    for key, value in secrets_to_sync.items():
        ok = set_secret(key, value)
        status = "✅" if ok else "❌"
        # Mostra apenas prefixo da chave por segurança
        masked = value[:10] + "..." if len(value) > 10 else value
        print(f"{status} {key} = {masked}")

    print("\n🚀 Done! Verifique: gh secret list")
    print("💡 Dica: Adicione novas chaves no .env e rode este script novamente")

if __name__ == "__main__":
    main()
