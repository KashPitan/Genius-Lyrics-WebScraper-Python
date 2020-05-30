import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords


#### WEB SCRAPING ###

#test url to scrape information from
url = "https://genius.com/Microwave-diawb-lyrics"

#get url
result = requests.get(url,headers={"User-Agent": "Requests"})

#various information from the result object
resultStatusCode = result.status_code
resultHeaders = result.headers
src = result.content
# print(src)

#Convert content to a beautiful soup object
soup = BeautifulSoup(src,'lxml')

#retrieve lyrics from the p tag within the lyrics div and remove html tags)
# lyricsDiv = soup.find("div", {"class": "container"})
# print(lyricsDiv)
# lyricsText = lyricsDiv.find("p").text
# print(lyricsText)

lyrics = soup.find_all('p')[0].text
print(lyrics)

# ### NLP PROCESSING ###
# lyrics_words = word_tokenize(lyricsText)
#
# stop_words = set(stopwords.words("english"))
# filtered_sentence = []
# for w in lyrics_words:
#     if w not in stop_words:
#         filtered_sentence.append(w)
# # print(lyricsText)
# print(filtered_sentence)
# print(word_tokenize(lyricsText))

