from datetime import timedelta
from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import (
    ContactUpdateCallbackData,
    ContactDeleteCallbackData,
    ContactDetailCallbackData,
)
from models import Contact
from views import View

__all__ = (
    'ContactDetailView',
    'ContactListView',
)


class ContactDetailView(View):

    def __init__(self, contact: Contact):
        self.__contact = contact

    def get_text(self) -> str:
        if self.__contact.to_user.username is not None:
            username = f'@{self.__contact.to_user.username}'
        else:
            username = 'нет'

        created_at_local_time = self.__contact.created_at + timedelta(hours=6)

        lines = [
            '<b>🙎🏿‍♂️ Контакт:</b>',
            f'Имя профиля: {self.__contact.to_user.fullname}',
            f'Username: {username}',
            f'Публичное имя: {self.__contact.public_name}',
            f'Приватное имя: {self.__contact.private_name}',
            f'Дата создания: {created_at_local_time:%H:%M %d.%m.%Y}'
        ]
        if self.__contact.is_hidden:
            lines.append('❗️ Скрыт в списке контактов')
        return '\n'.join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        is_hidden_status_toggle_button_text = (
            '✅ Показать в списке контактов' if self.__contact.is_hidden
            else '❌ Скрыть из списка контактов'
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='📝 Поменять публичное имя',
                        callback_data=ContactUpdateCallbackData().new(
                            contact_id=self.__contact.id,
                            field='public_name',
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='📝 Поменять приватное имя',
                        callback_data=ContactUpdateCallbackData().new(
                            contact_id=self.__contact.id,
                            field='private_name',
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=is_hidden_status_toggle_button_text,
                        callback_data=ContactUpdateCallbackData().new(
                            contact_id=self.__contact.id,
                            field='is_hidden',
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='❌ Удалить',
                        callback_data=ContactDeleteCallbackData().new(
                            contact_id=self.__contact.id,
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='🔙 Назад',
                        callback_data='show-contacts-list',
                    ),
                ],
            ],
        )


class ContactListView(View):

    def __init__(self, contacts: Iterable[Contact]):
        self.__contacts = tuple(contacts)

    def get_text(self) -> str:
        return (
            'Список ваших контактов 👱‍♂️'
            if self.__contacts else 'У вас нет контактов 😔'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for contact in self.__contacts:
            text = contact.private_name
            if contact.is_hidden:
                text = f'🙈 {text}'
            markup.row(
                InlineKeyboardButton(
                    text=text,
                    callback_data=ContactDetailCallbackData().new(
                        contact_id=contact.id,
                    ),
                ),
            )
        return markup
