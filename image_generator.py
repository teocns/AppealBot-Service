from PIL import Image, ImageDraw, ImageFilter
import numpy
import glob
import math
from random import randrange
import os
import random
import time
import re
import sys
import argparse
from io import BytesIO
import base64
import pprint

import requests
from requests.auth import HTTPBasicAuth
import shutil

from urllib.request import urlopen, urlretrieve



def generate(code, fullname, username,coordinates, PIL_boilerplate_image):
    # try:

    jobs = []
    rqig_pic = 39
    rqig_id = code
    rqig_name = fullname
    rqig_user = username

    jobs.append([rqig_id, rqig_name, rqig_user, rqig_pic])

    def find_coeffs(pa, pb):
            matrix = []
            for p1, p2 in zip(pa, pb):
                matrix.append([p1[0], p1[1], 1, 0, 0, 0, -
                            p2[0]*p1[0], -p2[0]*p1[1]])
                matrix.append([0, 0, 0, p1[0], p1[1], 1, -
                            p2[1]*p1[0], -p2[1]*p1[1]])

            A = numpy.matrix(matrix, dtype=numpy.float)
            B = numpy.array(pb).reshape(8)

            res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
            return numpy.array(res).reshape(8)

    def autocrop_image(image, border=0):
        # Get the bounding box
        bbox = image.getbbox()
        # Crop the image to the contents of the bounding box
        image = image.crop(bbox)
        # Determine the width and height of the cropped image
        (width, height) = image.size
        # Add border
        width += border * 2
        height += border * 2
        # Create a new image object for the output image
        cropped_image = Image.new(
            "RGBA", (width, height), (0, 0, 0, 0))
        # Paste the cropped image onto the new image
        cropped_image.paste(image, (border, border))
        # Done!
        return cropped_image

    
    
    rqig_user = str(rqig_user.replace('_', ''))
    

    # TODO rqig_email_id = job[3]
    # TODO rqig_inbox = job[4]

    # print("processing @"+str(rqig_user))

    f = urlopen("https://handwriting.io/demo")
    source = f.read().decode('utf-8')

    match = re.search(r'\"key\"\: \"(.*?)\"', source)
    key1 = match.group(1)

    match = re.search(r'\"secret\"\: \"(.*?)\"', source)
    key2 = match.group(1)
    
    
    handwriting_ids_random = ['5WGWVXYR00WR','8X3WP84R009Z','8X3WNN2G0099']
    
    rqHandwriting = random.choice(handwriting_ids_random)
    rqHandwritingSize = '100px'
    
    hex_random_array = ['1c1c1b']
    
    rqHandwritingColor = '%23'+random.choice(hex_random_array)
    rqRandomSeed = str(random.randint(1, 9999999))

    charNewLine = '%0A'
    charMention = '%40'
    
    url = 'handwriting_id='+rqHandwriting+'&text='+rqig_id+charNewLine+rqig_name+charNewLine+charMention+rqig_user + \
        '&handwriting_size='+rqHandwritingSize+'&handwriting_color=' + \
        rqHandwritingColor+'&width=auto&height=auto&random_seed='+rqRandomSeed
    time.sleep(5)

    response = requests.get(
        "https://api.handwriting.io/render/png?"+url, auth=HTTPBasicAuth(key1, key2), stream=True)
    
    
    buffer_save_png = BytesIO()
    shutil.copyfileobj(response.raw, buffer_save_png)
    # with open('save.png', 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)

    """url_auth = "https://"+key1+":"+key2+"@api.handwriting.io/render/png?"+url
    print(url_auth)
    urlretrieve (url_auth, 'save.png')"""
    
    # Separate RGB arrays
    im = Image.open(buffer_save_png)
    R, G, B, A = im.convert('RGBA').split()
    r = R.load()
    g = G.load()
    b = B.load()
    a = A.load()
    w, h = im.size

    # Convert non-black pixels to white
    for i in range(w):
        for j in range(h):
            # and a[i, j] != 0 :
            if (r[i, j] > 110 or g[i, j] > 110 or b[i, j] > 110):
                r[i, j] = 0  # Just change R channel
                g[i, j] = 0
                b[i, j] = 0
                a[i, j] = 0

    # Merge just the R channel as all channels
    im = Image.merge('RGBA', (R, G, B, A))
    #im.save("black_and_white.png")

    #image = Image.open('black_and_white.png')
    ready = autocrop_image(im)

    #ready.save("black_and_white-fixed.png")


    

    arr = coordinates.split('-')

    # extract idId
    
    # ig_id = arr0[1]

    # extract scalingFactor
    
    
    scalingFactor = 60
    # scalingFactor = 0.9 # scalingFactor / 100.0 # 100 w/o .0 will result in 0
    scalingFactor = scalingFactor / 100.0
    # print("scaling factor: "+str(scalingFactor))

    # extract coords and multiple by scalingFactor
    
    arr = [x for x in arr if x]
    x1 = int(float(arr[0]))
    y1 = int(float(arr[1]))
    x2 = int(float(arr[2]))
    y2 = int(float(arr[3]))
    x3 = int(float(arr[4]))
    y3 = int(float(arr[5]))
    x4 = int(float(arr[6]))
    y4 = int(float(arr[7]))

    # tmpTuple = [x1, y1, x4, y4, x3, y3, x2, y2]

    x2x1 = (x2 - x1)
    x4x3 = (x3 - x4)
    y4y1 = (y4 - y1)
    y3y2 = (y3 - y2)

    x1 = int(x1 + x2x1 * (1 - scalingFactor) / 2.0)
    x2 = int(x2 - x2x1 * (1 - scalingFactor) / 2.0)
    x3 = int(x3 - x4x3 * (1 - scalingFactor) / 2.0)
    x4 = int(x4 + x4x3 * (1 - scalingFactor) / 2.0)
    y1 = int(y1 + y4y1 * (1 - scalingFactor) / 2.0)
    y2 = int(y2 + y3y2 * (1 - scalingFactor) / 2.0)
    y3 = int(y3 - y3y2 * (1 - scalingFactor) / 2.0)
    y4 = int(y4 - y4y1 * (1 - scalingFactor) / 2.0)

    # print(x1,y1,x2,y2,x3,y3,x4,y4)

    selfie = PIL_boilerplate_image

    
    handwriting = ready
    handwriting = handwriting.filter(
        ImageFilter.GaussianBlur(radius=2)
    )
    handwriting_width, handwriting_height = handwriting.size

    selfie_width, selfie_height = selfie.size

    coeffs = find_coeffs(
        [(x1, y1), (x2, y2), (x3, y3), (x4, y4)],
        [(0, 0), (handwriting_width, 0), (handwriting_width, handwriting_height), (0, handwriting_height)])

    newhandwriting = handwriting.transform(
        (selfie_width, selfie_height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    # newhandwriting = handwriting.transform((selfie_width, selfie_height), Image.QUAD, tmpTuple, Image.BICUBIC)

    selfie.paste(newhandwriting, (0, 0), newhandwriting)

    # Generate random filename
    #filename = str(randrange(123567,999999))+"_"+str(randrange(123567,999999))+"_"+str(randrange(123567,999999))+".jpg"
    
    buffered = BytesIO()
    selfie.save(buffered, quality=70, format="JPEG")
    
    #selfie.save("C:\\Users\\Teo\\Documents\\GitHub\\AppealBot-Service\\TESTS\\"+str(time.time())+".jpeg", quality=75, format="JPEG")
    return base64.b64encode(buffered.getvalue())
    #selfie.show()
    #return img_str
    # Save image
    #selfie.save(filename, quality=100)
    # Move saved file to directory
    #os.rename(filename,r'generated/'+filename)
    #return r'generated/'+filename
    
    # TODO cur.execute("UPDATE emails SET file_path = %(file)s WHERE inbox = %(inbox)s", { 'file':outFile, 'inbox':rqig_inbox })

    # update db
    # cur.execute("UPDATE accounts SET state = 'picture-rendered' WHERE unban_id = %(id)s", { 'id':rqig_id })
    # print("database updated")
    
    # except:
    #     return False
