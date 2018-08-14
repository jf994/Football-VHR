import json
import os, sys

def writeToJSONFile(dir, fileName, data):
    filePathNameWExt = './' + dir + '/' + fileName + '.json'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)
