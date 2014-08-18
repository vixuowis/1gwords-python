# encoding=utf-8
import jieba
import jieba.posseg as pseg
import MySQLdb
import codecs

## 执行sql
def exec_sql(sql_str,is_select = True):
  # connect to db
  db = MySQLdb.connect("localhost","root","","userview_test")
  # 使用cursor()方法获取操作游标 
  cursor = db.cursor()
  # 使用execute方法执行SQL语句
  cursor.execute(sql_str)
  if is_select:
    results = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    return results
  else:
    db.commit()

    # 关闭数据库连接
    db.close()

def tokenize(raw_text):
  result = []
  seg_list = jieba.cut(raw_text)

  for w in seg_list:
    w = w.strip()
    if w!="":
      print w,
      result.append(w)

  return result

def isNumber(char):
  numbers = ["1","2","3","4","5","6","7","8","9","0",u"一",u"二",u"三",u"四",u"五",u"六",u"七",u"八",u"九",u"零",u"十",u"百",u"千",u"万",u"亿"]

  if char in numbers:
    return True
  else:
    return False

def addToHash(word,all_hash):
  print "\n*"+word,"Added*"
  if all_hash.has_key(word):
    all_hash[word] += 1
  else:
    all_hash[word] = 1

  return all_hash

def analyzeText(raw_text,all_hash):
  print raw_text
  tokens = tokenize(raw_text)
  print ""

  for index,token in enumerate(tokens):
    if len(token) == 1:
      print token
      if isNumber(token) and index!=len(tokens)-1:
        addToHash(tokens[index+1],all_hash)
    else:
      for index2,char in enumerate(token):
        print char,
        if isNumber(char) and index2!=len(token)-1:
          if index2==len(token)-1:
            addToHash(tokens[index+1],all_hash)
          else:
            addToHash(token[index2+1],all_hash)

      print ""

  return all_hash



################################
all_hash = {}
text_list = exec_sql("SELECT * from posts ORDER BY RAND()")

for text in text_list:
  analyzeText(text[5],all_hash)

f = codecs.open("result_0818.txt",'w','utf-8')
for (k,v) in sorted(all_hash.iteritems(), key=lambda (k,v): (v,k)):
  f.write(k+","+str(v)+"\n")
  print k,v
f.close()






