#!/usr/bin/env python
# -*- coding=utf-8 -*-
import requests        #导入requests包
from bs4 import    BeautifulSoup
import MySQLdb

def get_words(word_filePath):
    print('word_filePath:')
    print(word_filePath)
    fr = open(word_filePath,"r")
    words=[]
    for word in fr.readlines():
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

    # 获取释义
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

    # 获取例句
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
    new_sentences=[]
    for k,v in enumerate(sentences):
        if(k%2==0):
            new_sentences.append(v[3:])
        else:
            new_sentences.append(v)
    # print(new_sentences)
    for i in new_sentences:
        # print("==="+i)
        if i.find('\"')==-1:
            sentences_str+=i+'='
            j+=1
        else:
            sentences[j]='none'
            sentences[j+1] = 'none'
    # print(sentences_str)

    # 获取词义变化
    inflexion = soup.select('#t')
    if inflexion:
        # print('不为空')
        inflexion = inflexion[0].get_text()
    else:
        inflexion=''
    # print(inflexion)



    insert_order="INSERT INTO words_details_test (" \
                 "word,soundmark,noun,transitive_verb,intransitive_verb," \
                 "adjectives,adverbs,conjunction,preposition,sentences," \
                 "pronouns,inflexion) VALUES ('"\
                 +word+"',"+word_soundmark+",'"+noun+"','"+transitive_verb+"','"+intransitive_verb+"','"\
                 +adjectives+"','"+adverbs+"','"+conjunction+"','"+preposition+"',\""+sentences_str+"\",'"\
                 +pronouns+"','"+inflexion+"');"
       # print(insert_order)
    print("success")
    return insert_order

def mysqlInsert(insert_order):
    try:
        # 执行sql语句
        # cursor.execute()
        cursor.execute(insert_order)
        myresult = cursor.fetchall()

        for x in myresult:
            print(x)
        print('1')
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # Rollback in case there is any error
        db.rollback()
        print(e)
        print('2')

def inputTxt(wors_orders):
    with open('F:/毕设/数据/test/words_order.txt', 'a',encoding='utf-8') as file_handle:  # .txt可以不自己新建,代码会自动新建
        for i in wors_orders:
            file_handle.write(i)  # 写入
            print('写入：')
            print(i)
            print('sucess')
            file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据


if __name__ == '__main__':
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "yry2137", "graduationproject", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    word_filePath='F:/毕设/数据/test/words.txt'
    words=get_words(word_filePath)
    print('words:')
    print(words)
    orders=[]
    for word in words:
        order=wordDetails(word)
        mysqlInsert(order)
        orders.append(order)
    # inputTxt(orders)

    # 关闭数据库连接
    db.close()