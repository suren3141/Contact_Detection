import cv2
import argparse
import os

# Construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-ext", "--extension", required=False, default='png', help="extension name. default is 'png'.")
# ap.add_argument("-o", "--output", required=False, default='output.mp4', help="output video file")
# args = vars(ap.parse_args())

# Arguments
dir_path = 'viz_predictions/handshake3'
ext = 'jpg'
output = 'handshake3_1.mp4'
# ext = args['extension']
# output = args['output']

images = []
for f in os.listdir(dir_path):
    if f.endswith(ext):
        images.append(f)

images = sorted(images, key=lambda x:int(x[0:-4]))
save_path = 'results/'
# Determine the width and height from the first image
image_path = os.path.join(dir_path, images[0])

frame = cv2.imread(image_path)
# cv2.imshow('video',frame)
height, width, channels = frame.shape

#Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
out = cv2.VideoWriter(save_path+output, fourcc, 10,(width, height))

for image in images:

    image_path = os.path.join(dir_path, image)
    frame = cv2.imread(image_path)

    out.write(frame) # Write out frame to video

    cv2.imshow('video',frame)
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break

#Release everything if job is finished
out.release()
cv2.destroyAllWindows()

print("The output video is {}".format(output))