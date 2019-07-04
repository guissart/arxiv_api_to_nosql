import requests
from pymongo import MongoClient
import xmltodict
import urllib.request 
import xmljson
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import arxiv
from py2neo import Graph


client = MongoClient('mongodb',27017)
db = client['arxiv']
Papers = db["Papers"]


uri = "http://neo4j:7474"
password="esgi_password"
graph = Graph(uri,password=password)

def paper_abstract(paper) :
    to_return = ""
    to_return += "paper url :"
    to_return += paper["id"]
    to_return += "Title :"
    to_return += paper["title"]
    to_return += "Summary :"
    to_return += paper['summary']
    to_return += "Autors :"
    to_return += " ".join(paper["authors"])
    return to_return

def get_paper(author_name, tag):
    c = graph.run("MATCH (a:AUTHOR {name : \"%s\"})-[]-(p:PAPER)-[]-(t:TAG {name: '%s'}) return p"%(author_name,tag ))
    to_return = ""
    for result in c.data() :
        to_return += paper_abstract(Papers.find_one({"id":result['p'].get('id')}))
        to_return += "\n\n"
    return to_return


def sorted_colaborators(author_names):
    if isinstance(author_names, str):
        author_names = [author_names]
    dict_author_link = {}
    for name in author_names :
        c = graph.run("MATCH (a:AUTHOR {name : \"%s\"})-[]-(p:PAPER)-[]-(a2:AUTHOR) return a2.name"%(name))
        for result in c.data():
            name_bis = result["a2.name"]
            number_author = dict_author_link.get(name_bis, 0)
            number_author+=1
            dict_author_link[name_bis] = number_author
    author_sorted = sorted(list(dict_author_link.items()), key=lambda x : x[1], reverse=True)

    return author_sorted
            
