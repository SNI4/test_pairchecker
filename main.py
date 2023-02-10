from requests import get

pair = "XRPUSDT"

mark_link = f"https://www.binance.com/fapi/v1/premiumIndex?symbol={pair}"
highest_for_1h_link = f"https://www.binance.com/fapi/v1/continuousKlines?limit=1000&pair={pair}&contractType=PERPETUAL&interval=1h"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 RuxitSynthetic/1.0 v1421166880075707927 t7527522693257895152 ath5ee645e0 altpriv cvcv=2 smf=0",
    "Reffer": "https://www.binance.com/en/futures/XRP_USDT",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip,deflate,br",
    "lang": "en"
}

res_message = lambda lprice, lhigh_price, ldifference: f"XRP/USDT Mark price: {lprice}\nHighest XRP/USDT mark price: {lhigh_price}\n" \
           f"The difference in prices is more than 1 ({ldifference}) percent!"


def get_highest_1h_price(url: str, heads: dict) -> float:
    return float(get(url, headers=heads, timeout=1.5).json()[-1][2])


def get_mark_price(url: str, heads: dict) -> float:
    return float(get(url, headers=heads, timeout=1.5).json()['markPrice'])


def mark_scanner(mark_url: str, highest_url: str, heads: dict) -> list:
    highest_price = get_highest_1h_price(highest_url, heads)
    mark_price = get_mark_price(mark_url, heads)
    res_difference = ((highest_price - mark_price) / mark_price) * 100

    return [res_difference, mark_price, highest_price]


if __name__ == "__main__":
    # в get-запросах выставлена задержка в 1.5 секунды
    while 1:
        difference, price, high_price = mark_scanner(mark_url=mark_link, highest_url=highest_for_1h_link, heads=headers)
        if difference >= 1:
            print(res_message(difference, price, high_price))