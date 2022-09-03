import telegram
import requests
from util import *

def upload_photo_to_telegram_storage_bucket_and_return_file_id(file_data_name):
    file_data = open(file_data_name, 'rb')
    bot = telegram.Bot(TOKEN)
    b = bot.send_document(chat_id=CHAT_ID, document=file_data)
    print(b)
    return {
        'file_id': b['document']['file_id'],
        'file_unique_id': b['document']['file_unique_id']
    }

def get_file_name(file_id):
    file_about = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    about = requests.get(file_about).json()
    #print(about)
    file_name = about['result']['file_path'].split('/')[-1]

    #print(file_name)
    return file_name

def download_file_from_telegram_storage_bucket(file_name):
    actual_file = f'https://api.telegram.org/file/bot{TOKEN}/documents/{file_name}'
    r = requests.get(actual_file, allow_redirects=True)
    open(file_name, 'wb').write(r.content)


# id = upload_photo_to_telegram_storage_bucket_and_return_file_id('schema.jpg')
# name = get_file_name(id['file_id'])
# download_file_from_telegram_storage_bucket(name)
