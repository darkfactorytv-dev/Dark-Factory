"""
scripts/test_suno_real.py
Testa a API REAL da Suno com sua chave
"""
import os
import sys
from pathlib import Path
import time

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from audio.api_manager import AudioAPIManager

def main():
    print("🧪 TESTE REAL DA API SUNO")
    print("=" * 60)
    
    # Verificar chave
    api_key = os.getenv('SUNO_API_KEY')
    if not api_key:
        print("❌ SUNO_API_KEY não encontrada no ambiente")
        print("   Execute: python scripts/load_env.py primeiro")
        return False
    
    print(f"✅ Suno API Key encontrada ({len(api_key)} caracteres)")
    
    # Criar manager
    manager = AudioAPIManager()
    
    # Testar conexão
    print(f"\n🔗 Testando conexão com api.sunoapi.org...")
    connection = manager.test_suno_connection()
    
    if not connection['success']:
        print(f"❌ Falha na conexão: {connection.get('error', 'Unknown')}")
        
        # Dicas de solução
        print(f"\n🔧 TENTE:")
        print(f"   1. Verifique se a chave está ativa no painel da Suno")
        print(f"   2. URL atual: {manager.suno_config['base_url']}")
        print(f"   3. Formato da chave: {api_key[:20]}...")
        
        return False
    
    print(f"✅ Conexão estabelecida (Status: {connection.get('status', 'N/A')})")
    
    # Teste de geração REAL
    print(f"\n🎵 TESTE REAL DE GERAÇÃO")
    print("   ⚠️  Esta chamada usará seus créditos da Suno!")
    print("   ⚠️  Use duração CURTA para teste (ex: 30 segundos)")
    
    print(f"\n📝 Configure o teste:")
    
    duration = input("   Duração (segundos, 10-30 recomendado): ").strip()
    if not duration.isdigit():
        duration = 30
    else:
        duration = int(duration)
        if duration > 120:
            print("   ⚠️  Duração muito longa para teste. Usando 30s.")
            duration = 30
    
    prompt = input("   Prompt (ex: dark ambient): ").strip()
    if not prompt:
        prompt = "dark industrial ambient music with factory sounds"
    
    style = input("   Estilo (Ambient/Electronic/Classical): ").strip()
    if not style:
        style = "Ambient"
    
    print(f"\n📋 CONFIGURAÇÃO DO TESTE:")
    print(f"   Duração: {duration}s")
    print(f"   Prompt: {prompt}")
    print(f"   Estilo: {style}")
    
    print(f"\n❓ Confirmar envio para API Suno? (s/n): ", end='')
    choice = input().strip().lower()
    
    if choice not in ['s', 'sim', 'y', 'yes']:
        print("✅ Teste cancelado")
        return False
    
    print(f"\n📤 Enviando para Suno API...")
    
    result = manager.generate_with_suno(
        prompt=prompt,
        title="Dark Factory Test",
        style=style,
        duration=duration
    )
    
    if not result:
        print("❌ Falha na geração")
        return False
    
    task_id = result['task_id']
    print(f"✅ Tarefa criada: {task_id}")
    print(f"   Status inicial: {result['status']}")
    
    # Verificar status automaticamente
    print(f"\n🔍 Verificando status (pode levar 1-3 minutos)...")
    print("   Pressione Ctrl+C para interromper")
    
    max_attempts = 12  # 12 tentativas * 15s = 3 minutos
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"   Tentativa {attempt}/{max_attempts}...")
            status_result = manager.check_suno_status(task_id)
            
            if status_result:
                if status_result['status'] == 'completed':
                    print(f"✅ Tarefa COMPLETA!")
                    print(f"   Arquivo: {status_result['audio_file']}")
                    
                    # Verificar se arquivo existe
                    audio_file = Path(status_result['audio_file'])
                    if audio_file.exists():
                        size = audio_file.stat().st_size
                        print(f"   Tamanho: {size} bytes")
                        return True
                    else:
                        print(f"❌ Arquivo não encontrado!")
                        return False
                        
                elif status_result['status'] == 'failed':
                    print(f"❌ Tarefa FALHOU")
                    return False
                else:
                    print(f"   Status: {status_result['status']}")
            
            time.sleep(15)  # Espera 15 segundos
            
        except KeyboardInterrupt:
            print(f"\n⏸️  Verificação interrompida")
            print(f"   Tarefa ID: {task_id}")
            print(f"   Verifique manualmente mais tarde")
            return True
    
    print(f"⚠️  Tempo esgotado (3 minutos)")
    print(f"   Tarefa ID: {task_id}")
    print(f"   Verifique manualmente mais tarde")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
