# -*- coding: utf-8 -*-
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import json
import codecs
import MySQLdb
def read():
	json_file = codecs.open("items.json", 'r', 'utf-8')
	data = json.load(json_file)
	return data

def save(index_,url,description,date,title):
	try:
		db = MySQLdb.connect("localhost","root","666666","python",charset='utf8')

		data = (index_,url,description,date,title)

		cursor = db.cursor()
	except:

		print ("error")

	sql = "INSERT INTO `search_result` (`index_`, `url`, `description`, `date`, `title`) VALUES(%s,%s,%s,%s,%s)"


	try:
		cursor.execute(sql,data)

		db.commit()
	except:
		db.rollback()

	cursor.close()

	db.close()
data = read()
global index
index = 400 
for line in data:
	#print line['description'][0]
	if(line['description'] and line['title']):
	    save(index,line['url'],line['description'][0],'2017-04-15',line['title'][0])
	    index +=1
	    #print index