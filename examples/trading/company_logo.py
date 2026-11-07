from pathlib import Path

from degiro_connector.trading.actions.action_get_company_logo import (
    ActionGetCompanyLogo,
)
from degiro_connector.trading.actions.action_get_company_logo_url import (
    ActionGetCompanyLogoUrl,
)

if __name__ == "__main__":
    # No credentials, configuration file, or connect() call are needed.
    product_isin = "US0378331005"  # Apple
    logo_url = ActionGetCompanyLogoUrl.get_company_logo_url(product_isin)
    print(logo_url)

    logo = ActionGetCompanyLogo.get_company_logo(product_isin, include_metadata=True)
    if logo is None:
        raise SystemExit("Could not download the company logo.")

    # Use Content-Type to choose .svg, .png, etc.; unknown types use .bin.
    output = Path(f"apple-logo{logo.extension}")
    output.write_bytes(logo.content)
    print(f"Saved {len(logo.content)} bytes ({logo.content_type}) to {output}")
