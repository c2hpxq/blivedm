import datetime
import time
import socket
import threading
import os

import openai
import json

openai.api_key = "www.keniutech.cn" 
openai.api_base = "http://www.windblow.world/v1"

from flask import Flask, render_template


app = Flask(__name__)
qa_lock = threading.Lock()
qa_list = []

init = False
socket_path = ''
sock = ''


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/timestamp')
def timestamp():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time

@app.route('/qa')
def qa():
    line_break = '<br /> <br/> >>>>>>>>>>>>>>>>> <br /> <br />'
    print("impl qa")
    global init
    global socket_path
    global sock
    if not init:
        socket_path = '/Users/pjq/projects/BILIBILIxLLM/blivedm/my_socket.sock'
        os.remove(socket_path)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

        print("binding...")
        # Bind the socket to the socket path
        sock.bind(socket_path)
        print("done")

        sock.settimeout(1.0)

        init = True

    global qa_list
    try:
        data, addr = sock.recvfrom(1024)
    except TimeoutError:
        res = line_break.join(qa_list)
        print("res is: ", res)
        return res

    data = data.decode()
    uname = data.split("：")[0]
    question = "".join(data.split("：")[1:])
    # print(data)

    output = openai.Completion.create(
        model="Keniu-Chat",
        prompt=question,
        max_tokens=1024,
        temperature = 0.0
    )

    print(json.dumps(output, indent=2).encode('utf-8').decode('unicode_escape'))
    if len(qa_list) > 3:
        qa_list = qa_list[1:]
    
    
    #output = openai.Completion.create(
    #        model="Keniu-Chat", 
    #        prompt=data,
    #        max_tokens=1024,
    #        temperature = 0.0
    #    )

    #print(json.dumps(output, indent=2).encode('utf-8').decode('unicode_escape'))

    #echo = output["choices"][0]["text"].encode('utf-8')
    #print(echo)

    resp = output["choices"][0]["text"]
    print(resp)
    qa_list.append("给" + uname + "的问题" + question + "的答复：" + resp)

    res = line_break.join(qa_list)

    print(len(qa_list))
    print("resss is", res)
    return res
    
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2687, debug=True)
    print("here")
    # Create a Unix domain socket
    while True:
        time.sleep(1.0)
        app.jinja_env.cache = {}