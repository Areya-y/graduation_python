# import nltk
# nltk.download('punkt')
import sys, re, collections, nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import MySQLdb

# patterns that used to find or/and replace particular chars or words
# to find chars that are not a letter, a blank or a quotation
pat_letter = re.compile(r'[^a-zA-Z \']+')
# to find the 's following the pronouns. re.I is refers to ignore case
pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
# to find the 's following the letters
pat_s = re.compile("(?<=[a-zA-Z])\'s")
# to find the ' following the words ending by s
pat_s2 = re.compile("(?<=s)\'s?")
# to find the abbreviation of not
pat_not = re.compile("(?<=[a-zA-Z])n\'t")
# to find the abbreviation of would
pat_would = re.compile("(?<=[a-zA-Z])\'d")
# to find the abbreviation of will
pat_will = re.compile("(?<=[a-zA-Z])\'ll")
# to find the abbreviation of am
pat_am = re.compile("(?<=[I|i])\'m")
# to find the abbreviation of are
pat_are = re.compile("(?<=[a-zA-Z])\'re")
# to find the abbreviation of have
pat_ve = re.compile("(?<=[a-zA-Z])\'ve")

lmtzr = WordNetLemmatizer()


def get_words(file):
    with open(file,encoding="UTF-8") as f:
        words_box = []
        pat = re.compile(r'[^a-zA-Z \']+')
        for line in f:
            words_box.extend(merge(replace_abbreviations(line).split()))
    return collections.Counter(words_box)


def merge(words):
    new_words = []
    for word in words:
        if word:
            tag = nltk.pos_tag(word_tokenize(word))  # tag is like [('bigger', 'JJR')]
            pos = get_wordnet_pos(tag[0][1])
            if pos:
                lemmatized_word = lmtzr.lemmatize(word, pos)
                new_words.append(lemmatized_word)
            else:
                new_words.append(word)
    return new_words


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''


def replace_abbreviations(text):
    new_text = text
    new_text = pat_letter.sub(' ', text).strip().lower()
    new_text = pat_is.sub(r"\1 is", new_text)
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_not.sub(" not", new_text)
    new_text = pat_would.sub(" would", new_text)
    new_text = pat_will.sub(" will", new_text)
    new_text = pat_am.sub(" am", new_text)
    new_text = pat_are.sub(" are", new_text)
    new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text


def append_ext(words):
    new_words = []
    for item in words:
        word, count = item
        mysqlUpdate(word, count)
        new_words.append((word, count))
    return new_words


def mysqlUpdate(word,count):
    selectSql = "SELECT * FROM words_details_test WHERE word='" + word + "'"
    print(selectSql)
    degree = 0
    if (count < 2):
        degree = 0
    elif (count >= 2 and count < 6):
        degree = 1
    else:
        degree = 2
    updateSql = "UPDATE words_details_test SET test_requency_two=" + str(count) + ",degree_two=" + str(
        degree) + " WHERE word='" + word + "'"
    print(updateSql)

    try:
        cursor.execute(selectSql)
        myresult = cursor.fetchone()
        print("select:")
        print(myresult)
        if (myresult != None):
            # 执行sql语句
            cursor.execute(updateSql)
            print('1')
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # Rollback in case there is any error
        db.rollback()
        print(e)
        print('2')

if __name__ == '__main__':
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "yry2137", "graduationproject", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    book_file='F:/毕设/数据/英二/英语二2010-2019.txt'
    print("counting...")
    words = get_words(book_file)
    print("writing file...")
    append_ext(words.most_common())

    # 关闭数据库连接
    db.close()

