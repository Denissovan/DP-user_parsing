import os
import tqdm
import gc


# gets the acm models from the given directory
def get_list_from_file(dir_path, num_of_files_to_read="all"):
    sec_files = os.listdir(dir_path)                               # get all the files in the chapters dir
    sec_dict = {}
    num_of_files_to_read = len(os.listdir(dir_path)) if num_of_files_to_read == "all" else num_of_files_to_read
    for file in tqdm.tqdm(sec_files[:num_of_files_to_read]):
        with open(os.path.join(dir_path, file), "r") as f:
            file_string = f.read().strip()
            tuples = eval(file_string)
            del file_string
            gc.collect()
            sec_dict[file.split(".txt")[0]] = [tup for tup in (set(tuple(i) for i in tuples))]  # deduplicating the tuple list
    return sec_dict


def get_user_dict_from_file(dir_path):
    user_dirs = os.listdir(dir_path)                               # get all the folders in the answer/question dir
    user_dict = {}
    for dir in tqdm.tqdm(user_dirs):
      # print(dir)
      user_files = os.listdir(os.path.join(dir_path, dir))
      tuple_list = []
      for user_f in user_files:
        local_dir = os.path.join(dir_path, dir)
        with open(os.path.join(local_dir, user_f), "r") as f:
            file_string = f.read().strip()
            tuple_list += eval(file_string)

      #empty list check   
      if tuple_list:
        user_dict[dir.split(".txt")[0]] = [tup for tup in (set(tuple(i) for i in tuple_list))] # deduplicating the tuple list
    
    del user_dirs
    del tuple_list
    del user_files
    gc.collect()
    return user_dict


def get_user_reputation_dict_from_file(path):
    with open(path, "r") as f:
        # file_string = f.read().strip()
        rep_dict = eval(f.read())
        rep_dict = { key: int(val) for key, val in rep_dict.items()}
        return rep_dict