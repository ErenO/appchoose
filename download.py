import os
import re
import urllib
import urllib.request
import urllib.parse
from PIL import Image
from resizeimage import resizeimage

d_str = {"-": "_",
         " ": "_",
         "'": "",
         ".": "",
         "?": "",
         "!": "",
         "%20": "_"}

def resize_img(imgpath, target_size = 224):
    
        try:
            with open(imgpath, 'r+b') as f:
                with Image.open(f) as img:
                    img = resizeimage.resize_cover(img, [target_size, target_size])
                    img.save(imgpath, img.format)
        except: 
            os.remove(imgpath)
            print("Impossible to resize file {0}. Deleting file...".format(imgpath))
            
def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

def extract_filepath(source, 
                     aws = 'https://s3.amazonaws.com/crawler.appchoose.io/img/'):
    imgpath = urllib.parse.unquote(source['img'].replace(aws, ''))
    brd = replace(imgpath.split("/")[0].lower(), d_str)
    filename = imgpath.split("/")[-1]
    return([brd, filename])
    
def img_downloader(source, 
                   target_dir, 
                   aws = 'https://s3.amazonaws.com/crawler.appchoose.io/img/',
                   target_size = 224):
    filepath = extract_filepath(source = source, aws = aws)
    
    if not os.path.exists('/'.join([target_dir, filepath[0]])):
        os.makedirs('/'.join([target_dir, filepath[0]]))
    
    if not os.path.exists('/'.join([target_dir, filepath[0], filepath[1]])):
        if 'img' in source:
            try:
                urllib.request.urlretrieve(source['img'], '/'.join([target_dir, filepath[0], filepath[1]]))
            except:
                0
                
    if os.path.exists('/'.join([target_dir, filepath[0], filepath[1]])):
        resize_img('/'.join([target_dir, filepath[0], filepath[1]]), target_size = target_size)