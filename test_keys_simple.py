# test_keys_simple.py
print("TESTE SIMPLES DAS CHAVES")
print("=" * 40)

import os

# Ler .env.local linha por linha
try:
    with open('.env.local', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Limpar aspas
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                os.environ[key] = value
                print(f"Carregado: {key}")
                
except FileNotFoundError:
    print("ERROR: .env.local nao encontrado")
    exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

# Verificar
suno = os.getenv('SUNO_API_KEY')
stable = os.getenv('STABLE_AUDIO_API_KEY')

print(f"\nRESULTADO:")
if suno:
    print(f"SUNO_API_KEY: OK ({len(suno)} chars)")
else:
    print("SUNO_API_KEY: NAO ENCONTRADA")

if stable:
    print(f"STABLE_AUDIO_API_KEY: OK ({len(stable)} chars)")
else:
    print("STABLE_AUDIO_API_KEY: NAO ENCONTRADA")

if suno and stable:
    print("\nSUCESSO! Ambos configurados.")
    print("Pronto para testar APIs.")
else:
    print("\nERRO: Configure as chaves no .env.local")
    exit(1)
