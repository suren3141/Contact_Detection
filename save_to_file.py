# Saves a list of images into a text file with its path

import os
import argparse


def save_to_file(text):

    with open('imagelist.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(text))
        myfile.write('\n')


ap = argparse.ArgumentParser()
ap.add_argument("-dir", "--directory", required=False, help="directory path to image list text file")
ap.add_argument("-ext", "--extension", required=False, default='jpg', help="extension name. default is 'png'.")
args = vars(ap.parse_args())

dir_path = args['directory']
ext = args['extension']
# dir_path = 'viz_predictions/dance-twirl'
# ext = 'jpg'

images = []
image_path = []
for f in os.listdir(dir_path):
    if f.endswith(ext):
        images.append(f)

images = sorted(images, key=lambda x: int(x[0:-4]))

for image in images:
    image_path.append(os.path.join(dir_path, image))

save_to_file(image_path)