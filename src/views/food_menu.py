import textwrap

from aiogram.types import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder

from models import DailyFoodMenu
from views.base import View

__all__ = ('FoodMenuMediaGroupView', 'FoodMenuFAQView')


class FoodMenuMediaGroupView(View):

    def __init__(self, daily_food_menu: DailyFoodMenu):
        self.__daily_food_menu = daily_food_menu

    def get_text(self) -> str:
        caption: list[str] = [
            f'🍽️ <b>Меню на {self.__daily_food_menu.at:%d.%m.%Y}</b> 🍽️\n'
        ]

        total_calories_count: int = 0

        for food_menu_item in self.__daily_food_menu.items:
            caption.append(
                f'🧂 <u>{food_menu_item.name}</u>\n'
                f'🌱 Калории: <i>{food_menu_item.calories_count}</i>\n'
            )

            total_calories_count += food_menu_item.calories_count

        caption.append(f'<b>Сумма калорий: {total_calories_count}</b>')
        return '\n'.join(caption)

    def as_media_group(self) -> list[InputMediaPhoto]:
        input_media_photos: list[InputMediaPhoto] = [
            InputMediaPhoto(
                media=str(food_menu_item.photo_url),
                caption=self.get_text(),
            ) for food_menu_item in self.__daily_food_menu.items
        ]
        media_group_builder = MediaGroupBuilder(
            media=input_media_photos,
            caption=self.get_text(),
        )
        return media_group_builder.build()


class FoodMenuFAQView(View):
    text = textwrap.dedent('''\
    <b>🤤Срочный просмотр меню в йемекхане:</b>

    🍏На сегодня:
    <code>/yemek today</code>
    
    🍏На завтра:
    <code>/yemek tomorrow</code>
    
    🍏На неделю вперёд:
    <code>/yemek week</code>
    
    <b>🧐Так же можно просматривать на N дней вперёд:</b>
    
    •<code>/yemek {N}</code>
    
    Например👇
    🍎На послезавтра - <code>/yemek 2</code>
    🍎10 дней вперёд - <code>/yemek 10</code>
    
    <b>👇 Так же можете посмотреть меню в онлайн режиме:</b>
    https://t.me/duck_duck_robot/yemek
    ''')
