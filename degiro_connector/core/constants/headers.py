HEADERS = {
    "Connection": "keep-alive",
    # The length is setup automatically by the Requests library
    # "Content-Length": "39",
    "Sec-Fetch-Dest": "empty",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/94.0.4606.54 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://trader.degiro.nl",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    # Requests library doesn't support "br" (brotli algorithm)
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
}
