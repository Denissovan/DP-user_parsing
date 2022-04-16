import re
import fitz
import pandas as pd
import numpy as np
import os
import nltk
import tqdm

# getting the list of all the sections from the book (ToC)
def get_toc_list(file_path):
    with fitz.open(file_path) as doc:
        toc = doc.get_toc()
        return [(t[0], re.sub(r'\xa0', ' ', t[1]), t[2]) for t in toc]


def trim_headers(page):
  if page == '':
    return page
  if "C H A P T E R" in page:
    return page.split("\n",3)[3]
  else:
    return page.split("\n",1)[1]

# section_range_end needs to be negative
def get_section_dict(sections, level, section_range_start, section_range_end):
  section_list = [list(row) for row in sections]
  np_section_list = np.array(section_list)

  df_section_list = pd.DataFrame(np_section_list, columns = ['chapter_lvl','chapter_name','begin_page'])
  df_section_list = df_section_list.iloc[section_range_start:section_range_end]
  df_section_list['chapter_lvl'] = df_section_list['chapter_lvl'].astype(int)
  df_section_list['begin_page'] = df_section_list['begin_page'].astype(int)

  pd_dict = df_section_list.loc[df_section_list['chapter_lvl'] <= level, ['chapter_name', 'begin_page']].to_dict(orient = 'list')
  combined = dict(zip(pd_dict['begin_page'], pd_dict['chapter_name']))
  # lookup = set()  # a temporary lookup set
  # ls = [x for x in ls if x not in lookup and lookup.add(x) is None]
  return combined


sub_section_pattern = re.compile(r'(?:\d+\.)+\d+ [\w ]+')

def remove_sub_sec_headers(sections):
    for idx,i in enumerate(sections):
        sections[idx] = re.sub(sub_section_pattern, '', sections[idx])
        sections[idx] = os.linesep.join([s for s in sections[idx].splitlines() if s])


# sub_sub_sec_pattern = re.compile(r'(?:\d+\.)+\d+ [\w ]+')
floating_point_num_pat = re.compile(r'[+-]?([0-9]*[.])?[0-9]+')

def remove_floating_point_nums(sections):
    for idx,i in enumerate(sections):
        sections[idx] = re.sub(floating_point_num_pat, '', sections[idx])               # removing the floats
        sections[idx] = re.sub(r'§+', '', sections[idx])                                # removing the paragraphs
        sections[idx] = re.sub(r'\([, ]*\)', '', sections[idx])                         # removing empty brackets
        sections[idx] = re.sub(r'•+', '', sections[idx])                                # removing bullets
        sections[idx] = os.linesep.join([s for s in sections[idx].splitlines() if s])   # removing the empty lines


def remove_newlines(sections):
    for idx,i in enumerate(sections):
        sections[idx] = re.sub('\n', ' ', sections[idx])


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def tokenize(chap):
    return nltk.sent_tokenize(chap)


delete_signs = ["{", "}", ";", "Example", "/**", "/", "<", ">" ]

def delete_unwanted_signs(tokenized_chap):
    return [sentence for sentence in tokenized_chap if not any([sign in sentence for sign in delete_signs]) ]


def preproces_sections_into_tokens(section_dict):
    for key in tqdm.tqdm(section_dict.keys()):
        remove_sub_sec_headers(section_dict[key])
    for key in tqdm.tqdm(section_dict.keys()):
        section_dict[key] = list(map(trim_headers, section_dict[key][:]))
    for key in tqdm.tqdm(section_dict.keys()):
        remove_floating_point_nums(section_dict[key])
    for key in tqdm.tqdm(section_dict.keys()):
        remove_newlines(section_dict[key])

