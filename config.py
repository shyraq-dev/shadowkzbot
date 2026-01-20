"""
ShadowKZ Bot - Configuration
Боттың барлық конфигурациясы
"""

from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

# .env файлын жүктеу
load_dotenv()


@dataclass
class DatabaseConfig:
    """Database конфигурациясы"""
    path: str


@dataclass
class TgBot:
    """Telegram Bot конфигурациясы"""
    token: str
    owner_id: int
    payment_token: Optional[str] = None


@dataclass
class GameConfig:
    """Ойын конфигурациясы"""
    min_players: int = 9
    max_players: int = 30
    registration_time: int = 60  # секунд
    extend_time: int = 30  # /extend командасы үшін қосымша секунд
    
    # Рөлдердің бөлінуі (ойыншылар санына қарай)
    role_distribution: dict = None
    
    def __post_init__(self):
        if self.role_distribution is None:
            self.role_distribution = {
                9: {"peaceful": 4, "shadow": 4, "neutral": 1},
                12: {"peaceful": 6, "shadow": 4, "neutral": 2},
                15: {"peaceful": 8, "shadow": 5, "neutral": 2},
                20: {"peaceful": 11, "shadow": 6, "neutral": 3},
                25: {"peaceful": 14, "shadow": 7, "neutral": 4},
                30: {"peaceful": 17, "shadow": 9, "neutral": 4},
            }


@dataclass
class EconomyConfig:
    """Экономика конфигурациясы"""
    # Сыйлықтар
    win_coins: int = 100
    lose_coins: int = -50
    win_rating: int = 10
    lose_rating: int = -5
    streak_diamonds: int = 5  # 5 ойын қатарынан жеңгенге
    streak_required: int = 5  # қанша ойын қатарынан жеңу керек
    
    # Айырбастау (💎 ↔ 🪙)
    exchange_rates: dict = None
    
    # Сатып алу бағалары (₸)
    shop_prices: dict = None
    
    def __post_init__(self):
        if self.exchange_rates is None:
            self.exchange_rates = {
                "diamond_to_coin": {
                    1: 100,
                    2: 200,
                    5: 1000
                },
                "coin_to_diamond": {
                    100: 1,
                    200: 2,
                    1000: 5
                }
            }
        
        if self.shop_prices is None:
            self.shop_prices = {
                # Алмаз сатып алу (₸)
                "diamonds": {
                    1: 250,
                    2: 500,
                    5: 750
                },
                # Тиын сатып алу (₸)
                "coins": {
                    200: 500,
                    500: 750,
                    1000: 1000
                },
                # Заттар (🪙 немесе 💎)
                "items": {
                    "fake_document": {"coins": 200, "diamonds": 0},
                    "shield": {"coins": 500, "diamonds": 0},
                    "role_peaceful": {"coins": 0, "diamonds": 5},
                    "role_neutral": {"coins": 0, "diamonds": 10},
                    "role_shadow": {"coins": 0, "diamonds": 20}
                }
            }


@dataclass
class Config:
    """Жалпы конфигурация"""
    tg_bot: TgBot
    db: DatabaseConfig
    game: GameConfig
    economy: EconomyConfig
    debug: bool = False


def load_config(path: Optional[str] = None) -> Config:
    """
    Конфигурацияны жүктеу
    
    Args:
        path: .env файлының жолы (опционалды)
    
    Returns:
        Config: Толық конфигурация объектісі
    """
    if path:
        load_dotenv(path)
    
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN', ''),
            owner_id=int(os.getenv('OWNER_ID', 0)),
            payment_token=os.getenv('PAYMENT_TOKEN')
        ),
        db=DatabaseConfig(
            path=os.getenv('DATABASE_PATH', 'shadowkz.db')
        ),
        game=GameConfig(),
        economy=EconomyConfig(),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )


# Конфигурацияны тексеру
def validate_config(config: Config) -> bool:
    """
    Конфигурацияның дұрыстығын тексеру
    
    Args:
        config: Config объектісі
    
    Returns:
        bool: Дұрыс болса True
    """
    if not config.tg_bot.token:
        raise ValueError("BOT_TOKEN орнатылмаған!")
    
    if not config.tg_bot.owner_id:
        raise ValueError("OWNER_ID орнатылмаған!")
    
    if config.game.min_players < 9:
        raise ValueError("Минималды ойыншылар саны 9-дан кем болмауы керек!")
    
    if config.game.max_players > 30:
        raise ValueError("Максималды ойыншылар саны 30-дан көп болмауы керек!")
    
    return True


if __name__ == '__main__':
    # Конфигурацияны тексеру
    config = load_config()
    
    try:
        validate_config(config)
        print("✅ Конфигурация дұрыс!")
        print(f"🤖 Bot Token: {config.tg_bot.token[:10]}...")
        print(f"👤 Owner ID: {config.tg_bot.owner_id}")
        print(f"💾 Database: {config.db.path}")
        print(f"🎮 Min/Max players: {config.game.min_players}/{config.game.max_players}")
        print(f"💰 Win reward: {config.economy.win_coins}🪙, {config.economy.win_rating}⭐")
    except ValueError as e:
        print(f"❌ Қате: {e}")
