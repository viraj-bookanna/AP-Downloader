import subprocess,os
from dotenv import load_dotenv
from pyngrok import ngrok,conf

load_dotenv(override=True)

def create_tunnel():
    conf.get_default().auth_token = os.environ['NGROK_TOKEN']
    ngrok_tunnel = ngrok.connect(5000, "tcp")
    return ngrok_tunnel.public_url.replace("tcp://", "http://")

SERVER_URL = create_tunnel()
js = '''avascript:(function(){
    fetch(window.location.href).then(r=>r.text()).then(r=>{
        VideoStreamer=null;
        navigator.clipboard.writeText(JSON.stringify({
            url: r.match(/(https?:\/\/.+?\/stream\/[0-9a-f-]+)/g)[0],
            title: document.title,
            server: '__SERVER_URL__'
        })).then(()=>{
            alert('Data copied to clipboard');
        }).catch(e=>{
            alert('Copy error: '+e.message);
        })
    }).catch(e=>{
        alert('Error: '+e.message);
    })
})();'''.replace('__SERVER_URL__', SERVER_URL)

print('1. Copy the code between the lines\n2. Then goto the video playing page in browser and type "j" in the url bar\n3. Paste the copied data and hit enter\nrequired data for client.py will be copied to clipboard auotmatically')
line = '-'*40
print(f'{line}\n{js}\n{line}')
subprocess.check_call(["python3", "server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
