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

Papers.drop()

uri = "http://neo4j:7474"
password="esgi_password"
graph = Graph(uri,password=password)
graph.run("MATCH (n) DETACH DELETE n")

## insersion base 
for paper in arxiv.query(query="quantum", max_results=1000):
    Papers.insert_one(paper)

cursor_paper = Papers.find()

for paper in cursor_paper:
    create_paper = "CREATE (p:PAPER {id: '%s' })" %paper["id"]
    match_authors = ""
    link_authors = ""
    for i, author in enumerate(paper["authors"]):
        match_authors += "MERGE (u%s:AUTHOR {name:\"%s\"}) \n"%(i, author)
        link_authors += "MERGE (u%s)-[:AUTHORED {author_rank: %s}]->(p) \n"%(i, i)
    match_tags = ""
    link_tags = ""
    for i, tag in enumerate(paper["tags"]):
        match_tags += "MERGE (t%s:TAG {name:\"%s\"}) \n"%(i, tag["term"])
        link_tags+= "MERGE (p)-[:TAGGED]->(t%s) \n"%i
    graph.run(create_paper+'\n'+match_authors+'\n'+link_authors+'\n'+match_tags+'\n'+link_tags)


