import os
import sys
from pathlib import Path

# Получаем абсолютный путь к текущей директории
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

from models import States, Messages, MenuBuilder, BallStats
from data import HandballBallAdvisor

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def setup_project_structure():
    """Создание необходимой структуры проекта"""
    try:
        directories = [
            'images/novice',
            'images/intermediate',
            'images/professional',
            'logs'
        ]
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created/verified directory: {dir_path}")

        env_path = Path('.env')
        if not env_path.exists():
            env_content = (
                "TELEGRAM_TOKEN=your-telegram-token-here\n"
                "OPENAI_API_KEY=your-openai-api-key-here\n"
            )
            env_path.write_text(env_content)
            logger.info("Created .env file")

    except Exception as e:
        logger.error(f"Error in setup_project_structure: {e}")
        raise


def check_environment():
    """Проверка переменных окружения"""
    load_dotenv()

    telegram_token = os.getenv('TELEGRAM_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not telegram_token:
        raise ValueError("TELEGRAM_TOKEN не найден в .env файле")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY не найден в .env файле")

    return telegram_token, openai_api_key


class TelegramBot:
    """Основной класс бота"""

    def __init__(self, token: str, advisor: HandballBallAdvisor):
        self.application = Application.builder().token(token).build()
        self.advisor = advisor
        self.menu_builder = MenuBuilder()
        self.stats = BallStats()

    def setup_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                States.CHOOSING_LEVEL: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.level_chosen)
                ],
                States.CHOOSING_SURFACE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.surface_chosen)
                ],
                States.SHOWING_DETAILS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.show_details)
                ],
                States.SHOWING_PHOTOS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.show_photos)
                ],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_error_handler(self.error_handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(
            Messages.WELCOME,
            reply_markup=self.menu_builder.get_level_keyboard()
        )
        return States.CHOOSING_LEVEL

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(Messages.HELP)

    async def level_chosen(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data['level'] = update.message.text
        logger.info(f"Выбран уровень: {update.message.text}")
        await update.message.reply_text(
            Messages.SURFACE_QUESTION,
            reply_markup=self.menu_builder.get_surface_keyboard()
        )
        return States.CHOOSING_SURFACE

    async def surface_chosen(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            context.user_data['surface'] = update.message.text
            logger.info(f"Выбрана поверхность: {update.message.text}")

            self.stats.update_stats(
                context.user_data['level'],
                context.user_data['surface']
            )

            recommendation, balls = await self.advisor.get_recommendation(context.user_data)
            context.user_data['current_balls'] = balls

            await update.message.reply_text(recommendation)

            if balls:
                await update.message.reply_text(
                    "Что бы вы хотели узнать о рекомендованных мячах?",
                    reply_markup=self.menu_builder.get_details_keyboard()
                )
                return States.SHOWING_DETAILS
            else:
                await update.message.reply_text(
                    "К сожалению, не найдено подходящих мячей для ваших критериев. "
                    "Попробуйте изменить параметры поиска."
                )
                return ConversationHandler.END

        except Exception as e:
            logger.error(f"Error in surface_chosen: {e}", exc_info=True)
            await update.message.reply_text(Messages.ERROR_API)
            return ConversationHandler.END

    async def show_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text == "Завершить":
            await update.message.reply_text(Messages.CANCELLED)
            return ConversationHandler.END

        if update.message.text == "Показать детали":
            balls = context.user_data.get('current_balls', [])
            for ball in balls:
                message = (
                        f"🏐 *{ball.name}*\n"
                        f"📊 Уровень: {ball.level}\n"
                        f"💰 Цена: {ball.price:.2f} €\n"
                        f"📏 Размер: {ball.size}\n"
                        f"🏭 Материал: {ball.material}\n"
                        f"🏟 Тип поверхности: {ball.surface_type}\n\n"
                        f"📝 Описание: {ball.description}\n\n"
                        f"✨ Особенности:\n" +
                        "\n".join(f"• {feature}" for feature in ball.features)
                )
                await update.message.reply_text(message, parse_mode='Markdown')

            keyboard = [
                [KeyboardButton("Показать фото")],
                [KeyboardButton("Завершить")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "Что еще вы хотели бы узнать?",
                reply_markup=reply_markup
            )
            return States.SHOWING_PHOTOS

        if update.message.text == "Показать фото":
            return await self.show_photos(update, context)

        return States.SHOWING_DETAILS

    async def show_photos(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text == "Завершить":
            await update.message.reply_text(Messages.CANCELLED)
            return ConversationHandler.END

        if update.message.text == "Показать фото":
            balls = context.user_data.get('current_balls', [])
            for ball in balls:
                try:
                    image_path = Path(ball.image_url)
                    if image_path.exists():
                        with open(image_path, 'rb') as photo:
                            await update.message.reply_photo(
                                photo=photo,
                                caption=f"🏐 {ball.name}\n💰 Цена: {ball.price:.2f} €\n📏 Размер: {ball.size}"
                            )
                    else:
                        await update.message.reply_text(
                            f"🏐 Изображение мяча {ball.name} временно недоступно\n"
                            f"💰 Цена: {ball.price:.2f} €\n"
                            f"📏 Размер: {ball.size}"
                        )
                except Exception as e:
                    logger.error(f"Error sending photo for {ball.name}: {e}")
                    await update.message.reply_text(f"Не удалось загрузить фото мяча {ball.name}")

            keyboard = [
                [KeyboardButton("Показать детали")],
                [KeyboardButton("Завершить")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "Что еще вы хотели бы узнать?",
                reply_markup=reply_markup
            )
            return States.SHOWING_DETAILS

        return States.SHOWING_PHOTOS

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(Messages.CANCELLED)
        return ConversationHandler.END

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.error(f"Exception while handling an update: {context.error}")
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(Messages.ERROR_API)

    def run(self):
        self.setup_handlers()
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Основная функция запуска бота"""
    try:
        setup_project_structure()
        logger.info("Project structure created successfully")

        telegram_token, openai_api_key = check_environment()
        logger.info("Environment checked successfully")

        advisor = HandballBallAdvisor(openai_api_key)
        bot = TelegramBot(telegram_token, advisor)
        logger.info("Bot initialized, starting...")
        bot.run()

    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()