import logging
from typing import Dict, List, Any, Tuple
from openai import AsyncOpenAI
from models import HandballBall, Config, ImagePaths

logger = logging.getLogger(__name__)


class HandballBallDatabase:
    """База данных гандбольных мячей"""

    @staticmethod
    def get_balls_database() -> Dict[str, List[HandballBall]]:
        return {
            'novice': [
                HandballBall(
                    name="Erima Pure Grip No. 4 Handball",
                    level="Новичок",
                    price=29.99,
                    material="Синтетическая кожа с покрытием Pure Grip",
                    size="0 (48-50 см)",
                    description="Идеальный тренировочный мяч для начинающих игроков и детей. Оборудован специальным покрытием Pure Grip для лучшего контроля.",
                    surface_type="Универсальный",
                    image_url=ImagePaths.ERIMA_PURE_GRIP_4,
                    features=[
                        "Технология Pure Grip для лучшего сцепления",
                        "Оптимальный размер 0 для детей и начинающих",
                        "Прочная синтетическая кожа",
                        "Отличный контроль мяча",
                        "Подходит для всех покрытий"
                    ]
                ),
                HandballBall(
                    name="Molten Handball H00F1800",
                    level="Новичок",
                    price=24.99,
                    material="Мягкая синтетическая кожа",
                    size="0 (48-50 см)",
                    description="Легкий и удобный мяч для начинающих гандболистов. Идеально подходит для детских тренировок и развития базовых навыков.",
                    surface_type="Зал",
                    image_url=ImagePaths.MOLTEN_H0F1800,
                    features=[
                        "Мягкая поверхность для комфортной игры",
                        "Размер 0 для юных спортсменов",
                        "Хорошее сцепление",
                        "Стабильная траектория полета",
                        "Оптимален для зала"
                    ]
                ),
                HandballBall(
                    name="Select Tucana DB v24 Handball",
                    level="Новичок",
                    price=27.99,
                    material="HPU материал с двойным сцеплением",
                    size="1 (50-52 см)",
                    description="Тренировочный мяч с двойным сцеплением для начинающих игроков постарше. Обеспечивает отличный контроль и точность передач.",
                    surface_type="Универсальный",
                    image_url=ImagePaths.SELECT_TUCANA,
                    features=[
                        "Технология двойного сцепления DB",
                        "Размер 1 для игроков постарше",
                        "Улучшенный контроль",
                        "Высокая износостойкость",
                        "Универсальное использование"
                    ]
                )
            ],
            'intermediate': [
                HandballBall(
                    name="Select Replica EHF European League v24",
                    level="Средний",
                    price=49.99,
                    material="HPU 1700 с микрофиброй",
                    size="1-2-3",
                    description="Реплика официального мяча Европейской лиги. Доступен в разных размерах для разных возрастных категорий.",
                    surface_type="Зал",
                    image_url=ImagePaths.SELECT_REPLICA_EHF,
                    features=[
                        "Дизайн официального мяча EHF",
                        "Выбор размера под возраст",
                        "Превосходное сцепление",
                        "Контролируемый отскок",
                        "Высокая прочность"
                    ]
                ),
                HandballBall(
                    name="Molten SchoolMasteR Handball",
                    level="Средний",
                    price=42.99,
                    material="Синтетическая кожа PRO",
                    size="1-2-3",
                    description="Профессиональный тренировочный мяч для школ и клубов. Подходит для регулярных тренировок и соревнований.",
                    surface_type="Универсальный",
                    image_url=ImagePaths.MOLTEN_SCHOOLMASTER,
                    features=[
                        "Профессиональное покрытие PRO",
                        "Три варианта размера",
                        "Стабильная форма",
                        "Улучшенный отскок",
                        "Долгий срок службы"
                    ]
                ),
                HandballBall(
                    name="Erima Vranjes",
                    level="Средний",
                    price=45.99,
                    material="Синтетическая кожа Premium",
                    size="1-2-3",
                    description="Универсальный мяч среднего уровня для тренировок и соревнований. Обеспечивает отличный контроль и точность.",
                    surface_type="Универсальный",
                    image_url=ImagePaths.ERIMA_VRANJES,
                    features=[
                        "Премиальное покрытие",
                        "Размеры для всех возрастов",
                        "Отличное сцепление",
                        "Точная траектория",
                        "Повышенная прочность"
                    ]
                )
            ],
            'professional': [
                HandballBall(
                    name="Erima Pure Grip No. 1 Handball",
                    level="Профессионал",
                    price=79.99,
                    material="Премиум синтетическая кожа Pro+",
                    size="2-3",
                    description="Профессиональный мяч высшего класса с технологией Pure Grip Pro+. Используется в профессиональных соревнованиях.",
                    surface_type="Профессиональный",
                    image_url=ImagePaths.ERIMA_PURE_GRIP_1,
                    features=[
                        "Технология Pure Grip Pro+",
                        "Профессиональные размеры 2-3",
                        "Максимальное сцепление",
                        "Идеальный баланс",
                        "Соревновательный стандарт"
                    ]
                ),
                HandballBall(
                    name="Molten H3X5001-BW Handball",
                    level="Профессионал",
                    price=84.99,
                    material="Премиум композитная кожа X5000",
                    size="2-3",
                    description="Официальный игровой мяч IHF для профессиональных соревнований высшего уровня. Сертифицирован для международных турниров.",
                    surface_type="Профессиональный",
                    image_url=ImagePaths.MOLTEN_H3X5001,
                    features=[
                        "Сертификация IHF",
                        "Технология X5000 Premium",
                        "Профессиональные размеры",
                        "Превосходная аэродинамика",
                        "Высочайшая точность"
                    ]
                ),
                HandballBall(
                    name="Select Ultimate EHF Champions League v24",
                    level="Профессионал",
                    price=89.99,
                    material="Shark Skin с микрофиброй",
                    size="2-3",
                    description="Официальный мяч Лиги чемпионов EHF. Эталон качества для профессионального гандбола.",
                    surface_type="Профессиональный",
                    image_url=ImagePaths.SELECT_ULTIMATE_CL,
                    features=[
                        "Официальный мяч EHF",
                        "Технология Shark Skin",
                        "Оптимальный вес и баланс",
                        "Исключительное сцепление",
                        "Максимальная износостойкость"
                    ]
                )
            ]
        }


class HandballBallAdvisor:
    """Класс для предоставления рекомендаций по выбору мяча"""

    def __init__(self, openai_api_key: str):
        if not openai_api_key:
            raise ValueError("OpenAI API key is required")

        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.ball_db = HandballBallDatabase()

    async def get_recommendation(self, user_data: Dict[str, Any]) -> Tuple[str, List[HandballBall]]:
        level_map = {
            'Новичок': 'novice',
            'Средний': 'intermediate',
            'Профессионал': 'professional'
        }

        try:
            balls = self.ball_db.get_balls_database().get(level_map.get(user_data['level'], 'novice'), [])

            if 'surface' in user_data:
                surface = user_data['surface'].lower()
                filtered_balls = [
                    ball for ball in balls
                    if (ball.surface_type.lower() in surface or
                        'универсальный' in ball.surface_type.lower() or
                        'универсальное' in surface)
                ]
                balls = filtered_balls if filtered_balls else balls

            try:
                gpt_recommendation = await self._get_gpt_recommendation(user_data)
            except Exception as e:
                logger.error(f"Error getting GPT recommendation: {e}")
                gpt_recommendation = (
                    f"На основе вашего уровня ({user_data['level']}) "
                    f"и места использования ({user_data.get('surface', 'разных условий')}) "
                    f"я подобрал подходящие мячи. У каждого из них есть свои преимущества, "
                    f"просмотрите детальную информацию ниже, чтобы выбрать наиболее подходящий вариант."
                )

            return gpt_recommendation, balls

        except Exception as e:
            logger.error(f"Error in get_recommendation: {str(e)}")
            raise

    async def _get_gpt_recommendation(self, user_data: Dict[str, Any]) -> str:
        messages = [
            {
                "role": "system",
                "content": "Вы - эксперт по гандбольному оборудованию. Дайте краткую рекомендацию на русском языке."
            },
            {
                "role": "user",
                "content": (
                    f"Посоветуйте гандбольный мяч для игрока уровня {user_data['level']}, "
                    f"который будет использовать его в {user_data.get('surface', 'разных условиях')}. "
                    f"Укажите оптимальный размер мяча для данного уровня, рекомендуемые материалы "
                    f"и приблизительный ценовой диапазон в евро."
                )
            }
        ]

        try:
            response = await self.client.chat.completions.create(
                model=Config.GPT_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in GPT request: {e}")
            raise