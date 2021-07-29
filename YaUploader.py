import requests


class YaUploader:
    _token = ''
    _request_methods = ['get', 'post', 'put', 'patch', 'delete']
    api_uri = 'https://cloud-api.yandex.net'
    file_url = ''

    def __init__(self, file_url, token):
        self._token = token
        self.file_url = file_url

    def _do_request(self, method, url, is_full_url=False, **kwargs):
        if method not in self._request_methods:
            print('Недопустимый метод')

        headers = dict({
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self._token}'
        }, **kwargs.get('headers', {}))
        kwargs['headers'] = headers

        return requests.request(method, f'{self.api_uri if not is_full_url else ""}{url}', **kwargs)

    def _create_dir(self, dir_path):
        result_path = ''

        try:
            for dir_name in dir_path.split('/'):
                params = {'path': f'{result_path}{dir_name}', 'overwrite': 'true'}
                response = self._do_request('put', '/v1/disk/resources', params=params)
                result_path += dir_name + '/'
                response.raise_for_status()
            return dir_path
        except requests.exceptions.HTTPError as error:
            if response.status_code == 409:
                return dir_path
            raise error

    def upload_from_url(self, target_path, file_name):
        if target_path:
            self._create_dir(target_path)

        params = {'url': self.file_url, 'path': f'{target_path}/{file_name}'}
        response = self._do_request('post', '/v1/disk/resources/upload', params=params)
        response.raise_for_status()

        return response.json()
