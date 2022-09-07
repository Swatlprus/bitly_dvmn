import os
import json
import requests
from urllib.parse import urlparse
from environs import Env
import argparse


def shorten_link(url, bitly_token):
    headers = {'Authorization': f'Bearer {bitly_token}'}
    payload = {'long_url': url}
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(bitlink, bitly_token):
    url_parts = urlparse(bitlink)
    basic_url = f'{url_parts.netloc}{url_parts.path}'
    headers = {'Authorization': f'Bearer {bitly_token}'}
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{basic_url}\
    /clicks/summary'
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def is_bitlink(url, bitly_token):
    url_parts = urlparse(url)
    basic_url = f'{url_parts.netloc}{url_parts.path}'
    headers = {'Authorization': f'Bearer {bitly_token}'}
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{basic_url}'
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def main():
    env = Env()
    env.read_env()
    bitly_token = env("BITLY_TOKEN")
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    if is_bitlink(args.url, bitly_token):
        print('Total clicks:', count_clicks(args.url, bitly_token))
    else:
        print('Shorten link:', shorten_link(args.url, bitly_token))


if __name__ == '__main__':
    main()