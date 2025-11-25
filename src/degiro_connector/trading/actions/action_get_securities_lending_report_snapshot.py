import logging
import re
from datetime import date as Date

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.securities_lending import SecuritiesLendingReportSnapshot
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.actions.action_get_securities_lending_report_date import ActionGetSecuritiesLendingReportDate

# Date format constant for API compatibility
DATE_FORMAT = "%Y-%m-%d"


class ActionGetSecuritiesLendingReportSnapshot(AbstractAction):

    @staticmethod
    def build_model(response: requests.Response) -> SecuritiesLendingReportSnapshot:
        model = SecuritiesLendingReportSnapshot.model_validate_json(json_data=response.text)

        return model

    @staticmethod
    def build_params_map(date: Date | str | None = None) -> dict:
        """Build params map with date parameter.
        
        Args:
            date: Date object or string in YYYY-MM-DD format. If None, date is omitted.
                String dates are validated to ensure they match YYYY-MM-DD format.
                Invalid string formats will raise ValueError.
        
        Returns:
            dict: Parameters map with date formatted as YYYY-MM-DD string.
        
        Raises:
            TypeError: If date is not a date object or string.
            ValueError: If date is a string that doesn't match YYYY-MM-DD format or is not a valid date.
        """
        params_map = {}
        if date is not None:
            # Convert date object to YYYY-MM-DD format string
            if isinstance(date, Date):
                date_str = date.strftime(DATE_FORMAT)
            elif isinstance(date, str):
                # Validate string format matches YYYY-MM-DD and is a valid date
                date_str = date
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                    raise ValueError(
                        f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD format (e.g., '2024-01-15')"
                    )
                # Validate that it's actually a valid date (catches cases like 2025-13-45)
                try:
                    Date.fromisoformat(date_str)
                except ValueError as e:
                    raise ValueError(
                        f"Invalid date value: '{date_str}'. {str(e)}"
                    ) from e
            else:
                raise TypeError(
                    f"Invalid date type: expected date or str, got {type(date).__name__}"
                )
            params_map["date"] = date_str

        return params_map

    def _fetch_default_date(self) -> str | None:
        """Fetch the default date from get_securities_lending_report_date.
        
        Returns:
            str | None: The date string if successful, None otherwise.
        """
        date_action = ActionGetSecuritiesLendingReportDate(
            credentials=self.credentials,
            connection_storage=self.connection_storage,
            logger=self.logger,
            session_storage=self.session_storage,
        )
        date_result = date_action.call(raw=False)
        
        if date_result is None:
            # Check connection state to provide context
            session_id = self.connection_storage.session_id
            has_session = session_id is not None and session_id != ""
            connection_status = "connected" if has_session else "not connected"
            
            self.logger.error(
                "Failed to fetch securities lending report date. "
                f"Connection status: {connection_status}. "
                "Check logs above for detailed error information (HTTP status, response body, etc.)"
            )
            return None
        
        # Extract date from the response
        if isinstance(date_result, dict):
            # When raw=True, date is still a string in the dict
            date_value = date_result.get("data", {}).get("date")
        else:
            # When raw=False, date is a date object from the model
            date_value = date_result.data.date
        
        if date_value is None:
            self.logger.error("Date not found in securities lending report date response")
            return None
        
        # Convert date object to YYYY-MM-DD string format if needed
        if isinstance(date_value, Date):
            return date_value.strftime(DATE_FORMAT)
        else:
            # Already a string (from raw=True case)
            return str(date_value)

    @classmethod
    def get_securities_lending_report_snapshot(
        cls,
        session_id: str,
        credentials: Credentials,
        date: Date | str | None = None,
        logger: logging.Logger | None = None,
        raw: bool = False,
        session: requests.Session | None = None,
    ) -> SecuritiesLendingReportSnapshot | dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.SECURITIES_LENDING_REPORTING_SNAPSHOT
        params_map = cls.build_params_map(date=date)
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
        date: Date | str | None = None,
        raw: bool = False,
    ) -> SecuritiesLendingReportSnapshot | dict | None:
        # If date is not provided, fetch it from get_securities_lending_report_date
        if date is None:
            date = self._fetch_default_date()
            if date is None:
                return None

        return self.get_securities_lending_report_snapshot(
            session_id=self.connection_storage.session_id,
            credentials=self.credentials,
            date=date,
            logger=self.logger,
            raw=raw,
            session=self.session_storage.session,
        )

