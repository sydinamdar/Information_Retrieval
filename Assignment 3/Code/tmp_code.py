# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:07:15 2019

@author: Sayed Inamdar
"""

def __init__(self):
    # you'll want to create something here to hold your index, and other
    # necessary data members
    frontier_list=[]
    tmp_frontier=[]
    base_url_list=''
    frontier_graph=dict()
    
    
# index_url( url )
# purpose: crawl through a web directory of html files and generate an
#   index of the contents
# preconditions: none
# returns: num of documents indexed
# hint: use BeautifulSoup and urllib
# parameters:
#   url - a string containing a url to begin indexing at

def get_last_index_of_url(url):
    base_url=url
    last_part_of_index=base_url.rfind('/')
    return last_part_of_index

def crawl_webpage(url):
    data=requests.get(url)
    soup_data=BeautifulSoup(data.text,'html.parser')
    temporary_frontier=soup_data.find_all('a')
    page_anchor_list=[]
    
    for alist in temporary_frontier:
        page_anchor_list.append(alist.get('href'))
    
    ##make the graph
    #last_part_url_index=get_last_index_of_url(url)
    #frontier_graph[url[last_part_url_index+1:]]=page_anchor_list
    
    for li in page_anchor_list:
        if li not in frontier_list:
            frontier_list.append(li)
            tmp_frontier.append(li)
    
    #make the graph now
    page_anchor_list_indexes=[]
    for i in page_anchor_list:
        page_anchor_list_indexes.append(frontier_list.index(i))
        
    last_part_url_index=get_last_index_of_url(url)
    frontier_graph[frontier_list.index(url[last_part_url_index+1:])]=page_anchor_list_indexes
    

def index_url(self, url):
    #initial crawling
    last_part_url_index=get_last_index_of_url(url)
    base_url=url[:last_part_url_index]
    
    frontier_list.append(url[last_part_url_index+1:])
    crawl_webpage(url)
    
    #traverse recursively and form the final set of all the pages
    while(tmp_frontier):
        tmp_url=tmp_frontier.pop()
        crawl_webpage(base_url+'/'+tmp_url)
    
    return 0