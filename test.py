#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "yry2137", "graduationproject", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# # 使用execute方法执行SQL语句
# cursor.execute("SELECT VERSION()")
# # 如果数据表已经存在使用 execute() 方法删除表。
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
# # 创建数据表SQL语句
# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""
#
# cursor.execute(sql)

# SQL 插入语句
word='abnormal'
noun='n.不正常的人'
transitive_verb=''
intransitive_verb=''
adjectives='adj.反常的；不正常的；变态的'
adverbs=''
conjunction=''
preposition=''
pronouns=''
inflexion='副词: abnormally '
#
sql='INSERT INTO words_details (`word` ,`noun` , `transitive_verb` , `intransitive_verb` ,`adjectives` ,`adverbs` ,`conjunction` ,`preposition` ,`pronouns` ,`inflexion` )VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)' % \
               (word,noun,transitive_verb,intransitive_verb,adjectives,adverbs,conjunction,preposition,pronouns,inflexion)
print(sql)
try:
    # 执行sql语句
    # cursor.execute()
    cursor.execute(sql)
    print('1')
    cursor.close()
    # 提交到数据库执行
    db.commit()
except Exception as e:
   # Rollback in case there is any error
   db.rollback()
   print(e)
   print('2')

# 关闭数据库连接
db.close()