# homework 1
# goal: tokenize, index, boolean query
# exports: 
#   student - a populated and instantiated ir4320.Student object
#   Index - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents


# ########################################
# first, create a student object
# ########################################

import cs525
import PorterStemmer
import glob, os
import re
import time

MY_NAME = "Sayed Inamdar"
MY_ANUM  = 637508815 # put your WPI numerical ID here
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


# ########################################
# now, write some code
# ########################################

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
class Index(object):
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._inverted_index = {}
        # _documents contains file names of documents
        self._documents = []
        # example:
        #   given the following documents:
        #     doc1 = "the dog ran"
        #     doc2 = "the cat slept"
        #   _documents = ['doc1', 'doc2']
        #   _inverted_index = {
        #      'the': [0,1],
        #      'dog': [0],
        #      'ran': [0],
        #      'cat': [1],
        #      'slept': [1]
        #      }


    # index_dir( base_path )
    # purpose: crawl through a nested directory of text files and generate an
    #   inverted index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
        num_files_indexed = 0
        # PUT YOUR CODE HERE
        files_in_path=[]
        curr_path=os.getcwd()
        os.chdir(base_path)
        for file in glob.glob("*.txt"):
            files_in_path.append(file)
            num_files_indexed+=1
        print("Number of files in the path are: "+str(num_files_indexed))
        
        ######For loop  ========================================================================
        for file in files_in_path:
            with open (file, "r",encoding="utf8") as myfile:
                data=myfile.read().replace('\n', ' ')
            tokens=self.tokenize(data)
            stemmed_tokens=self.stemming(tokens)
            
            #append documents to the documents list
            #self._documents.append(file)
            file=file[:-4]
            self._documents.append(file)
            
            ##insert token into inverted index
            for token in stemmed_tokens:
                if token in self._inverted_index:
                    token_list=self._inverted_index[token]
                    token_list.add(file)
                else:
                    self._inverted_index[token]=set([file])
        
        ###  end for loop=====================================================================================================
       
        
        os.chdir(curr_path)
        return num_files_indexed

    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self,text):
        tokens = []
        text=text.lower()
        # converting non-alphanumeric text to a whitespace
        text=re.sub('[^A-Za-z0-9]+',' ',text)
        for word in text.split():
            tokens.append(word)
        # PUT YOUR CODE HERE
        return tokens

    # purpose: convert a string of terms into a list of tokens.        
    # convert a list of tokens to a list of stemmed tokens,     
    # preconditions: tokenize a string of terms
    # returns: list of stemmed tokens
    # parameters:
    #   tokens - a list of tokens
    def stemming(self, tokens):
        stemmed_tokens = []
        p=PorterStemmer.PorterStemmer()
        for token in tokens:
            stemmed_tokens.append(p.stem(token,0,len(token)-1))
        return stemmed_tokens
    
    # boolean_search( text )
    # purpose: searches for the terms in "text" in our corpus using logical OR or logical AND. 
    # If "text" contains only single term, search it from the inverted index. If "text" contains three terms including "or" or "and", 
    # do OR or AND search depending on the second term ("or" or "and") in the "text".  
    # preconditions: _inverted_index and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def boolean_search(self, text):
        results = []
        tokens=[]
        
        ##Handles if there are beyond 3 terms in the input query
        ini_text=text.split()
        if(len(ini_text)>3):
            results.append("Beyond 3 words entered!")
            return results
        
        ##perform tokenization
        tok=self.tokenize(text)
        ## handle the 's
        if(len(tok)>3):
            tmp_tokens=tok
            boolean_keyword=tok[2]
            first_word=tok[0]
            last_word=tok[-2]
            tok=[]
            tok.append(first_word)
            tok.append(boolean_keyword)
            tok.append(last_word)
            
        
        ##handles stemming
        tokens=self.stemming(tok)
        
        
        ## single word retrieval
        if ( len(tokens)<3 ):
            if tokens[0] in self._inverted_index:
                file_list=self._inverted_index[tokens[0]]
                for fil in file_list:
                    results.append(fil+'.txt')
        
        #### Boolean retrieval done here
        elif(len(tokens)>2):
            first_list=[]
            second_list=[]
            
            if tokens[0] in self._inverted_index:
                file_list=self._inverted_index[tokens[0]]
                for fil in file_list:
                    first_list.append(fil)

            if tokens[2] in self._inverted_index:
                file_list=self._inverted_index[tokens[2]]
                for fil in file_list:
                    second_list.append(fil)
            
            first_list.sort()
            second_list.sort()
            
            if tokens[1].lower()=='or':
                final_set=set()
                for f in first_list:
                    final_set.add(f)
                for f in second_list:
                    final_set.add(f)
                
                for fin in final_set:
                    results.append(fin+'.txt')
                    
            elif tokens[1].lower()=='and':
                l1=0
                l2=0
                while l1!=len(first_list) and l2!=len(second_list):
                    if first_list[l1] == second_list[l2]:
                        results.append(first_list[l1]+'.txt')
                        l1+=1
                        l2+=1
                    elif int(first_list[l1] < second_list[l2]):
                        l1+=1
                    else:
                        l2+=1
                        
        # PUT YOUR CODE HERE
        if not results:
            results.append('Not Found')
        else:
            results.sort()
        return results
    

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = Index()
    print("starting indexer")
    num_files = index.index_dir('data/')
    print("indexed %d files" % num_files)
    for term in ('football', 'mike', 'sherman', 'mike OR sherman', 'mike AND sherman'):
        results = index.boolean_search(term)
        print("searching: %s -- results: %s" % (term, ", ".join(results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    start_time=time.time()
    import sys
    main(sys.argv)
    print("\nTime taken is %d",time.time()-start_time)
