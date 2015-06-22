from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import re
import mysql.connector

a = "CCCAAGACCCGAGGGTGCGGGAAGCCTACCTTAGCCTGTAGGAGGTCTACATGGGAGCGTTTTCGGGAAGGACGGTCCTCGTCACCGGCGCGGGAAGCGGCATCGGCCTGGCCATCGCCAGGGCCTTCGCCCGGGAGGGGGCGCGGGTCTTGGTCCACGACGTTCGGGACGCCTCGACGCTCGCCGAGGAGCTTTCCGGGGTCTTCCTCCAGGCGGACCTCGCCGACCCCACAGATGTGGCGGCCCTGGGCACTGAGGCCGCGCCCATCGTCCTCGACCTTCCTGTGCACCACGCCTCCTT"
b = str(input("Sequence Blast / Complement Sequence Blast:  "))



def main(seq=a, action = "sb"): 

    if action == "Sequence Blast" or action.upper() == "SB":                #conditionele check op variabel action. Zeer belangrijk voor de voortgang van het programma, het interpreteren van de optie sb of csb, gekozen door de client.
        blastOld(seq)
    elif action == "Complement Sequence Blast" or action.upper() == "CSB":
        blastNew(seq)
    else:
        print ("Somthing went wrong!! Try 'sb' or 'csb' with quotes")

def blastOld(old):
    
    zoeken = checkdb(old)
    
    
def blastNew(old):
    complement = toComplement(old)
    new = turnAround(complement)
    print ("Sequence Complement Turned Around: \n"+str(new)+"\n\n")
    zoeken = checkdb(new)
    

def toComplement(reverse):
    seqF = []
    seqB = ""
    for nuc in reverse:
        if nuc == "C":
            seqF.append("G")
            seqB += "G"
        elif nuc == "G":
            seqF.append("C")
            seqB += "C"
        elif nuc == "A":
            seqF.append("T")
            seqB += "T"
        elif nuc == "T":
            seqF.append("A")
            seqB += "A"

    print ("Seq: \n"+str(reverse)+"\n\n")
    print ("Seq Complement: \n"+str(seqB)+"\n\n")

    return (seqF)

def turnAround(list):
    c = len(list)
    f = ""
    c -= 1
    for item in list: 
        f += str(list[c])
        c -= 1
    return (f)

def checkdb(zoek):
    p1 = re.compile("^[ATGCatgc]*$")
    m1 = p1.search(zoek)

    conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
    cursor = conn.cursor()
    query = ("SELECT * FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
-id` AND `seq-id` LIKE '%seqwebapp%';")
    print (query)
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows == []:
        count = 0
    else:
        count = len(rows)
    cursor.execute(query)
    rows = cursor.fetchall()
    if m1:
        
        print ("Searching in colums: nucleotide-sequence")     
        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
        cursor = conn.cursor()
        query = ("SELECT `seq-id`, `nucleotide-sequence`, `match-found-bool`, \
`SOURCE_SEQ_seq-id`,`amount-hits`,`result1-accession-code`,`result1-alignmen\
t-score`,`result1-query-coverage-percentage`,`result1-E-value`,`result1-ident\
-percentage` FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
-id` AND `nucleotide-sequence` LIKE '%"+str(zoek)+"%';")
        print (query)
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows == []:
            print ("Sequence: \n"+str(zoek)+"\n\n")
            print ("\n\n\n----------------------Blast---------------------\n")
            cursor.close()
            conn.close()
            blast(zoek, count)
        else:
            cursor.close()
            conn.close()
            print ("Your sequence does already exists in our database. Go to the search option on the website to see the blast results.")
                   
    else:
        print ("Your sequence isn't DNA!! Change your input into DNA please!!")
        
            
def blast(seq, number=""):
    bool = True
    
    results_handle = NCBIWWW.qblast("tblastx", "nr", seq, hitlist_size=10, expect=0.001, matrix_name="BLOSUM62")
    blast_results = results_handle
    
    blast_records = NCBIXML.parse(results_handle)

    E_VALUE_THRESH = 1

    c = 1
    
    for blast_record in blast_records:
        desc = blast_record.descriptions
        if desc == []:
            
            bool = False
            print (1)
            conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
            cursor = conn.cursor()
            query = ("INSERT INTO `blast`.`SOURCE_SEQ`(`seq-id`, `match-found-bool`, `nucleotide-sequence`) VALUES ('seqwebapp_"+str(number+1)+"', "+str(bool)+",'"+str(seq)+"');")
            cursor.execute(query)   
            conn.commit()
            cursor.close()
            conn.close()
            print ("No Blast results have been found to your sequence with Blastx, BLOSUM62, e-value < 0.001, nr database. Try different arguments on the Blast tool website: http://blast.ncbi.nlm.nih.gov/Blast.cgi.")
            
            
        else:
            
            numhits = len(desc)
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < E_VALUE_THRESH:
                    alignmentnr =  ("\n\n-----Alignment-"+str(c)+"----")
                    hithead =  alignment.title
                    length = alignment.length
                    evalue =  hsp.expect
                    gaps =  hsp.gaps
                    query =  hsp.query
                    sub = hsp.sbjct
                    match = hsp.match
                    score = hsp.score
                    identity = hsp.identities
                    querylen = len(query)
                    qcov = float(identity) / float(querylen) * float(100)
                    if numhits == None:
                        numhits ="NULL"
                    print (alignmentnr)
                    print ("\nHITHEAD:   ", hithead)
                    print ("LENGTH:    ", length)
                    print ("E-VALUE:   ", evalue)
                    print ("GAPS:      ", gaps)
                    print (query)
                    print (match)
                    print (sub)
                    print ("IDENTITY:  ", identity)
                    print ("SCORE:     ", score)
                    print ("QCOV:      ", qcov)
                    if number == 0 and c == 1:
                        print (1)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query = ("INSERT INTO `blast`.`SOURCE_SEQ`(`seq-id`, `match-found-bool`, `nucleotide-sequence`) VALUES ('seqwebapp_"+str(number+1)+"', "+str(bool)+",'"+str(seq)+"');")
                        cursor.execute(query)   
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        if c == 1:
                            print (2)
                            conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                            cursor = conn.cursor()
                            query1 = ("INSERT INTO `blast`.`BLAST_RESULT`(`amount-hits`, `result1-accession-code`, `result1-alignment-score`, `result1-query-coverage-percentage`, `result1-E-value`, `result1-ident-percentage`, `SOURCE_SEQ_seq-id`) VALUES ("+str(numhits)+", '"+str(hithead)+"', "+str(score)+", "+str(qcov)+", "+str(evalue)+", "+str(identity)+",'seqwebapp_"+str(number+1)+"');")
                            cursor.execute(query1)
                            print (query1)
                            conn.commit()
                            cursor.close()
                            conn.close()
                            c += 1
                            
                    elif number == 0 and c < 11:
                        print (3)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query2 = ("UPDATE `blast`.`BLAST_RESULT` SET `result"+str(c)+"-accession-code`='"+str(hithead)+"', `result"+str(c)+"-alignment-score`='"+str(score)+"', `result"+str(c)+"-query-coverage-percentage`='"+str(qcov)+"', `result"+str(c)+"-E-value`='"+str(evalue)+"', `result"+str(c)+"-ident-percentage`='"+str(identity)+"' WHERE `SOURCE_SEQ_seq-id`='seqwebapp_"+str(number+1)+"';")
                        cursor.execute(query2)
                        print (query2)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        c += 1
                        
                    elif number > 0 and c == 1:
                        print (4)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query = ("INSERT INTO `blast`.`SOURCE_SEQ`(`seq-id`, `match-found-bool`, `nucleotide-sequence`) VALUES ('seqwebapp_"+str(number+1)+"', "+str(bool)+",'"+str(seq)+"');")
                        cursor.execute(query)   
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        if c == 1:
                            print(5)
                            conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                            cursor = conn.cursor()
                            query1 = ("INSERT INTO `blast`.`BLAST_RESULT`(`amount-hits`, `result1-accession-code`, `result1-alignment-score`, `result1-query-coverage-percentage`, `result1-E-value`, `result1-ident-percentage`, `SOURCE_SEQ_seq-id`) VALUES ("+str(numhits)+", '"+str(hithead)+"', "+str(score)+", "+str(qcov)+", "+str(evalue)+", "+str(identity)+",'seqwebapp_"+str(number+1)+"');")
                            cursor.execute(query1)
                            print (query1)
                            conn.commit()
                            cursor.close()
                            conn.close()
                            c += 1                            
                            
                    elif number > 0 and c < 11:
                        print(6)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query2 = ("UPDATE `blast`.`BLAST_RESULT` SET `result"+str(c)+"-accession-code`='"+str(hithead)+"', `result"+str(c)+"-alignment-score`='"+str(score)+"', `result"+str(c)+"-query-coverage-percentage`='"+str(qcov)+"', `result"+str(c)+"-E-value`='"+str(evalue)+"', `result"+str(c)+"-ident-percentage`='"+str(identity)+"' WHERE `SOURCE_SEQ_seq-id`='seqwebapp_"+str(number+1)+"';")
                        cursor.execute(query2)
                        print (query2)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        c += 1
                        
                        
                    
                        
                        
    print (bool)
main(action=b)
