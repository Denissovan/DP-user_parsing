import os
from xml.dom import minidom
import gc
import tqdm
import concurrent.futures
from .preprocessing.user_preprocessing import get_list_of_posts
from .dep_parsing_module import parse_section, basic_pos_relations

def parse_xml_files(root_folder, folder_names):
    dir_list = os.listdir(root_folder)
    print(dir_list)
    dir_list = [item for item in dir_list if item.split(".")[1] == "xml" if item.split(".")[0].lower() in folder_names]
    
    print(dir_list)
    domtrees = {elem.split(".")[0] : minidom.parse(os.path.join(root_folder, elem)) for elem in tqdm.tqdm(dir_list)}
    print(domtrees)
    groups = {elem.split(".")[0].lower() : domtrees[elem.split(".")[0]].documentElement for elem in tqdm.tqdm(dir_list)}
    del domtrees    
    gc.collect()
    del dir_list
    gc.collect()

    return groups


def parse_users(user_list, destination_path):
    for user in user_list:
        post_list = get_list_of_posts(user)
        with concurrent.futures.ProcessPoolExecutor() as exec:
            sub_post_list = [post_list[n:n+4] for n in range(0, len(post_list), 4)]
            for sub_post in tqdm.tqdm(sub_post_list):
                for key in sub_post:
                    exec.submit(parse_section, *(user[key], key, basic_pos_relations, destination_path))





