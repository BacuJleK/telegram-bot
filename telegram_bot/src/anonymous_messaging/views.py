from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.views import View

__all__ = (
    'AnonymousMessagingToggledInGroupChatView',
    'AnonymousMessagingEnabledView',
    'AnonymousMessagingDisabledView',
)


class AnonymousMessagingToggledInGroupChatView(View):
    text = 'Чтобы писать анонимные сообщения, перейдите в лс бота'

    def __init__(self, bot_username: str):
        self.__bot_username = bot_username

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        url = f'https://t.me/{self.__bot_username}?start=settings'
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Перейти в лс',
                        url=url,
                    )
                ],
            ],
        )


class AnonymousMessagingEnabledView(View):
    text = (
        '💚 Вы <b><u>включили</u></b> анонимные сообщения.'
        '\n❗️ Всё что вы будете отправлять сюда, <b><u>будет'
        ' перенаправляться</u></b> в чат Манаса '
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='❗️ Выключить',
                    callback_data='toggle-anonymous-messaging-mode',
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='show-user-settings',
                )
            ],
        ],
    )


class AnonymousMessagingDisabledView(View):
    text = (
        '❤️ Вы <b><u>выключили</u></b> анонимные сообщения.'
        '\n❗️ Ваши сообщения больше <b><u>не</u></b>'
        ' будут перенаправляться в чат Манаса'
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='❗️ Включить',
                    callback_data='toggle-anonymous-messaging-mode',
                )
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='show-user-settings',
                )
            ],
        ],
    )
