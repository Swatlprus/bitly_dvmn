import os
import json
import requests
from urllib.parse import urlparse
from environs import Env
import argparse

BITLY_TOKEN = None

def shorten_link(BITLY_TOKEN, url):
    headers = {'Authorization': f'Bearer {BITLY_TOKEN}'}
    payload = {'long_url': url}
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(BITLY_TOKEN, bitlink):
    headers = {'Authorization': f'Bearer {BITLY_TOKEN}'}
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}\
    /clicks/summary'
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def is_bitlink(url, BITLY_TOKEN):
    headers = {'Authorization': f'Bearer {BITLY_TOKEN}'}
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def main():
    env = Env()
    env.read_env()
    BITLY_TOKEN = env("BITLY_TOKEN")
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    url_parts = urlparse(args.url)
    basic_url = f'{url_parts.netloc}{url_parts.path}'
    if is_bitlink(basic_url, BITLY_TOKEN):
        print('Total clicks:', count_clicks(BITLY_TOKEN, basic_url))
    else:
        print('Shorten link:', shorten_link(BITLY_TOKEN, args.url))


if __name__ == '__main__':
    main()

