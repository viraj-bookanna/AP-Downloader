import os,sys,time,platform,dotenv,json

def create_bat()
    headers_crlf = ' -headers "{}"'.format('!CR!!LF!'.join([f'{h}: {headers[h]}' for h in headers]))
    converter_bat = f'''@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem Get CR and LF characters
for /f %%a in ('copy /Z "%~dpf0" nul') do set "CR=%%a"

(set LF=^
%=EMPTY=%
)

ffmpeg{proxy}{headers_crlf} -i "{inFileName}" -c copy "{outFilePath}" 1>NUL 2>"{logFilePath}"
'''
    with open(f"{outFilePath}.bat", 'w') as f:
        f.write(converter_bat)
	return f"{outFilePath}.bat"
def linux_cmd():
    headers_crlf = ' -headers "{}"'.format(r'\r\n'.join([f'{h}: {headers[h]}' for h in headers]))
    return f'ffmpeg{proxy}{headers_crlf} -i "{inFileName}" -c copy "{outFilePath}" 1> "{logFilePath}" 2>&1'

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file, override=True)
proxy = ''
if os.getenv("USE_PROXY", 'False')=='True':
    proxy = f' -http_proxy {os.environ["PROXY_URL"]}'
jdata = json.loads(bytes.fromhex(sys.argv[1]).decode())
inFileName = jdata['i']
headers = jdata['h']
outFilePath = jdata['o']
logFilePath = f"{outFilePath}.log"
cmd = linux_cmd() if platform.system()!='Windows' else create_bat()
with open(logFilePath, 'w') as f:
    pass
os.system(cmd)
cmd2 = f'ffmpeg -i {outFilePath} -ss 00:00:01 -vframes 1 {outFilePath}.jpg'
os.system(cmd2)
time.sleep(3)
os.remove(logFilePath)
