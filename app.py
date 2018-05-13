import sys
from subprocess import Popen, PIPE
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, minimal-ui" />
        </head>
        <body style="display:flex;">
        <style>
        h1 {
        font-size:50px;
        }
        input {
        text-align:center;
        }
        </style>
        <div style="display:flex; flex-direction:column; margin:0;justify-content:center;align-items:center; width:100%;">
        <h1>Badge id</h1>
        <form action="/post" method="post" style="display:flex; flex-direction:column;">
        <input type="text" style="height:100px;font-size:25px;" autocorrect="off" placeholder="badge id" id="badgeid" name="badgeid" required>
        <input type="submit">
        </form>
        </div>
        </body>
        </html>
        '''


@app.route('/post', methods=["POST"])
def post():
    badgeid = request.form['badgeid']
    post = "curl 'https://www.cteleadnet.com/pycon11/nup/get_lead.reg' -XPOST -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Origin: https://www.cteleadnet.com' -H 'Host: www.cteleadnet.com' -H 'Accept: */*' -H 'Connection: keep-alive' -H 'Accept-Language: en-us' -H 'Accept-Encoding: br, gzip, deflate' -H 'Cookie: cteleadnet-sessionreq-x=0d77343c3532b45e8d23c2b52404413b; cteleadnet-sessionreq=f3865c559b8567698d4d97156b2eb104' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15' -H 'Referer: https://www.cteleadnet.com/pycon11/leadnet.reg' -H 'Content-Length: 73' -H 'X-Requested-With: XMLHttpRequest' --data 'form_id=f3865c559b8567698d4d97156b2eb104&user_id=Gn3qzq7x&p_badge_id=%s'" % badgeid

    line = ''
    proc = Popen(post, stdout=PIPE, bufsize=1, shell=True)
    for line in iter(proc.stdout.readline, b''):
        line += line

    line = line.decode('utf-8')
    print(line)
    if 'good' in line.lower():
        return '''
            <html>
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, minimal-ui" />
            </head>
            <body style="display:flex;">
            <style>
            h1 {
            font-size:50px;
            }
            input {
            text-align:center;
            }
            </style>
            <div style="display:flex; flex-direction:column; margin:0;justify-content:center;align-items:center; width:100%;">
            <h2> added ''' + '-'.join([line.rsplit('|', 1)[-1] + ' ', ' ' + line.split('|', 1)[0]]) + ''' </h2>
            <h1>Badge id</h1>
            <form action="/post" method="post" style="display:flex; flex-direction:column;">
            <input type="text" style="height:100px;font-size:25px;" autocorrect="off" placeholder="badge id" id="badgeid" name="badgeid" required>
            <input type="submit">
            </form>
            </div>
            </body>
            </html>'''
    return "not found"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
