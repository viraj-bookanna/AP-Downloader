import os,requests,sqlite3,hashlib,json,urllib.parse
from flask import Flask,request,Response,stream_with_context

app = Flask(__name__)

def db_get(key, default=None):
    try:
        CONN = sqlite3.connect('database.db')
        cursor = CONN.cursor()
        cursor.execute('SELECT value FROM key_values WHERE key=?', (key,))
        return json.loads(cursor.fetchone()[0])
        CONN.close()
    except:
        return default
def db_put(key, value):
    CONN = sqlite3.connect('database.db')
    cursor = CONN.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS key_values (
    key CHAR PRIMARY KEY,
    value TEXT
)
''')
    cursor.execute('INSERT OR REPLACE INTO key_values (key, value) VALUES (?, ?)', (key, json.dumps(value)))
    CONN.commit()
    CONN.close()

@app.route('/', methods=['POST'])
def getlink():
    try:
        vid_hash = hashlib.md5(request.json['title'].encode()).hexdigest()
        host = request.headers['host']
        title = urllib.parse.quote(request.json['title'])
        db_put(vid_hash, request.json)
        return json.dumps({'ok': True, 'msg': f"http://{host}/playlist/{vid_hash}/{title}.m3u8"})
    except Exception as e:
        return json.dumps({'ok': False, 'msg': repr(e)})
@app.route('/playlist/<vid_hash>/<filename>')
def playlist(vid_hash, filename):
    playlist = db_get(vid_hash)
    if playlist:
        return playlist["playlist"].replace("/stream-data", f"/{vid_hash}/stream-data")
    return Response(status=404)
@app.route('/<vid_hash>/stream-data/<path:path>')
def chunk(vid_hash, path):
    def stream_file(playlist):
        response = requests.get(f'{playlist["url_prefix"]}/stream-data/{path}', headers=playlist["headers"], cookies=playlist["cookies"], stream=True, proxies=proxies, verify=verify)
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk
    playlist = db_get(vid_hash)
    if playlist:
        return Response(stream_with_context(stream_file(playlist)))
    return Response(status=404)

proxies=None#{'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
verify=False
requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
    app.run()