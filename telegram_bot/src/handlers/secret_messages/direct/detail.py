from uuid import UUID

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import (
    SecretMessageDetailCallbackData,
    SecretMessageForTeamCallbackData,
)
from repositories import (
    ContactRepository,
    SecretMessageRepository,
    HTTPClientFactory,
    TeamMemberRepository,
)
from services import can_see_contact_secret, can_see_team_secret

__all__ = ('register_handlers',)


async def on_show_team_message(
        callback_query: CallbackQuery,
        callback_data: dict,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    team_id: int = callback_data['team_id']
    secret_message_id: UUID = callback_data['secret_message_id']

    async with closing_http_client_factory() as http_client:
        team_member_repository = TeamMemberRepository(http_client)
        secret_message_repository = SecretMessageRepository(http_client)

        team_members = await team_member_repository.get_by_team_id(team_id)
        secret_message = await secret_message_repository.get_by_id(
            secret_message_id=secret_message_id,
        )

    if not can_see_team_secret(
            user_id=callback_query.from_user.id,
            team_members=team_members,
    ):
        text = 'Это сообщение не предназначено для тебя 😉'
    else:
        text = secret_message.text
    await callback_query.answer(text, show_alert=True)


async def on_show_contact_message(
        callback_query: CallbackQuery,
        callback_data: SecretMessageDetailCallbackData,
        closing_http_client_factory: HTTPClientFactory,
) -> None:

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        secret_message_repository = SecretMessageRepository(http_client)

        contact = await contact_repository.get_by_id(callback_data.contact_id)
        secret_message = await secret_message_repository.get_by_id(
            secret_message_id=callback_data.secret_message_id,
        )

    if not can_see_contact_secret(
            user_id=callback_query.from_user.id,
            contact=contact,
    ):
        text = 'Это сообщение не предназначено для тебя 😉'
    else:
        text = secret_message.text
    await callback_query.answer(text, show_alert=True)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_team_message,
        SecretMessageForTeamCallbackData.filter(),
        StateFilter('*'),
    )
    router.callback_query.register(
        on_show_contact_message,
        SecretMessageDetailCallbackData.filter(),
        StateFilter('*'),
    )
