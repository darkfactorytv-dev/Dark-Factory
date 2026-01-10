"""
src/audio/api_manager.py - VERSÃO COM CARREGAMENTO AUTOMÁTICO
"""
import os
from pathlib import Path

# CARREGAR .env.local
env_file = Path(".env.local")
if env_file.exists():
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    except Exception:
        pass
"""
src/audio/api_manager.py - VERSÃO COM API REAL SUNO
"""
import os
import json
import requests
from pathlib import Path
import time
from datetime import datetime

class AudioAPIManager:
    """Gerencia APIs de áudio com Suno REAL"""
    
    def __init__(self):
        self.suno_api_key = os.getenv('SUNO_API_KEY')
        self.stable_audio_key = os.getenv('STABLE_AUDIO_API_KEY')
        
        # Configurações Suno (REAIS da documentação)
        self.suno_config = {
            "base_url": "https://api.sunoapi.org/api/v1",
            "headers": {
                "Authorization": f"Bearer {self.suno_api_key}",
                "Content-Type": "application/json"
            }
        }
        
        # Configurações Stable Audio
        self.stable_config = {
            "base_url": "https://api.stability.ai/v2alpha/audio",
            "headers": {
                "Authorization": f"Bearer {self.stable_audio_key}",
                "Content-Type": "application/json"
            }
        }
        
        # Diretórios
        self.output_dir = Path("productions/audio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Log
        self.log_file = Path("logs/audio_api.log")
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Registra log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(f"[{level}] {message}")
    
    def generate_with_suno(self, prompt, duration=600, title=None, style="Ambient"):
        """
        Gera música usando API REAL da Suno
        
        Documentação: https://api.sunoapi.org/docs
        """
        if not self.suno_api_key:
            self.log("❌ Suno API Key não configurada", "ERROR")
            return None
        
        self.log(f"🎵 Gerando com Suno (REAL): {prompt[:50]}...")
        
        # URL REAL da Suno
        url = f"{self.suno_config['base_url']}/generate"
        
        # Payload REAL (baseado na documentação fornecida)
        # A API espera duration em MILISEGUNDOS
        duration_ms = duration * 1000
        
        payload = {
            "customMode": True,
            "instrumental": True,
            "model": "V4_5ALL",
            "callBackUrl": "",  # Deixar vazio se não tem callback
            "prompt": prompt,
            "style": style,
            "title": title or f"Dark Factory - {int(time.time())}",
            "personaId": "",  # Opcional
            "negativeTags": "Upbeat, Pop, Happy",
            "vocalGender": "m",  # 'm' ou 'f' (mesmo sendo instrumental)
            "styleWeight": 0.7,
            "weirdnessConstraint": 0.5,
            "audioWeight": 0.8,
            "duration": duration_ms  # Em milissegundos
        }
        
        try:
            self.log(f"Enviando para Suno API: {url}")
            self.log(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Chamada REAL à API
            response = requests.post(
                url, 
                headers=self.suno_config['headers'], 
                json=payload, 
                timeout=300
            )
            
            self.log(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.log(f"Resposta: {json.dumps(result, indent=2)}")
                
                # Verificar estrutura da resposta
                if 'id' in result:
                    task_id = result['id']
                    self.log(f"✅ Tarefa criada: ID {task_id}")
                    
                    # TODO: Implementar polling para verificar status
                    # Por enquanto, retorna o ID da tarefa
                    return {
                        "task_id": task_id,
                        "status": "submitted",
                        "prompt": prompt,
                        "timestamp": int(time.time())
                    }
                else:
                    self.log(f"❌ Resposta inesperada: {result}", "ERROR")
                    return None
                    
            else:
                self.log(f"❌ Erro HTTP {response.status_code}: {response.text}", "ERROR")
                return None
                
        except requests.exceptions.Timeout:
            self.log("❌ Timeout na API Suno", "ERROR")
            return None
        except Exception as e:
            self.log(f"❌ Erro na API Suno: {e}", "ERROR")
            return None
    
    def check_suno_status(self, task_id):
        """Verifica status de uma tarefa Suno"""
        url = f"{self.suno_config['base_url']}/tasks/{task_id}"
        
        try:
            response = requests.get(url, headers=self.suno_config['headers'])
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', 'unknown')
                audio_url = result.get('audio_url')
                
                self.log(f"Status tarefa {task_id}: {status}")
                
                if status == 'completed' and audio_url:
                    # Baixar áudio
                    audio_response = requests.get(audio_url)
                    output_file = self.output_dir / f"suno_{task_id}.mp3"
                    
                    with open(output_file, 'wb') as f:
                        f.write(audio_response.content)
                    
                    self.log(f"✅ Áudio baixado: {output_file}")
                    return {
                        "status": "completed",
                        "audio_file": str(output_file),
                        "task_id": task_id
                    }
                else:
                    return {
                        "status": status,
                        "task_id": task_id
                    }
            else:
                self.log(f"❌ Erro ao verificar status: {response.status_code}")
                return None
                
        except Exception as e:
            self.log(f"❌ Erro ao verificar status: {e}", "ERROR")
            return None
    
    def generate_with_stable_audio(self, prompt, duration=600):
        """
        Gera áudio ambience com Stable Audio (REAL)
        """
        if not self.stable_audio_key:
            self.log("❌ Stable Audio API Key não configurada", "ERROR")
            return None
        
        self.log(f"🌫️ Gerando com Stable Audio (REAL): {prompt[:50]}...")
        
        url = f"{self.stable_config['base_url']}/generation"
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "model": "stable-audio-v2",
            "output_format": "wav"
        }
        
        try:
            self.log(f"Enviando para Stable Audio API...")
            
            # Chamada REAL (descomente para usar)
            # response = requests.post(url, headers=self.stable_config['headers'], json=payload, timeout=300)
            # response.raise_for_status()
            
            # SIMULAÇÃO (REMOVA QUANDO TESTAR)
            self.log("⚠️  MODO SIMULAÇÃO - Descomente para API real", "WARNING")
            time.sleep(1)
            
            # Criar arquivo dummy
            output_file = self.output_dir / f"stable_audio_{int(time.time())}.wav"
            with open(output_file, 'wb') as f:
                f.write(b"STABLE AUDIO SIMULATION - UNCOMMENT API CALL")
            
            self.log(f"✅ Áudio ambience (simulado): {output_file}")
            return str(output_file)
            
            # Código REAL (use este quando testar):
            # output_file = self.output_dir / f"stable_audio_{int(time.time())}.wav"
            # with open(output_file, 'wb') as f:
            #     f.write(response.content)
            # 
            # self.log(f"✅ Áudio ambience gerado: {output_file}")
            # return str(output_file)
            
        except Exception as e:
            self.log(f"❌ Erro na API Stable Audio: {e}", "ERROR")
            return None
    
    def test_suno_connection(self):
        """Testa conexão com API Suno"""
        if not self.suno_api_key:
            return {"success": False, "error": "API Key não configurada"}
        
        # Endpoint de teste simples
        url = f"{self.suno_config['base_url']}/generate"
        
        try:
            # Tentativa de HEAD request (não consome créditos)
            response = requests.head(url, headers=self.suno_config['headers'], timeout=10)
            return {"success": True, "status": response.status_code}
                
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection failed - check URL"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Instância global
audio_manager = AudioAPIManager()

if __name__ == "__main__":
    print("🔊 AUDIO API MANAGER - VERSÃO COM SUNO REAL")
    print("=" * 60)
    
    manager = AudioAPIManager()
    
    print(f"✅ Suno API Key: {len(manager.suno_api_key) if manager.suno_api_key else 0} chars")
    print(f"✅ Stable Audio Key: {len(manager.stable_audio_key) if manager.stable_audio_key else 0} chars")
    
    # Teste de conexão Suno
    print(f"\n🔗 Testando conexão Suno...")
    test_result = manager.test_suno_connection()
    
    if test_result['success']:
        print(f"✅ Conexão Suno OK (Status: {test_result.get('status', 'N/A')})")
    else:
        print(f"❌ Falha na conexão: {test_result.get('error', 'Unknown')}")
    
    print(f"\n📁 Output dir: {manager.output_dir}")
    print(f"📄 Log file: {manager.log_file}")

