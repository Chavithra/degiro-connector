import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.login import RememberedDevice

DEVICE_COOKIE_PREFIX = "device"  # deviceUUID, deviceToken


class ActionRememberDevice(AbstractAction):
    @classmethod
    def remember_device(
        cls,
        credentials: Credentials | None = None,
        logger: logging.Logger | None = None,
        session: requests.Session | None = None,
    ) -> RememberedDevice | None:
        """Ask DeGiro to remember this device, like "Remember me" on the website.

        Call it right after a login approved in the app. Keep the result (it is as sensitive
        as the password) and set it on the credentials of later logins:
        `device_cookies` and `user_tokens`. Those logins then skip the in-app approval
        until the tokens expire (`ttl`, about 30 days).

        Args:
            credentials (Credentials, optional):
                Updated in place with the device data when given.
            session (requests.Session, optional):
                The session used for the login: DeGiro identifies it by its cookies.

        Returns:
            RememberedDevice | None: The device data, or None if DeGiro returned none.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        request = requests.Request(method="POST", url=urls.REMEMBER_ME)
        prepped = session.prepare_request(request)

        try:
            response_raw = session.send(prepped)
            response_raw.raise_for_status()
            payload = response_raw.json()
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        data = payload.get("data", payload) if isinstance(payload, dict) else {}
        user_tokens = data.get("userTokens") or data.get("tokens") or []
        device_cookies = {
            cookie.name: cookie.value
            for cookie in session.cookies
            if cookie.name.startswith(DEVICE_COOKIE_PREFIX) and cookie.value
        }

        if not user_tokens:
            logger.warning("remember_device: no tokens returned")
            return None

        device = RememberedDevice(
            user_tokens=user_tokens, device_cookies=device_cookies
        )

        if credentials is not None:
            credentials.user_tokens = device.user_tokens
            credentials.device_cookies = device.device_cookies

        return device

    def call(self) -> RememberedDevice | None:
        return self.remember_device(
            credentials=self.credentials,
            logger=self.logger,
            session=self.session_storage.session,
        )
