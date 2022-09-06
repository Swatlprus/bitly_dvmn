import os
import json
import requests
from urllib.parse import urlparse
from environs import Env
import argparse

env = Env()
env.read_env()
TOKEN_BITLY = env("TOKEN_BITLY")

def shorten_link(TOKEN_BITLY, url):
    headers = {'Authorization': f'Bearer {TOKEN_BITLY}'}
    payload = {'long_url': url}
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(TOKEN_BITLY, bitlink):
    headers = {'Authorization': f'Bearer {TOKEN_BITLY}'}
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}\
    /clicks/summary'
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def is_bitlink(url, TOKEN_BITLY):
    headers = {'Authorization': f'Bearer {TOKEN_BITLY}'}
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    response = requests.get(bitly_url, headers=headers)
    return response.ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    url_arg = parser.add_argument('url')
    args = parser.parse_args()
    link_from_args = args.url
    url_parts = urlparse(link_from_args)
    basic_url = f'{url_parts.netloc}{url_parts.path}'
    if is_bitlink(basic_url, TOKEN_BITLY):
        print('Total clicks:', count_clicks(TOKEN_BITLY, basic_url))
    else:
        print('Shorten link:', shorten_link(TOKEN_BITLY, link_from_args))
