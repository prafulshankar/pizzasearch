from bs4 import BeautifulSoup
from text_formatting import *

def is_tag_type(object):
    return str(type(object)) == "<class 'bs4.element.Tag'>"

def concat(string_list):
    while(len(string_list) > 1):
        first = string_list[0]
        second = string_list[1]
        first.replace_with(first + second)
        string_list.pop(1)

# Removes the tag from a non-nested tag
def format_unicode_html(unicode_string):
    try:
        bullet = u"\u2022"
        soup = BeautifulSoup(unicode_string, "html.parser")
        hyperlinks = []
        while(len(soup.find_all()) > 0):
            tag = soup.find_all()[-1]
            concat(tag.contents)
            if(str(tag.name) == "b"):
                old_string = tag.string
                new_string = bold(old_string)
                tag.replace_with(new_string)
            elif(str(tag.name) == "strong"):
                old_string = tag.string
                new_string = bold(old_string)
                tag.replace_with(new_string)
            elif(str(tag.name) == "a"):
                url = str(tag['href'])
                display_name = cyan(str(tag.string))
                entry = display_name + ": " + url
                hyperlinks.append(entry)
    
                del tag['href']
                old_string = tag.string
                new_string = cyan(old_string)
                tag.replace_with(new_string)
            elif(str(tag.name) == "li"):
                old_string = tag.string
                new_string = "    " + bullet + " " + old_string + "\n"
                tag.replace_with(new_string)
            elif(str(tag.name) == "code" or str(tag.name) == "pre"):
                old_string = tag.string
                new_string = blue(old_string)
                tag.replace_with(new_string)
            else:
                tag.unwrap()
    
        post = str(soup)
        #if (hyperlinks): 
        #    post += "\n\n"
        #    post += "Hyperlinks\n"
        #    post += "==========\n"
        #    for link in hyperlinks:
        #        post += link + "\n"
    
        return post
    except:
        return unicode_string.encode('ascii', 'ignore')
