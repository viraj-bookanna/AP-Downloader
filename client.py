import re,requests,uuid,json

def create_playlist(server_url, playlist_url, title):
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
    response = requests.post(server_url, json=jdata, proxies=proxies, verify=verify).json()
    return response, 'sessionid='+playlist.cookies.get('sessionid')

proxies = None#{'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
verify = False
requests.packages.urllib3.disable_warnings()
data = json.loads(input('JSON data: '))
r,cookies = create_playlist(data['server'], data['url'], data['title'])
if r['ok']:
    print(f"\nPlaylist link: {r['msg']}")
    print(f'\nFFMPEG command: ffmpeg -i "{r["msg"]}" -c copy "{data["title"]}.mp4"')
else:
    print(f"Error: {r['msg']}")