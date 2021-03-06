from nltk.parse.stanford import StanfordDependencyParser
import time
import os

# Path to CoreNLP jar unzipped
jar_path = 'stanford-corenlp-4.2.2/stanford-corenlp-4.2.2.jar'

# Path to CoreNLP model jar
models_jar_path = 'drive/MyDrive/Colab Notebooks/dependency_parser/stanford-corenlp-4.2.2-models-english.jar'

# sentence = 'An element of such an array may have as its value a null reference or an instance of any type that implements the interface. Array with an abstract class type as the element type are allowed. An element of such an array may have as its value a null reference or an instance of any subclass of the abstract class that is not itself abstract. An array length is not part of its type. The supertypes of an array type are specified in §4.10.3. The supertype relation for array types is not the same as the superclass relation. The direct supertype of  is  according to §4.10.3, but the direct superclass of  is Object according to the Class object for  (§10.8).'


# Initialize StanfordDependency Parser from the path
parser = None

def parse_dependencies(data, pos_relations):
  
  # print("I am in parse_dependecies!")

  global parser

  # set the parser
  if parser is None:
      parser = StanfordDependencyParser(path_to_jar = jar_path, path_to_models_jar = models_jar_path)

  # Parse the sentence
  # print(data)
  result = parser.raw_parse(data)
  # result = parser.raw_parse("I only have 2 1/2 years or work   experience in the industry.")

  
  dependency = result.__next__()


  print ("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}".format('Head', 'Head POS','Relation','Dependent', 'Dependent POS'))
  print ("-" * 75)
    
  # Use dependency.triples() to extract the dependency triples in the form
  # ((head word, head POS), relation, (dependent word, dependent POS))  

  section_dependecies = []
  for dep in list(dependency.triples()):
    # continue
    print ("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}"
          .format(str(dep[0][0]),str(dep[0][1]), str(dep[1]), str(dep[2][0]),str(dep[2][1])))
    for relation in pos_relations:
        if relation[0] in str(dep[0][1]) and relation[1] in str(dep[2][1]) and str(dep[0][0]).isalpha() and str(dep[2][0]).isalpha():
            section_dependecies.append((str(dep[0][0]), str(dep[2][0])))
  return section_dependecies


basic_pos_relations = [("NN","VB"), ("VB","NN")]
file_type = ".txt"

def parse_section(section, key, pos_relations, path_dir):
  start = time.time()
  # print(f"Path to jar_path is : {jar_path}")
  # print(f"Path to models_jar_path is : {models_jar_path}")

  print(section)

  dependency_words = []
  
  # print()
  if not os.path.exists(os.path.join(path_dir, key + file_type)):
    # print("file exists")
    with open(os.path.join(path_dir, key + file_type), "a") as fi:
      for idx, token in enumerate(section):
          token_splited = token.split(". ")
          print(f"Index: {idx}")
          for splited in token_splited:
              count_of_words = len(splited.split(" "))
              print(len(splited))
              if splited is not None and count_of_words > 2 and len(splited) < 500:
                  print(f"Splited is : {splited}")
                  dependency_words.append(parse_dependencies(splited, pos_relations))
                  # parse_dependencies(splited, pos_relations, path_dir, key)

      end = time.time()
      print(f"Time of execution {str(end - start)}")

      dependency_words = [j for sub in dependency_words for j in sub]

      print(dependency_words)

      fi.writelines(str(dependency_words))