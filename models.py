from dataclasses import dataclass
from typing import List, Dict, Any
from telegram import ReplyKeyboardMarkup, KeyboardButton


class States:
    """Состояния разговора с ботом"""
    CHOOSING_LEVEL = 0
    CHOOSING_SURFACE = 1
    SHOWING_DETAILS = 2
    SHOWING_PHOTOS = 3


class Config:
    """Конфигурационные параметры"""
    MAX_RETRIES = 3
    RETRY_DELAY = 15
    MAX_PROMPT_LENGTH = 4000
    GPT_MODEL = "gpt-3.5-turbo"
    API_TIMEOUT = 30


class Messages:
    """Текстовые сообщения бота"""
    WELCOME = "👋 Добро пожаловать! Я помогу вам выбрать подходящий мяч для гандбола.\n\nВыберите ваш уровень игры:"
    SURFACE_QUESTION = "Отлично! Где вы планируете использовать мяч?"
    SHOW_DETAILS = "Хотите увидеть детальную информацию о рекомендованных мячах?"
    SHOW_PHOTOS = "Хотите посмотреть фотографии мячей?"
    ERROR_API = "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
    CANCELLED = "Выбор мяча завершен. Для начала нового подбора введите /start"
    ERROR_TOO_LONG = "Запрос слишком длинный, попробуйте сократить требования."
    ERROR_AUTH = "Ошибка аутентификации. Пожалуйста, попробуйте позже."
    ERROR_TIMEOUT = "Время ожидания истекло. Пожалуйста, попробуйте еще раз."
    HELP = """
🏐 Команды бота:
/start - Начать подбор мяча
/help - Показать это сообщение
/cancel - Отменить текущий процесс

ℹ️ Как пользоваться:
1. Выберите ваш уровень игры
2. Укажите где планируете использовать мяч
3. Получите персональные рекомендации
4. Изучите детали и фото мячей
"""


class ImagePaths:
    """Пути к изображениям мячей"""
    BASE_PATH = "images"

    # Мячи для новичков (размер 0 и 1)
    ERIMA_PURE_GRIP_4 = f"{BASE_PATH}/novice/erima_pure_grip_4.jpg"  # размер 0
    MOLTEN_H0F1800 = f"{BASE_PATH}/novice/molten_h0f1800.jpg"  # размер 0
    SELECT_TUCANA = f"{BASE_PATH}/novice/select_tucana.jpg"  # размер 1

    # Мячи для среднего уровня (размер 1,2,3)
    SELECT_REPLICA_EHF = f"{BASE_PATH}/intermediate/select_replica_ehf.jpg"
    MOLTEN_SCHOOLMASTER = f"{BASE_PATH}/intermediate/molten_schoolmaster.jpg"
    ERIMA_VRANJES = f"{BASE_PATH}/intermediate/erima_vranjes.jpg"

    # Мячи для профессионалов (размер 2 и 3)
    ERIMA_PURE_GRIP_1 = f"{BASE_PATH}/professional/erima_pure_grip_1.jpg"
    MOLTEN_H3X5001 = f"{BASE_PATH}/professional/molten_h3x5001.jpg"
    SELECT_ULTIMATE_CL = f"{BASE_PATH}/professional/select_ultimate_cl.jpg"


@dataclass
class HandballBall:
    """Класс для хранения информации о гандбольном мяче"""
    name: str
    level: str
    price: float
    material: str
    size: str
    description: str
    surface_type: str
    image_url: str
    features: List[str]


class MenuBuilder:
    """Класс для создания меню и клавиатур"""

    @staticmethod
    def get_level_keyboard() -> ReplyKeyboardMarkup:
        keyboard = [
            [KeyboardButton("Новичок")],
            [KeyboardButton("Средний")],
            [KeyboardButton("Профессионал")]
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    @staticmethod
    def get_surface_keyboard() -> ReplyKeyboardMarkup:
        keyboard = [
            [KeyboardButton("В зале")],
            [KeyboardButton("На улице")],
            [KeyboardButton("Универсальное использование")]
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    @staticmethod
    def get_details_keyboard() -> ReplyKeyboardMarkup:
        keyboard = [
            [KeyboardButton("Показать детали")],
            [KeyboardButton("Показать фото")],
            [KeyboardButton("Завершить")]
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


class BallStats:
    """Класс для сбора статистики"""

    def __init__(self):
        self.level_stats = {
            'Новичок': 0,
            'Средний': 0,
            'Профессионал': 0
        }
        self.surface_stats = {
            'В зале': 0,
            'На улице': 0,
            'Универсальное использование': 0
        }
        self.total_requests = 0

    def update_stats(self, level: str, surface: str):
        self.level_stats[level] = self.level_stats.get(level, 0) + 1
        self.surface_stats[surface] = self.surface_stats.get(surface, 0) + 1
        self.total_requests += 1

    def get_stats_message(self) -> str:
        if self.total_requests == 0:
            return "📊 Статистика пока отсутствует"

        message = "📊 Статистика запросов:\n\n"
        message += "По уровню игры:\n"
        for level, count in self.level_stats.items():
            percentage = (count / self.total_requests * 100)
            message += f"- {level}: {count} ({percentage:.1f}%)\n"

        message += "\nПо типу поверхности:\n"
        for surface, count in self.surface_stats.items():
            percentage = (count / self.total_requests * 100)
            message += f"- {surface}: {count} ({percentage:.1f}%)\n"

        return message