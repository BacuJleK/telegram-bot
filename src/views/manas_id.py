from aiogram.types import InputFile

from enums import Course, Gender
from models import ManasId
from services.dates import compute_age
from services.manas_id import (
    generate_manas_id_number,
    humanize_personality_type, determine_zodiac_sign
)
from views import PhotoView

__all__ = ('ManasIdView',)


class ManasIdView(PhotoView):

    def __init__(self, manas_id: ManasId, photo: str | InputFile):
        self.__manas_id = manas_id
        self.__photo = photo

    def get_caption(self) -> str:
        course_name = {
            Course.BACHELOR_FIRST: '1 бакалавр',
            Course.BACHELOR_SECOND: '2 бакалавр',
            Course.BACHELOR_THIRD: '3 бакалавр',
            Course.BACHELOR_FOURTH: '4 бакалавр',
            Course.PREPARATION: 'хазырлык',
        }[self.__manas_id.course]
        gender_name = {
            Gender.MALE: 'мужской',
            Gender.FEMALE: 'женский',
        }[self.__manas_id.gender]

        manas_id_number = generate_manas_id_number(self.__manas_id)

        age = compute_age(self.__manas_id.born_at)
        if 1 <= age % 10 <= 4 and age // 10 != 1:
            age_suffix = 'года'
        else:
            age_suffix = 'лет'

        personality_type = humanize_personality_type(
            personality_type=self.__manas_id.personality_type,
        )
        zodiac_sign = determine_zodiac_sign(
            month=self.__manas_id.born_at.month,
            day=self.__manas_id.born_at.day,
        )

        lines = [
            '<b>🪪 Карточка студента</b>\n',
            '<b>📲 Личная информация:</b>',
            f'ФИО: {self.__manas_id.last_name} {self.__manas_id.first_name}',
            f'Дата рождения: {self.__manas_id.born_at:%d.%m.%Y}',
            f'Возраст: {compute_age(self.__manas_id.born_at)} {age_suffix}',
            f'Пол: {gender_name}\n',
            f'<b>🎓 Информация о студенте:</b>',
            f'Направление: {self.__manas_id.department.name}',
            f'Курс: {course_name}\n',
            f'<b>☁️ Система:</b>',
            f'ID номер: {manas_id_number}',
            f'Дата выдачи: {self.__manas_id.created_at:%d.%m.%Y}\n',
            f'<b>✏️ Прочее:</b>',
            f'Тип личности: {personality_type}',
            f'Знак зодиака: {zodiac_sign}',
        ]
        return '\n'.join(lines)

    def get_photo(self) -> str | InputFile:
        return self.__photo
