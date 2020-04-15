import os
import cv2
import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.patches as mpatches
from skimage.io import imread


def vis(im_url,response):
    response = response.json()
    print(response)
    if 'wrinkle' not in response:
        print('No Response')
        return
    fig,ax = plt.subplots(1,figsize=(10,10))
    ax.axis('off')
    handles = []
    img = imread(im_url)
    print('image shape',img.shape)
    ax.imshow(img)
    h,w,c = img.shape
    interval = h*0.06
    ax.text(1.02*w, h/3, 'Prediction with threshold:')
    for i,(region, pd) in enumerate(response['debug'].items()):
        color = color_map[region]
        text_color = 'red'
        score = pd['score']
        box = [int(b) for b in pd['box'].split(',')]
        rect = patches.Rectangle((box[0],box[1]),box[2]-box[0],box[3]-box[1],linewidth=1,edgecolor=color,facecolor='none')
        ax.add_patch(rect)
        patch = mpatches.Patch(color=color, label='{} region - {}'.format(region,score))
        handles.append(patch)
        if score > threshold[region]:
            text_color = 'green'
        ax.text(1.02*w, h/3+(i+1)*interval, region+' wrinkle', bbox=dict(facecolor=text_color, alpha=0.5))
    plt.legend(handles=handles,bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    plt.show()
        
color_map = {
    'forehead':'red',
    'frown':'green',
    'left_cheek':'blue',
    'right_cheek':'blue',
    'urchin':'orange'
}

threshold = {
    'forehead':0.35,
    'frown':0.76,
    'left_cheek':0.70,
    'right_cheek':0.58,
    'urchin':0.36
    }

    
    
