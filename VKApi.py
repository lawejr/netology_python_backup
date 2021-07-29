import requests


class VKApi:
    _token = ''
    owner = ''

    def __init__(self, token):
        while not self.owner:
            self._token = token
            self.owner = input('Введите ID пользователя, для сохранения фотографий: ')

    def get_photos(self, count=5, album='profile'):
        params = {'access_token': self._token,
                  'owner_id': self.owner,
                  'album_id': album,
                  'extended': '1',
                  'count': count,
                  'v': 5.131}
        photos = requests.get('https://api.vk.com/method/photos.get', params=params).json()['response']['items']

        return photos
