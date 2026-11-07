from urllib.parse import quote

from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.core.constants import urls


class ActionGetCompanyLogoUrl(AbstractAction):
    @staticmethod
    def get_company_logo_url(product_isin: str) -> str:
        """Build a public logo URL without authentication or a network request."""
        return f"{urls.COMPANY_LOGO}/{quote(product_isin, safe='')}"

    def call(self, product_isin: str) -> str:
        return self.get_company_logo_url(product_isin=product_isin)
