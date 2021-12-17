# IMPORTATION STANDARD
import logging
from typing import Dict, List, Union

# IMPORTATION THIRD PARTY
import requests
from google.protobuf import json_format

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
    ProductsInfo,
)


class ActionGetProductsInfo(AbstractAction):
    @staticmethod
    def products_info_to_api(
        request: ProductsInfo.Request,
    ) -> List[str]:
        request_dict = json_format.MessageToDict(
            message=request,
            including_default_value_fields=True,
            preserving_proto_field_name=False,
            use_integers_for_enums=True,
            descriptor_pool=None,
            float_precision=None,
        )
        payload = request_dict["products"]
        payload = list(map(str, payload))

        return payload

    @staticmethod
    def products_info_to_grpc(payload: dict) -> ProductsInfo:
        products_info = ProductsInfo()
        json_format.ParseDict(
            js_dict={"values": payload["data"]},
            message=products_info,
            ignore_unknown_fields=False,
            descriptor_pool=None,
        )
        return products_info

    @classmethod
    def get_products_info(
        cls,
        request: ProductsInfo.Request,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[ProductsInfo, Dict, None]:
        """Search for products using their ids.
        Args:
            request (ProductsInfo.Request):
                List of products ids.
                Example :
                    request = ProductsInfo.Request()
                    request.products.extend([96008, 1153605, 5462588])
            session_id (str):
                API's session id.
            credentials (Credentials):
                Credentials containing the parameter "int_account".
            raw (bool, optional):
                Whether are not we want the raw API response.
                Defaults to False.
            session (requests.Session, optional):
                This object will be generated if None.
                Defaults to None.
            logger (logging.Logger, optional):
                This object will be generated if None.
                Defaults to None.
        Returns:
            ProductsInfo: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.PRODUCTS_INFO

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        payload = cls.products_info_to_api(request=request)

        http_request = requests.Request(
            method="POST",
            url=url,
            json=payload,
            params=params,
        )
        prepped = session.prepare_request(http_request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.products_info_to_grpc(
                    payload=response_dict,
                )
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        request: ProductsInfo.Request,
        raw: bool = False,
    ) -> Union[ProductsInfo, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_products_info(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
