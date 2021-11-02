# IMPORTATION STANDARD
import logging

# IMPORTATION THIRD PARTY
import onetimepass as otp
import requests

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
)


class ActionConnect(AbstractAction):
    @classmethod
    def get_session_id(
        cls,
        credentials: Credentials,
        session: requests.Session = None,
        logger: logging.Logger = None,
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

        if credentials.HasField("oneof_2fa") is True:
            url = urls.LOGIN + "/totp"
            username = credentials.username
            password = credentials.password

            if credentials.HasField("totp_secret_key") is True:
                totp_secret_key = credentials.totp_secret_key
                one_time_password = str(otp.get_totp(totp_secret_key))
            else:
                one_time_password = str(credentials.one_time_password)

            payload_dict = {
                "username": username,
                "password": password,
                "isPassCodeReset": False,
                "isRedirectToMobile": False,
                "queryParams": {},
                "oneTimePassword": one_time_password,
            }
        else:
            url = urls.LOGIN
            username = credentials.username
            password = credentials.password

            payload_dict = {
                "username": username,
                "password": password,
                "isPassCodeReset": False,
                "isRedirectToMobile": False,
                "queryParams": {},
            }

        request = requests.Request(
            method="POST",
            url=url,
            json=payload_dict,
        )
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()
        except Exception as e:
            logger.fatal("response_raw:%s", response_raw)
            raise ConnectionError(e)

        logger.info("get_session_id:response_dict: %s", response_dict)

        if "sessionId" in response_dict:
            return response_dict["sessionId"]
        elif "status" in response_dict and response_dict["status"] == 6:
            logger.fatal("response_dict:%s", response_dict)
            raise ConnectionError('2FA is enabled, please provide the "totp_secret".')
        else:
            logger.fatal("response_dict:%s", response_dict)
            raise ConnectionError("No session id returned.")

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
