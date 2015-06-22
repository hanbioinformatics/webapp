from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


def main():
    boolL = []
   # seqR = "CCCCCAGCCCCTTCGCTTCATCCCTCTCCGTCCCCCTTTGTTTCTCTGCCCCCCCGCCCTCTCCATCCCCTTCCTCTTCCGTTTCCTCCCCTCCACTGCGCCCTCCTCCCCCCCCTCCATCTTCTCCCATCCCCCCTTGTTCCCCACCATTTCCACCCCCCTCGCCGCTCCCTCCTTTCCCCCTCCCTCCTCCCCCTTTCCCTCCTCCACCTCCTCCTCGCTCTCCCCCCCTTCACCCTCCTCCCCCTCCCTCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCTCCCC"
    seqR = "CCCAAGACCCGAGGGTGCGGGAAGCCTACCTTAGCCTGTAGGAGGTCTACATGGGAGCGTTTTCGGGAAGGACGGTCCTCGTCACCGGCGCGGGAAGCGGCATCGGCCTGGCCATCGCCAGGGCCTTCGCCCGGGAGGGGGCGCGGGTCTTGGTCCACGACGTTCGGGACGCCTCGACGCTCGCCGAGGAGCTTTCCGGGGTCTTCCTCCAGGCGGACCTCGCCGACCCCACAGATGTGGCGGCCCTGGGCACTGAGGCCGCGCCCATCGTCCTCGACCTTCCTGTGCACCACGCCTCCTT"
    Subforward = toForward(seqR)
    forward = turnAround(Subforward)
    print ("Seq Complement Turned Around: \n"+str(forward)+"\n\n")
    print ("\n\n\n----------------------Blast Seq----------------------------------------------\n")
    blastR = blast(seqR, boolL)

    print ("\n\n\n----------------------Blast Seq Complement Turned Around---------------------\n")
    blastF = blast(forward, boolL)
    print (boolL)

def toForward(reverse):
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

def blast(seq, lijst):

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
        else:
            numhits = len(desc)
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < E_VALUE_THRESH:
                    alignmentnr =  ("-----Alignment-"+str(c)+"----")
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
                    print ("hithead:   ", hithead)
                    print ("length:    ", length)
                    print ("e-value:   ", evalue)
                    print ("gaps:      ", gaps)
                    print (query)
                    print (match)
                    print (sub)
                    print ("identity:  ", identity)
                    print ("score:     ", score)
                    print ("qcov:      ", qcov)
                    hithead.replace("[","<")
                    hithead.replace("]","<")
                    lijstje = hithead.split("<")
                    organisme = lijstje[1]
                    print ("ORGANISM: "+str(organisme)) 

    #print ("match found: " + str(bool))
    lijst.append(str(bool))
    return (lijst)
main()
