import mysql.connector
import re

a = input("Geef input: ")
   

def main(invoer=a):
    
    regex(invoer)


def regex(zoek):
    count1 = 1
    count2 = 1
   
    seqs = []
    p1 = re.compile("^[ATGCatgc]*$")
    m1 = p1.search(zoek)
    p2 = re.compile("^[A-Za-z]*$")
    m2 = p2.search(zoek)
    p3 = re.compile("[A-Z\|a-z.,\[\]0-9]*")
    m3 = p3.search(zoek)
    if m1:
        
        print ("Searching in colums: nucleotide-sequence")
        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
        cursor = conn.cursor()
    
        query = ("SELECT `seq-id`, `nucleotide-sequence`, `match-found-bool`, \
`SOURCE_SEQ_seq-id`,`amount-hits`,`result1-accession-code`,`result1-alignmen\
t-score`,`result1-query-coverage-percentage`,`result1-E-value`,`result1-ident\
-percentage` FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
-id` AND `nucleotide-sequence` LIKE '%"+str(zoek)+"%';")
        
       # print (query)
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows == []:
            print ("Your sequence can't found in our database. Blast your sequence with the Blast option")
            cursor.close()
            conn.close()
        else:      
        
            for row in rows:
        #        print (row)
                header = row[0]
                seq = row[2]
                numhits = row[4]
                if seq not in seqs:
                    seqs.append(seq)
                    print ("\n\n---------------------RESULTNUMBER:  "+str(count2)+"--------------------------")
                    print ("\nHEADER:          "+str(header))
                    print ("SEQUENCE:        "+str(seq))
                    print ("NUMBER OF HITS:  "+str(numhits))
                    count2 += 1
                hithead = row[5]
                score = row[6]
                qcov = row[7]
                evalue = row[8]
                ident = row[9]
                print ("\n\n---------------------HITNUMBER:  "+str(count1)+"--------------------------")
                print ("\nHITHEAD:         "+str(hithead))                        
                print ("BIT_SCORE:       "+str(score))
                print ("QUERY COVERAGE:  "+str(qcov))
                print ("E-VALUE:         "+str(evalue))
                print ("IDENTITY:        "+str(ident))
                count1 += 1
            cursor.close()
            conn.close()

    elif m2:
              
        print ("Searching in colums: seq-id")
        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
        cursor = conn.cursor()
    
        query = ("SELECT * FROM `SOURCE_SEQ`, `BLAST_RESULT` WHERE `seq-id`=`SOURCE_SEQ_seq-id` AND (`result1-accession-code` LIKE '%"+str(zoek)+"%' OR `result2-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result3-accession-code` LIKE '%"+str(zoek)+"%' OR `result4-accession-code` LIKE '%"+str(zoek)+"%' OR `result5-accession-code` LIKE '%"+str(zoek)+"%' OR `result6-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result7-accession-code` LIKE '%"+str(zoek)+"%' OR `result8-accession-code` LIKE '%"+str(zoek)+"%' OR `result9-accession-code` LIKE '%"+str(zoek)+"%' OR `result10-accession-code` LIKE '%"+str(zoek)+"%');")
        
     #   print (query)
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows == []:
            print ("None of the proteins or organisms in our database corresponds to a your string.")
            cursor.close()
            conn.close()
        else:
            
            for row in rows:
           #     print (row)
                header = row[0]
                seq = row[2]
                numhits = row[4]
                if seq not in seqs:
                    seqs.append(seq)
                    print ("\n\n---------------------RESULTNUMBER:  "+str(count2)+"--------------------------")
                    print ("\nHEADER:          "+str(header))
                    print ("SEQUENCE:        "+str(seq))
                    print ("NUMBER OF HITS:  "+str(numhits))
                    count2 += 1
                hithead = row[5]
                score = row[6]
                qcov = row[7]
                evalue = row[8]
                ident = row[9]
                print ("\n\n---------------------HITNUMBER:  "+str(count1)+"--------------------------")
                print ("\nHITHEAD:         "+str(hithead))                        
                print ("BIT_SCORE:       "+str(score))
                print ("QUERY COVERAGE:  "+str(qcov))
                print ("E-VALUE:         "+str(evalue))
                print ("IDENTITY:        "+str(ident))
                count1 += 1    
            cursor.close()
            conn.close()
            
    elif m3:
        print ("Searching in colums: seq-id")
        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
        cursor = conn.cursor()
        
        query = ("SELECT * FROM `SOURCE_SEQ`, `BLAST_RESULT` WHERE `seq-id`=`SOURCE_SEQ_seq-id` AND (`result1-accession-code` LIKE '%"+str(zoek)+"%' OR `result2-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result3-accession-code` LIKE '%"+str(zoek)+"%' OR `result4-accession-code` LIKE '%"+str(zoek)+"%' OR `result5-accession-code` LIKE '%"+str(zoek)+"%' OR `result6-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result7-accession-code` LIKE '%"+str(zoek)+"%' OR `result8-accession-code` LIKE '%"+str(zoek)+"%' OR `result9-accession-code` LIKE '%"+str(zoek)+"%' OR `result10-accession-code` LIKE '%"+str(zoek)+"%');")
        
##        query = ("SELECT `seq-id`, `nucleotide-sequence`, `match-found-bool`, \
##`SOURCE_SEQ_seq-id`,`amount-hits`,`result1-accession-code`,`result1-alignmen\
##t-score`,`result1-query-coverage-percentage`,`result1-E-value`,`result1-ident\
##-percentage` FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
##-id` AND `seq-id` LIKE '%"+str(zoek)+"%';")
##        
   #     print (query)
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows == []:
            print ("Your header can't found in our database.")
            cursor.close()
            conn.close()
            for row in rows:
                print (row)
       #         header = row[0]
                seq = row[2]
                numhits = row[4]
                if seq not in seqs:
                    seqs.append(seq)
                    print ("\n\n---------------------RESULTNUMBER:  "+str(count2)+"--------------------------")
                    print ("\nHEADER:          "+str(header))
                    print ("SEQUENCE:        "+str(seq))
                    print ("NUMBER OF HITS:  "+str(numhits))
                    count2 += 1
                hithead = row[5]
                score = row[6]
                qcov = row[7]
                evalue = row[8]
                ident = row[9]
                print ("\n\n---------------------HITNUMBER:  "+str(count1)+"--------------------------")
                print ("\nHITHEAD:         "+str(hithead))                        
                print ("BIT_SCORE:       "+str(score))
                print ("QUERY COVERAGE:  "+str(qcov))
                print ("E-VALUE:         "+str(evalue))
                print ("IDENTITY:        "+str(ident))
                count1 += 1    
            cursor.close()
            conn.close()
    else:
        print("Your input probably isn't a DNA sequence, header or normal word, so we can't perfor, a search in our database. Please change your input!!")
main()
