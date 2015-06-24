# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 00:00:01 2015

@author: Asus
"""


#   Made By Lysanne Rosaria
#        PG1 Bi1A Course 4 HAN Nijmegen, Netherlands

#   Worked on from 15-06 to 22-06
#   Updates:       
#   23-06 update Dyogo Borst to html genarating script 
#   24-06 debugged by Lysanne

#   Name: Singleblast.py

#   Used for webapplication by PG1 including option to blast
#   or searching in database made by Richard Jansen, filled by
#   Lysanne Rosaria with scripts project.py and projectReverse.py,
#   written by Lysanne Rosaria.

#   This script performs checking database for sequence input, ifso
#   referring client to search option of webapplication. Ifnot
#   continuing to Blast sequence and update our database with results.


#   Imports
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import re
import mysql.connector
from mod_python import apache
#   Global variables a and bused as default for the main function, this way
#   this script will work eventhough not linked to the standard .psp and .html
#   for the webapplication where the client gives input.
#a = "CCCAAGACCCGAGGGTGCGGGAAGCCGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGCGTTTTCGGGAAGGACGGTCCTCGTCACCGGCGCGGGAAGCGGCATCGGCCTGGCCATCGCCAGGGCCTTCGCCCGGGAGGGGGCGCGGGTCTTGGTCCACGACGTTCGGGACGCCTCGACGCTCGCCGAGGAGCTTTCCGGGGTCTTCCTCCAGGCGGACCTCGCCGACCCCACAGATGTGGCGGCCCTGGGCACTGAGGCCGCGCCCATCGTCCTCGACCTTCCTGTGCACCACGCCTCCTT"
#b = str(input("Sequence Blast / Complement Sequence Blast:  "))


#   Main function. Input seq and action with defaults a and "sb" which stands
#   for Sequence Blast. It can be changed into csb, Complement Sequence Blast
#   when no results have been found while trying to blast a sequence, this will
#   generate a complement of the input sequence to blast again. 
def index(req, seq="", action =""): 
    req.content_type = "text/html"
    req.write("<!DOCTYPE html>\n<html>\n<head>\n<title>BLASTx in progress</title>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"css/hoofd.css\" />\n</head>\n<body>\n<div id=\"header\">\n<ul>\n<li>\n<a href=\"index.html\" class=\"current\">\n<img src=\"image/home.png\" height=\"22\" />\n</a>\n</li>\n<li>\n<a href=\"blastx.psp\">BLASTx</a>\n</li>\n<li>\n<a href=\"search.psp\">Search database</a>\n</li>\n<li>\n<a href=\"info.psp\">Downloads</a>\n</li>\n</ul>\n</div>\n")
	
    try:
        
        if action == "Sequence Blast" or action.upper() == "SB":                    #Process main
           blastOld(req, seq)                                                            #Input action bekijken en bepalen welke functie er vervolgens                                                                                                                                                                                                                                
                                                                                    #aangeroepen moet worden, andere soort action wordt opgevangen
        elif action == "Complement Sequence Blast" or action.upper() == "CSB":      #met een melding en daarnaast staat in deze functie ook de exceptionhandling     
            blastNew(req, seq)                                                           #voor errors die tijdens het runnen van het programma kunnen ontstaan.
                                                                                    #"sb" roept blastOld aan met seq, "csb" roept blastNew aan met seq.
        else:
            req.write ("<br /><br />Somthing went wrong!! Try 'sb' or 'csb' with quotes")
            
    except IOError:                                                                 #Output main
        req.write ("<br /><br />Something went wrong with the Input and Output in Singleblast.py.") #Melding bij een andere action dan "sb" of "csb"
    except ZeroDivisionError:                                                       #Meldingen bij errors door de exception handling. 
        req.write ("<br /><br />Something made a zero division occur in Singleblast.py")
    except IndexError:
        req.write ("<br /><br />While indexing an error popped up in Singleblast.py")
    except mysql.connector.Error as err:
        req.write("<br /><br />Something went wrong between Singleblast.py and the database.")

    req.write("<br /><br /><br /><div id=\"footer\">Copyright &copy; 2015 Dyogo Borst &ndash; Lysanne Rosaria &ndash; Richard Jansen &ndash; Roel van de Wiel</div>\n")
   # req.write("</body>\n</html>")
    
#   Input blastOld
#   Een sequentie in de parameter old. Main stopt hier het variabel seq in.          
def blastOld(req, old):
    
    zoeken = checkdb(req, old)                                                           #Process blastOld
                                                                                    #Aanroepen van de functie checkdb met variabel old erin. 
    

#   Input blastNew
#   Een sequentie in parameter old. Main stopt hier het variabel seq in.     
def blastNew(req, old):
    complement = toComplement(req, old)                                                  #Process blastNew
    new = turnAround(req, complement)                                                    #Aanroepen van de functie toComplement met variabel old erin.
    req.write ("<br /><br />Sequence Complement Turned Around: \n"+str(new)+"\n\n")                 #List geretourneerd uit deze functie stoppen in variabel Complement.
    zoeken = checkdb(req, new)                                                           #Vervolgens aanroepen van turnAround met variabel complement erin.
                                                                                    #String geretourneerd uit deze functie stoppen in variabel new.
#   Output blastNew                                                                 #Aanroepen functie checkdb met argument new erin.
#   Weergave van de complementair omgedraaide sequentie.

#   Input toComplement
#   Een sequentie in parameter reverse. BlastNew stopt hier het variabel old in. 
def toComplement(req, reverse):
    seqF = []
    seqB = ""                                                                       #Process toComplement
    for nuc in reverse:                                                             #lijst seqF maken met de complementaire sequentie waarbij iedere  
        if nuc == "C":                                                              #nucleotide een item in de lijst is. A wordt T, T wordt A,  
            seqF.append("G")                                                        #G wordt C en C wordt G.
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

    return (seqF)                                               
#   Output toComplement
#   retourneerd de lijst seqF naar blastNew.

#   Input turnAround
#   Een sequentie in parameter list. BlastNew stopt hier het variabel complement in. 
def turnAround(req, list):
    c = len(list)                                                                   #Process turnAround
    f = ""                                                                          #Dmv list wordt per item vanaf de achterste een string f aangevuld.
    c -= 1                                                                          #Hierdoor ontstaat in string f de omgekeerde volgorde van de list.
    for item in list:                                                               
        f += str(list[c])
        c -= 1
    return (f)
#   Output turnAround
#   retourneerd de string naar blastNew.

#   Input checkdb
#   Een sequentie in parameter zoek. BlastNew stopt hier het variabel new  in, blastOld het variabel old. 
def checkdb(req, zoek):
    p1 = re.compile("^[ATGCatgc]*$")
    m1 = p1.search(zoek)

    conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
    cursor = conn.cursor()
    query = ("SELECT DISTINCT(`seq-id`) FROM `SOURCE_SEQ`, `BLAST_RESULT` WHERE `seq-id` LIKE '%seqwebapp%';")
   # req.write (query)
    cursor.execute(query)                       #Process checkdb
                                                #De deze functie wordt er ten eerste er bepaald hoeveel rijen er al in de database staan die overeenkomen met 
    rows = cursor.fetchall()                    #een seq id dat de naam seqwebapp bevat, dit komt in variabel count. 
    if rows == []:                              
        count = 0
    else:
        count = len(rows)
         
    
    if m1:                                      #Met een regular expression wordt gecontroleerd of het wel echt een DNA sequentie is.
                                                #Is dit niet zo levert dit een melding op. 
        req.write ("<br /><br />Searching in colums: nucleotide-sequence")     
        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
        cursor = conn.cursor()
        query = ("SELECT `seq-id`, `nucleotide-sequence`, `match-found-bool`, \
`SOURCE_SEQ_seq-id`,`amount-hits`,`result1-accession-code`,`result1-alignmen\
t-score`,`result1-query-coverage-percentage`,`result1-E-value`,`result1-ident\
-percentage` FROM `SOURCE_SEQ`, `BLAST_RESULT` where `seq-id`=`SOURCE_SEQ_seq\
-id` AND `nucleotide-sequence` LIKE '%"+str(zoek)+"%';")
     #   req.write (query)                           #Is dit wel het geval, wordt de sequentie opgezocht in de database. 
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows == []:
            req.write ("<br/><br/>Sequence: \n"+str(zoek)+"\n\n")
            req.write ("\n\n\n----------------------Blast---------------------\n")
            cursor.close()                      #Staat het in de database, verschijnt er een melding. Staat het niet in de database, 
            conn.close()                        #dan wordt de functie blast aangeroepen met de variabelen zoek en count erin.
            req.write ("count ="+str(count)) 
            blast(req, zoek, count)
        else:
            cursor.close()
            conn.close()
            req.write ("<br /><br />Your sequence does already exists in our database. Go to the search option on the website to see the blast results.")
                   
    else:                                       
        req.write ("<br /><br />Your sequence isn't DNA!! Change your input into DNA please!!")
#   Output checkdb
#   Sql querys om te controleren. Melding wanneer sequentie  geen DNA is. Melding wanneer sequentie al in database staan. Aangeven dat blast begint. 

#   Input blast
#   Een sequentie in parameter seq, een aantal in parameter count. Checkdb stopt hier het variabel zoek en count in. 
def blast(req, seq, number=""):
    bool = True
    
    results_handle = NCBIWWW.qblast("tblastx", "nr", seq, hitlist_size=10, expect=0.001, matrix_name="BLOSUM62")
    blast_results = results_handle                          #Process blast
                                                            #Dmv de modules NCBIWWW en NCBIXML uit Bio.Blast kan een blastx worden uitgevoerd
    blast_records = NCBIXML.parse(results_handle)           #tegen de dr database, e-value threshold van 0.001, score-matrix BLOSUM62. 

    E_VALUE_THRESH = 1

    c = 1
    
    for blast_record in blast_records:
        desc = blast_record.descriptions
        if desc == []:
            
            bool = False
           # req.write (1)
            conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
            cursor = conn.cursor()
            query = ("INSERT INTO `blast`.`SOURCE_SEQ`(`seq-id`, `match-found-bool`, `nucleotide-sequence`) VALUES ('seqwebapp_"+str(number+1)+"', "+str(bool)+",'"+str(seq)+"');")
            cursor.execute(query)   
            conn.commit()
            cursor.close()
            conn.close()
            req.write ("<br /><br />No Blast results have been found to your sequence with Blastx, BLOSUM62, e-value < 0.001, nr database. Try different arguments on the Blast tool website: http://blast.ncbi.nlm.nih.gov/Blast.cgi.")
            
            
        else:
            
            numhits = len(desc)
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < E_VALUE_THRESH:
                    alignmentnr =  ("-----Alignment-"+str(c)+"----")
                    hithead =  alignment.title
                    length = alignment.length               #Uit de xml output hiervan worden interessante waarden gehaald en daarmee 
                    evalue =  hsp.expect                    #wordt de database uiteindelijk geupdate.
                    gaps =  hsp.gaps
                    query =  hsp.query
                    sub = hsp.sbjct
                    match = hsp.match
                    match = match.replace(" ", " &nbsp;")
                    score = hsp.score
                    identity = hsp.identities
                    querylen = len(query)
                    qcov = float(identity) / float(querylen) * float(100)
                    if numhits == None:
                        numhits ="NULL"
                    req.write ("<br /><br /><br />"+str(alignmentnr))
                    req.write ("<br />HITHEAD:   "+str(hithead))
                    req.write ("<br />LENGTH:    "+str(length))
                    req.write ("<br />E-VALUE:   "+str(evalue))
                    req.write ("<br />GAPS:      "+str(gaps)+"<br /><br />")
                    req.write (query)
                    req.write ("<br />")
                    req.write (match)
                    req.write ("<br />")
                    req.write (sub) 
                    req.write ("<br /><br />IDENTITY:  "+str(identity))
                    req.write ("<br />SCORE:     "+str(score))
                    req.write ("<br />QCOV:      "+str(qcov))
                    match.replace("&nbsp;", " ")
          #          req.write ("c ="+str(c))
           #          req.write ("number ="+str(number)) 
                    if number == 0 and c == 1:
                      #  req.write (1)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query = ("INSERT INTO `blast`.`SOURCE_SEQ`(`seq-id`, `match-found-bool`, `nucleotide-sequence`) VALUES ('seqwebapp_"+str(number+1)+"', "+str(bool)+",'"+str(seq)+"');")
                        cursor.execute(query)   
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        if c == 1:
                      #      req.write (2)
                            conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                            cursor = conn.cursor()
                            query1 = ("INSERT INTO `blast`.`BLAST_RESULT`(`amount-hits`, `result1-accession-code`, `result1-alignment-score`, `result1-query-coverage-percentage`, `result1-E-value`, `result1-ident-percentage`, `SOURCE_SEQ_seq-id`) VALUES ("+str(numhits)+", '"+str(hithead)+"', "+str(score)+", "+str(qcov)+", "+str(evalue)+", "+str(identity)+",'seqwebapp_"+str(number+1)+"');")
                            cursor.execute(query1)
                            req.write (query1)
                            conn.commit()
                            cursor.close()
                            conn.close()
                            c += 1
                            
                    elif number == 0 and c < 11:
                     #   req.write (3)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query2 = ("UPDATE `blast`.`BLAST_RESULT` SET `result"+str(c)+"-accession-code`='"+str(hithead)+"', `result"+str(c)+"-alignment-score`='"+str(score)+"', `result"+str(c)+"-query-coverage-percentage`='"+str(qcov)+"', `result"+str(c)+"-E-value`='"+str(evalue)+"', `result"+str(c)+"-ident-percentage`='"+str(identity)+"' WHERE `SOURCE_SEQ_seq-id`='seqwebapp_"+str(number+1)+"';")
                        cursor.execute(query2)
                        req.write (query2)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        c += 1
                        
                    elif number > 0 and c == 1:
                    #    req.write (4)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query = ("INSERT INTO `blast`.`SOURCE_SEQ`(`seq-id`, `match-found-bool`, `nucleotide-sequence`) VALUES ('seqwebapp_"+str(number+1)+"', "+str(bool)+",'"+str(seq)+"');")
                        cursor.execute(query)   
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        if c == 1:
                    #        req.write(5)
                            conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                            cursor = conn.cursor()
                            query1 = ("INSERT INTO `blast`.`BLAST_RESULT`(`amount-hits`, `result1-accession-code`, `result1-alignment-score`, `result1-query-coverage-percentage`, `result1-E-value`, `result1-ident-percentage`, `SOURCE_SEQ_seq-id`) VALUES ("+str(numhits)+", '"+str(hithead)+"', "+str(score)+", "+str(qcov)+", "+str(evalue)+", "+str(identity)+",'seqwebapp_"+str(number+1)+"');")
                            cursor.execute(query1)
                            req.write (query1)
                            conn.commit()
                            cursor.close()
                            conn.close()
                            c += 1                            
                            
                    elif number > 0 and c < 11:
                     #   req.write(6)
                        conn = mysql.connector.connect(host="ithurtswhenip.nl",user = "richard", password = "richard", db = "blast", port = 3307)
                        cursor = conn.cursor()
                        query2 = ("UPDATE `blast`.`BLAST_RESULT` SET `result"+str(c)+"-accession-code`='"+str(hithead)+"', `result"+str(c)+"-alignment-score`='"+str(score)+"', `result"+str(c)+"-query-coverage-percentage`='"+str(qcov)+"', `result"+str(c)+"-E-value`='"+str(evalue)+"', `result"+str(c)+"-ident-percentage`='"+str(identity)+"' WHERE `SOURCE_SEQ_seq-id`='seqwebapp_"+str(number+1)+"';")
                        cursor.execute(query2)
                        req.write (query2)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        c += 1
                        
                    elif number > 0 and c > 10: 
                        c += 1
                        
                    
                        
                        
    

