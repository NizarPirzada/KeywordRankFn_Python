import simplejson as json
import azure.functions as func
import nltk

# these 4 lines need only in first run
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download("wordnet")


from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation

stopword = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()

# lower of the text
def to_lower(text):
    return [w.lower() for w in word_tokenize(text)]

# remove punctuations
def strip_punctuation(text):
    return ''.join(c for c in text if c not in punctuation)
# text preprocessing 
def pre_processing(text):
    # remove punctations
    lower_text = strip_punctuation(text)
    word_tokens = to_lower(lower_text)
    word_tokens = [word for word in word_tokens if word not in stopword]
    word_tokens = [word for word in word_tokens if word.isalnum()]
    word_tokens = [wordnet_lemmatizer.lemmatize(word) for word in word_tokens]
    return word_tokens

def Extract_Keywords(comments, limits=20):
    words = []
    # the comments of the submission
    for comment in comments:
        comment_words = pre_processing(comment)
        comment_words = list(set(comment_words))
        words += comment_words

    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    max_len = min(limits, len(word_counts))
    word_list = sorted(word_counts, key=word_counts.get, reverse=True)[0:max_len]   
    new_word_counts = []
    for  word in word_list:
        key_dict = {}
        key_dict["Keyword"] = word
        key_dict["Frequency"] = word_counts[word]
        new_word_counts.append(key_dict)
    return new_word_counts

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        comments = req_body.get('comments')
        limits = req_body.get('limits')
    try:
        limits = int(limits)
    except:
        limits = 20
    if comments:
        results = Extract_Keywords(comments, limits)
        data = {"Keywords": results}
        return func.HttpResponse(json.dumps(data, indent=4, sort_keys=True, default=str),status_code=200)        
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
