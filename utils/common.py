# -*- coding:utf-8 -*-

def check_http_resp(request_url, response):
    if response.status_code != 200:
        raise RuntimeError(f'Ops.. Request to {request_url} error.\n code: #{response.status_code} \n')


if __name__ == '__main__':
    pass
