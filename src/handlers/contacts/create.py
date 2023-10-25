from aiogram import Router, F
from aiogram.filters import Command, invert_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models import User
from repositories import ContactRepository, UserRepository
from repositories import HTTPClientFactory
from states import ContactCreateWaitForForwardedMessage

__all__ = ('register_handlers',)


async def on_add_bot_to_contacts(message: Message) -> None:
    await message.reply('Вы не можете добавить бота в контакты')


async def on_add_self_to_contacts(message: Message) -> None:
    await message.reply('Вы не можете добавить себя в контакты')


async def on_contact_create_via_forwarded_message(
        message: Message,
        user: User,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    name = message.forward_from.username or message.forward_from.full_name
    async with closing_http_client_factory() as http_client:
        contact = ContactRepository(http_client)
        contacts = await contact.get_by_user_id(user.id)

        await contact.create(
            of_user_id=user.id,
            to_user_id=message.forward_from.id,
            private_name=name,
            public_name=name,
        )
        await message.reply(
            '✅ Контакт успешно добавлен.'
            ' Вы можете продолжать пересылать сообщения'
            ' чтобы добавить кого-то в контакты'
        )


async def on_enable_contact_create_via_forwarded_message_mode(
        message: Message,
        state: FSMContext
) -> None:
    await state.set_state(ContactCreateWaitForForwardedMessage.enabled)
    await message.reply(
        'Чтобы добавить кого-то, перешлите сообщение сюда любое его сообщение'
    )


async def on_contact_command_is_not_replied_to_user(
        message: Message,
) -> None:
    await message.reply(
        'Вы должны <b><u>ответить</u></b> на сообщение другого пользователя\n'
        'Подробная инструкция: <a href="https://graph.org/Kak-dobavit'
        '-polzovatelya-v-kontakty-08-14">*ссылка*</a>'
    )


async def on_add_contact(
        message: Message,
        user: User,
        user_repository: UserRepository,
        contact_repository: ContactRepository,
) -> None:
    reply = message.reply_to_message
    name = reply.from_user.username or reply.from_user.full_name

    to_user, is_to_user_created = await user_repository.get_or_create(
        user_id=reply.from_user.id,
        fullname=reply.from_user.full_name,
        username=reply.from_user.username,
    )

    if not to_user.can_be_added_to_contacts:
        await message.reply(
            '😔 Этот пользователь запретил добавлять себя в контакты',
        )
        return

    await contact_repository.create(
        of_user_id=user.id,
        to_user_id=to_user.id,
        private_name=name,
        public_name=name,
    )
    await message.reply('✅ Контакт успешно добавлен')


def register_handlers(router: Router) -> None:
    reply_to_user_is_bot = F.reply_to_message.from_user.is_bot
    from_self = F.reply_to_message.from_user.id == F.from_user.id

    router.message.register(
        on_contact_command_is_not_replied_to_user,
        Command('contact'),
        invert_f(F.reply_to_message),
        StateFilter('*'),
    )
    router.message.register(
        on_add_bot_to_contacts,
        Command('contact'),
        reply_to_user_is_bot,
        StateFilter('*'),
    )
    router.message.register(
        on_add_self_to_contacts,
        Command('contact'),
        from_self,
        StateFilter('*'),
    )
    router.message.register(
        on_add_contact,
        Command('contact'),
        StateFilter('*'),
    )
