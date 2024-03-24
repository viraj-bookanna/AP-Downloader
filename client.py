import re,requests,uuid,json

def create_playlist(playlist_url, title):
    headers = {
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Accept-Language': str(uuid.uuid4()),
        'Sec-Ch-Ua-Mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Android"',
        'Accept': '*/*',
        'Origin': 'https://ap.lk',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    playlist = requests.get(playlist_url, headers=headers, proxies=proxies, verify=verify)
    jdata = {
        'title': title,
        'url_prefix': playlist_url.split("/stream")[0],
        'headers': headers,
        'cookies': requests.utils.dict_from_cookiejar(playlist.cookies),
        'playlist': playlist.text
    }
    with open(f'{title}.json', 'w') as f:
        f.write(json.dumps(jdata, indent=4))
    return True

proxies = None#{'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
verify = False
requests.packages.urllib3.disable_warnings()
data = json.loads(input('JSON data: '))
create_playlist(data['url'], data['title'])
print(f"Config saved in {data['title']}.json\nSend the file to bot for downloading")