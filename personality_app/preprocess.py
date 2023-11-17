import re
import string
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;.<>]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')

def remove_emoji(text):
    # Remove emojis from the text
    cleaned_text = emoji.demojize(text)
    return cleaned_text

def remove_punctuation(text):
    # Remove punctuations from the text
    cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
    return cleaned_text

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters, numbers, and extra whitespaces
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Remove mention
    text = re.sub("@[A-Za-z0-9]+", "", text)
    
    # Remove urls   
    text = re.sub(r'http\S+|www.\S+', '', text)
    
    text = remove_emoji(text)
    text = remove_punctuation(text)
    
    # Remove bad symbols
    text = BAD_SYMBOLS_RE.sub('', text)
    text = REPLACE_BY_SPACE_RE.sub('', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Join tokens back into a sentence
    cleaned_text = ' '.join(tokens)
    
    return cleaned_text


if __name__ == "__main__":
    text = "my text to clean"
    text = clean_text(text)
    print(text)
