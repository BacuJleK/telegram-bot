from aiogram.filters.callback_data import CallbackData

__all__ = (
    'ContactDetailCallbackData',
    'ContactUpdateCallbackData',
    'ContactDeleteCallbackData',
)


class ContactDetailCallbackData(CallbackData, prefix='contact-detail'):
    contact_id: int


class ContactUpdateCallbackData(CallbackData, prefix='contact-update'):
    contact_id: int
    field: str


class ContactDeleteCallbackData(CallbackData, prefix='contact-delete'):
    contact_id: int
