'''
USAGE

NOTE :
LMB and drag for rectangle (this signifies a shake)
RMB to remove rectangle (but this is a marking which signifies the end of shake)
MMB to unmark (do this if you click LMB or RMB by mistake)

Enter for next frame
q to quit

'''

import sys
import os
import cv2
import numpy as np

import bisect
from util import *

class Marker():
    def __init__(self):
        self.color = (0,255,0)
        self.thickness = 2

        self.LM = False
        self.RM = False

        self.frame = None   # input image
        self.img = None     # output image

        self.mark = False   # marked at current frame
        self.shake = False  # shaking or not

        self.rect = (0, 0, 0, 0)
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0

    def mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.LM = True
            self.mark, self.shake = True, True
            self.x1, self.y1 = x,y
            self.img = self.frame.copy()
            cv2.rectangle(self.img, (self.x1, self.y1), (x, y), self.color, self.thickness)
            print("LBD", self.x1, self.x2, x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.LM == True:
                self.img = self.frame.copy()
                cv2.rectangle(self.img, (self.x1, self.y1), (x, y), self.color, self.thickness)
                # print("LBM", self.x1, self.x2, x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.LM = False
            self.x2, self.y2 = x,y
            self.img = self.frame.copy()
            cv2.rectangle(self.img, (self.x1, self.y1), (x, y), self.color, self.thickness)
            self.rect = (min(self.x1, x), min(self.y1, y), max(self.x1, x), max(self.y1, y))
            print("LBU", self.x1, self.x2, x, y)

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.mark = True
            self.shake = False
            self.img = self.frame.copy()
            self.rect = (0, 0, 0, 0)
            self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0

        elif event == cv2.EVENT_MBUTTONUP:
            self.mark = False
            self.shake = False
            self.img = self.frame.copy()
            self.rect = (0, 0, 0, 0)
            self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0

        cv2.imshow('frame', self.img)

    def get_start_end(self, marked_points, shake):
        start = []
        end = []

        stat = 0
        for m in range(len(marked_points)):
            p = marked_points[m]
            if shake[p] == 1 and stat == 0:
                stat = 1
                start.append(p)
            elif shake[p] == 0 and stat == 1:
                marked_points[m] = p-1
                end.append(p-1)

        return start, end

    def post_process(self, points, mark, shake):

        bounding_box = {}

        marked_points = np.where(mark == 1)[0]

        start, end = self.get_start_end(marked_points, shake)

        for ind, (sp, ep) in enumerate(zip(start, end)):
            s_ind = bisect.bisect_left(marked_points, sp)
            e_ind = bisect.bisect_right(marked_points, ep)
            mp_ind = marked_points[s_ind:e_ind]

            marked_rectangles = points[mp_ind, :]

            x_cords = (marked_rectangles[:, 0] + marked_rectangles[:, 2])/2
            y_cords = (marked_rectangles[:, 1] + marked_rectangles[:, 3])/2
            h = np.max(np.abs(marked_rectangles[:, 0] - marked_rectangles[:, 2]))
            w = np.max(np.abs(marked_rectangles[:, 1] - marked_rectangles[:, 3]))

            x_cords_ = np.interp(np.arange(sp, ep+1), mp_ind, x_cords).reshape(-1, 1)
            y_cords_ = np.interp(np.arange(sp, ep+1), mp_ind, y_cords).reshape(-1, 1)

            point_ind = np.concatenate((x_cords_-h/2, y_cords_-w/2, x_cords_+h/2, y_cords_+w/2), axis = -1)

            bounding_box[ind] = {
                "rectangles" : point_ind.tolist(),
                "marked_points" : mp_ind.tolist()
            }

        return bounding_box

    def BB_to_points(self, json_data):

        n_person = 0
        for ind in json_data:
            print(ind, type(ind))
            if str(ind).isdigit():
                n_person += 1

        points = np.zeros((n_person, json_data["frames"], 4))

        for ind in json_data:
            if str(ind).isdigit():
                bounding_box = json_data[ind]["bounding_box"]
                p_id = json_data[ind]["person_id"]

                for bb in bounding_box:
                    point_ind = bounding_box[bb]["rectangles"]
                    mp_ind = bounding_box[bb]["marked_points"]
                    sp, ep = mp_ind[0], mp_ind[-1]
                    points[p_id, sp:ep+1, :] = np.array(point_ind)

        return points


    def run(self, file_name):
        # cv2.namedWindow('frame', cv2.WINDOW_GUI_NORMAL)  # WINDOW_GUI_NORMAL stops context menu on right click
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', self.mouse_callback)

        cap = cv2.VideoCapture(file_name)
        mark = []
        shake = []
        points = []

        while (1):
            ret, frame = cap.read()
            if ret == True:
                self.mark = False
                self.frame = frame
                self.img = np.array(frame, copy=True)
                cv2.rectangle(self.img, (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3]), self.color, self.thickness)
                cv2.imshow('frame', self.img)

                k = cv2.waitKey(0) & 0xff
                if k == ord('q'):
                    break


                points.append(self.rect)
                mark.append(1 if self.mark else 0)
                shake.append(1 if self.shake else 0)
            else:
                cv2.destroyAllWindows()
                break

        points = np.asarray(points)
        mark = np.array(mark)
        shake = np.array(shake)

        return points, mark, shake


    def marked_video(self, file_name, points_):
        points_ = points_.astype(int)

        cv2.namedWindow('frame')

        cap = cv2.VideoCapture(file_name)
        ind = 0

        while (1):
            ret, frame = cap.read()
            if ret == True:
                rect = points_[ind, :]
                print(rect)
                ind += 1
                self.img = np.array(frame, copy=True)
                cv2.rectangle(self.img, (rect[0], rect[1]), (rect[2], rect[3]), self.color, self.thickness)
                cv2.imshow('frame', self.img)
                # print(rect)

                k = cv2.waitKey(0) & 0xff
                if k == ord('q'):
                    break
            else:
                cv2.destroyAllWindows()
                break



if __name__ == "__main__":

    MARK = True
    TEST = False

    file_name = "./dataset/handshake.avi"
    file_name = file_name.replace("\\", "/")

    output_dir = "/".join(i for i in file_name.split("/")[:-1])
    output_name = output_dir + "/%s3.json"%(file_name.split("/")[-1].split(".")[0])

    marker = Marker()


    if MARK:
        # run is to mark the points
        points, mark, shake = marker.run(file_name)

        # post process returns the bounding box from the marked points
        bounding_box = marker.post_process(points, mark, shake)

        # Write to json
        init_json(output_name)

        json_data = {"frames" : len(mark)}
        json_data[0] = {"person_id": 0, "bounding_box": bounding_box}

        update_json(json_data, output_name)

    json_data = read_json(output_name)

    points_= marker.BB_to_points(json_data)
    print("[n_person, n_frames, 4] : ", points_.shape)
    print(points_[0, :, :])

    marker.marked_video(file_name, points_[0, :, :])



