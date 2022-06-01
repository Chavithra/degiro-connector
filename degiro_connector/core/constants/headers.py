HEADERS = {
    "Accept": "application/json, text/plain, */*",
    # Requests library doesn't support "br" (brotli algorithm)
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    # The length is setup automatically by the Requests library
    # "Content-Length": "39",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://trader.degiro.nl",
    "Referer": "https://trader.degiro.nl/login/fr",
    "Sec-CH-UA": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/102.0.5005.63 Safari/537.36",
}
