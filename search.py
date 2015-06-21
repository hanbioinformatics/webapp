import mysql.connector
import re


def main():
    invoer = input("Geef input: ")
    regex(invoer)


def regex(zoek):
    count = 0
    seqs = []
    p1 = re.compile("^[ATGCatgc]*$")
    m1 = p1.search(zoek)
    p2 = re.compile("_1")
    m2 = p2.search(zoek)
    p3 = re.compile("_2")
    m3 = p3.search(zoek)
    if m1:
        print ("Searching in colums: nucleotide-sequence")
        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
        cursor = conn.cursor()
        query = ("select `seq-id`, `nucleotide-sequence`, `match-found-bool`, \
`SOURCE_SEQ_seq-id`,`amount-hits`,`result1-accession-code`,`result1-alignmen\
t-score`,`result1-query-coverage-percentage`,`result1-E-value`,`result1-ident\
-percentage` FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
-id` AND `nucleotide-sequence` LIKE '%ATG%';")   
        print (query)
        cursor.execute(query)
        for row in cursor:
            header = row[0]
            seq = row[1]
            numhits = row[4]
            if seq not in seqs:
                seqs.append(seq)
                print ("\n\n---------------------HITNUMBER:  "+str(count)+"--------------------------")
                print ("\nHEADER:          "+str(header))
                print ("SEQUENCE:        "+str(seq))
                print ("NUMBER OF HITS:  "+str(numhits))
            
            hithead = row[5]
            score = row[6]
            qcov = row[7]
            evalue = row[8]
            ident = row[9]
            print ("\nHITHEAD:         "+str(hithead))                        
            print ("BIT_SCORE:       "+str(score))
            print ("QUERY COVERAGE:  "+str(qcov))
            print ("E-VALUE:         "+str(evalue))
            print ("IDENTITY:        "+str(ident))
            
            count += 1
##        rows = str(cursor.fetchall())
##        print (rows)
        cursor.close()
        conn.close()

main()
