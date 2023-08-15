from aiogram import Dispatcher
from aiogram.types import Update

from exceptions import ContactDoesNotExistError, ContactAlreadyExistsError

__all__ = ('register_handlers',)


async def on_contact_does_not_exist_error(
        update: Update,
        _: ContactDoesNotExistError,
) -> bool:
    text = '😔 Контакт не существует или был удален'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    return True


async def on_contact_already_exists_error(
        update: Update,
        _: ContactAlreadyExistsError,
) -> bool:
    text = '😶 Этот пользователь уже есть в ваших контактах'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    return True


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_contact_does_not_exist_error,
        exception=ContactDoesNotExistError,
    )
    dispatcher.register_errors_handler(
        on_contact_already_exists_error,
        exception=ContactAlreadyExistsError,
    )
