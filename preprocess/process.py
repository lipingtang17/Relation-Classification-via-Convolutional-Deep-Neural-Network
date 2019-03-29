# coding=utf-8

'''
Preprocess original Sem-eval task8 data
'''

import json

def process_question(question):
  question = question.replace("'", " '") # 将句子中的, ' . 当成一个字符串，与前面的单词分隔开
  question = question.replace(",", " ,")
  question = question.replace(".", " .")
  question = question.split(' ')  #以字符串中的空格进行分割
  e1_begin = e1_end = e2_begin = e2_end = 0
  for i, item in enumerate(question): # 根据<e1>获取位置
    if item.startswith('<e1>'):
      e1_begin = i
    if item.endswith('</e1>'):
      e1_end = i
    if item.startswith('<e2>'):
      e2_begin = i
    if item.endswith('</e2>'):
      e2_end = i
  def remove_tag(x): # 去掉所有<e1>这些tag
    x = x.replace('<e1>', '')
    x = x.replace('</e1>', '')
    x = x.replace('<e2>', '')
    x = x.replace('</e2>', '')
    return x
  question = list(map(remove_tag, question))
  return question, e1_begin, e1_end, e2_begin, e2_end


def process_file(in_filename="./data/TRAIN_FILE.TXT",\
  out_filename="../data/train.txt"):
  max_len = 0
  max_distance = 0
  with open(in_filename, 'r') as f:
    lines = f.readlines()
  new_lines = []
  for i in range(0, len(lines), 4):
    relation = lines[i+1].strip()  #第i+1行 为关系标签
    question = lines[i].strip().split('\t')[1][1:-1]  # 以字符串中的\t进行分割，第一个为编号，取[1]，即句子
    question, e1_begin, e1_end, e2_begin, e2_end = process_question(question) #question为将<e1>符号去掉的句子
    max_len = max(max_len, len(question)) # max_len为所有句子长度的max
    max_distance = max(max_distance, e1_end)
    max_distance = max(max_distance, len(question) - e1_end) 
    max_distance = max(max_distance, e2_end) 
    max_distance = max(max_distance, len(question) - e2_end) #relative position的最大值
    new_lines.append('{}\t{}\t{}\t{}\t{}\t{}\n'.format(' '.join(question),\
      e1_begin, e1_end, e2_begin, e2_end, relation))
  with open(out_filename, 'w') as f:
    f.writelines(new_lines)
  print("Max length: {}".format(max_len))
  print("Max distance: {}".format(max_distance))
      
if __name__ == '__main__':
  import fire
  fire.Fire()
