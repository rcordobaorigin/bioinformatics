from requests_html import HTMLSession
import xml.etree.ElementTree as ET
from Bio import Phylo
from io import StringIO

def ObtainIds(database, term):
    Idlist = []
    session = HTMLSession()
    r = session.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db='+database+'&term='+term+'&usehistory=y')
    root = ET.fromstring(r.content)
    for subchild in root.iter('Id'):
        Idlist.append(subchild.text)
    r.close()
    return Idlist

def OpenSessionPubMed(id, database):
    session = HTMLSession()
    r = session.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db='+database+'&id='+id+'&rettype=fasta&retmode=text')
    return r

def CloseSession(r):
    r.close()

def GenerateTxt(IdList, database, path):
    f = open(path,"w+")
    if len(IdList)>1:
        for id in IdList:
            if 'RNA' in id:
                id = ObtainIds(database, id)
                id = id[0]
            r = OpenSessionPubMed(id, database)
            f.write(r.text)
            CloseSession(r)
    else:
        id = IdList[0]
        r = OpenSessionPubMed(id, database)
        f.write(r.text)
        CloseSession(r)
    f.close()


def StringToList(IdList):
    Ids = IdList.split(',')
    return Ids


def ClustalRequester(email, title, order, dealign, mbed, mbediteration, iterations, hmmiterations, outfmt, sequence):
    session = HTMLSession()
    data = {"email": email, "title": title, "order": order, "dealign": dealign, "mbed": mbed, "mbediteration": mbediteration, "iterations": iterations, "hmmiterations": hmmiterations, "outfmt": outfmt, "sequence": sequence}
    r = session.post('http://www.ebi.ac.uk/Tools/services/rest/clustalo/run/', data = data)
    job = r.text
    CloseSession(r)
    return job

def ClustalStatus(Job):
    session = HTMLSession()
    status = session.get('http://www.ebi.ac.uk/Tools/services/rest/clustalo/status/'+ Job)
    result = status.text
    session.close()
    return result

def ClustalObtainTypeResults(Job):
    TypeList = []
    session = HTMLSession()
    r = session.get('http://www.ebi.ac.uk/Tools/services/rest/clustalo/resulttypes/' + Job)
    root = ET.fromstring(r.content)
    for subchild in root.iter('identifier'):
            TypeList.append(subchild.text)
    r.close()
    return TypeList

def ClustalGetResults(Job, TypeList):
    print(TypeList)
    for type in TypeList:
        if (type == 'aln-clustal'):
            session = HTMLSession()
            r = session.get('http://www.ebi.ac.uk/Tools/services/rest/clustalo/result/'+ Job +'/'+ type)
            compare = r.text
            r.close()
            print(compare)
        if (type == 'phylotree'):
            session = HTMLSession()
            r = session.get('http://www.ebi.ac.uk/Tools/services/rest/clustalo/result/'+ Job +'/'+ type)
            print(r.text)
            tree = Phylo.read(StringIO(r.text), "newick")
            r.close()
            Phylo.draw(tree)
        if (type == 'pim'):
            session = HTMLSession()
            r = session.get('http://www.ebi.ac.uk/Tools/services/rest/clustalo/result/'+ Job +'/'+ type)
            matrix = r.text
            r.close()
            print(matrix)