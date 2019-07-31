from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, OrGroup


FILES_TO_INDEX = "faqs"

def conduct_search(query_str):
    '''
    Conducts search over indexed documents using a user-provided query.


    Args:
        query_str (string): The query used for the search


    Returns:
        results_list: A ranked list of 3 tuples containing highest scoring question and answer data
        
    '''

    #number of search results returned to user
    NUM_OF_RESULTS_SHOWN = 3

    #open the index directory
    ix = open_dir("indexdir")

    #conduct index search
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        query = MultifieldParser(["title", "content"], ix.schema, group=OrGroup).parse(query_str)
        results = searcher.search(query,limit=NUM_OF_RESULTS_SHOWN,terms=True)
        if NUM_OF_RESULTS_SHOWN < len(results):
            results_list = [(results[num]["title"], results[num]["content"]) for num in range(NUM_OF_RESULTS_SHOWN)]
        else:
            results_list = [(results[num]["title"], results[num]["content"]) for num in range(len(results))]
        return results_list

print(conduct_search("how do i get to university"))