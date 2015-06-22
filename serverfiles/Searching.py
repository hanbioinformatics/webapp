import mysql.connector
import re

a = input("Geef input: ")
   

def main(invoer=a):
    
    obj = found(invoer)
    

class found: 
    def __init__(self, zoek):
        count1 = 1
        count2 = 1
        self.seqs = []
        zoek = zoek.upper()
        p1 = re.compile("^[ATGCatgc]*$")
        m1 = p1.search(zoek)
        p2 = re.compile("^[A-Za-z]*$")
        m2 = p2.search(zoek)
        p3 = re.compile("[A-Z\|a-z@.,_\[\]0-9]*")
        m3 = p3.search(zoek)

        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
        cursor = conn.cursor()
        if m1:
             
            query = ("SELECT * FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
-id` AND `nucleotide-sequence` LIKE '%"+str(zoek)+"%';")            
            print (query)
            cursor.execute(query)
            for row in cursor:
                index(self, row)
                count2 += 1
                toprint(self, count2)
                                 
            
        elif m2:            
        
            query = ("SELECT * FROM `SOURCE_SEQ`, `BLAST_RESULT` WHERE `seq-id`=`SOURCE_SEQ_seq-id` AND (`result1-accession-code` LIKE '%"+str(zoek)+"%' OR `result2-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result3-accession-code` LIKE '%"+str(zoek)+"%' OR `result4-accession-code` LIKE '%"+str(zoek)+"%' OR `result5-accession-code` LIKE '%"+str(zoek)+"%' OR `result6-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result7-accession-code` LIKE '%"+str(zoek)+"%' OR `result8-accession-code` LIKE '%"+str(zoek)+"%' OR `result9-accession-code` LIKE '%"+str(zoek)+"%' OR `result10-accession-code` LIKE '%"+str(zoek)+"%');")
            
            print (query)
            cursor.execute(query)
            for row in cursor:
                index(self, row)
                count2 += 1
                toprint(self, count2)
                    
                   
        elif m3:
                    
            query = ("SELECT * FROM `SOURCE_SEQ`, `BLAST_RESULT` WHERE `seq-id`=`SOURCE_SEQ_seq-id` AND (`result1-accession-code` LIKE '%"+str(zoek)+"%' OR `result2-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result3-accession-code` LIKE '%"+str(zoek)+"%' OR `result4-accession-code` LIKE '%"+str(zoek)+"%' OR `result5-accession-code` LIKE '%"+str(zoek)+"%' OR `result6-accession-code` LIKE '%"+str(zoek)+"%' OR\
`result7-accession-code` LIKE '%"+str(zoek)+"%' OR `result8-accession-code` LIKE '%"+str(zoek)+"%' OR `result9-accession-code` LIKE '%"+str(zoek)+"%' OR `result10-accession-code` LIKE '%"+str(zoek)+"%' OR `seq-id` LIKE '%"+str(zoek)+"%');")
            
            print (query)
            cursor.execute(query)
            for row in cursor:
                index(self, row)
                count2 += 1
                toprint(self, count2)
                
                
def index(self, row):
  
    self.header = row[0]
    self.bool = row[1]
    self.seq = row[2]
    self.header2 = row[3]
    self.numhits = row[4]
    self.hithead1 = row[5]
    self.score1 = row[6]
    self.qcov1 = row[7]
    self.evalue1 = row[8]
    self.ident1 = row[9]
    self.hithead2 = row[10]
    self.score2 = row[11]
    self.qcov2 = row[12]
    self.evalue2 = row[13]
    self.ident2 = row[14]
    self.hithead3 = row[15]
    self.score3 = row[16]
    self.qcov3 = row[17]
    self.evalue3 = row[18]
    self.ident3 = row[19]
    self.hithead4 = row[20]
    self.score4 = row[21]
    self.qcov4 = row[22]
    self.evalue4 = row[23]
    self.ident4 = row[24]
    self.hithead5 = row[25]
    self.score5 = row[26]
    self.qcov5 = row[27]
    self.evalue5 = row[28]
    self.ident5 = row[29]
    self.hithead6 = row[30]
    self.score6 = row[31]
    self.qcov6 = row[32]
    self.evalue6 = row[33]
    self.ident6 = row[34]
    self.hithead7 = row[35]
    self.score7 = row[36]
    self.qcov7 = row[37]
    self.evalue7 = row[38]
    self.ident7 = row[39]
    self.hithead8 = row[40]
    self.score8 = row[41]
    self.qcov8 = row[42]
    self.evalue8 = row[43]
    self.ident8 = row[44]
    self.hithead9 = row[45]
    self.score9 = row[46]
    self.qcov9 = row[47]
    self.evalue9 = row[48]
    self.ident9 = row[49]
    self.hithead10 = row[50]
    self.score10 = row[51]
    self.qcov10 = row[52]
    self.evalue10 = row[53]
    self.ident10 = row[54]
                    
            
def toprint(self, count2):
    if self.seq not in self.seqs:
        self.seqs.append(self.seq)
        print ("\n\n\n\n----------------------------------RESULTNUMBER:  "+str(count2)+"---------------------------------------------------------------")
              
        print ("\n\nHEADER:    "+str(self.header))
        print ("SEQUENCE:      "+str(self.seq))
        
    print ("\n-----------------ACCESSION-CODE RESULT 1----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead1))                        
    print ("BIT_SCORE:       "+str(self.score1))
    print ("QUERY COVERAGE:  "+str(self.qcov1))
    print ("E-VALUE:         "+str(self.evalue1))
    print ("IDENTITY:        "+str(self.ident1))
    print ("\n-----------------ACCESSION-CODE RESULT 2----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead2))                        
    print ("BIT_SCORE:       "+str(self.score2))
    print ("QUERY COVERAGE:  "+str(self.qcov2))
    print ("E-VALUE:         "+str(self.evalue2))
    print ("IDENTITY:        "+str(self.ident2))
    print ("\n-----------------ACCESSION-CODE RESULT 3----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead3))                        
    print ("BIT_SCORE:       "+str(self.score3))
    print ("QUERY COVERAGE:  "+str(self.qcov3))
    print ("E-VALUE:         "+str(self.evalue3))
    print ("IDENTITY:        "+str(self.ident3))
    print ("\n-----------------ACCESSION-CODE RESULT 4----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead4))                        
    print ("BIT_SCORE:       "+str(self.score4))
    print ("QUERY COVERAGE:  "+str(self.qcov4))
    print ("E-VALUE:         "+str(self.evalue4))
    print ("IDENTITY:        "+str(self.ident4))
    print ("\n-----------------ACCESSION-CODE RESULT 5----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead5))                        
    print ("BIT_SCORE:       "+str(self.score5))
    print ("QUERY COVERAGE:  "+str(self.qcov5))
    print ("E-VALUE:         "+str(self.evalue5))
    print ("IDENTITY:        "+str(self.ident5))
    print ("\n-----------------ACCESSION-CODE RESULT 6----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead6))                        
    print ("BIT_SCORE:       "+str(self.score6))
    print ("QUERY COVERAGE:  "+str(self.qcov6))
    print ("E-VALUE:         "+str(self.evalue6))
    print ("IDENTITY:        "+str(self.ident6))
    print ("\n-----------------ACCESSION-CODE RESULT 7----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead7))                        
    print ("BIT_SCORE:       "+str(self.score7))
    print ("QUERY COVERAGE:  "+str(self.qcov7))
    print ("E-VALUE:         "+str(self.evalue7))
    print ("IDENTITY:        "+str(self.ident7))
    print ("\n-----------------ACCESSION-CODE RESULT 8----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead8))                        
    print ("BIT_SCORE:       "+str(self.score8))
    print ("QUERY COVERAGE:  "+str(self.qcov8))
    print ("E-VALUE:         "+str(self.evalue8))
    print ("IDENTITY:        "+str(self.ident8))
    print ("\n-----------------ACCESSION-CODE RESULT9----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead9))                        
    print ("BIT_SCORE:       "+str(self.score9))
    print ("QUERY COVERAGE:  "+str(self.qcov9))
    print ("E-VALUE:         "+str(self.evalue9))
    print ("IDENTITY:        "+str(self.ident9))
    print ("\n-----------------ACCESSION-CODE RESULT 10----------------------------")
    print ("\nHITHEAD:         "+str(self.hithead10))                        
    print ("BIT_SCORE:       "+str(self.score10))
    print ("QUERY COVERAGE:  "+str(self.qcov10))
    print ("E-VALUE:         "+str(self.evalue10))
    print ("IDENTITY:        "+str(self.ident10))
           
main()
