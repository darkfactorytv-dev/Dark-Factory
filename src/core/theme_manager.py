# 🏭 DARK FACTORY - ADVANCED THEME MANAGER
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

from utils.logger import logger

class ThemeManager:
    """Gerenciador avançado de temas para Dark Factory"""
    
    def __init__(self, database_path: str = "data/themes/database.json"):
        self.database_path = Path(database_path)
        self.usage_file = Path("data/themes/usage.json")
        self.stats_file = Path("data/themes/stats.json")
        
        # Carregar dados
        self.database = self._load_database()
        self.usage_data = self._load_usage_data()
        self.stats_data = self._load_stats_data()
        
        logger.info(f"ThemeManager inicializado com {len(self.database.get('themes', []))} temas")
    
    def _load_database(self) -> Dict:
        """Carrega banco de dados de temas"""
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Database não encontrado: {self.database_path}")
            return {"themes": [], "categories": {}}
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao carregar JSON: {e}")
            return {"themes": [], "categories": {}}
    
    def _load_usage_data(self) -> Dict:
        """Carrega dados de uso"""
        default_data = {
            "used_themes": [],
            "theme_history": [],
            "category_usage": {},
            "last_reset": None,
            "total_productions": 0
        }
        
        if not self.usage_file.exists():
            return default_data
        
        try:
            with open(self.usage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_data
    
    def _load_stats_data(self) -> Dict:
        """Carrega estatísticas"""
        default_stats = {
            "themes_used": 0,
            "categories_used": {},
            "avg_days_between_use": 0,
            "most_used_category": None,
            "least_used_category": None
        }
        
        if not self.stats_file.exists():
            return default_stats
        
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_stats
    
    def _save_usage_data(self):
        """Salva dados de uso"""
        self.usage_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.usage_file, 'w', encoding='utf-8') as f:
            json.dump(self.usage_data, f, indent=2, ensure_ascii=False)
    
    def _save_stats_data(self):
        """Salva estatísticas"""
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats_data, f, indent=2, ensure_ascii=False)
    
    def get_random_theme(self, category: Optional[str] = None) -> Optional[Dict]:
        """
        Retorna um tema aleatório não usado recentemente
        
        Args:
            category: Categoria específica (opcional)
        
        Returns:
            Dict com dados do tema ou None
        """
        available_themes = self.get_available_themes(category)
        
        if not available_themes:
            logger.warning("Nenhum tema disponível")
            return None
        
        # Priorizar temas nunca usados
        never_used = [t for t in available_themes if t["id"] not in self.usage_data["used_themes"]]
        
        if never_used:
            theme = random.choice(never_used)
        else:
            # Usar algoritmo de peso: temas menos recentes têm mais chance
            weighted_themes = []
            for theme in available_themes:
                last_used = self._get_last_used_date(theme["id"])
                if last_used:
                    days_since_use = (datetime.now() - last_used).days
                    weight = max(30, days_since_use)  # Mínimo 30 dias
                else:
                    weight = 100  # Alta prioridade se nunca usado
                
                weighted_themes.extend([theme] * weight)
            
            theme = random.choice(weighted_themes) if weighted_themes else random.choice(available_themes)
        
        # Registrar uso
        self._register_theme_usage(theme)
        
        logger.success(f"Tema selecionado: {theme['name']} (ID: {theme['id']})")
        return theme
    
    def get_available_themes(self, category: Optional[str] = None) -> List[Dict]:
        """Retorna lista de temas disponíveis"""
        all_themes = self.database.get("themes", [])
        
        # Filtrar por categoria se especificado
        if category and category in self.database.get("categories", {}):
            filtered = [t for t in all_themes if t.get("category") == category]
        else:
            filtered = all_themes
        
        # Filtrar temas usados muito recentemente (últimos 7 dias)
        recently_used = self._get_recently_used_themes(days=7)
        available = [t for t in filtered if t["id"] not in recently_used]
        
        return available
    
    def _get_recently_used_themes(self, days: int = 7) -> List[str]:
        """Retorna IDs de temas usados recentemente"""
        recent_cutoff = datetime.now() - timedelta(days=days)
        recently_used = []
        
        for usage in self.usage_data.get("theme_history", []):
            usage_date = datetime.fromisoformat(usage.get("timestamp", "2000-01-01"))
            if usage_date > recent_cutoff:
                recently_used.append(usage.get("theme_id"))
        
        return recently_used
    
    def _get_last_used_date(self, theme_id: str) -> Optional[datetime]:
        """Retorna data do último uso de um tema"""
        for usage in reversed(self.usage_data.get("theme_history", [])):
            if usage.get("theme_id") == theme_id:
                return datetime.fromisoformat(usage.get("timestamp"))
        return None
    
    def _register_theme_usage(self, theme: Dict):
        """Registra uso de um tema"""
        usage_record = {
            "theme_id": theme["id"],
            "theme_name": theme["name"],
            "category": theme.get("category"),
            "timestamp": datetime.now().isoformat(),
            "production_id": f"DF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        }
        
        # Atualizar lista de usados
        if theme["id"] not in self.usage_data["used_themes"]:
            self.usage_data["used_themes"].append(theme["id"])
        
        # Adicionar ao histórico
        self.usage_data["theme_history"].append(usage_record)
        
        # Atualizar contagem por categoria
        category = theme.get("category")
        if category:
            self.usage_data["category_usage"][category] = self.usage_data["category_usage"].get(category, 0) + 1
        
        # Incrementar total
        self.usage_data["total_productions"] += 1
        
        # Manter histórico limitado (últimos 1000 usos)
        if len(self.usage_data["theme_history"]) > 1000:
            self.usage_data["theme_history"] = self.usage_data["theme_history"][-1000:]
        
        # Salvar dados
        self._save_usage_data()
        self._update_stats()
    
    def _update_stats(self):
        """Atualiza estatísticas"""
        # Calcular categoria mais usada
        category_usage = self.usage_data.get("category_usage", {})
        if category_usage:
            self.stats_data["most_used_category"] = max(category_usage, key=category_usage.get)
            self.stats_data["least_used_category"] = min(category_usage, key=category_usage.get)
        
        # Contar temas usados
        self.stats_data["themes_used"] = len(set(self.usage_data.get("used_themes", [])))
        
        # Calcular média de dias entre usos
        history = self.usage_data.get("theme_history", [])
        if len(history) >= 2:
            dates = [datetime.fromisoformat(h["timestamp"]) for h in history]
            dates.sort()
            total_days = sum((dates[i+1] - dates[i]).days for i in range(len(dates)-1))
            avg_days = total_days / (len(dates) - 1)
            self.stats_data["avg_days_between_use"] = round(avg_days, 1)
        
        # Atualizar contagem por categoria
        self.stats_data["categories_used"] = category_usage.copy()
        
        self._save_stats_data()
    
    def get_theme_by_id(self, theme_id: str) -> Optional[Dict]:
        """Busca tema por ID"""
        for theme in self.database.get("themes", []):
            if theme["id"] == theme_id:
                return theme
        return None
    
    def get_themes_by_category(self, category: str) -> List[Dict]:
        """Retorna todos temas de uma categoria"""
        return [t for t in self.database.get("themes", []) if t.get("category") == category]
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas completas"""
        total_themes = len(self.database.get("themes", []))
        used_themes = len(set(self.usage_data.get("used_themes", [])))
        available = total_themes - used_themes
        
        return {
            "total_themes": total_themes,
            "used_themes": used_themes,
            "available_themes": available,
            "usage_percentage": round((used_themes / total_themes * 100), 1) if total_themes > 0 else 0,
            "total_productions": self.usage_data.get("total_productions", 0),
            "categories": self.database.get("categories", {}),
            "category_usage": self.usage_data.get("category_usage", {}),
            "stats": self.stats_data
        }
    
    def reset_usage(self, confirm: bool = False) -> bool:
        """Reseta todo o histórico de uso (perigoso!)"""
        if not confirm:
            logger.warning("Reset requer confirmação explícita")
            return False
        
        self.usage_data = {
            "used_themes": [],
            "theme_history": [],
            "category_usage": {},
            "last_reset": datetime.now().isoformat(),
            "total_productions": 0
        }
        
        self._save_usage_data()
        self._update_stats()
        
        logger.info("Histórico de uso resetado completamente")
        return True
    
    def suggest_next_category(self) -> Optional[str]:
        """Sugere próxima categoria baseado em uso"""
        category_usage = self.usage_data.get("category_usage", {})
        all_categories = list(self.database.get("categories", {}).keys())
        
        if not all_categories:
            return None
        
        # Encontrar categoria menos usada
        unused_categories = [c for c in all_categories if c not in category_usage]
        if unused_categories:
            return random.choice(unused_categories)
        
        # Se todas usadas, retornar a menos usada
        return min(category_usage, key=category_usage.get)

# Teste
if __name__ == "__main__":
    print("🧪 TESTE DO THEME MANAGER")
    print("=" * 50)
    
    manager = ThemeManager()
    
    # Estatísticas
    stats = manager.get_statistics()
    print(f"📊 ESTATÍSTICAS:")
    print(f"   • Total de temas: {stats['total_themes']}")
    print(f"   • Temas usados: {stats['used_themes']}")
    print(f"   • Disponível: {stats['available_themes']}")
    print(f"   • Uso: {stats['usage_percentage']}%")
    print(f"   • Produções totais: {stats['total_productions']}")
    
    # Selecionar tema
    theme = manager.get_random_theme()
    if theme:
        print(f"\n🎯 TEMA SELECIONADO:")
        print(f"   • Nome: {theme['name']}")
        print(f"   • ID: {theme['id']}")
        print(f"   • Categoria: {theme.get('category', 'N/A')}")
        print(f"   • Dificuldade: {theme.get('difficulty', 'N/A')}")
        print(f"   • Fatos: {len(theme.get('facts', []))}")
        print(f"   • Hook: {theme.get('script_hook', 'N/A')[:80]}...")
    
    # Sugerir categoria
    next_category = manager.suggest_next_category()
    print(f"\n🤔 PRÓXIMA CATEGORIA SUGERIDA: {next_category}")
    
    print("\n✅ Teste concluído!")
