import matplotlib.pyplot as plt
import numpy as np


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')



def plot_vals(val_dict1=None, val_dict2=None, metric_name1=None, metric_name2=None):
  
  plt.rcParams['figure.figsize'] = [15, 6]
  # plt.style.use('ggplot')
  plt.rcParams["figure.autolayout"] = True
  
  labels = [str(i+1) for i in range(0, len(val_dict1.keys()))]

  x = np.arange(len(labels))  # the label locations
  width = 0.4  # the width of the bars

  fig, ax = plt.subplots()
  rects2 = ax.bar(x + 0.2, val_dict1.values(), width, label= metric_name1, align="center")
  rects1 = ax.bar(x - 0.2, val_dict2.values(), width, label=metric_name2, color="red", align="center")
  # rects3 = ax.bar(x + width, phrases_overal_cos_sim.values(), width, label='Cosine')

  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel('Reputácia [%]')
  ax.set_xlabel('Používatelia')
  ax.set_title('Reputácia používateľov podľa metriky')
  # ax.set_xticks(x)
  # ax.set_xticklabels(labels)
  ax.legend()


  # autolabel(rects1, ax)
  # autolabel(rects2, ax)
  # autolabel(rects3)


  plt.show()


def plot_chapter_matching(matching_dict, id_name):
  chap_names = list(map(str, matching_dict.keys()))
  matching_values = list(matching_dict.values())

  fig = plt.figure(figsize = (10, 5))
  #  Bar plot
  plt.bar(chap_names, matching_values, color ='blue',
          width = 0.5)

  plt.xticks(rotation='vertical')

  plt.xlabel("Kapitoly z knihy")
  plt.ylabel("Matching [%]")
  plt.title(f"Profil používateľa s ID {id_name}")

  plt.show()


def plot_chapter_matching_pie(matching_dict, id_name, legend_vals=None):
  chap_names = legend_vals
  matching_values = list(matching_dict.values())

  fig = plt.figure(figsize = (10, 5))
  plt.pie(matching_values, labels=chap_names,
  autopct='%1.1f%%', shadow=True, startangle=140)
  plt.title(f"Profil používateľa s ID {id_name}")
  # if legend_vals is not None:
  #   plt.legend(legend_vals,loc="best")
  plt.show()