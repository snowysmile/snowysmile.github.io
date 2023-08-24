import requests
import re
from bs4 import BeautifulSoup

# https://dictionary.cambridge.org/help/phonetics.html
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-ssml-phonetic-sets
def get_phonetic_symbols(text):
    pure_english_text = re.sub(r'[^a-zA-Z\s]', '', text)
    url = f"https://toipa.org/AmE/{pure_english_text}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://toipa.org/"
    }
    response = requests.get(url, headers=headers)
    # with open("scraped_page.html", "w", encoding="utf-8") as html_file:
    #    html_file.write(response.text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        word_elements = soup.find_all("a", class_="source")
        words = []
        ipas = []
        for word_element in word_elements:
            word = word_element.get_text().strip()
            ipa_element = word_element.find_next(["span", "div"], class_=["pronunciation", "text-base"])
            if ipa_element:
                ipa = ipa_element.get_text().strip()
                words.append(word)
                ipas.append(ipa[1:-1])

        for word, ipa in zip(words, ipas):
            print(f"{word}: {ipa}", end=";  ")
        print()

        inner_html = ""
        textPos = 0
        wordId = 0
        while textPos < len(text):
            if wordId < len(words) and text[textPos: textPos + len(words[wordId])] == words[wordId]:
                inner_html += f"<ruby>{words[wordId]} <rt>{ipas[wordId]}</rt> </ruby>"
                textPos += len(words[wordId])
                wordId += 1
            else:
                inner_html += text[textPos]
                textPos += 1
        print("inner_html:", inner_html)
        return inner_html
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

text_to_lookup = "this is a the example test! I want to record a record? please run fast."
get_phonetic_symbols(text_to_lookup)

