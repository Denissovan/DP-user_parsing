from collections import Counter
from itertools import count
from statistics import mean
from scipy.spatial import distance
import numpy as np
import statistics


# jaccard metric
def jaccard_similarity(list1, list2):
    intersection = len(set(list1).intersection(list2)) #no need to call list here
    union = len(list1 + list2) - intersection #you only need to call len once here
    return round((intersection / union)*100, 5) #also no need to cast to float as this will be done for you


def cosine_sim(list1, list2):
    a = Counter(list(set(list1)))
    b = Counter(list(set(list2)))

    phrases  = list(a.keys() | b.keys())

    a_vect = [a.get(phrase, 0) for phrase in phrases]
    b_vect = [b.get(phrase, 0) for phrase in phrases] 

    len_a  = sum(av for av in a_vect) ** 0.5
    len_b  = sum(bv for bv in b_vect) ** 0.5

    dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))

    # if (len_a * len_b) == 0:
    #     cosine = 0
    # else:
    return dot / (len_a * len_b)  


def get_cosine_sim(user_dict, merged_book):
  results = {}
  for key in user_dict.keys():
    # a = Counter(list(set(user_dict[key])))
    # b = Counter(list(set(merged_book)))

    # phrases  = list(a.keys() | b.keys())

    # a_vect = [a.get(phrase, 0) for phrase in phrases]
    # b_vect = [b.get(phrase, 0) for phrase in phrases] 

    # len_a  = sum(av for av in a_vect) ** 0.5
    # len_b  = sum(bv for bv in b_vect) ** 0.5

    # dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))

    # if (len_a * len_b) == 0:
    #     cosine = 0
    # else:
    # cosine = dot / (len_a * len_b) 
    cosine = cosine_sim(user_dict[key], merged_book)


    results[key] = (round(cosine * 100, 5))
  return results


def euclid_dis(list1, list2):
  a = Counter(list(set(list1)))
  b = Counter(list(set(list2)))

  phrases  = list(a.keys() | b.keys())

  a_vect = [a.get(phrase, 0) for phrase in phrases]
  b_vect = [b.get(phrase, 0) for phrase in phrases]

  return distance.euclidean(a_vect, b_vect)
 

def get_euclid_dis(user_dict, merged_book):

  results = {}
  for key in user_dict.keys():
    # a = Counter(list(set(user_dict[key])))
    # b = Counter(list(set(merged_book)))

    # phrases  = list(a.keys() | b.keys())

    # a_vect = [a.get(phrase, 0) for phrase in phrases]
    # b_vect = [b.get(phrase, 0) for phrase in phrases] 
 
    # results[key] = (distance.euclidean(a_vect, b_vect))
    results[key] = euclid_dis(user_dict[key], merged_book)

  return results


def get_sorted_dicts(metric_dict1, ref_dict2):
    return (dict(sorted(metric_dict1.items(), key=lambda item: item[1])), dict(sorted(ref_dict2.items(), key=lambda item: item[1])))


def calculate_order_score(metric_dict1, ref_dict2):

    sorted_metric_dict, sorted_ref_dict = get_sorted_dicts(metric_dict1, ref_dict2)

    right = 0
    wrong = 0

    print(f"reference list: {list(sorted_ref_dict.keys())}")
    print(f"metric list: {list(sorted_metric_dict.keys())}")

    for metric_key, ref_key in zip(sorted_metric_dict.keys(), sorted_ref_dict.keys()):
        if metric_key == ref_key:
            right += 1
        else:
            wrong += 1

    print(f"User on correct position: {right}")
    print(f"User on wrong position: {wrong}")


def calculate_max_deviation(metric_dict1, ref_dict2):
    sorted_metric_dict, sorted_ref_dict = get_sorted_dicts(metric_dict1, ref_dict2)

    max_deviation = 0

    for idx, metric_key in enumerate(sorted_metric_dict.keys()):
        for cur_idx, ref_key in enumerate(sorted_ref_dict.keys()): # the index of the enumerate is the var to calculate the current deviation
            if metric_key == ref_key:
                deviation = abs(cur_idx - idx)
                if deviation > max_deviation:
                    max_deviation = deviation
    print(f"maximal deviation is: {max_deviation}")

    return max_deviation


def calculate_mean_deviation(metric_dict1, ref_dict2):
    sorted_metric_dict, sorted_ref_dict = get_sorted_dicts(metric_dict1, ref_dict2)

    deviation_list = []
    # deviation_dict = {}


    for ref_idx, metric_key in enumerate(sorted_ref_dict.keys()):
        for met_idx, ref_key in enumerate(sorted_metric_dict.keys()): # the index of the enumerate is the var to calculate the current deviation
            if metric_key == ref_key:
                deviation_list.append(abs(ref_idx - met_idx)) # go throught the whole second dict and find for every elemnt the deviation compared to the true position
                # deviation_dict[ref_key] = ref_idx - met_idx 
    # print(f"deviation list is: {deviation_list}")
    # print(f"deviation dict is: {deviation_dict}")

    mean_dev = np.mean(np.array(deviation_list))
    bellow_mean_dev_count = len([elem for elem in deviation_list if elem < mean_dev])  # calculate count of values < mean_dev
    # mode_dev = statistics.mode(deviation_list)
    # bellow_mode_dev_count = len([elem for elem in deviation_list if elem < mode_dev])  # calculate count of values < mode_dev
    print(f"mean deviation: {mean_dev}")
    print(f"num of values bellow mean dev: {bellow_mean_dev_count}")
    # print(f"num of values bellow mode dev: {bellow_mode_dev_count}")

    
    return np.mean(np.array(deviation_list))


def calculate_total_deviation(metric_dict1, ref_dict2, scale_coef=None):
    sorted_metric_dict, sorted_ref_dict = get_sorted_dicts(metric_dict1, ref_dict2)

    deviation_list = []
    deviation_dict = {}
    scaled_deviation_dict = {}

    

    for ref_idx, metric_key in enumerate(sorted_ref_dict.keys()):
        for met_idx, ref_key in enumerate(sorted_metric_dict.keys()): # the index of the enumerate is the var to calculate the current deviation
            if metric_key == ref_key:
                deviation_list.append(abs(ref_idx - met_idx)) # go throught the whole second dict and find for every elemnt the deviation compared to the true position
                deviation_dict[ref_key] = met_idx - ref_idx  # if the num is < 0 our metric set the order much bellow as it should be
                if scale_coef is not None:
                    # deviation between ref rep and metric rep in %
                    scaled_deviation_dict[ref_key] = (1 - ( (sorted_metric_dict[ref_key]*scale_coef) / sorted_ref_dict[ref_key] ) ) * 100 if sorted_metric_dict[ref_key] != 0 else 100

    scaled_deviation_list = list(scaled_deviation_dict.values())
    print(f"order deviation list is: {deviation_list}")
    print(30*"*")
    print(f"order deviation dict is: {deviation_dict}")
    print(30*"*")
    print(f"total order dev: {np.sum(np.array(deviation_list))}")
    print(30*"*")
    print(f"scaled deviation dict is: {scaled_deviation_dict}")
    print(30*"*")
    if len(scaled_deviation_list) != 0:
        print(f"mean scaled deviation is: {np.mean(np.abs(np.array(scaled_deviation_list)))}")
        print(30*"*")
        print(f"max scaled deviation is: {np.max(np.abs(np.array(scaled_deviation_list)))}")
        print(30*"*")

    return np.sum(np.array(deviation_list))


def min_max_normalize(dict):
    min_max_list = dict.values()
    norm_min, norm_max = min(min_max_list), max(min_max_list)
    min_max_norm = lambda x: (x - norm_min)/(norm_max - norm_min)

    return { key : min_max_norm(dict[key]) for key in dict.keys() }


def get_min_max(list):
    return min(list), max(list)
