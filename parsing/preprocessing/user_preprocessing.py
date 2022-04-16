import re
import tqdm
import os
from .pdf_preprocessing import tokenize, delete_unwanted_signs
# tags_pattern = re.compile(r"</?(p|li|code|ol|pre)>")

tags_pattern = re.compile(r"<.*?>")

def remove_tags_from_body(post):
    body_to_change = post.getAttribute('Body')
    body_to_change = re.sub(tags_pattern, "", body_to_change)
    post.setAttribute('Body', body_to_change)
    # print(f"changed: {body_to_change}")
    return post


def remove_df_body_tags(body):
    return re.sub(tags_pattern, "", body)


def display_post(posts: list) -> None:
  if posts is None or None in posts:
      return None
  for p in posts:
    print(f"Post# {p.getAttribute('Id')}, Date of creation: {p.getAttribute('CreationDate')}, PostTypeId: {p.getAttribute('PostTypeId')}, OwnerUserId: {p.getAttribute('OwnerUserId')}")


def display_post_by_user_id(posts: list, user_id) -> None:
  if posts is None or None in posts:
      return None
  for p in posts:
    if p.getAttribute('OwnerUserId') == user_id:
      print(f"Post# {p.getAttribute('Id')}, Date of creation: {p.getAttribute('CreationDate')}, PostTypeId: {p.getAttribute('PostTypeId')}, OwnerUserId: {p.getAttribute('OwnerUserId')}")


def display_questions(questions: list) -> None:
  if questions is None or None in questions:
      return None
  for q in questions:
    print(f"Question# {q.getAttribute('Id')}, Score: {q.getAttribute('Score')}, ViewCount: {q.getAttribute('ViewCount')}, AnswerCount: {q.getAttribute('AnswerCount')}, Title: {q.getAttribute('Title')}, Date of creation: {q.getAttribute('CreationDate')}, PostTypeId: {q.getAttribute('PostTypeId')}, Tags: {q.getAttribute('Tags')}")


def display_answers(answers: list) -> None:
  if answers is None or None in answers:
      return None
  for a in answers:
    print(f"Answer# {a.getAttribute('Id')}, ParentId: {a.getAttribute('ParentId')}, PostTypeId: {a.getAttribute('PostTypeId')}, Score: {a.getAttribute('Score')}, OwnerUserId: {a.getAttribute('OwnerUserId')}, Date of creation: {a.getAttribute('CreationDate')}, CommentCount: {a.getAttribute('CommentCount')}")


def display_question_bodies(questions: list) -> None:
  if questions is None or None in questions:
      return None
  for q in questions:
    print(f"Question# {q.getAttribute('Id')}, Score: {q.getAttribute('Score')}, {q.getAttribute('Body')}")


sort_key_numerical = lambda x, y: int(x.getAttribute(y))

# returns the list of user ids of users which mention a tag in the about me
def get_user_ids_by_tags_and_rep(users, reputation):
    # print(users)
    return [user for user in users if re.search(r'\bJAVA\b', user.getAttribute('AboutMe'), re.IGNORECASE)
                                   if int(user.getAttribute('Reputation')) > reputation]


def display_users(users):
    for user in users:
        print(f"Id: {user.getAttribute('Id')}, Reputation: {user.getAttribute('Reputation')}, DisplayName: {user.getAttribute('DisplayName')}")


def get_questions_answers_by_user(posts, user_id):
  questions, answers = [post for post in posts  
            if post.getAttribute('PostTypeId') == "1" 
            if post.getAttribute('OwnerUserId') == user_id 
         ],[post for post in posts  
              if post.getAttribute('PostTypeId') == "2" 
              if post.getAttribute('OwnerUserId') == user_id]
  if len(answers) >= 1:
      return questions, answers
  return None, None


def filter_users(posts, users):
    user_list = []
    for user in tqdm.tqdm(users):
        _, user_a = get_questions_answers_by_user(posts, user.getAttribute('Id'))
        if user_a is not None:
            user_list.append(user)
    return user_list


def get_accepted_questions(questions):
    return [question for question in questions if question.getAttribute('AcceptedAnswerId')]


def get_user_id_by_accepted_answer(answers, accepted_answer_id):
    for answer in answers:
        if answer.getAttribute('Id') == accepted_answer_id:
            return answer.getAttribute('OwnerUserId')


def get_accepted_answer_by_q(question, post_answers):
    for answer in post_answers:
        if answer.getAttribute('Id') == question.getAttribute('AcceptedAnswerId'):
            return answer


def get_accepted_answer2q(question, post_rows):
    accepted_answer_id = question.getAttribute('AcceptedAnswerId')
    print(accepted_answer_id)
    if accepted_answer_id is "" or accepted_answer_id is None:
        return None
    else:
      for post in post_rows:
          if post.getAttribute('Id') == accepted_answer_id:
               return post


def display_count_of_user_q_a(posts, users):
    for user in users:
        user_q, user_a = get_questions_answers_by_user(posts, user.getAttribute('Id'))
        print(f"user_id : {user.getAttribute('Id')}, reputation : {user.getAttribute('Reputation')}, count of answers : {len(user_a)}, count of questions : {len(user_q)}")


def remove_newlines_in_post(sentence):
    return re.sub('\n', ' ', sentence)


def preproces_questions_into_tokens(q_dict):
    for key in tqdm.tqdm(q_dict.keys()):
        q_dict[key] = remove_newlines_in_post(q_dict[key])
    for key in tqdm.tqdm(q_dict.keys()):
        q_dict[key] = tokenize(q_dict[key])
    for key in tqdm.tqdm(q_dict.keys()):
        q_dict[key] = delete_unwanted_signs(q_dict[key])


def save_reputation_list(path_dir, file_name, user_dict):
  if not os.path.exists(os.path.join(path_dir, file_name)):
      with open(os.path.join(path_dir, file_name), "a") as fi:
          fi.writelines(str(user_dict))


def get_list_of_posts(id_body):
    post_list = [key for key in id_body.keys()]
    return post_list