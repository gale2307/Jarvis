from bs4 import BeautifulSoup
from collections import deque
import os.path
import requests
import time

def urltofilename(url):
    filename = url.replace("://", "_").replace(".", "_").replace("/", "_").replace(":", "_").replace("%", "_")
    filename = filename + ".txt"
    return filename

def craftingrecipe(tag):
    #class="invslot animated" <-- animated frame
    #class="invslot" <-- normal frame
    #class="animated-subframe animated-active" / class="animated-subframe" <-- loop through different types of same ingredient
    #class="invslot-item animated-active" <-- first item in loop
    #get title in tags 'a'
    #class="mcui-output" <-- crafting output
    hlist = list()
    rlist = list(list())
    rcounter = -1 #account for header

    for row in tag.find_all("tr"):
        if rcounter < 0:
            for header in row.find_all("th"):
                hlist.append(str(''.join(header.findAll(text=True))))
        else:
            rlist.append(list())

            recipelist = list(list())
            resultlist = list()

            for col in row.find_all("td"):
                if col.has_attr("style"):
                    for span in col.find_all("span"):
                        tmp = list()                                                #List of ingredients for a single frame
                        if ''.join(span["class"]) == "invslot":                     #INGREDIENT
                            sprite = span.find_all("span", class_= "sprite inv-sprite")
                            if not(sprite):
                                sprite = span.find_all("a")
                            if not(sprite):
                                tmp.append("empty")
                            else:
                                for item in sprite:
                                    tmp.append(str(item["title"]))
                            recipelist.append(tmp)

                        elif ''.join(span["class"]) == "invslotanimated":          #LOOPING INGREDIENT
                            for item in span.find_all("span"):
                                if "animated-subframe" in ''.join(item["class"]):   #SIMILAR ITEM IN LOOPING INGREDIENT
                                    for sprite in item.find_all("span", class_ = "sprite inv-sprite"):
                                        tmp.append(str(sprite["title"]))
                                        break
                                    for x in item.find_all("span"):
                                        x["class"] = "done"
                                elif "invslot-item" in ''.join(item["class"]):
                                    for sprite in item.find_all("span", class_ = "sprite inv-sprite"):
                                        tmp.append(str(sprite["title"]))
                            #print(tmp)
                            recipelist.append(tmp)

                        elif ''.join(span["class"]) == "mcui-output":               #RECIPE OUTPUT
                            for item in span.find_all("span", class_ = "sprite inv-sprite"):
                                resultlist.append(str(item["title"]))

                    if len(recipelist)>=9:
                        recipe = ""
                        for i in range(len(resultlist)):
                            recipe += "The crafting recipe for " + resultlist[i] + " is"
                            for j in range(9):
                                if len(recipelist[j])>0:
                                    recipe += " " + recipelist[j][i % len(recipelist[j])] + ","
                            recipe = recipe[:-1] + ".\n"
                        rlist[rcounter].append(recipe)

                #else:
                    #rlist[rcounter].append(str(''.join(col.findAll(text=True))))

        rcounter += 1


    #for x in hlist:
    #    print(x)

    text = ""
    for lists in rlist:
        for x in lists:
            #print(x)
            text += x

    return text

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

if not os.path.exists("MinecraftWiki"):
    os.mkdir("MinecraftWiki")

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
    for tag in soup.find_all(["p", "table"]):
        if tag.name == "table":
            if tag.has_attr('data-description'):
                if tag['data-description'] == "Crafting recipes":
                    my_str = my_str + craftingrecipe(tag)
        else:
            my_str = my_str + str(''.join(tag.findAll(text=True)))
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