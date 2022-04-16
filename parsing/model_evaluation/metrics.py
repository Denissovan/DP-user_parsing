from collections import Counter
from scipy.spatial import distance


# jaccard metric
def jaccard_similarity(list1, list2):
    intersection = len(set(list1).intersection(list2)) #no need to call list here
    union = len(list1 + list2) - intersection #you only need to call len once here
    return round((intersection / union)*100, 5) #also no need to cast to float as this will be done for you


def get_cosine_sim(user_dict, merged_book):
  results = {}
  for key in user_dict.keys():
    a = Counter(list(set(user_dict[key])))
    b = Counter(list(set(merged_book)))

    phrases  = list(a.keys() | b.keys())

    a_vect = [a.get(phrase, 0) for phrase in phrases]
    b_vect = [b.get(phrase, 0) for phrase in phrases] 

    len_a  = sum(av for av in a_vect) ** 0.5
    len_b  = sum(bv for bv in b_vect) ** 0.5

    dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))

    # if (len_a * len_b) == 0:
    #     cosine = 0
    # else:
    cosine = dot / (len_a * len_b) 
    
    results[key] = (round(cosine * 100, 5))
  return results


def get_euclid_dis(user_dict, merged_book):

  results = {}
  for key in user_dict.keys():
    a = Counter(list(set(user_dict[key])))
    b = Counter(list(set(merged_book)))

    phrases  = list(a.keys() | b.keys())

    a_vect = [a.get(phrase, 0) for phrase in phrases]
    b_vect = [b.get(phrase, 0) for phrase in phrases] 
 
    results[key] = (distance.euclidean(a_vect, b_vect))
  return results