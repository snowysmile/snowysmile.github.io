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

def dprint(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)

def lprint(*args, **kwargs):
    if DEBUG_MODE or LOCAL_TEST:
        print(*args, **kwargs)

@app.route('/chatgpt-emoji', methods=['POST'])
def chatgpt_emoji():
    try:
        input_text = request.json['text']
        openai.api_key = request.json['apikey']
        lprint("input_text:", input_text)

        messages = [{
            "role": "system",
            "content": "Please translate my input to many many many emojis as many as you can. Do your best with only emojis only."
        }, {"role": "user", "content": input_text}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=60,
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

@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    try:
        input_text = request.json['text']
        openai.api_key = request.json['apikey']
        query_type = request.json['query']
        max_token = 280

        lprint("input_text:", input_text)
        lprint("query_type:", query_type)

        messages = []
        if query_type == "cute-japanese":
            messages.append({
                "role": "system",
                "content": "Please translate/convert my input sentence to happy, friendly, and positive Japanese. Make my Japanese grammar correct and don't return extra things."
            })
        elif query_type == "related-emojis":
            messages.append({
                "role": "system",
                "content": "Please convert input to related emojis, answer me with as many different emojis as you can."
            })
            max_token = 160
        elif query_type == "sentence-emojis":
            messages.append({
                "role": "system",
                "content": "Please add many 顔文字 to my input sentence to make it cute and interesting. Don't do other things."
            })
            max_token = 160
        elif query_type == "translate-ja":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to decent, natural, and standard Japanese."
            })
        elif query_type == "translate-en":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to decent, natural, and standard English."
            })
        elif query_type == "translate-cn":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to decent, natural, and standard Traditional Chinese."
            })
        elif query_type == "cute-ja":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to cute and natural Japanese."
            })
        elif query_type == "lovely-ja":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to lovely and friendly Japanese with 顔文字. (Don't make the texts much longer than before)"
            })
        else:
            print("wrong query type")
            return "wrong query type"

        messages.append({"role": "user", "content": input_text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=160,
        )
        response_text = response.choices[0].message['content']
        lprint("response_text:", response_text)
        lprint("response:", response.usage)

        if query_type == "related-emojis":
            emoji_list = []
            demoji_text = emoji.demojize(response_text)
            matches = re.findall(r':[^:]*:', demoji_text)
            for word in matches:
                the_emoji = emoji.emojize(word)
                if the_emoji not in emoji_list:
                    emoji_list.append(the_emoji)
            emoji_text = ' '.join(emoji_list)
            return emoji_text
        else:
            return response_text

    except Exception as e:
        print('error:', str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    LOCAL_TEST = True if 0 else False
    DEBUG_MODE = True if 0 else False

    if LOCAL_TEST:
        print("LOCAL_TEST")
        app.run(debug=DEBUG_MODE, threaded=True, port=3002, host='localhost', use_reloader=False)
    else:
        print("SERVER_RUN")
        current_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_path)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(current_dir + '/fullchain.pem', current_dir + '/privkey.pem')
        app.run(debug=DEBUG_MODE, threaded=True, port=3002, host='0.0.0.0', use_reloader=False, ssl_context=context)
