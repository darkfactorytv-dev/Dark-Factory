# 🏭 DARK FACTORY - PROFESSIONAL LOGGING SYSTEM
import logging
import sys
import os
from datetime import datetime
from pathlib import Path
import colorama

# Inicializar colorama para cores no Windows
colorama.init()

class DarkFactoryLogger:
    """Sistema de logging profissional para Dark Factory"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.name = "DarkFactory"
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remover handlers existentes para evitar duplicação
        self.logger.handlers.clear()
        
        # Configurar formato
        self._setup_formatters()
        self._setup_handlers()
        
        self._initialized = True
    
    def _setup_formatters(self):
        """Configurar formatadores de log"""
        # Formato detalhado para arquivo
        self.file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Formato simples para console
        self.console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
    
    def _setup_handlers(self):
        """Configurar handlers de log"""
        # Console Handler (colorido)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler (todos logs)
        self._setup_file_handler("all", logging.DEBUG)
        
        # File Handler (apenas erros)
        self._setup_file_handler("errors", logging.WARNING)
        
        # File Handler (apenas produção)
        self._setup_file_handler("production", logging.INFO)
    
    def _setup_file_handler(self, log_type, level):
        """Configurar handler para arquivo específico"""
        log_dir = Path("logs/system")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        filename = log_dir / f"darkfactory_{log_type}_{datetime.now().strftime('%Y%m')}.log"
        file_handler = logging.FileHandler(filename, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(self.file_formatter)
        
        # Filtro por tipo de log
        if log_type == "production":
            file_handler.addFilter(lambda record: "PRODUCTION" in record.getMessage())
        elif log_type == "errors":
            file_handler.addFilter(lambda record: record.levelno >= logging.WARNING)
        
        self.logger.addHandler(file_handler)
    
    # Métodos públicos
    def info(self, message):
        self.logger.info(f"📝 {message}")
    
    def success(self, message):
        self.logger.info(f"✅ {message}")
    
    def warning(self, message):
        self.logger.warning(f"⚠️  {message}")
    
    def error(self, message):
        self.logger.error(f"❌ {message}")
    
    def debug(self, message):
        self.logger.debug(f"🔧 {message}")
    
    def production_start(self, production_id, theme):
        self.logger.info(f"🏭 PRODUCTION START | ID: {production_id} | THEME: {theme}")
    
    def production_step(self, step, details=""):
        self.logger.info(f"   ↳ {step} {details}")
    
    def production_end(self, production_id, status, duration=None):
        duration_str = f" | DURATION: {duration}" if duration else ""
        self.logger.info(f"🏁 PRODUCTION END | ID: {production_id} | STATUS: {status}{duration_str}")
    
    def api_call(self, service, endpoint, status):
        self.logger.info(f"🌐 API CALL | SERVICE: {service} | ENDPOINT: {endpoint} | STATUS: {status}")
    
    def file_created(self, filepath, size_kb=None):
        size_str = f" | SIZE: {size_kb}KB" if size_kb else ""
        self.logger.info(f"💾 FILE CREATED | PATH: {filepath}{size_str}")

# Criar instância global
logger = DarkFactoryLogger()

if __name__ == "__main__":
    # Testar sistema de logs
    print("🧪 TESTANDO SISTEMA DE LOGS")
    print("=" * 50)
    
    logger.info("Sistema de logs inicializado com sucesso")
    logger.success("Operação concluída com sucesso")
    logger.warning("Aviso: Configuração incompleta")
    logger.error("Erro: Arquivo não encontrado")
    logger.debug("Informação de debug")
    
    # Simular produção
    logger.production_start("DF-20240115-001", "clipe de papel")
    logger.production_step("Seleção de tema", "clipe de papel")
    logger.production_step("Geração de roteiro", "512 caracteres")
    logger.production_step("Síntese de áudio", "45 segundos")
    logger.production_end("DF-20240115-001", "SUCCESS", "2m 15s")
    
    # Simular API call
    logger.api_call("YouTube", "videos.insert", "200 OK")
    
    print("\n✅ Teste concluído!")
    print("📁 Logs salvos em: logs/system/")
