import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import TweetTokenizer
import re
import os

#genius api calls
import requests

#testing syllable count impl #1
import hyphenate

#testing syllable count impl #2
from nltk.corpus import cmudict

def get_single_song_lyrics(song_url):

    req = Request(url,headers = {"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage,"lxml")
    html = soup.prettify()

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

    hyphenated_lyrics = []
    for word in frequency_tokenized_lyrics:
        hyphenated_lyrics.append(hyphenate.hyphenate_word(word))
    # print(hyphenated_lyrics)

    syllable_count_per_word = []
    for hyphenated_word in hyphenated_lyrics:
        syllable_count_per_word.append(len(hyphenated_word))
        # print(str(len(hyphenated_word)) + " " + str(hyphenated_word))

    # print(syllable_count_per_word)

    average_syllable_count = sum(syllable_count_per_word)/len(syllable_count_per_word)
    average_syllable_count = "{0:0.2f}".format(average_syllable_count)
    return average_syllable_count

#second function with an alternative method for calculating the average syllable count
def get_average_syllable_count_2(frequency_tokenized_lyrics):
    d = cmudict.dict()
    syllable_per_word = []
    sylllabe = None
    for word in frequency_tokenized_lyrics:
        try:
            syllables = [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
            syllable_per_word.append(syllables[0])
            print(str(word) + " " + str(syllables[0]))
        except(KeyError):
            continue
    print(syllable_per_word)
    total_syllables = sum(syllable_per_word)
    average_syllables = total_syllables/len(syllable_per_word)
    average_syllables = "{0:0.2f}".format(average_syllables)
    print(average_syllables)
    return average_syllables

#
def get_song_info_genius():
    search_url = "http://api.genius.com/search/"
    access_token = "Ecr32ujznnSmv4yLPRQ_bjz7q3XLq3K-8TKOY8a2n-CXbZOVu5PzfxytGSscrSZk"
    # headers = {'Authorization': 'Bearer Ecr32ujznnSmv4yLPRQ_bjz7q3XLq3K-8TKOY8a2n-CXbZOVu5PzfxytGSscrSZk'}
    song_name = "diawb"
    token = 'Bearer {}'.format(access_token)
    data = {'q': song_name}
    headers = {'Authorization': token}
    response = requests.get(search_url, params=data, headers=headers)
    jsonResponse = response.json()
    print(jsonResponse)
    song_info = jsonResponse["response"]["hits"][0]["result"]
    print(song_info)

# def get_song_info_lastfm():


# test url to scrape from
# url = "https://genius.com/Microwave-diawb-lyrics"
# url = "https://genius.com/Kendrick-lamar-maad-city-lyrics"
url = "https://genius.com/Eminem-godzilla-lyrics"
# url = "https://genius.com/Aesop-rock-none-shall-pass-lyrics"
# url = "https://genius.com/Lupe-fiasco-mural-lyrics"

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

#test getting average syllable count
print("average syllables per word: " + get_average_syllable_count(frequency_tokenized_lyrics))
# print(get_average_syllable_count_2(frequency_tokenized_lyrics))

# get_song_info()
# print(lyrics)
# print(lyrics_words)
# print(filtered_sentence)
