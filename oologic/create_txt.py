import os

def writeToTXTFile(dir, fileName, data):
    filePathNameWExt = './' + dir + '/' + fileName + '.txt'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(filePathNameWExt, 'w') as fp:
        fp.write(data)
