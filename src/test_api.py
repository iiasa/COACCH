"""Test searching of Zenodo via its REST API"""

import os
import requests

def zen_search(dummy):
    """
    Search Zenodo
 
    Parameters:
       dummy( str): Does nothing for now
    """
    response = requests.get('https://zenodo.org/api/records',
                            params={'q': 'my title',
                                    'access_token': os.environ['ZENODO_API_TOKEN']})
    print(response.json())

zen_search("dummy")

