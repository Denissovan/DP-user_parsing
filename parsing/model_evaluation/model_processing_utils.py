import nltk
import tqdm

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def join_tuples_and_lemantize(dictionary):
    for key in tqdm.tqdm(dictionary.keys()):
        dictionary[key] = [f"{WordNetLemmatizer().lemmatize(t1.lower())} {WordNetLemmatizer().lemmatize(t2.lower())}" for t1,t2 in dictionary[key] if t1.lower() not in stopwords.words('english') and t2.lower() not in stopwords.words('english')]


def merge_models(dictionary):
    loc_list = []
    for key in tqdm.tqdm(dictionary.keys()):
        loc_list += dictionary[key]
    return [phrase for phrase in (set(i for i in loc_list))]


def merge_into_existing_model(original_model, model_to_add):
    # loc_model = merge_models(model_to_add)
    loc_model = original_model + model_to_add
    return [phrase for phrase in (set(i for i in loc_model))]


def merge_sub_sec_into_sec(sec_df, book_dict):
    section_list = sorted(list(sec_df['sections'].unique()))
    top_range = section_list[-1]

    section_dict = {}

    for sec in range(1, top_range + 1):
        local_df = sec_df.loc[sec_df['sections'] == sec]
        local_phrase_list = []
        
        for row in local_df['sub_sections']:
            sub_sec_key = row
            local_phrase_list += book_dict[str(sub_sec_key)]
            
        deduplicated_phrase_list = merge_into_existing_model([], local_phrase_list)
        section_dict[sec] = deduplicated_phrase_list

    return section_dict


# if user_book == "users" -> phrase_dict is a dict
# if user_book == "book" -> phrase_dict is a list
def join_phrases_into_words(phrase_dict, users_book="book"):
    all_words = None
    local_words = None
    if users_book == "users":
        all_words = {}
        for key in tqdm.tqdm(phrase_dict.keys()):
            local_words = list(map(lambda x: x.split(), list(phrase_dict[key])))
            local_words = list(sum(local_words, []))
            all_words[key]= local_words
        return all_words
    elif users_book == "book":
        all_words = list(map(lambda x: x.split(), list(phrase_dict)))
        return list(sum(all_words, []))
    else:
        return None

