# homework 3
# goal: ranked retrieval, PageRank, crawling
# exports:
#   student - a populated and instantiated cs525.Student object
#   PageRankIndex - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents and providing a
#     ranked result set

# ########################################
# first, create a student object
# ########################################

import cs525
from bs4 import BeautifulSoup  # you will want this for parsing html documents
import numpy as np
import requests,sys
import re,operator

#### Write code to pip requests===================================================================================

MY_NAME = "Sayed Inamdar"
MY_ANUM  = 637508815 # put your UID here
MY_EMAIL = "sinamdar@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = []

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "An Aggie does not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs525.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################


# our index class definition will hold all logic necessary to create and search
# an index created from a web directory
#
# NOTE - if you would like to subclass your original Index class from homework
# 1 or 2, feel free, but it's not required.  The grading criteria will be to
# call the index_url(...) and ranked_search(...) functions and to examine their
# output.  The index_url(...) function will also be examined to ensure you are
# building the index sanely.

class PageRankIndex(object):
    def __init__(self):
        # you'll want to create something here to hold your index, and other
        # necessary data members
        self._inverted_index = {}
        self.frontier_list=[]
        self.tmp_frontier=[]
        self.base_url=''
        self.frontier_graph=dict()
        self.alpha=0.1
        self.tolerance=1e-8
        

    # index_url( url )
    # purpose: crawl through a web directory of html files and generate an
    #   index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: use BeautifulSoup and urllib
    # parameters:
    #   url - a string containing a url to begin indexing at

    def get_last_index_of_url(self,url):
        base_url=url
        last_part_of_index=base_url.rfind('/')
        return last_part_of_index

    ## Build the inverted index
    def build_inverted_index(self,doc_no,soup_data):
        tokens=self.tokenize(str(soup_data))
        for token in tokens:
            if token in self._inverted_index:
                token_list=self._inverted_index[token]
                token_list.add(doc_no)
            else:
                self._inverted_index[token]=set([doc_no])
    
    # Crawls the webpage    
    def crawl_webpage(self,url):
        data=requests.get(url)
        soup_data=BeautifulSoup(data.text,'html.parser')
        temporary_frontier=soup_data.find_all('a')
        page_anchor_list=[]
        
        for alist in temporary_frontier:
            page_anchor_list.append(alist.get('href'))
        
        for li in page_anchor_list:
            if li not in self.frontier_list:
                self.frontier_list.append(li)
                self.tmp_frontier.append(li)
        
        #make the graph now
        page_anchor_list_indexes=[]
        for i in page_anchor_list:
            page_anchor_list_indexes.append(self.frontier_list.index(i))

        
        last_part_url_index=self.get_last_index_of_url(url)
        self.frontier_graph[self.frontier_list.index(url[last_part_url_index+1:])]=page_anchor_list_indexes
        ##Build inverted index
        self.build_inverted_index(self.frontier_list.index(url[last_part_url_index+1:]),soup_data)
       
        
        

    def index_url(self, url):
        #initial crawling
        last_part_url_index=self.get_last_index_of_url(url)
        base_url=url[:last_part_url_index]
        self.base_url=url[:last_part_url_index]
        
        self.frontier_list.append(url[last_part_url_index+1:])
        self.crawl_webpage(url)
        
        #traverse recursively and form the final set of all the pages
        while(self.tmp_frontier):
            tmp_url=self.tmp_frontier.pop()
            self.crawl_webpage(base_url+'/'+tmp_url)
        
        return len(self.frontier_list)

    # tokenize( text )
    # purpose: convert a string of terms into a list of terms 
    # preconditions: none
    # returns: list of terms contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        text=text.lower()
        # converting non-alphanumeric text to a whitespace
        text=re.sub('[^A-Za-z0-9]+',' ',text)
        for word in text.split():
            tokens.append(word)
        # PUT YOUR CODE HERE
        return tokens

    # ranked_search( text )
    # purpose: searches for the terms in "text" in our index and returns
    #   AND results for highest 10 ranked results
    # preconditions: .index_url(...) has been called on our corpus
    # returns: list of tuples of (url,PageRank) containing relevant
    #   search results
    # parameters:
    #   text - a string of query terms
    def ranked_search(self, text):
        # ADD CODE HERE
        text=text.lower()
        tokens=text.split()
        tmp_list=[]

        for token in tokens:
            tmp_list.append(self._inverted_index.get(token) )

        if None in tmp_list or not tmp_list:
            return []
        
        ##for any number of queries terms-------------==================================
        self.temp_final=set()
        final_string='self.temp_final='
        
        for lis in range(len(tmp_list)):
            final_string+='set(tmp_list['+str(lis)+']) &'
        
        final_string=final_string[:-1]
        exec(final_string)
        
        final_list=list(self.temp_final)
          
        return final_list


    def formulate_transition_matrix(self,transition_matrix):
        for i in range(transition_matrix.shape[0]):
            if self.frontier_graph.get(i):
                connected_node=self.frontier_graph.get(i)
                for con in connected_node:
                    transition_matrix[i][con]=transition_matrix[i][con]+1/len(connected_node)
        return transition_matrix
      
        
    
    
    def compute_PageRank(self,teleportation_matrix,transition_matrix):
 
        no_of_pages=transition_matrix.shape[0]
        page_rank_matrix=np.zeros((no_of_pages,no_of_pages))    
        
        prev_page_rank=[0]*no_of_pages
        page_rank=prev_page_rank
        page_rank[0]=1
        
        difference_array=[sys.maxsize]*no_of_pages
        
        page_rank_matrix=(1-self.alpha)*transition_matrix + self.alpha*teleportation_matrix
        
        while(max(difference_array)>=self.tolerance):
            prev_page_rank = page_rank
            page_rank = np.dot(page_rank,page_rank_matrix)
            for i in range(len(page_rank)):
                difference_array[i]=abs(page_rank[i]-prev_page_rank[i])
         
        return page_rank  #page_rank
        
    def sort_page_rank(self,res,page_ranks):
        final_results=[]
        ranked_document=dict()
        max_counter=0
        
        for i in range(len(res)):
            ranked_document[res[i]]=page_ranks[res[i]]
            
        ranked_document = sorted(ranked_document.items(), key=operator.itemgetter(1),reverse=True)
        
        for i in range(len(ranked_document)):
            if max_counter<10:
                doc_name=self.frontier_list[ranked_document[i][0]]
                tmp_tuple=[doc_name,f'{ranked_document[i][1]}']
                final_results.append(tuple(tmp_tuple))
                max_counter+=1
        return final_results
            
        
        

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = PageRankIndex()
    #url = 'http://web.cs.wpi.edu/~kmlee/cs525/new10/index.html'
    url = 'http://localhost:8000/index.html'
    num_files = index.index_url(url)
    transition_matrix=np.zeros((num_files,num_files))
    teleportation_matrix=np.zeros((num_files,num_files))
    teleportation_matrix[:]=1/num_files
    transition_matrix=index.formulate_transition_matrix(transition_matrix)
    
    ##Compute page Rank
    final_page_rank=index.compute_PageRank(teleportation_matrix,transition_matrix)
    
    #search_queries = ('palatial','kjal**l\'s nm&','sayed hj&6 kj', 'college ', 'palatial college', 'college supermarket', 'famous aggie supermarket','sayed inamn')
    search_queries = ('sayed inamdar','sayed alvi inamdar kjga154 ','saj io*9 mn()(','football', 'mike','sherman', 'mike sherman', 'wiki', 'King', 'source http', 'history coaches', 'elected','1916', 'allied powers', 'world war', 'Germany Austria','yo yo lkjh','dskah mdnas')
    for q in search_queries:
        results = index.ranked_search(q)
        final_results=index.sort_page_rank(results,final_page_rank)
        print("searching: %s -- results: %s" % (q, final_results))


# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

