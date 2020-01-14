import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import contractions
import emoji
import string
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;.<>]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_data(text):
    text = BeautifulSoup(text, "lxml").text
    #text to lower
    text = text.lower()
    #text contractions
    text = contractions.fix(text)
    #remove mention
    text=re.sub("@[A-Za-z0-9]+","", text)
    #remove urls
    text = re.sub(r'http\S+|www.\S+', '', text)
    #remove_emoji
    text = remove_emoji(text)
    #remove panctuations
    text = remove_punctuations(text)
    #remove digits
    text = ''.join([i for i in text if not i.isdigit()])
    #remove stopword
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    #remove bad symbols
    text = BAD_SYMBOLS_RE.sub('', text)
    text = REPLACE_BY_SPACE_RE.sub('', text)

    return text

def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_punctuations(text):
    for punctuation in string.punctuation:

        text = text.replace(punctuation,'')
    return text

#Prediciton catagories YES and NO



import pickle
from .models import Model
traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']

def predict_cat(data):
        result = []
        for i in range(5):
            #with open('twitter_auth/backend/'+traits[i]+'_model.pkl', 'rb') as f:
		            # cl = pickle.load(f)
            f = open('twitter_auth/backend/'+traits[i]+'_model.pkl', 'rb')
            cl = pickle.load(f)
            pred=cl.predict(data,regression= False)

            score = float(str(np.mean(np.array(pred) )))
            result.append(score)
            final_result = boolean_to_class(result)
        return final_result

def predict_reg(data):

        result_r = []

        for i in range(5):
            f = open('twitter_auth/backend/'+traits[i]+'_model.pkl', 'rb')
            cl = pickle.load(f)
            pred=cl.predict(data ,regression= True)

            score = float(str(np.mean(np.array(pred) )))
            result_r.append(score)
            final_score = percentage(result_r)

        return final_score

def boolean_to_class(result):
        result = [round(i) for i in result ]
        results = []

        for i in result:
            if i == 1.0:
                results.append('YES')
            else:
                results.append('NO')

        return results

#predict percentage
def percentage(result):
        #x = np.array(1,result)
        score=[]
        #score.append(pd.DataFrame(x/float(np.sum(x))).applymap(lambda x: '{:.2%}'.format(x)).values)

        total= sum(result)

        for i in result:
            score.append('{0:.2f}%'.format((i /total  * 100)))
            #print(int(round(result_r[i]*total /100)))
            #print('{0:.2f}%'.format((i /total  * 100)))
        return score

def prepare_tweet(tweets):
    X=[]
    for item in tweets:
        X.append(clean_data(item.full_text))
    return X

def retrieve_data(tweets):
    X=[]
    for item in tweets:
        X.append(item.full_text)
    return X

def get_result(data):
        cat = predict_cat(data)
        reg = predict_reg(data)
        return reg,cat


###################################################################################

def test_prepare_tweet(filename):
    df = pd.read_csv(filename, encoding='UTF-8')
    X = df['full_text'].apply(clean_data)
    return X



def perdict_OPN(data):
    f = open('twitter_auth/backend/OPN_model.pkl', 'rb')
    cl = pickle.load(f)
    sOPN =cl.predict(data ,regression= True)
    s_OPN = float(str(np.mean(np.array(sOPN) )))
    cOPN =cl.predict(data ,regression= False)
    c_OPN = float(str(np.mean(np.array(cOPN) )))
    return s_OPN,c_OPN

def perdict_CON(data):
    f = open('twitter_auth/backend/CON_model.pkl', 'rb')
    cl = pickle.load(f)
    sCON =cl.predict(data ,regression= True)
    s_CON = float(str(np.mean(np.array(sCON) )))
    cCON =cl.predict(data ,regression= False)
    c_CON = float(str(np.mean(np.array(cCON) )))
    return s_CON,c_CON

def perdict_EXT(data):
    f = open('twitter_auth/backend/EXT_model.pkl', 'rb')
    cl = pickle.load(f)
    sEXT =cl.predict(data ,regression= True)
    s_EXT = float(str(np.mean(np.array(sEXT) )))
    cEXT =cl.predict(data ,regression= False)
    c_EXT = float(str(np.mean(np.array(cEXT))))
    return s_EXT,c_EXT

def perdict_AGR(data):
    f = open('twitter_auth/backend/AGR_model.pkl', 'rb')
    cl = pickle.load(f)
    sAGR =cl.predict(data ,regression= True)
    s_AGR = float(str(np.mean(np.array(sAGR) )))
    cAGR =cl.predict(data ,regression= False)
    c_AGR = float(str(np.mean(np.array(cAGR) )))
    return s_AGR,c_AGR

def perdict_NEU(data):
    f = open('twitter_auth/backend/OPN_model.pkl', 'rb')
    cl = pickle.load(f)
    sNEU =cl.predict(data ,regression= True)
    s_NEU = float(str(np.mean(np.array(sNEU) )))
    cNEU =cl.predict(data ,regression= False)
    c_NEU = float(str(np.mean(np.array(cNEU) )))
    return s_NEU,c_NEU

def changeClass(result):
        result = round(result)
        if i == 1.0:
                results='YES'
        else:
                results='NO'

        return results



#Prediction
