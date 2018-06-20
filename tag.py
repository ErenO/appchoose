from appchoose import download
import os
import re
import webcolors

def simplify_color(color, color_dict):
    if color in color_dict:
        return color_dict[color]
    else:
        return color
    
def correct_tag(x, tag_dict):
    if x in tag_dict:
        return tag_dict[x]
    else:
        return x

def get_category(source):
    if 'catText' in source:
        cat = source['catText'].lower().split(" ")[0]
    return cat
    
def get_gender(source):
    if 'cat' in source:
        gender = source['cat'].lower().split("-")[-1]
    return gender
    
def get_colors(source):
    if 'color' in source:
        clr = source['color'].lower().split("/")
    return clr

def parse_color(clr, exp):
    try:
        x = clr
        webcolors.name_to_rgb(x)
    except:
        try:
            x = clr.replace(" ", "")
            webcolors.name_to_rgb(x)
        except:
            try:
                x = re.search(exp, clr).group()
            except:
                x = None
    return x
            
def tag_image(source, categories, exp, color_dict, tag_dict, target_dir):
    img_labels = []
    try:
        img_labels.append(get_gender(source))
    except:
        None
    try:
        cat = get_category(source)
        img_labels.append(correct_tag(cat, tag_dict))
    except:
        try:
            cat = get_category(source['doc'])
            img_labels.append(correct_tag(cat, tag_dict))
        except:
            None
    try: 
        clr = get_colors(source)
        for c in clr:
            res = parse_color(c, exp)
            if res is not None:
                img_labels.append(simplify_color(res, color_dict))
    except:
        None
    if cat in categories:
        return img_labels
    else:
        return []