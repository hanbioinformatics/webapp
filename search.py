import mysql.connector
import re


def main():
    invoer = input("Geef input: ")
    regex(invoer)


def regex(zoek):
    p1 = re.compile("^[ATGCatgc]*$")
    m1 = p1.search(zoek)
    p2 = re.compile("_1")
    m2 = p2.search(zoek)
    p3 = re.compile("_2")
    m3 = p3.search(zoek)
 #   if m1:
##        print ("Searching in colums: nucleotide-sequence")
##        conn = mysql.connector.connect(host="localhost",user = "richard", password = "richard", db = "blast", port = 3307)
##        cursor = conn.cursor()
##        query = ("select `seq-id`, `nucleotide-sequence`, `match-found-bool`, \
##`SOURCE_SEQ_seq-id`,`amount-hits`,`result1-accession-code`,`result1-alignmen\
##t-score`,`result1-query-coverage-percentage`,`result1-E-value`,`result1-ident\
##-percentage` FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
##-id` AND `nucleotide-sequence` LIKE '%ATG%'"';")   
##        print (query)
##        cursor.execute(query)
##        conn.commit()
##        cursor.close()
##        conn.close()

main()
