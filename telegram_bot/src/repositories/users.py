import models
from exceptions import (
    UserDoesNotExistError,
    ServerAPIError,
    UserAlreadyExistsError,
)
from repositories import APIRepository

__all__ = ('UserRepository',)


class UserRepository(APIRepository):

    async def get_by_id(self, user_id: int) -> models.User:
        """Get user by ID.

        Args:
            user_id: User's Telegram ID.

        Returns:
            User model.

        Raises:
            UserDoesNotExistError: If user with given ID does not exist.
            ServerAPIError: If server returns unexpected response status code.
        """
        url = f'/users/{user_id}/'
        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise UserDoesNotExistError(user_id=user_id)
            if response.status != 200:
                raise ServerAPIError
            response_data = await response.json()
        return models.User.model_validate(response_data)

    async def create(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
    ) -> models.User:
        """Create user on the server.

        Keyword Args:
            user_id: User's Telegram ID.
            fullname: User's full name.
            username: User's username.

        Returns:
            User model.

        Raises:
            UserAlreadyExistsError: If user with given ID already exists.
            ServerAPIError: If server returns unexpected response status code.
        """
        request_data = {
            'id': user_id,
            'fullname': fullname,
            'username': username,
        }
        url = '/users/'
        async with self._http_client.post(url, json=request_data) as response:
            if response.status == 409:
                raise UserAlreadyExistsError
            if response.status != 201:
                raise ServerAPIError
            response_data = await response.json()
        return models.User.model_validate(response_data)

    async def update(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
            can_be_added_to_contacts: bool,
            is_premium: bool,
            secret_messages_theme_id: int | None,
    ) -> None:
        """Update user's data on the server.

        Keyword Args:
            user_id: User's Telegram ID.
            fullname: User's full name.
            username: User's username.
            can_be_added_to_contacts: Whether user can be added to contacts.
            is_premium: Whether user is premium.
            secret_messages_theme_id: User's secret messages theme ID.

        Raises:
            UserDoesNotExistError: If user with given ID does not exist.
            ServerAPIError: If server returned unexpected response status code.
        """
        request_data = {
            'fullname': fullname,
            'username': username,
            'can_be_added_to_contacts': can_be_added_to_contacts,
            'is_premium': is_premium,
            'secret_message_theme_id': secret_messages_theme_id,
        }
        url = f'/users/{user_id}/'
        async with self._http_client.put(url, json=request_data) as response:
            if response.status == 404:
                raise UserDoesNotExistError(user_id=user_id)
            if response.status != 204:
                raise ServerAPIError
