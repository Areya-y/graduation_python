#!/usr/bin/env python
# -*- coding=utf-8 -*-
import requests        #导入requests包
from bs4 import    BeautifulSoup
def get_words(word_filePath):
    print('word_filePath:')
    print(word_filePath)
    fr = open(word_filePath,"r")
    words=[]
    for word in fr.readlines():
        if word:
            word = word.strip()
            words.append(word)
    print('words:')
    print(words)
    print('yes!')
    return words

def wordDetails(word):
    url = 'http://dict.cn/mini.php?utf8=true&q='+word
    strhtml=requests.get(url)
    soup=BeautifulSoup(strhtml.text,'lxml')
    word_en=soup.select('body > span.g.b > span')[0].get_text()
    print("word:"+word_en)

    word_soundmark="\""+soup.select('body > span.p')[0].get_text()[2:-1]+"\""
    # print("pron:"+word_soundmark)

    word_interpretation=str(soup.select('#e')[0])
    interpretation_replace = word_interpretation.replace('<br/>',"|")   #用换行符替换'<br/>'
    while True:                      #用换行符替换所有的'<br/>'
        index_begin = interpretation_replace.find("<")
        index_end = interpretation_replace.find(">",index_begin + 1)
        if index_begin == -1:
            break
        interpretation_replace = interpretation_replace.replace(interpretation_replace[index_begin:index_end+1],"")
    interpretations=interpretation_replace.split('|')
    adjectives = ''
    adverbs = ''
    preposition = ''
    noun = ''
    transitive_verb = ''
    intransitive_verb= ''
    pronouns = ''
    conjunction = ''
    for i in interpretations:
        partOfSpeech=i.split('.')[0]
        if partOfSpeech=='adj'or partOfSpeech=='a':
            adjectives=i
        elif partOfSpeech=='adv'or partOfSpeech=='ad':
            adverbs=i
        elif partOfSpeech == 'v' or partOfSpeech == 'vi':
            intransitive_verb = i
        elif partOfSpeech == 'vt':
            transitive_verb = i
        elif partOfSpeech == 'prep':
            preposition = i
        elif partOfSpeech == 'n':
            noun = i
        elif partOfSpeech == 'pron':
            pronouns = i
        elif partOfSpeech == 'conj':
            conjunction = i
        else:
            continue
    # print("interpretations:")
    # print(interpretations)
    # print(adjectives)
    # print(adverbs)
    # print(preposition)
    # print(noun)
    # print(transitive_verb)
    # print(intransitive_verb)
    # print(pronouns)
    # print(conjunction)

    sentences_example=str(soup.select('#s')[0])
    sentences_replace = sentences_example.replace('<br/>',"|")   #用换行符替换'<br/>'
    while True:                      #用换行符替换所有的'<br/>'
        index_begin = sentences_replace.find("<")
        index_end = sentences_replace.find(">",index_begin + 1)
        if index_begin == -1:
            break
        sentences_replace = sentences_replace.replace(sentences_replace[index_begin:index_end+1],"")
    sentences=sentences_replace.split('|')[0:-1]
    sentences_str=''
    j=0
    # print(sentences)
    for i in sentences:
        # print("==="+i)
        if i.find('\"')==-1:
            sentences_str+=i+'+'
            j+=1
        else:
            sentences[j]='none'
            sentences[j+1] = 'none'
    # print(sentences)
    # print(sentences_str)
    inflexion = soup.select('#t')
    if inflexion:
        # print('不为空')
        inflexion = inflexion[0].get_text()
    else:
        inflexion=''
    # print(inflexion)
    insert_order="INSERT INTO words_details (word,soundmark,noun,transitive_verb,intransitive_verb,adjectives,adverbs,conjunction,preposition,sentences,pronouns,inflexion) VALUES ('"+word+"',"+word_soundmark+",'"+noun+"','"+transitive_verb+"','"+intransitive_verb+"','"+adjectives+"','"+adverbs+"','"+conjunction+"','"+preposition+"',\""+sentences_str+"\",'"+pronouns+"','"+inflexion+"');"
       # print(insert_order)
    print("success")
    return insert_order

def inputTxt(wors_orders):
    with open('F:/毕设/数据/test/words_order.txt', 'a',encoding='utf-8') as file_handle:  # .txt可以不自己新建,代码会自动新建
        for i in wors_orders:
            file_handle.write(i)  # 写入
            print('写入：')
            print(i)
            print('sucess')
            file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据


if __name__ == '__main__':
    word_filePath='F:/毕设/数据/test/word_test.txt'
    words=get_words(word_filePath)
    print('words:')
    print(words)
    orders=[]
    for word in words:
        order=wordDetails(word)
        orders.append(order)
    inputTxt(orders)