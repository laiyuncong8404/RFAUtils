from BeautifulSoup import BeautifulSoup
import os
import re

#with open("a.txt") as f:
    #html_content=f.readlines()
#print type(html_content)



def parse_html_file(html_content, html_filename):
    soup = BeautifulSoup(''.join(html_content))
    t = soup.prettify()
    with open(html_filename,"w") as ff:
        ff.write(t)

parse_html_file(html_content,'my.html')
