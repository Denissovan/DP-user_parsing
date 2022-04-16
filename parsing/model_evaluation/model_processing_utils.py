import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def join_tuples_and_lemantize(dictionary):
    for key in dictionary.keys():
        dictionary[key] = [f"{WordNetLemmatizer().lemmatize(t1.lower())} {WordNetLemmatizer().lemmatize(t2.lower())}" for t1,t2 in dictionary[key] if t1.lower() not in stopwords.words('english') and t2.lower() not in stopwords.words('english')]


def merge_models(dictionary):
    loc_list = []
    for key in dictionary.keys():
        loc_list += dictionary[key]
    return [phrase for phrase in (set(i for i in loc_list))]


def merge_into_existing_model(original_model, model_to_add):
    # loc_model = merge_models(model_to_add)
    loc_model = original_model + model_to_add
    return [phrase for phrase in (set(i for i in loc_model))]
