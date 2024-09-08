import logging

from degiro_connector.core.exceptions import DeGiroConnectionError
import onetimepass as otp
import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.login import Login, LoginError, LoginSuccess


class ActionConnect(AbstractAction):
    @classmethod
    def get_session_id(
        cls,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> str:
        """Establish a connection with Degiro's Trading API.
        Args:
            credentials (Credentials):
                credentials.int_account (int)
                    Account unique identifer in Degiro's system.
                    It is optional.
                credentials.password (str)
                    Password used to log in the website.
                    It is mandatory.
                credentials.username (str)
                    Username used to log in the website.
                    It is mandatory.
                credentials.totp_secret is optional.
                    Secret code for Two-factor Authentication (2FA).
                    It is optional.
            session (requests.Session, optional):
                If you one wants to reuse existing "Session" object.
                Defaults to None.
            logger (logging.Logger, optional):
                If you one wants to reuse existing "Logger" object.
                Defaults to None.
        Raises:
            ConnectionError: Connection failed.
        Returns:
            str: Session id
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        if credentials.one_time_password or credentials.totp_secret_key:
            url = urls.LOGIN + "/totp"

            if credentials.one_time_password:
                one_time_password = str(credentials.one_time_password)
            else:
                totp_secret_key = credentials.totp_secret_key
                one_time_password = str(otp.get_totp(totp_secret_key))
        else:
            url = urls.LOGIN
            one_time_password = None

        login = Login(
            username=credentials.username,
            password=credentials.password,
            is_pass_code_reset=False,
            is_redirect_to_mobile=False,
            query_tarams={},
            one_time_password=one_time_password,
        )
        payload = login.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )
        request = requests.Request(
            method="POST",
            url=url,
            json=payload,
        )
        prepped = session.prepare_request(request)
        login_error = None
        login_sucess = None

        try:
            response = session.send(prepped)

            if response.status_code == 200:
                login_sucess = LoginSuccess.model_validate_json(json_data=response.text)
            else:
                login_error = LoginError.model_validate_json(json_data=response.text)
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
        except Exception as e:
            logger.fatal(e)

        if login_error:
            logger.fatal(
                "login_error:%s",
                login_error.model_dump(mode="python", by_alias=True, exclude_none=True),
            )

        if login_error and login_error.status == 6:
            raise DeGiroConnectionError('2FA is enabled, please provide the "totp_secret".', login_error)

        if login_sucess is None:
            raise DeGiroConnectionError("No session id returned.", login_error)

        logger.info(
            "login_sucess: %s",
            login_sucess.model_dump(mode="python", by_alias=True, exclude_none=True),
        )

        return login_sucess.session_id

    def call(self):
        connection_storage = self.connection_storage
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        connection_storage.session_id = self.get_session_id(
            credentials=credentials,
            logger=logger,
            session=session,
        )

        return connection_storage.session_id
