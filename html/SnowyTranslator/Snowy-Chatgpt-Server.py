from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import openai
import emoji
import ssl
import os
import re
emojis = emoji.UNICODE_EMOJI["en"].keys()

app = Flask(__name__)
CORS(app)

api_key = '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'
openai.api_key = api_key

def dprint(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)

def lprint(*args, **kwargs):
    if DEBUG_MODE or LOCAL_TEST:
        print(*args, **kwargs)

@app.route('/chatgpt-emoji', methods=['POST'])
def chatgpt_emoji():
    try:
        messages = [{
            "role": "system",
            "content": "Please translate the input to many many many emojis as many as you can. Do your best with only emojis only."
        }]
        input_text = request.json['text']
        lprint("input_text:", input_text)
        messages.append({"role": "user", "content": input_text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=50,
        )
        response_text = response.choices[0].message['content']
        lprint("response_text:", response_text)

        emoji_list = []
        demoji_text = emoji.demojize(response_text)
        matches = re.findall(r':[^:]*:', demoji_text)
        for word in matches:
            the_emoji = emoji.emojize(word)
            if the_emoji not in emoji_list:
                emoji_list.append(the_emoji)
        emoji_text = ' '.join(emoji_list)

        # return response_text + " \n " + emoji_text
        return emoji_text

    except Exception as e:
        print('error:', str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    LOCAL_TEST = True if 1 else False
    DEBUG_MODE = True if 0 else False
    IS_BANNED = True if 0 else False

    if LOCAL_TEST:
        print("haha")
        app.run(debug=DEBUG_MODE, threaded=True, port=3002, host='localhost', use_reloader=False)
    else:
        print("hehe")
        current_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_path)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(current_dir + '/fullchain.pem', current_dir + '/privkey.pem')
        app.run(debug=DEBUG_MODE, threaded=True, port=3002, host='0.0.0.0', use_reloader=False, ssl_context=context)
