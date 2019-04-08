import pprint
import re
from urllib.request import urlopen


# class NeedleStack:
#     def __init__(self,url,max_level=3):
#
#     def lookup(self,keyword):


# 1. Read the contents of a given URL and find all the links embedded in the page.
# Links are found inside anchor tags, for example <a href=”http://uvu.edu”>.
# The link here is the string “http://uvu.edu”.
# You need to scan the entire page’s contents and return all the links.
# Write a function, get_all_links, that takes a URL and returns a set (to ignore duplicates)
# containing all links on the page.
# Only keep links that begin with “http://…”.
# I suggest you use regular expressions to extract the links for this assignment. 


def get_all_links(scrapeSite):
    html = urlopen(scrapeSite)
    htmlbytes = html.read()
    html_str = htmlbytes.decode("utf8")
    html.close()
    urlset = set(
        re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', html_str))
    return urlset


# The heart of the search engine is the web crawler. You pass a starting URL to seed this
# function and it visits every link on the page, and in turn visits every link on every linked page,
# and so on. It returns two important dictionaries:
#
# a) An index that maps every word encountered on each crawled page to a list of URLs of
# all the pages that contain that word. Only keep words consisting of alphanumeric
# characters and underscores. Convert all words to lower case. Only consider text that is
# found outside of HTML tags.
#
# b) A graph that maps every URL encountered to a list of the web pages it links to directly.
# (This will be used subsequently for ranking web pages by “popularity”.)


def crawl(seed, max_level):
    tocrawl = [seed]
    crawled = []
    visited = 0
    word_dict = dict()
    graph = dict()

    while tocrawl and visited < max_level:
        crawlingURL = tocrawl[0]
        if len(tocrawl) == 0:
            break

        html = urlopen(crawlingURL)
        htmlbytes = html.read()
        html_str = htmlbytes.decode("utf8")
        html.close()
        text_str = re.sub('<[^<]+?>', '', html_str)
        text_str = re.sub('[^\w\s]', '', text_str)
        split_str = text_str.split()

        for x in split_str:
            lowercase = x.lower()
            try:
                if word_dict[lowercase].__contains__(crawlingURL):
                    pass
                else:
                    word_dict[lowercase].append(crawlingURL)
            except KeyError:
                word_dict[lowercase] = [crawlingURL]

        while split_str:
            split_str.pop()

        links = get_all_links(crawlingURL)

        for value in links:
            if value in tocrawl or value in crawled:
                pass
            else:
                tocrawl.append(value)
            try:
                graph[crawlingURL].append(value)
            except KeyError:
                graph[crawlingURL] = [value]

        tocrawl.remove(crawlingURL)
        crawled.append(crawlingURL)
        visited += 1

    return word_dict, graph


# 3. The next function, I will give you. It takes the graph created by crawl and returns a dictionary, ranks,
# that maps each url in the graph to its relative rank.
# You will call this in the function after you have finished crawling.
# This is the foundation of the algorithm Google uses for ranking pages.
# If you would like to know more about it, visit http://en.wikipedia.org/wiki/PageRank.


def compute_ranks(graph):
    d = 0.85     # probability that surfer will bail
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for url in graph:
                if page in graph[url]:  # this url links to “page”
                    newrank += d*ranks[url]/len(graph[url])
            newranks[page] = newrank
        ranks = newranks
    return ranks

# 4. Write a function, lookup(keyword), (which uses ranks) to return all the web pages in your index that
# contain a particular word, sorted in descending order by their page rank (but don’t display the page rank).
# Include no duplicates in your url results.


def lookup(keyword):
    keyword = keyword.lower()
    link_list = list()
    word_dict, graph = (crawl("http://freshsources.com/page1.html", 5))
    for links in word_dict.get(keyword):
        link_list.append(links)
    ranks1 = compute_ranks(graph)

    link_list.sort(key = lambda x: ranks1[x], reverse=True)
    print(link_list)




# Here is a sample main to use:


if __name__ == '__main__':
    # print('index:')
    # word_dict, graph = (crawl("http://freshsources.com/page1.html", 5))
    # pprint.pprint(word_dict)
    # pprint.pprint(graph)
    # pprint.pprint(compute_ranks(graph))
    lookup("pages")
    lookup("links")
    lookup("you")
    lookup("have")
    lookup("I")

