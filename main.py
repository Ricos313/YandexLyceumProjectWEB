import time

from flask import Flask, url_for, request, render_template, abort


app = Flask(__name__)
db = []

@app.route("/")
def form_sample1():
    return render_template("mainMenu.html")


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or "text" not in data:
        return abort(400)
    if len(data) != 2:
        return abort(400)

    name = data['name']
    text = data['text']
    if not isinstance(text, str) \
            or not isinstance(name, str) \
            or name == ''\
            or text == '':
        return abort(400)
    message = {
        "time": time.time(),
        "name": name,
        "text": text,
    }
    db.append(message)
    print(message['text'])
    return {"ok": True}


@app.route("/messages")
def get_message():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)
    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break
    return {'messages': result}


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")