import requests
from bs4 import BeautifulSoup

url = "https://www.purpleculture.net/chinese-pinyin-converter/?session=f55c0c0c86315671cf71762d4c49a087"
response = requests.get(url)
with open("scraped_page.html", "w", encoding="utf-8") as html_file:
    html_file.write(response.text)
exit()

"""
soup = BeautifulSoup(response.content, "html.parser")
post_response = requests.post(url + form_action, data=form_data)
american_radio = soup.find("input", {"name": "output_dialect", "value": "am"})
if american_radio:
    american_radio.parent["class"] = "btn btn-outline-secondary btn-sm active"
    print("american_radio.parent:", american_radio.parent)

line_by_line_radio = soup.find("input", {"name": "output_style", "value": "inline"})
if line_by_line_radio:
    line_by_line_radio.parent["class"] = "btn btn-outline-secondary btn-sm active"
    print("line_by_line_radio.parent:", line_by_line_radio.parent)
"""

def get_IPA(text):
    url = "https://tophonetics.com/"
    form_data = {
        "text_to_transcribe": text,
        "submit": "Show transcription",
        "output_style": "inline",
        "output_dialect": "am",
    }
    post_response = requests.post(url, data=form_data)

    post_soup = BeautifulSoup(post_response.content, "html.parser")
    transcr_output_element = post_soup.find(id="transcr_output")
    transcribed_word_elements = transcr_output_element.find_all("span", class_="transcribed_word")
    for transcribed in transcribed_word_elements:
        parent_div = transcribed.find_parent("div", class_="inline_ipa")
        if parent_div:
            inline_orig = parent_div.find_previous_sibling("div", class_="inline_orig")
            if inline_orig:
                print(f"{transcribed.text.strip()}: {inline_orig.text.strip()}")

get_IPA("I have a cat, I have 10 books. I have a girl")


"""
import requests
from bs4 import BeautifulSoup

def get_phonetic_symbols(text):
    url = f"https://toipa.org/AmE/{text}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://toipa.org/"
    }
    response = requests.get(url, headers=headers)
    with open("scraped_page.html", "w", encoding="utf-8") as html_file:
        html_file.write(response.text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser", from_encoding="ISO-8859-1")

        word_elements = soup.find_all("a", class_="source")
        words = []
        pronunciations = []

        for word_element in word_elements:
            word = word_element.get_text().strip()
            pronunciation_element = word_element.find_next(["span", "div"], class_=["pronunciation", "text-base"])
            if pronunciation_element:
                pronunciation = pronunciation_element.get_text().strip()
                words.append(word)
                pronunciations.append(pronunciation)

        # words = [word.get_text() for word in word_elements]
        # pronunciations = [pronunciation.get_text() for pronunciation in pronunciation_elements]
        print("words:", words)
        print("pronunciations:", pronunciations)

        return words, pronunciations
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

    return [], []


text_to_lookup = "this is a the example test! I have 10 # books. 1! 2@ 3# 4$ 5% 6^ 7& 8* 9( 0) END"
words, pronunciations = get_phonetic_symbols(text_to_lookup)
print(pronunciations)

if words and pronunciations:
    for word, pronunciation in zip(words, pronunciations):
        print(f"{word}: {pronunciation}")
else:
    print("Words not found or pronunciations not available.")

"""