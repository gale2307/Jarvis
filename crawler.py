import requests
from bs4 import BeautifulSoup
from collections import deque
import time

def urltofilename(url):
    filename = url.replace("://", "_").replace(".", "_").replace("/", "_").replace(":", "_").replace("%", "_")
    filename = filename + ".txt"
    return filename

wiki_url = 'https://minecraft.gamepedia.com'
my_url = 'https://minecraft.gamepedia.com/minecraft_wiki'

stacked_url = set()
stacked_url.add(my_url)
url_list = deque()
url_list.append(my_url)#initialize stack

#URL keywords to skip
banlist = ["?", "#", "/special:", "/template:", "/module:", "/user:", "talk", "/category:", "list_of_gamepedia_staff", "list_of_administrators", "/file:", "/minecraft_dungeons:"]

#uncomment all lines with fo to get the list of websites traversed in websites.txt
#fo = open("websites.txt", "a")

while url_list:
    cur_url = url_list.popleft()

    print(cur_url)
    print("URLs left: " + str(len(url_list)))

    try:
        r = requests.get(cur_url, timeout=5)
    except requests.exceptions.ConnectionError:
        url_list.append(cur_url)
        continue
    except requests.exceptions.Timeout:
        url_list.append(cur_url)
        continue
    except requests.exceptions.TooManyRedirects:
        continue
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    print("code: " + str(r.status_code))
    #if bad status skip URL
    if not(r.status_code == requests.codes.ok): 
        time.sleep(1)
        continue
    html_text = r.text
    soup = BeautifulSoup(html_text, 'html.parser')
    #index the URL (probably can be improved)
    my_str = ""
    for node in soup.findAll('p'):
        my_str = my_str + str(''.join(node.findAll(text=True)))
        #if tag.name == li:         #how to relate it to previous text?
        #   my_str = my_str + '\n'

    if not(my_str == ""):
        with open("MinecraftWiki/" + urltofilename(cur_url), "w", encoding='utf-8') as file:
            file.write(my_str)

    for link in soup.find_all('a'):
        new_url = str(link.get('href'))
        if new_url[0] == '/':
            if new_url[1] != '/':
                ban = False
                for sample in banlist:
                    if sample in new_url.lower():
                        ban = True
                        break
                if not(ban):
                    new_url = wiki_url+new_url
                    if not(new_url.lower() in stacked_url):
                        stacked_url.add(new_url.lower())
                        url_list.append(new_url)
                        #fo.write(new_url + '\n')

#fo.close()