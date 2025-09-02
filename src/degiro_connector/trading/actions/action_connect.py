import logging

from degiro_connector.core.exceptions import CaptchaRequiredError, DeGiroConnectionError, MaintenanceError
from html.parser import HTMLParser
import pyotp
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
                credentials.in_app_token is optional.
                    Token for in-app TOTP confirmation.
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
            str: Session id if successful
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        one_time_password = None
        in_app_token = None

        if credentials.one_time_password or credentials.totp_secret_key:
            url = urls.LOGIN + "/totp"

            if credentials.one_time_password:
                one_time_password = str(credentials.one_time_password)
            else:
                totp_secret_key = credentials.totp_secret_key
                one_time_password = str(pyotp.TOTP(totp_secret_key).now())
        elif credentials.in_app_token:
            url = urls.LOGIN + "/in-app"
            if credentials.in_app_token:
                in_app_token = credentials.in_app_token
        else:
            url = urls.LOGIN

        login = Login(
            username=credentials.username,
            password=credentials.password,
            is_pass_code_reset=False,
            is_redirect_to_mobile=False,
            query_tarams={},
            one_time_password=one_time_password,
            in_app_token=in_app_token,
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
            elif response.status_code == 405:
                login_error = cls.__get_maintenance_message()
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

        if login_error:
            if login_error.captcha_required:
                raise CaptchaRequiredError(
                    "Captcha required. Login to DEGIRO via the browser and solve the captcha.",
                    login_error,
                )

            if login_error.status == 6:
                raise DeGiroConnectionError('2FA is enabled, please provide the "totp_secret".', login_error)

            if login_error.status == 12:
                raise DeGiroConnectionError('Open the DEGIRO app. To verify your login attempt, open the DEGIRO app and tap \'Yes\' to approve it".', login_error)

            if login_error.status == 405:
                raise MaintenanceError('Scheduled Maintenance.', login_error)

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

    @classmethod
    def __get_maintenance_message(cls) -> LoginError:
        response = requests.get(
            "https://trader.degiro.nl/login",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )
        parser = UnderConstContentParser()
        parser.feed(response.text)
        text_content = " ".join(parser.content)
        return LoginError(error=text_content, status=405, status_text="Scheduled maintenance")

class UnderConstContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.content = []
        self.capture = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("id") == "under-const-content":
            self.recording = True
        elif self.recording:
            self.capture = True

    def handle_endtag(self, tag):
        if self.recording and tag == "div":
            self.recording = False
        self.capture = False

    def handle_data(self, data):
        if self.recording and self.capture:
            cleaned = data.strip()
            if cleaned:
                self.content.append(cleaned)