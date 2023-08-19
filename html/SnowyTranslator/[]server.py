from flask import Flask, render_template, request, jsonify, url_for
from flask_cors import CORS  # Import the CORS module
import aiohttp
from bs4 import BeautifulSoup
from langdetect import detect
from pyfranc import franc
import asyncio
import ssl
import os
import re

# app = Flask(__name__, template_folder='.')
app = Flask(__name__, template_folder=os.path.expanduser('~/snowy-server/html/'), static_url_path='/static', static_folder=os.path.expanduser('~/snowy-server/html/static'))
CORS(app)

@app.route('/')
def index():
    return render_template('SnowySpeechTranslator.html')

@app.route('/formatJpExp', methods=['POST'])
def process():
    text = request.json.get('text')
    print("process text:", text)
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(ichimoe_japanese_split(text))
    loop.close()
    return jsonify(result=result)

@app.route('/furigana', methods=['POST'])
def process_furigana():
    text = request.json.get('text')
    print("process_furigana text:", text)
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(ichimoe_japanese_furigana(text))
    loop.close()
    return jsonify(result=result)

@app.route('/detect-language', methods=['POST'])
def process_detect_language():
    text = request.json.get('text')
    print("process_detect_language text:", text)
    loop = asyncio.new_event_loop()
    language = loop.run_until_complete(detect_language(text))
    loop.close()
    return jsonify(language=language)

async def ichimoe_japanese_split(text):
    inner_html = ""
    try:
        url = f"https://ichi.moe/cl/qr/?q={text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.read(), 'html.parser')
        row_gloss_rows = soup.find_all('div', class_='row gloss-row')
        for row_gloss_row in row_gloss_rows:
            glosses = row_gloss_row.find_all('div', class_='gloss')
            romaji_str = ""
            inner_html += " 【"
            for i in range(len(glosses)):
                gloss = glosses[i]
                hiragana = gloss.find('dt')
                if i > 0:
                    inner_html += " - "
                    romaji_str += " "

                word = hiragana.get_text()
                word = word.replace("1. ", "")
                word = word.replace("【", "<rt>")
                word = word.replace("】", "</rt>")
                word = "<ruby> " + word + "</ruby>"
                romaji = gloss.find('em').get_text()
                romaji_str += romaji
                inner_html += f"{word}"
            inner_html += f" | {romaji_str}】<br> "
        # return jsonify({'text': inner_html})
        return inner_html
    except Exception as e:
        return f"japanese_split: an error occurred: {str(e)}"

def is_not_japanese_character(char):
    code_point = ord(char)
    japanese_ranges = [
        (0x3040, 0x309F),  # Hiragana
        (0x30A0, 0x30FF),  # Katakana
        (0x4E00, 0x9FFF),  # Kanji
        (0x3400, 0x4DBF),  # Extended Kanji (Rare)
        (0xFF00, 0xFFEF),  # Japanese Full Width Characters & Half-width Katakana
    ]
    for start, end in japanese_ranges:
        if start <= code_point <= end:
            return False
    return True

eng_to_jpn_map = {}
def eng_to_jpn_init():
    for c in range(ord('０'), ord('９') + 1):
        jpn_char = chr(c)
        eng_char = chr(c + ord('0') - ord('０'))
        eng_to_jpn_map[eng_char] = jpn_char
    eng_to_jpn_map['!'] = '！'
    eng_to_jpn_map['?'] = '？'
    eng_to_jpn_map[':'] = '；'
    eng_to_jpn_map[','] = '，'
    eng_to_jpn_map['.'] = '｡'
eng_to_jpn_init()

def eng_to_jpn(c):
    if eng_to_jpn_map.get(c):
        return eng_to_jpn_map[c]
    return c

def str_en_to_jpn(text):
    rtn = ""
    for c in text:
        rtn += eng_to_jpn(c)
    return rtn

def only_japanese(text):
    ans_text = ""
    pos = 0
    is_japanese = True
    while pos < len(text):
        c = text[pos]
        # c = eng_to_jpn(c)
        if is_not_japanese_character(c):
            if is_japanese:
                ans_text += " "
            is_japanese = False
        else:
            ans_text += c
            is_japanese = True
        pos = pos + 1
    return ans_text

async def ichimoe_japanese_furigana(text):
    textPos = 0
    inner_html = ""
    text = str_en_to_jpn(text)
    try:
        url = f"https://ichi.moe/cl/qr/?q={text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.read(), 'html.parser')
        row_gloss_rows = soup.find_all('div', class_='row gloss-row')

        for row_gloss_row in row_gloss_rows:
            glosses = row_gloss_row.find_all('div', class_='gloss')
            for i in range(len(glosses)):
                gloss = glosses[i]
                hiragana = gloss.find('dt')
                if i > 0:
                    inner_html += " "
                word = hiragana.get_text()
                word = word.replace("1. ", "")
                word = word.replace("【", "<rt>")
                word = word.replace("】", "</rt>")

                # print("temp word:", word)
                wordPos = 0
                while textPos < len(text) and wordPos < len(word) and text[textPos] == word[wordPos]:
                    textPos += 1
                    wordPos += 1
                # 1: only word[wordPos] is Japanese ❌
                # 2: only text[textPos] is Japanese [word is over, go to next]
                # 3: both are not Japanese [word is over, text is punctuation]
                extra_string = ""
                while textPos < len(text) and is_not_japanese_character(text[textPos]):
                    extra_string += text[textPos]
                    textPos += 1
                word = "<ruby> " + word + "</ruby>" + extra_string
                # print("finished word:", word)
                inner_html += word
        print(inner_html)
        return inner_html
    except Exception as e:
        return f"japanese_split: an error occurred: {str(e)}"


async def detect_language(text):
    print("detect_language() text:", text)

    # from langdetect import detect
    # lang = detect(text)

    # from pyfranc import franc
    lang = franc.lang_detect(text, minlength=1, whitelist=['jpn', 'eng', 'cmn'])[0][0]
    if lang == "cmn":
        lang = "zh-TW"
    elif lang == "eng":
        lang = "en"
    elif lang == "jpn":
        lang = "jp"
    return lang

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    running_on_server = True
    if running_on_server:
        current_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_path)
        context.load_cert_chain(current_dir + '/fullchain.pem', current_dir + '/privkey.pem')
        app.run(debug=True, threaded=True, port=3001, host='0.0.0.0', use_reloader=False, ssl_context=context)
    else:
      app.run(debug=True, threaded=True, port=3001, host='localhost', use_reloader=False)