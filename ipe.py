import regex, re, sys, requests

print('''

 _____  _____  _______    _____  __   __
   |   |_____] |______   |_____]   \_/  
 __|__ |       |______ . |          |   
                                        
Instagram Picture Extractor
_________________________________________
''')

soup = requests.get(sys.argv[1]).text.encode('utf-8')
if "Page Not Found" in soup:
    quit("Error: Bad URL")
pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
imglist = []

print("Searching for images at: " + sys.argv[1])
for brackets in pattern.findall(str(soup)):
    if "src" in brackets:
        for match in re.finditer("src", brackets):
            begindex = match.end() + 3
            endex = brackets[begindex:-1].find("\"")
            imglist.append(brackets[begindex:begindex + endex])

print("Downloading images to " + sys.path[0])
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

