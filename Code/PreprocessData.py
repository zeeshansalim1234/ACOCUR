import nltk
import re
from stop_words import get_stop_words
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import contractions

ADD_STOP_WORDS_CACHE = {}

def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            #if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            #else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


def CleanReviews(review):
    review = review.lower()
    review = expandText(review)
    review = review.replace("&quot;", '"')
    review = review.replace("&#39;", "'")
    review = review.replace("&gt;", '>')
    review = review.replace("&lt;", '<')
    review = re.sub(r'<quote>', ' ', review)
    review = re.sub(r'\r', ' ', review)
    review = re.sub(r'&amp', ' ', review)
    review = re.sub(r'&gt', ' ', review)
    review = clean_common(review)

    if review:
        review = lemmatize_sentence(review)

    review = remove_StopWords(review)
    review = remove_Review_StopWords(review)

    chars = [',', '"', '*', ')', '(', '%', '|', '~', '=', ';', ':', '?', '!', '$', '%', '&', '+', '-',
             '/', '^', ' - ', '@', '_', '\\n', '\\r', '&;', '&#', '\'', '\\', '#', '>', '<']
    for char in chars:
        review = review.replace(char, ' ')

    match = re.search("(\d+)\.(\d+)", review)
    while match is not None:
        review = re.sub("(\d+)\.(\d+)", r"\1\2", review)
        match = re.search("(\d+)\.(\d+)", review)

    review = review.replace('.', ' ');

    review = re.sub(r'\b[a-z]{,2}\b', '', review)
    review = re.sub(r'\s+', ' ', review)  # Remove all extra whitespace
    return review.strip()


def clean_commitmsg(txt):
    txt = txt.lower()
    txt = expandText(txt)
    txt = re.sub(r'\b(\S*/\S*)\b', '', txt)  # remove words with /

    # txt = re.sub(r'(?:[a-z]+[0-9]+)*', '', txt)   # this should remove strings that are mix of number and char


    txt = re.sub(r'signed-off-by(.*?)>', '', txt)  # this will replace the part from signed-of-by till first occurrance of > --- eg. signed-off-by: Harsh Shandilya <msfjarvis@gmail.com>

    txt = clean_common(txt)

    if txt:
        txt = lemmatize_sentence(txt)

    txt = remove_StopWords(txt)
    txt = remove_Commit_StopWords(txt)

    # txt = re.sub(r'\b[a-z]{,2}\b', '', txt)

    # match = re.search("(\d+)\.(\d+)", txt)
    # while match is not None:
    #     txt = re.sub("(\d+)\.(\d+)", '', txt)
    #     match = re.search("(\d+)\.(\d+)", txt)

    txt = re.sub("(\d+)\.(\d+)", '', txt)

    chars = [',','"','*',')','(', '|','~','=',';',':','?','$','%','&','+','/','#','@','>','<','[',']','\'','\\', '-', '!', '.']
    for char in chars:
        txt = txt.replace(char, ' ');


    # txt = re.sub(r'\d+', ' ', txt)
    txt = re.sub(r'\b[a-z]{,2}\b', '', txt)     # remove strings which are 1 or 2 char long
    txt = re.sub(r'\s+', ' ', txt)

    return txt.strip()


def clean_common(txt):
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\t', ' ')
    txt = txt.replace('"', ' ')
    txt = txt.replace('“', ' ')
    txt = txt.replace('”', ' ')
    txt = txt.replace("’", "'")
    txt = txt.replace("--", ' ')
    txt = re.sub(r'(?:\@|https?\://)\S+', ' ', txt)
    txt = re.sub(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', ' ', txt)
    txt = re.sub(r'[^\x00-\x7f]', ' ', txt)
    txt = re.sub(r'(\d+)[\./-](\d+)[\./-](\d+)', '', txt)       #  remove dates
    return txt


def remove_StopWords(txt):
    stop_words = get_stop_words('english')
    for word in stop_words:
        txt = re.sub(r'\b' + word + '\\b', '', txt)
        # txt = txt.replace(' {} '.format(word), ' ')
    return txt.strip()


def remove_Commit_StopWords(txt):
    stop_words = ['change-id', 'merge', 'bug', 'commit', 'signed-off-by', 'pull', 'request', 'branch']
    for word in stop_words:
        txt = re.sub(r'\b' + word + '\\b', '', txt)
        # txt = txt.replace(' {} '.format(word), ' ')
    return txt.strip()


def expandText(txt):
    contractions.add("wont", "will not")
    contractions.add("dont", "do not")
    contractions.add("doesnt", "does not")
    contractions.add("dn't", "did not")
    contractions.add("wont", "will not")
    contractions.add("cant", "can not")
    contractions.add("its", "it is")
    contractions.add("idk", "i do not know")
    expand_txt = contractions.fix(txt)
    return expand_txt


def get_additional_stopwords(language='english', cache=True):

    if cache and language in ADD_STOP_WORDS_CACHE:
        return ADD_STOP_WORDS_CACHE[language]

    try:
        with open('stop_words.txt', 'rb') as language_file:
            stop_words = [line.decode('utf-8').strip()
                          for line in language_file.readlines()]
    except:
        print("Error reading additional stop words")

    if cache:
        ADD_STOP_WORDS_CACHE[language] = stop_words

    return stop_words


def remove_Review_StopWords(txt):
    stop_words = get_additional_stopwords()
    for word in stop_words:
        txt = re.sub(r'\b' + word + '\\b', '', txt)
    return txt.strip()