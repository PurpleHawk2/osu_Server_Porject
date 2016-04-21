import requests
import time
import re

beatmapArchive = [[],[],[]]
newBeatmaps = [[],[],[]]

def requestCheck(request):

    #Set variables and define subText
    found = False
    start = request.text.find('topt')
    sub = request.text[start:]
    sub=sub[:sub.find('News')]

    #Compilation patterns
    song = re.compile('"> ([A-Z].+-[^<)]+)')
    picture = re.compile('src="//(.*/\d+\.jpg)')
    creator = re.compile('href="/u/\d+">(\w+)')

    #findall songs, creators and pictures
    currentSongs = song.findall(sub)
    currentCreator = creator.findall(sub)
    currentPictures = picture.findall(sub)

    for i in range(len(currentSongs)):
        if currentSongs[i] not in beatmapArchive[0] and currentCreator[i] not in beatmapArchive[1] and currentPictures[i] not in beatmapArchive[2]:
            beatmapArchive[0].append(currentSongs[i])
            beatmapArchive[1].append(currentCreator[i])
            beatmapArchive[2].append(currentPictures[i])
            newBeatmaps[0].append(currentSongs[i])
            newBeatmaps[1].append(currentCreator[i])
            newBeatmaps[2].append(currentPictures[i])
            found = True
    return found

def init():
    #print("hey!")
    f = open('osuBeatmapArchive.txt','r')
    content=f.read()
    contentPattern = re.compile('(.*)\n')
    data = contentPattern.findall(content)
    for d in data:
        if d == '':
            data.remove(d)
    for i in range(len(data)-1):
        beatmapArchive[i%3].append(data[i])
    f.close()

def main():
    init()
    while True:
        #print("hey2!")
        t0 = time.time()
        try:
          request = requests.get('http://osu.ppy.sh/',timeout=1)
        except Exception as e:
             print(e.message)
        print(time.time() - t0)
        time.sleep(1)
        #print("\n")
        if requestCheck(request):
            writeUpdate()


def writeUpdate():
    f = open('osuBeatmapArchive.txt','a')
    for i in range(len(newBeatmaps)-1):
        for itemType in newBeatmaps:
            f.write(itemType[i]+"\n")
            print(itemType[i])
        f.write("\n")
        print("\n")
    f.close()

main()