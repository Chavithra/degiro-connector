import logging
from typing import Literal, overload

import requests

from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.company_logo import CompanyLogo
from degiro_connector.trading.actions.action_get_company_logo_url import (
    ActionGetCompanyLogoUrl,
)


class ActionGetCompanyLogo(AbstractAction):
    @overload
    @classmethod
    def get_company_logo(
        cls,
        product_isin: str,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
        timeout: float = 30,
        include_metadata: Literal[False] = False,
    ) -> bytes | None: ...

    @overload
    @classmethod
    def get_company_logo(
        cls,
        product_isin: str,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
        timeout: float = 30,
        *,
        include_metadata: Literal[True],
    ) -> CompanyLogo | None: ...

    @overload
    @classmethod
    def get_company_logo(
        cls,
        product_isin: str,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
        timeout: float = 30,
        include_metadata: bool = False,
    ) -> bytes | CompanyLogo | None: ...

    @classmethod
    def get_company_logo(
        cls,
        product_isin: str,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
        timeout: float = 30,
        include_metadata: bool = False,
    ) -> bytes | CompanyLogo | None:
        """Download logo bytes, returning None on request or content-type errors.

        No credentials or trading connection are required. When no session is
        supplied, a separate session is created and closed after the request.
        Set include_metadata=True to receive a CompanyLogo with the response's
        content type and a suitable file extension, alongside the image bytes.
        """
        if logger is None:
            logger = cls.build_logger()
        owns_session = session is None
        if session is None:
            session = cls.build_session()

        url = ActionGetCompanyLogoUrl.get_company_logo_url(product_isin)
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            content_type = (
                response.headers.get("Content-Type", "application/octet-stream")
                .split(";", 1)[0]
                .strip()
                .lower()
            ) or "application/octet-stream"
            if not content_type.startswith("image/") and content_type != (
                "application/octet-stream"
            ):
                logger.error("Unexpected company logo content type: %s", content_type)
                return None
            if include_metadata:
                return CompanyLogo(
                    content=response.content,
                    content_type=content_type,
                )
            return response.content
        except requests.RequestException as error:
            logger.error("Could not retrieve company logo: %s", error)
            return None
        finally:
            if owns_session:
                session.close()

    @overload
    def call(
        self,
        product_isin: str,
        timeout: float = 30,
        include_metadata: Literal[False] = False,
    ) -> bytes | None: ...

    @overload
    def call(
        self,
        product_isin: str,
        timeout: float = 30,
        *,
        include_metadata: Literal[True],
    ) -> CompanyLogo | None: ...

    @overload
    def call(
        self,
        product_isin: str,
        timeout: float = 30,
        include_metadata: bool = False,
    ) -> bytes | CompanyLogo | None: ...

    def call(
        self,
        product_isin: str,
        timeout: float = 30,
        include_metadata: bool = False,
    ) -> bytes | CompanyLogo | None:
        # Keep trading cookies and connection hooks out of this public request.
        return self.get_company_logo(
            product_isin=product_isin,
            logger=self.logger,
            timeout=timeout,
            include_metadata=include_metadata,
        )
