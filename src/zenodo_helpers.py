"""Helper functions for querying Zenodo datasets
"""

import chardet
import io
import json
import re
import requests
import time

def get_nb_hits(json_response):
    return len(json_response['hits']['hits'])

def get_next_link(json_response):
    return json_response['links'].get('next', None)

_request_delay = 1.0 # A dynamic delay to work around Zenodo rate limiting (seconds)

def reget(url, params=None, **kwargs):
    """
    Sends a GET request and resends it with increasing delays
    when status code 429 (too many requests) is received.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param **kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if params is None:
        print(f"URL: {url}")
    else:
        print(f"URL: {url}, params:")
        redacted_params = params
        del redacted_params['access_token'] # don't want to leak the token
        print(json.dumps(redacted_params, indent = 4))
    global _request_delay
    _request_delay /= 1.5
    time.sleep(_request_delay)
    while True:
        response = requests.get(url, params=params, **kwargs)
        if response.status_code != 429: # not too many requests
            return response
        _request_delay *= 1.5
        print(f"delay: {_request_delay}s to circumvent rate limiting...")
        time.sleep(_request_delay)

def guess_encoding(file, n_lines=20):
    '''Guess a file's encoding using chardet'''

    # Open the file as binary data
    if issubclass(type(file), io.BufferedIOBase):
        file.seek(0)
        rawdata = b''.join([file.readline() for _ in range(n_lines)])
        file.seek(0)
    else:
        # assume we were handed a file path
        with open(file, 'rb') as f:
            # Join binary lines for specified number of lines
            rawdata = b''.join([f.readline() for _ in range(n_lines)])

    return chardet.detect(rawdata)['encoding']

def strip_html_markup(html):
    html = re.sub(r'</?[a-zA-Z]+>', '', html)
    html = re.sub(r'&nbsp;', ' ', html)
    html = re.sub(r'&lt;', '<', html)
    html = re.sub(r'&gt;', '>', html)
    html = re.sub(r'&amp;', '&', html)
    return html

# Test
if __name__=="__main__":
    # When this fails, you might be running without appropriate environment variables set:
    # https://stackoverflow.com/questions/54828713/working-with-anaconda-in-visual-studio-code
    reget("https://google.com")
