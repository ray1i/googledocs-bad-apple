from PIL import Image
import cv2
import os

#"▖▗▘▙▚▛▜▝▞▟	▌▐▀▄"
#chars = " !?@#"

def convertimagefromurl(imageurl):
    chars = " ░▒▓█"
    m = int(255/4)

    image = Image.open(imageurl).convert('L')
    image = image.resize((80, 30))
    imagelist = list(image.getdata())

    res = ''

    for i in range(len(imagelist)):
        if i%80 == 0:
            res += '\n'
        res += chars[round(imagelist[i]/m)]

    return res

def convertimage(image):
    chars = "█▓▒░ "
    m = int(255/4)

    image = image.convert('L')
    image = image.resize((80, 30))
    imagelist = list(image.getdata())

    res = ''

    for i in range(len(imagelist)):
        if i%80 == 0:
            res += '\n'
        res += chars[round(imagelist[i]/m)]

    return res

def getframes(vidurl, fps):
    vid = cv2.VideoCapture(vidurl)
    frames = []
    curr = 0
    print('converting frames...')

    while True:
        ret, frame = vid.read()
        if ret:
            if curr % (30/fps) == 0:
                frames.append(convertimage(Image.fromarray(frame)))
        else:
            print('done.')
            break
        curr += 1

    vid.release()
    cv2.destroyAllWindows()

    return frames

'''
    image = Image.open('testimage.png').convert('L')
    image = image.resize((80, 30))
    imagelist = list(image.getdata())

    f = open('test.txt', 'w')
    f.write('')
    f.close()

    f = open('test.txt', 'a', encoding='utf-8')

    for i in range(len(imagelist)):
        if i%80 == 0:
            f.write('\n')
        f.write(chars[round(imagelist[i]/m)])

    f.close()
'''
