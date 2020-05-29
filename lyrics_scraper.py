import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords

#### WEB SCRAPING ###

#url to scrape information from
url = "https://genius.com/Microwave-diawb-lyrics"

#
result = requests.get(url)

#various information from the result object
resultStatusCode = result.status_code
resultHeaders = result.headers
src = result.content

soup = BeautifulSoup(src,'lxml')

lyricsDiv = soup.find("div", {"class": "lyrics"})
lyricsText = lyricsDiv.find("p").text

### NLP PROCESSING ###
lyrics_words = word_tokenize(lyricsText)

stop_words = set(stopwords.words("english"))
filtered_sentence = []
for w in lyrics_words:
    if w not in stop_words:
        filtered_sentence.append(w)
# print(lyricsText)
print(filtered_sentence)
# print(word_tokenize(lyricsText))

