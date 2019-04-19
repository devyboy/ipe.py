#!/usr/bin/python
# -*- coding: utf-8 -*-

import regex, re, sys, requests
from bs4 import BeautifulSoup


def downloadImages(imglist):
    print("Downloading images to " + sys.path[0] + "...")
    for image in imglist:
        with open("Instagram_IMG_" + str(imglist.index(image)) + ".jpg", 'wb') as handle:
            response = requests.get(image, stream=True)
            if not response.ok:
                print response
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    print("Done")


def start():
    print('''
██████╗ ██╗ ██████╗   ██████╗ ██╗   ██╗
██╔══██╗██║██╔════╝   ██╔══██╗╚██╗ ██╔╝
██████╔╝██║██║        ██████╔╝ ╚████╔╝ 
██╔═══╝ ██║██║        ██╔═══╝   ╚██╔╝  
██║     ██║╚██████╗██╗██║        ██║   
╚═╝     ╚═╝ ╚═════╝╚═╝╚═╝        ╚═╝   

Python Integer Converter
_______________________________________                             
''')
    soup = BeautifulSoup(requests.get(sys.argv[1]).text, "html.parser")
    imglist = []

    if "twitter.com" in sys.argv[1]:
        if "Sorry, that page doesn't exist" in soup:
            quit("Error: Bad URL")
        div = soup.find("div", {"class": "AdaptiveMedia"})
        for img in div.find_all("img"):
            if not img in imglist:
                imglist.append(img["src"])
        downloadImages(imglist)
    elif "instagram.com" in sys.argv[1]:
        if "Page Not Found" in soup:
            quit("Error: Bad URL")
        pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
        print("Searching for images at: " + sys.argv[1])
        for brackets in pattern.findall(str(soup)):
            if "src" in brackets:
                for match in re.finditer("src", brackets):
                    begindex = match.end() + 3
                    endex = brackets[begindex:-1].find("\"")
                    imglist.append(brackets[begindex:begindex + endex])
        downloadImages(imglist)
    else:
        print("Error: Please enter a Twitter or Instagram post")

if __name__ == "__main__":
    start()
