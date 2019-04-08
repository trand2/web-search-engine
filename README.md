# web-search-engine
Simple Web Search Engine

This assignment will walk you through the creation of a simple web search engine in Python. The final output will be a class, NeedleStack.

First, start with some simple functions, which you will later make methods of the NeedleStack class. Having you do these one at a time will lead you through the project.

1. Read the contents of a given URL and find all the links embedded in the page. Links are found inside anchor tags, for example <a href=”http://uvu.edu”>. The link here is the string “http://uvu.edu”. You need to scan the entire page’s contents and return all the links. Write a function, get_all_links, that takes a URL and returns a set (to ignore duplicates) containing all links on the page. Only keep links that begin with “http://…”. I suggest you use regular expressions to extract the links for this assignment.

2. The heart of the search engine is the web crawler. You pass a starting URL to seed this function and it visits every link on the page, and in turn visits every link on every linked page, and so on. It returns two important dictionaries: 

a) An index that maps every word encountered on each crawled page to a list of URLs of all the pages that contain that word. Only keep words consisting of alphanumeric characters and underscores. Convert all words to lower case. Only consider text that is found outside of HTML tags.

b) A graph that maps every URL encountered to a list of the web pages it links to directly. (This will be used subsequently for ranking web pages by “popularity”.)
Searching all the pages that are reachable from a given URL can be a very lengthy process. To make this assignment not take days to execute, we will pass a second parameter, an integer named max_level, that will only search pages that are max_level levels away from the seed page. For example, the call crawl(‘http://uvu.edu’,0) will search no pages beyond the seed page, and will therefore return only the links directly embedded in uvu.edu. A level of 1 would also record the contents of the pages linked to by uvu.edu, but stop there. Write crawl(seed,max_level). (Mine is only 10 lines of code.)

3. The next function, I will give you. It takes the graph created by crawl and returns a dictionary, ranks, that maps each url in the graph to its relative rank. You will call this in the function after you have finished crawling. This is the foundation of the algorithm Google uses for ranking pages. If you would like to know more about it, visit http://en.wikipedia.org/wiki/PageRank.

4. Write a function, lookup(keyword), (which uses ranks) to return all the web pages in your index that contain a particular word, sorted in descending order by their page rank (but don’t display the page rank). Include no duplicates in your url results.

5. Now that you’ve written all the functions above, create the NeedleStack class with the following “public” interface.The NeedleStack constructor takes the seed URL, and the optional maximum search level (defaulted to 3), and creates the index, graph, and ranks dictionaries, which become attributes of a NeedleStack instance. All the rest of the functions you wrote earlier become NeedleStack methods, some static, some non-static. You only need to come up with about 40 lines of code on your own for this assignment.

I have set up a test web site for you at http://freshsources.com/page1.html. There are 5 pages there. Here is a sample main to use:
```python
if __name__ == '__main__':
    engine = NeedleStack('http://freshsources.com/page1.html',5)
    for w in ['pages','links','you','have','I']:
        print(w,'\n',engine.lookup(w))
    print()
    print('index:')
    pprint.pprint(engine.index)
    print()
    print('graph:',engine.graph)
    print()
    print('ranks:',engine.ranks)
```
The expected output appears in the file [needle.txt](http://universe.tc.uvu.edu/cs3270/project/Hw7/needle.txt).

Do not use Beautiful Soup, Scrapy, or anything like them. Use urllib.request or requests.

Notes:
Make sure that when your file is imported as a module, no code executes other than the class definition (and import statements).
