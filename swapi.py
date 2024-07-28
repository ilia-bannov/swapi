from pathlib import Path
import requests


class APIRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url=None, params=None):
        url = self.base_url if url is None else self.base_url + url
        params = {'page': 1} if params is None else params
        try:
            response = requests.get(url, params)
            response.raise_for_status()
            return response
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')


class SWRequester(APIRequester):

    def __init__(self, base_url):
        super().__init__(base_url)

    def get_sw_categories(self):
        response = self.get('/')
        return response.json().keys()

    def get_sw_info(self, sw_type):
        response = self.get(f'/{sw_type}/')
        return response.text


def save_sw_data():
    swapi = SWRequester('https://swapi.dev/api')
    dir = 'data'
    Path(dir).mkdir(exist_ok=True)

    for category in swapi.get_sw_categories():
        with open(f'{dir}/{category}.txt', 'w') as f:
            f.write(swapi.get_sw_info(category))


save_sw_data()
