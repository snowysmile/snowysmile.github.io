import emoji
import re

def split_count(text):
    emoji_list = []
    text = emoji.demojize(text)
    matches = re.findall(r':[^:]*:', text)
    for word in matches:
        the_emoji = emoji.emojize(word)
        if the_emoji not in emoji_list:
            emoji_list.append(the_emoji)
    return emoji_list

text = "🚂❄️🌨️🕒🚂❄️🌨️🕒"
emojis = split_count(text)
print(emojis)