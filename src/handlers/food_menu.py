import asyncio

from aiogram import Router, F
from aiogram.filters import StateFilter, Command, or_f
from aiogram.types import Message

from exceptions import InsufficientFundsForWithdrawalError
from filters import (
    food_menu_for_tomorrow_filter,
    food_menu_for_today_filter,
    food_menu_for_n_days_filter,
)
from repositories import BalanceRepository, FoodMenuRepository
from services import BalanceNotifier
from views import FoodMenuMediaGroupView, answer_view, FoodMenuFAQView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == '/yemek week',
    StateFilter('*'),
)
async def on_show_food_menu_for_week_ahead(
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
        food_menu_repository: FoodMenuRepository,
) -> None:
    food_menus = await food_menu_repository.get_all()

    for daily_food_menu in food_menus[:7]:
        view = FoodMenuMediaGroupView(daily_food_menu)
        await message.answer_media_group(
            media=view.as_media_group(),
            disable_notification=True,
        )
        await asyncio.sleep(0.5)

    try:
        withdrawal = await balance_repository.create_withdrawal(
            user_id=message.from_user.id,
            amount=560,
            description='Просмотр йемека на неделю вперёд',
        )
    except InsufficientFundsForWithdrawalError:
        await message.reply(
            '❌ Недостаточно средств для списания\n'
            '💸 Стоимость просмотра йемека: 560 дак-дак коинов'
        )
        return
    await balance_notifier.send_withdrawal_notification(withdrawal)


@router.message(
    or_f(
        food_menu_for_today_filter,
        food_menu_for_tomorrow_filter,
        food_menu_for_n_days_filter,
    ),
    StateFilter('*'),
)
async def on_show_food_menu_for_specific_day(
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
        food_menu_repository: FoodMenuRepository,
        days_skip_count: int,
) -> None:
    food_menus = await food_menu_repository.get_all()

    try:
        food_menu = food_menus[days_skip_count]
    except IndexError:
        await message.reply('❌ Нет данных о меню на указанный день')
        return

    view = FoodMenuMediaGroupView(food_menu)
    await message.answer_media_group(media=view.as_media_group())

    try:
        withdrawal = await balance_repository.create_withdrawal(
            user_id=message.from_user.id,
            amount=80,
            description='Просмотр йемека на сегодня',
        )
    except InsufficientFundsForWithdrawalError:
        await message.reply(
            '❌ Недостаточно средств для списания\n'
            '💸 Стоимость просмотра йемека: 80 дак-дак коинов'
        )
        return
    await balance_notifier.send_withdrawal_notification(withdrawal)


@router.message(
    Command('yemek'),
    StateFilter('*'),
)
async def on_show_food_menu_instructions(message: Message) -> None:
    await answer_view(message=message, view=FoodMenuFAQView())
