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
