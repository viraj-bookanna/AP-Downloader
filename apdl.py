import aiohttp,aiofiles,re,urllib.parse,asyncio,sys
from tqdm import tqdm

class APLoader:
    def __init__(self, playlist_url):
        self.playlist_url = playlist_url
        self.urls = []
        self.error = False
        self.headers = {
            'authority': 'video.ap.lk',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://ap.lk',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
    async def __dl_chunk(self, session, url, file):
        async with session.get(url, headers=self.headers) as response:
            if response.status!=200:
                self.error = True
                return
            self.headers['sd-analyze'] = response.headers.get('sd-analyze', '')
            async for chunk in response.content.iter_chunked(1024):
                await file.write(chunk)
    async def load_source(self, auth):
        self.headers['sd-analyze'] = auth
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.playlist_url, headers=self.headers) as response:
                if response.status!=200:
                    self.error = True
                    return
                self.headers['sd-analyze'] = response.headers.get('sd-analyze', '')
                self.urls = re.sub(r'^#.+$\s+', '', await response.text(), flags=re.M).strip().split('\n')
    async def download(self, out_file):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with aiofiles.open(out_file, 'wb') as file:
                for url in tqdm(self.urls):
                    if self.error:
                        break
                    await self.__dl_chunk(session, urllib.parse.urljoin(self.playlist_url, url), file)
        print('error' if self.error else 'success')

async def main(playlist_url, auth, out_file):
    ap = APLoader(playlist_url)
    await ap.load_source(auth)
    await ap.download(out_file)

asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3]))