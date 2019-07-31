import os
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer

def createIndex(files_to_index):
    '''
    Takes a directory of files and indexes them so that they may be searched through.


    Args:
        files_to_index (string) = name of directory to create index in

    '''

    #analyser object for pre-processing search terms 
    stem_analyzer = StemmingAnalyzer()

    #create search schema
    schema = Schema(title=TEXT(analyzer = stem_analyzer, stored=True),path=ID(stored=True),
              content=TEXT(analyzer = stem_analyzer, stored=True),textdata=TEXT(stored=True))

    #if path to index does not exist, create it 
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
 
    # Creating a index writer to add document as per schema
    ix = create_in("indexdir",schema)
    writer = ix.writer()
 
    #parses every file in FAQs folder and extracts question and answer text data
    filepaths = [os.path.join(files_to_index,i) for i in os.listdir(files_to_index)]
    for path in filepaths:
        html = BeautifulSoup(open(path,'r'), "lxml")
        #parse question text
        question = html.find("div", {"id" : "question"}).getText()
        #parse answer text
        answer = html.find("div", {"id" : "answer"}).getText().replace(u'Â\xa0', u' ')
        writer.add_document(title=question, path=path,
          content=answer,textdata=answer)
    writer.commit()

createIndex("faqs")