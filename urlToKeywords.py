# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import jieba 
import jieba.analyse
import MySQLdb


def save(index_,keywords,tf_idf):
	db = MySQLdb.connect("localhost","root","666666","python",charset='utf8')

	cursor = db.cursor()

	data = (index_,keywords,tf_idf)

	print tf_idf

	sql = "INSERT INTO `inverted index`(`index_`, `keywords`, `tf_idf`) VALUES(%s,%s,%s)"


	try:
		cursor.execute(sql,data)

		db.commit()
	except:
		print "error"
		db.rollback()

	cursor.close()

	db.close()

def main():
	db = MySQLdb.connect("localhost","root","666666","python",charset='utf8')

	cursor = db.cursor()

	sql_query = "SELECT * FROM `search_result` WHERE 1"


	try:
		cursor.execute(sql_query)

		searchResult = cursor.fetchall()

		for row in searchResult:
			print row[0]
			seg_list = jieba.analyse.extract_tags(row[2],topK=30,withWeight=True)
			for line in seg_list:
				save(row[0],line[0], line[1])
	except:
		print "error"
		db.rollback()

	cursor.close()

	db.close()
	#seg_list = jieba.analyse.extract_tags(str2,topK=20,withWeight=True)
	#for line in seg_list:
		#save(line[0],line[1])


if __name__=="__main__":
	main()

