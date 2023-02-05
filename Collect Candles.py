import argparse
import sys
import os
import requests


def main(env, prog, argv):
    base_url = env.get("API_ENDPOINT")
    access_token = env.get("ACCESS_TOKEN")
    if not base_url or not access_token:
        print("API_ENDPOINT e ACCESS_TOKEN são obrigatoriamente requeridas.")
        return 1
    args = get_parser(env, prog).parse_args(argv)
    print(f"Coletando {args.instrument}...")
    start_time = "2017-01-01T00:00:00.00Z"
    candles = fetch_page(base_url, access_token, args.instrument, start_time)
    print(candles)


def get_parser(env, prog):
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument("instrument", type=str)
    return parser


def fetch_page(base_url, access_token, instrument, start_time):
    url = f"{base_url}/v3/instruments/{instrument}/candles"
    headers = {
        "Authorization": f"bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "price": "BA",
        "granularity": "M15",
        "from": start_time,
    }
    print(url)
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200, f"{response.status.code}, {response.text}"
    return response.json()


if __name__ == "__main__":
    sys.exit(main(os.environ, sys.argv[0], sys.argv[1:]))
