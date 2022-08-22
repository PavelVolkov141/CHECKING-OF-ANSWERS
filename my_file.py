pip install pymorphy2 #для выделения частей речи
import pymorphy2

pip install wiki-ru-wordnet #для выделения синонимов
from wiki_ru_wordnet import WikiWordnet
import re

def synonym(word):
  wikiwordnet = WikiWordnet()
  synsets = wikiwordnet.get_synsets(word) #слово (word) должно быть полностью с маленькой буквы и в начальной форме
  i=0
  syn=[]
  while i<len(synsets):
    s = synsets[i]
    for w in s.get_words():
      syn.append(w.lemma())
    for hyponym in wikiwordnet.get_hyponyms(s): #get_hyponyms() гипонимы (частные сущности) и get_hypernyms() гиперонимы (более общие сущности) [больше слов, но могут быть погрешности]
     {syn.append(w.lemma()) for w in hyponym.get_words()}
    for hypernym in wikiwordnet.get_hypernyms(s):
     {syn.append(w.lemma()) for w in hypernym.get_words()}
    i=i+1
  syn=list(set(syn)) #удалим все повторы
  return syn

def f(stud,ref):
  if len(stud)>0 and len(ref)>0:
    k=0
    for x in stud:
      i=0
      while i<len(ref):
        if x==ref[i]:
          k+=1
          break
        i+=1
      else:
        exitFlag=False
        for x_syn in synonym(x):
          for y in ref:
            if x_syn==y:
              k+=1
              exitFlag=True
              break
          if exitFlag==True:
            break
    return k/len(ref)
  return 0

def note(ref_answer,stud_answer,weight): #reference_answer- эталонный ответ, student_answer- ответ студента
  ref_NOUN=[] #сущ
  ref_NPRO=[] #местоимение-существительное
  ref_ADJF=[] #прил
  ref_VERB=[] #гл (также (изначально) прич или дееприч)
  ref_NUMR=[] #числ (буквенно)
  ref_ADVB=[] #нар
  ref_COMP=[] #компаратив (сравнение)
  ref_PREP=[] #предлог
  ref_CONJ=[] #союз
  ref_PRCL=[] #частица

  stud_NOUN=[] #сущ
  stud_NPRO=[] #местоимение-существительное
  stud_ADJF=[] #прил
  stud_VERB=[] #гл
  stud_NUMR=[] #числ (буквенно)
  stud_ADVB=[] #нар
  stud_COMP=[] #компаратив (сравнение)
  stud_PREP=[] #предлог
  stud_CONJ=[] #союз
  stud_PRCL=[] #частица

  marks = '''!()-[]{};?@#$%:'"\,./^&amp;*_'''
  for x in ref_answer: 
      if x in marks:  
          ref_answer=ref_answer.replace(x, "") #удалим всю пунктуацию 
  ref_answer=ref_answer.lower() #переведем строку в нижний регистр
  ref_answer=ref_answer.split() #поделим строку на слова
  ref_answer=list(set(ref_answer))

  for x in stud_answer: 
      if x in marks:  
          stud_answer=stud_answer.replace(x, "") #удалим всю пунктуацию 
  stud_answer=stud_answer.lower() #переведем строку в нижний регистр
  stud_answer=stud_answer.split() #поделим строку на слова
  stud_answer=list(set(stud_answer))

  morph=pymorphy2.MorphAnalyzer()
  for x in ref_answer:
    p=morph.parse(x)[0] #будет, наример, Parse(word='машинами', tag=OpencorporaTag('NOUN,inan,femn plur,ablt'), normal_form='машина', score=1.0, methods_stack=((DictionaryAnalyzer(), 'машинами', 55, 11),))
    if p.tag.POS=="NOUN":
      ref_NOUN.append(p.normal_form)
    elif p.tag.POS=="NPRO":
      ref_NPRO.append(p.normal_form)
    elif p.tag.POS=="ADJF" or p.tag.POS=="ADJS":
      ref_ADJF.append(p.normal_form)
    elif p.tag.POS=="VERB" or p.tag.POS=="INFN" or p.tag.POS=="PRTF" or p.tag.POS=="PRTS" or p.tag.POS=="GRND":
      ref_VERB.append(p.normal_form)
    elif p.tag.POS=="NUMR":
      ref_NUMR.append(p.normal_form)
    elif p.tag.POS=="ADVB":
      ref_ADVB.append(p.normal_form)
    elif p.tag.POS=="COMP":
      ref_COMP.append(p.normal_form)
    elif p.tag.POS=="PREP":
      ref_PREP.append(p.normal_form)
    elif p.tag.POS=="CONJ":
      ref_CONJ.append(p.normal_form)
    elif p.tag.POS=="PRCL":
      ref_PRCL.append(p.normal_form)

  for x in stud_answer:
    p=morph.parse(x)[0]
    if p.tag.POS=="NOUN":
      stud_NOUN.append(p.normal_form)
    elif p.tag.POS=="NPRO":
      stud_NPRO.append(p.normal_form)
    elif p.tag.POS=="ADJF" or p.tag.POS=="ADJS":
      stud_ADJF.append(p.normal_form)
    elif p.tag.POS=="VERB" or p.tag.POS=="INFN" or p.tag.POS=="PRTF" or p.tag.POS=="PRTS" or p.tag.POS=="GRND":
      stud_VERB.append(p.normal_form)
    elif p.tag.POS=="NUMR":
      stud_NUMR.append(p.normal_form)
    elif p.tag.POS=="ADVB":
      stud_ADVB.append(p.normal_form)
    elif p.tag.POS=="COMP":
      stud_COMP.append(p.normal_form)
    elif p.tag.POS=="PREP":
      stud_PREP.append(p.normal_form)
    elif p.tag.POS=="CONJ":
      stud_CONJ.append(p.normal_form)
    elif p.tag.POS=="PRCL":
      stud_PRCL.append(p.normal_form)

  ref_NOUN=list(set(ref_NOUN))
  ref_NPRO=list(set(ref_NPRO))
  ref_ADJF=list(set(ref_ADJF))
  ref_VERB=list(set(ref_VERB))
  #ref_LATN=list(set(ref_LATN))

  stud_NOUN=list(set(stud_NOUN))
  stud_NPRO=list(set(stud_NPRO))
  stud_ADJF=list(set(stud_ADJF))
  stud_VERB=list(set(stud_VERB))
  #stud_LATN=list(set(stud_LATN))

  #доля правдивости между ответами для каждой части речи
  f_all=[]
  f_NOUN=f(stud_NOUN,ref_NOUN) #сущ
  f_all.append(f_NOUN)
  f_NPRO=f(stud_NPRO,ref_NPRO) #местоимение-существительное
  f_all.append(f_NPRO)
  f_ADJF=f(stud_ADJF,ref_ADJF) #прил
  f_all.append(f_ADJF)
  f_VERB=f(stud_VERB,ref_VERB) #гл
  f_all.append(f_VERB)
  f_NUMR=f(stud_NUMR,ref_NUMR) #числ
  f_all.append(f_NUMR)
  f_ADVB=f(stud_ADVB,ref_ADVB) #нар
  f_all.append(f_ADVB)
  f_COMP=f(stud_COMP,ref_COMP) #компаратив (сравнение)
  f_all.append(f_COMP)
  f_PREP=f(stud_PREP,ref_PREP) #предлог
  f_all.append(f_PREP)
  f_CONJ=f(stud_CONJ,ref_CONJ) #союз
  f_all.append(f_CONJ)
  f_PRCL=f(stud_PRCL,ref_PRCL) #частица
  f_all.append(f_PRCL)
  #f_LATN=f(stud_LATN,ref_LATN) #латиница (английское слово)
  #f_all.append(f_LATN)

  k=0
  t=0
  i=0
  while i<len(f_all):
    k=k+f_all[i]*weight[i]
    t=t+weight[i]
    i=i+1

  return str(k/t*100)+"%"

  #s="Оценка: "+str(k/t*100)+"%"
  #return s

"""
Короткий пример:
s1="Создан класс Alf. Объекты, принадлежащие классу, имеют атрибут a равный 1 и метод b, который возвращает значение атрибута a, умноженного на 5."
s2="Cоздает класс Alf, в котором существует объект а. Далее функция умножает значение а на 5, полученное значение равно b."

#веса ([0;1]) для каждой части речи эталонного ответа (логично ставить вес только для той части речи, которая присутсвует в эталонном ответе)
weight=[]
w_NOUN=1 #сущ
weight.append(w_NOUN)
w_NPRO=0 #местоимение-существительное
weight.append(w_NPRO)
w_ADJF=0 #прил
weight.append(w_ADJF)
w_VERB=1 #гл
weight.append(w_VERB)
w_NUMR=0 #числ
weight.append(w_NUMR)
w_ADVB=0 #нар
weight.append(w_ADVB)
w_COMP=0 #компаратив (сравнение)
weight.append(w_COMP)
w_PREP=0 #предлог
weight.append(w_PREP)
w_CONJ=0 #союз
weight.append(w_CONJ)
w_PRCL=0 #частица
weight.append(w_PRCL)
#w_LATN=0.5 #латиница (английское слово)
#weight.append(w_LATN)

print(note(s1,s2,weight))
"""

#работа с EXCEL:

from google.colab import drive
drive.mount('/content/drive')
import pandas as pd
#import numpy as np

pip install XlsxWriter
import xlsxwriter

data = pd.read_excel("drive/MyDrive/pr/Otvety_1.xlsx", header=None) #работаем с исходным файлом Otvety_1.xlsx
#display(data)

weight=[]
w_NOUN=1 #сущ
weight.append(w_NOUN)
w_NPRO=0 #местоимение-существительное
weight.append(w_NPRO)
w_ADJF=0 #прил
weight.append(w_ADJF)
w_VERB=1 #гл
weight.append(w_VERB)
w_NUMR=0 #числ
weight.append(w_NUMR)
w_ADVB=0 #нар
weight.append(w_ADVB)
w_COMP=0 #компаратив (сравнение)
weight.append(w_COMP)
w_PREP=0 #предлог
weight.append(w_PREP)
w_CONJ=0 #союз
weight.append(w_CONJ)
w_PRCL=0 #частица
weight.append(w_PRCL)
#w_LATN=0.5 #латиница (английское слово)
#weight.append(w_LATN)

weight2=[]
w_NOUN=1 #сущ
weight2.append(w_NOUN)
w_NPRO=0 #местоимение-существительное
weight2.append(w_NPRO)
w_ADJF=0 #прил
weight2.append(w_ADJF)
w_VERB=1 #гл
weight2.append(w_VERB)
w_NUMR=0 #числ
weight2.append(w_NUMR)
w_ADVB=0 #нар
weight2.append(w_ADVB)
w_COMP=0 #компаратив (сравнение)
weight2.append(w_COMP)
w_PREP=0 #предлог
weight2.append(w_PREP)
w_CONJ=0 #союз
weight2.append(w_CONJ)
w_PRCL=0 #частица
weight2.append(w_PRCL)
#w_LATN=0 #латиница (английское слово)
#weight2.append(w_LATN)

weight3=[1,0,0,1,0,0,0,0,0,0]
weight4=[0,0,1,1,0,0,0,0,0,0]
weight5=[1,0,0,1,0,0,0,0,0,0]
weight6=[1,0,0,1,0,0,0,0,0,0]
weight7=[1,0,0,1,0,0,0,0,0,0]
weight8=[1,0,1,1,0,0,0,0,0,0]
weight9=[1,0,1,1,0,0,0,0,0,0]
weight10=[1,0,0.5,1,0,0,0,0,0,0]

weight_all=[]
weight_all.append(weight)
weight_all.append(weight2)
weight_all.append(weight3)
weight_all.append(weight4)
weight_all.append(weight5)
weight_all.append(weight6)
weight_all.append(weight7)
weight_all.append(weight8)
weight_all.append(weight9)
weight_all.append(weight10)

k=-1
for i in range(0, 19, 2):
  k+=1
  j=5
  ref=data[i][1]
  for x in data[i].items():
    if x[0]>4 and pd.notna(x[1]): #номер строки ячейки больше 4, а значение ячейки не null
      data[i+1][j]=note(ref,x[1],weight_all[k])
      print(i,j,x[1])
      j+=1

writer = pd.ExcelWriter('drive/MyDrive/pr/Otvety_out.xlsx') #создастся новый файл Otvety_out.xlsx
data.to_excel(writer)

writer.close()
