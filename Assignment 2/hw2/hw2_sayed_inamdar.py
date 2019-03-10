# homework 2
# goal: wildcard query
# exports: 
#   student - a populated and instantiated cs525.Student object
#   BetterIndex - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents

# we'll want this in our index
import binarytree
from functools import reduce
import time


# ########################################
# first, create a student object
# ########################################

import cs525
MY_NAME = "Sayed Inamdar"
MY_ANUM  = 637508815 # put your UID here
MY_EMAIL = "sinamdar@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = []

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "I do not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs525.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# crawl_tree( node, term )
# purpose: crawl a binary tree looking for permuterm matches
# hint: node.key.startswith(term)
# preconditions: none
# returns: list of documents contained matching the term
# parameters: a node within a binary tree and a term as a string
def crawl_tree(node, term):
    if not node: return set()
    if ('*' in term and node.key.startswith(term[:-1])) or term == node.key:
        x = node.data
    else: x = set()
    return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))
    #if term <= node.key[:len(term)]:
    #    x = x.union(crawl_tree(node.left, term))
    #else:
    #    x = x.union(crawl_tree(node.right, term))
    #return x

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
#
# NOTE - if you would like to subclass your original Index class from homework
# 1, feel free, but it's not required.  The grading criteria will be to call
# the index_dir(...), wildcard_search_or(...), and wildcard_search_and(...)
# functions and to examine their output.  The index_dir(...) function will also
# be examined to ensure you are building the permuterm index appropriately.
#
class BetterIndex(object):
    WILDCARD = '*'
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._bt = binarytree.binary_tree()
        # _documents contains file names of documents
        self._documents = []

    # _permute( term )
    # purpose: generate and return a list of permutations for the given term
    # preconditions: none
    # returns: list of permutations for the given term
    # parameters: a single term as a string 
    def _permute(self, term):
        x = term + "$"
        return [x[i:] + x[:i] for i in range(len(x))]

    # _rotate( term )
    # purpose: rotate a wildcard term to generate a search token
    # preconditions: none
    # returns: string containing a search token
    # parameters: a single term as a string
    def _rotate(self, term):
        x = term + "$"
        if self.WILDCARD not in term: return x
        n = x.index(self.WILDCARD) + 1
        return (x[n:] + x[:n])

    # index_dir( base_path )
    # purpose: crawl through a directory of text files and generate a
    #   permuterm index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
        num_files_indexed = 0
        from glob import glob
        for fn in glob("%s/*" % base_path):
            num_files_indexed += 1
            for line in open(fn,encoding="utf8"):
                if fn not in self._documents:
                    self._documents.append(fn)
                doc_idx = self._documents.index(fn)
                for t in self.tokenize(line):
                    for term in self._permute(t):
                        if term not in self._bt:
                            self._bt[term] = set()
                        if doc_idx not in self._bt[term]:
                            self._bt[term].add(doc_idx)
        return num_files_indexed


    # tokenize( text )
    # purpose: convert a string of terms into a list of terms 
    # preconditions: none
    # returns: list of terms contained within the text
    # parameters:
    #   text - a string of terms
    #   is_search - boolean which determines whether we strip out the wildcard
    #     character or not
    def tokenize(self, text, is_search=False):
        import re
        if is_search:
            # don't strip out our wildcard character from query terms
            clean_string = re.sub('[^a-z0-9 *]', ' ', text.lower())
        else:
            clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
        tokens = clean_string.split()
        return tokens


    # wildcard_search_or( text )
    # purpose: searches for the terms in "text" in our index
    # preconditions: _bt and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def wildcard_search_or(self, text):
        text=text.lower()
        tokens=text.split()
        temp_set=set()
        final_list=[]
        final_file_name=[]
        
        
        for token in tokens:
            rotated_token=self._rotate(token)
            token_docs=crawl_tree(self._bt.root,rotated_token)
            for tok in token_docs:
                temp_set.add(str(tok))
            
        final_list=list(temp_set)
        final_list.sort()
        
        if not final_list:
            final_file_name=["No Document Found"]
        else:
            for l in final_list:
                final_file_name.append(self._documents[int(l)])
                final_file_name.sort()
        
        #r=index._rotate(text)
        #a=crawl_tree(index._bt.root,r)
        #print("SEARCH OR : "+str(a))
        
        # FILL OUT CODE HERE
        return final_file_name


    # wildcard_search_and( text )
    # purpose: searches for the terms in "text" in our corpus
    # preconditions: _bt and _documents have been populated from
    #   the corpus.
    # returns: list of file names containing relevant search results
    # parameters:
    #   text - a string of terms
    def wildcard_search_and(self, text):
        # FILL OUT CODE HERE
        text=text.lower()
        tokens=text.split()
        temp_lists=[]
        final_list=[]
        final_file_name=[]
        
        for token in tokens:
            rotated_token=self._rotate(token)
            token_docs=crawl_tree(self._bt.root,rotated_token)
            temp_lists.append(token_docs)
        
        ##check this later-------------==================================
        self.temp_final=set()
        final_string='self.temp_final='
        
        for lis in range(len(temp_lists)):
            final_string+='set(temp_lists['+str(lis)+']) &'
        
        final_string=final_string[:-1]
        exec(final_string)
        
        final_list=list(self.temp_final)
        
        ### Final check if doc lis is empty or not
        if not final_list:
            final_file_name=["No Document Found"]
        else:
            final_list.sort()
            for l in final_list:
                final_file_name.append(self._documents[int(l)])
                final_file_name.sort()
            #for i in range(len(final_list)):
             #   final_list[i]=str(final_list[i])
        return final_file_name



# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = BetterIndex()
    print("starting indexer")
    num_files = index.index_dir('data/')
    #print index._bt.formattree()
    print("indexed %d files" % num_files)
    
    #for term in ('hel*o', 'aggies', 'agg*', 'mike sherm*', 'dot cat','N*L','jann'):
    for term in ('football', 'mike', 'sherman', 'mike sherman', 'mike *man', 'wiki*', 'King', 'source http',
             'history coaches', 'elected', '1916', 'all*d powers wor*d war', 'w*d war',
             'Germany Austria U*S France'):
        print()
        or_results = index.wildcard_search_or(term)
        print("Or length ",len(or_results))
        print("OR  searching: %s -- results: %s" % (term, ", ".join(or_results)))
        and_results = index.wildcard_search_and(term)
        print("And length ",len(and_results))
        print("AND searching: %s -- results: %s" % (term, ", ".join(and_results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    start=time.time()
    import sys
    main(sys.argv)
    print("\nTotal Time taken : ",time.time()-start)
    

