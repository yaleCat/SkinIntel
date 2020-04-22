import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.patches as mpatches
from skimage.io import imread
import scipy.ndimage as ndimage


def vis_box(img, response):
    fig,ax = plt.subplots(1,figsize=(10,10))
    ax.axis('off')
    handles = []
    ax.imshow(img)
    h,w,c = img.shape
    interval = h*0.04
    ax.text(1.02*w, h/3, 'Prediction with threshold:')
    for i,(region, pd) in enumerate(response['regions'].items()):
        color = color_map[region]
        text_color = 'red'
        score = pd['score']
        box = [int(b) for b in pd['box']]
        rect = patches.Rectangle((box[0],box[1]),box[2]-box[0],box[3]-box[1],linewidth=1,edgecolor=color,facecolor='none')
        ax.add_patch(rect)
        patch = mpatches.Patch(color=color, label='{} region - {}'.format(region,score))
        handles.append(patch)
        if score > threshold[region]:
            text_color = 'green'
        ax.text(1.02*w, h/3+(i+1)*interval, region+' wrinkle', bbox=dict(facecolor=text_color, alpha=0.5))
    ax.legend(handles=handles,bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    return ax

def merge_mask(img, response):
    height,width,channel = img.shape
    img = img / 255
    merge = np.zeros(img.shape)
    for i,(region, pd) in enumerate(response['regions'].items()):
        mask = np.array(pd['mask'])
        box = [int(b) for b in pd['box']]
        w = box[2]-box[0]
        h = box[3]-box[1]
        mask = cv2.resize(mask, (w, h))
        print(region, w,h,mask.shape)
        heatmap = cv2.applyColorMap(np.uint8(255*mask), cv2.COLORMAP_JET)
        heatmap = np.float32(heatmap) / 255
        merge[box[1]:box[3],box[0]:box[2]] += heatmap
    jet_rgb_low = cv2.applyColorMap(np.uint8([10]), cv2.COLORMAP_JET)[0][0] / 255
    merge[np.all(merge == (0,0,0), axis=-1)] = jet_rgb_low
    merge = ndimage.gaussian_filter(merge, sigma=(15, 15, 0), order=0)
    merge = merge + np.float32(img)
    merge = merge / np.max(merge)
#     merge = cv2.resize(merge, (height, width))
#     plt.imshow(merge[:,:,::-1])
#     plt.show()
    return merge[:,:,::-1]
    
def vis(im_url,response,save = False):
    if not response:
        print(im_url,response)
        return
    response = response.json()
    img = imread(im_url)
    img = merge_mask(img,response)
    ax = vis_box(img,response)
    if save:
        os.makedirs(os.path.join(os.path.dirname(img_path),'visualize'),exist_ok = True)
        plt.savefig(os.path.join(os.path.dirname(img_path),'visualize','{}_visualize.png'.format(img_path.split('/')[-1].split('.')[0])),bbox_inches='tight', pad_inches=0.5)
        plt.close()
        
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

    
    
