import click
import requests
import json
import os


def download_file(url, file_name):
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    return True

@click.command()
@click.argument('auth_id')
@click.argument('key')
@click.argument('sign')
def downloader(auth_id, key, sign):
    headers = {
        'Host': 'anti-captcha.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json; charset=utf-8',
    }

    data = {
        "auth": {
            "id": auth_id,
            "sign": sign,
            "key": key
        },
        "data": {
            "fromId": 0,
            "toTime": 0,
            "fromTime": 48,
            "showId": 0,
            "limit": 1000
        }
    }

    response = requests.post('https://anti-captcha.com/api/getcaptchas',
            headers=headers, json=data)

    if response.status_code != 200:
        print("Something went wrong with API !")
        return False
    
    result = json.loads(response.text)

    if result['error'] != 0:
        print("Something went wrong with API !")
        return False
    
    count = 0
    for item in result['response']:
        text = item['guesstext']
        img_path = "data/{}.png".format(text)
        if os.path.exists(img_path):
            print("- Duplicated captcha : {}".format(text))
        else:
            download_url = "https://anti-captcha.com{}".format(item['capcha_url'])
            download_file(download_url, img_path)
            count += 1
            print("+ Downloaded captcha : {}".format(text))

    print("===== Downloaded : {}".format(count))


if __name__ == '__main__':
    downloader()

