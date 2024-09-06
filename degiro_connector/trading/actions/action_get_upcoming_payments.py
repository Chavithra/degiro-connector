import logging

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.account import UpcomingPayments
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionGetUpcomingPayments(AbstractAction):

    @staticmethod
    def build_model(response: requests.Response) -> UpcomingPayments:
        model = UpcomingPayments.model_validate_json(json_data=response.text)

        return model

    @staticmethod
    def build_params_map() -> dict:
        params_map = {}

        return params_map

    @classmethod
    def get_upcoming_payements(
        cls,
        session_id: str,
        credentials: Credentials,
        logger: logging.Logger | None = None,
        raw: bool = False,
        session: requests.Session | None = None,
    ) -> UpcomingPayments | dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.UPCOMING_PAYMENTS
        url = f"{url}/{int_account}?intAccount={int_account};jsessionid={session_id}"
        params_map = cls.build_params_map()
        params_map.update({"intAccount": int_account, "sessionId": session_id})

        request = requests.Request(
            method="GET",
            params=params_map,
            url=url,
        )
        prepped = session.prepare_request(request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            if raw is True:
                model = loads(response.text)
            else:
                model = cls.build_model(response=response)
            return model
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        raw: bool = False,
    ) -> UpcomingPayments | dict | None:
        credentials = self.credentials
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        logger = self.logger

        return self.get_upcoming_payements(
            session_id=session_id,
            credentials=credentials,
            logger=logger,
            raw=raw,
            session=session,
        )
