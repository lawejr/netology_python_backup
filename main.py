import json
import os
from VKApi import VKApi
from YaUploader import YaUploader


class VKBackup:
    vk_api = None
    ya_access = None

    def __init__(self, vk_token, ya_token):
        self.vk_api = VKApi(vk_token)
        self.ya_access = ya_token

    def make_backup(self, dir_name='vk_photo_backup'):
        log = {}
        log_file = 'backup_log.json'
        photos = self.vk_api.get_photos()
        total_count = len(photos)
        result = []
        index = 0

        for photo in photos:
            size = sorted(photo['sizes'], key=lambda s: s['type'])[-1]
            likes_count = f'{photo["likes"]["count"]}'
            name = f'{likes_count}.jpg' if f'{likes_count}.jpg' not in log else f'{likes_count}{photo["date"]}.jpg'
            result_item = {
                'file_name': name,
                'link': size['url'],
                'size': size['type']
            }
            result.append(result_item)
            log[name] = {
                'file_name': name,
                'size': size['type']
            }

            uploader = YaUploader(file_url=size['url'], token=self.ya_access)
            uploader.upload_from_url(target_path=dir_name, file_name=name)
            index += 1

            print(f'Сохранено {index} из {total_count} файлов')

        print(f'Резервная копия сохранена в папке {dir_name} на Я.Диске')

        with open(log_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(list(log.values())))

        print(f'Лог сохранён в файл {os.path.abspath(os.getcwd())}{os.path.sep}{log_file}')

        return result


# ПОДСТАВИТЬ ТОКЕН ПРИЛОЖЕНИЯ VK
VK_ACCESS = ''
ya_access = input('Введите токен Яндекс.Диска: ')


vk = VKBackup(vk_token=VK_ACCESS, ya_token=ya_access)
vk.make_backup()
