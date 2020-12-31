# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
import numpy as np
from sys import platform
import argparse
import matplotlib.pyplot as plt

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        # sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        sys.path.append('/Users/jhassan/Documents/PycharmProjects/GaitAnalysis/pose_estimation')
        from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="pose_estimation/images/COCO_val2014_000000000241.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()


    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "/Users/jhassan/Documents/PycharmProjects/GaitAnalysis/pose_estimation/models/"
    params["face"] = False
    params["hand"] = True

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(args[0].image_path)
    datum.cvInputData = imageToProcess

    # if imageToProcess.shape[1] > 2160 or imageToProcess.shape[0] > 2160:
    #     scale_percent = 20  # percent of original size
    #     width = int(imageToProcess.shape[1] * scale_percent / 100)
    #     height = int(imageToProcess.shape[0] * scale_percent / 100)
    #     dim = (width, height)
    # elif imageToProcess.shape[1] > 920 or imageToProcess.shape[0] > 920:
    #     scale_percent = 70  # percent of original size
    #     width = int(imageToProcess.shape[1] * scale_percent / 100)
    #     height = int(imageToProcess.shape[0] * scale_percent / 100)
    #     dim = (width, height)
    # else:
    #     dim = (imageToProcess.shape[1], imageToProcess.shape[0])
    #
    # img = cv2.resize(imageToProcess, dim)
    # datum.cvInputData = img

    opWrapper.emplaceAndPop([datum])

    print(np.array(datum.handKeypoints).shape)
    # print(np.array(datum.poseKeypoints))
    # print(datum.cvOutputData.shape)

    # Display Image
    # print("Body keypoints: \n" + str(datum.poseKeypoints))
    # print("Face keypoints: \n" + str(datum.faceKeypoints))
    # print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
    # print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
    # cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", datum.cvOutputData)
    # cv2.waitKey(0)

    plt.figure()
    plt.imshow(cv2.cvtColor(imageToProcess, cv2.COLOR_BGR2RGB))

    num_ppl = np.array(datum.handKeypoints).shape[1]

    for pers in range(0, num_ppl):
        plt.scatter(datum.handKeypoints[1][pers][:, 0], datum.handKeypoints[1][pers][:, 1], s=2, c='cyan')
        plt.scatter(datum.handKeypoints[0][pers][:, 0], datum.handKeypoints[0][pers][:, 1], s=2, c='yellow')

    plt.savefig('pose_estimation/Results/test')
    plt.show()

except Exception as e:
    print(e)
    sys.exit(-1)
