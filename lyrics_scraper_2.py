import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import TweetTokenizer
import re
import os
import hyphenate


def get_single_song_lyrics(song_url):

    req = Request(url,headers = {"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage,"lxml")
    html = soup.prettify()
    # print(html)

    #create two lyricsDiv variables(see try except below)
    lyricsDiv = soup.find("div", {"class": "lyrics"})
    lyricsDiv2 = soup.select('div[class*="Lyrics__Container"]')
    lyricsText = ""

    #handle the inconsistent returns from the genius site
    #sometimes the div with the lyrics has different identifiers
    try:
        lyricsText = lyricsDiv.find('p').text
    except(AttributeError):
        lyricsText = ""
        for element in lyricsDiv2:
            lyricsText += element.get_text("\n")

    return lyricsText
    print(lyricsText)

### NLP PROCESSING ###

#basic formatting for lyrics
def format_lyrics(lyrics):

    #remove [chorus], [verse] etc. identifiers
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines from string
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics

def tokenize_for_frequency_analysis(lyrics):
    # tokenize lyrics with tweet tokenizer(doesn't split words with contractions)
    tknzr = TweetTokenizer()
    tokenized_lyrics = tknzr.tokenize(lyrics)

    # #tokenize lyrics
    # tokenized_lyrics = word_tokenize(lyrics)

    # define stop words(filler words) to remove from lyrics
    stop_words = set(stopwords.words("english"))
    filtered_lyrics = []
    for word in tokenized_lyrics:
        if word not in stop_words:
            filtered_lyrics.append(word)

    # remove uneccessary characters that are tokenized
    filtered_lyrics = list(filter(("I").__ne__, filtered_lyrics))
    filtered_lyrics = list(filter(("A").__ne__, filtered_lyrics))

    #get rid of punctuation
    filtered_lyrics = [word.lower() for word in filtered_lyrics if word.isalpha()]
    return filtered_lyrics

def get_word_frequency(frequency_tokenized_lyrics,number_of_top_words):
    # calculate frequency of words
    freq = FreqDist(frequency_tokenized_lyrics)
    word_frequency = freq.most_common(number_of_top_words)
    return(word_frequency)

def get_unique_words(frequency_tokenized_lyrics):
    return len(set(frequency_tokenized_lyrics))

def get_average_word_length(frequency_tokenized_lyrics):
    temp = [len(ele) for ele in frequency_tokenized_lyrics]
    res = 0 if len(temp) == 0 else (float(sum(temp))/len(temp))
    res = "{0:0.1f}".format(res)
    return res

#use frequency tokenized lyrics for now
def get_average_syllable_count(frequency_tokenized_lyrics):


# test url to scrape from
# url = "https://genius.com/Microwave-diawb-lyrics"
url = "https://genius.com/Kendrick-lamar-maad-city-lyrics"

# for testing manually inputting a genius url
# url = input("input a genius url here")

#scrape lyrics from site to use
lyrics = get_single_song_lyrics(url)
# print(lyrics)

#test formatting lyrics
formatted_lyrics = format_lyrics(lyrics)
print(formatted_lyrics)

#test getting word frequency and unique words
frequency_tokenized_lyrics = tokenize_for_frequency_analysis(formatted_lyrics)
# print(frequency_tokenized_lyrics)
print(get_word_frequency(frequency_tokenized_lyrics,10))
print("number of unique words: " + str(get_unique_words(frequency_tokenized_lyrics)))

#test getting average word length
average_word_length = get_average_word_length(frequency_tokenized_lyrics)
print("average word length: " + average_word_length + " letters")

# print(lyrics)
# print(lyrics_words)
# print(filtered_sentence)
