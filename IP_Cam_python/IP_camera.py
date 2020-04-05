import cv2
import requests
import numpy as np
from time import sleep, time

class Camera():
    '''
    API_url parameters isn't required
    but your IP camera might not work 
    without it.
    '''
    def __init__(self,ip,*,API_endpoint="cgi-bin/hi3510/",image_protocol="rtsp",image_endpoint="",usr="admin",pwd="admin",number_of_positions=8):
        self.ip=ip
        self.number_of_positions = number_of_positions
        self.preset_url = f"http://{ip}/{API_endpoint}preset.cgi?&-usr={usr}&pwd={pwd}"
        self.ptz_ulr = f"http://{ip}/{API_endpoint}ptzctrl.cgi?-usr={usr}&-pwd={pwd}"
        self.image_url = f"{image_protocol}://{ip}/{image_endpoint}"
        self.directions = set(["stop","left","right","up","down"])

    def _position(self, position,*, is_goto, not_unset=1):
        if position not in range(self.number_of_positions):
            raise Exception("Invalid camera position.")
        act = "goto" if is_goto else "set"
        url = self.preset_url + f"&-act={act}&-status={not_unset}&-number={position}"
        r = requests.get(url)
        r.raise_for_status()

    def _move(self, direction, all_the_way=False):
        if direction not in self.directions:
            raise Exception("Invalid camera moviment.")
        url  = self.ptz_ulr + f"&-step={int(not all_the_way)}&-act={direction}"
        r = requests.get(url)
        r.raise_for_status()

    def goto_position(self, position):
        self._position(position, is_goto=True)

    def set_position(self, position):
        self._position(position, is_goto=False)

    def stop(self):
        self._move("stop",all_the_way=True)

    def go_right(self, all_the_way=False):
        self._move("right", all_the_way=all_the_way)

    def go_left(self, all_the_way=False):
        self._move("left", all_the_way=all_the_way)

    def go_up(self, all_the_way=False):
        self._move("up", all_the_way=all_the_way)

    def go_down(self, all_the_way=False):
        self._move("down", all_the_way=all_the_way)

    def video_capture(self):
        return cv2.VideoCapture(self.image_url)

    def get_frame(self):
        cap = cv2.VideoCapture(self.image_url)
        ret, image = cap.read()
        if not ret:
            raise Exception("Failure at reading frames")
        cap.release()
        return image

    def get_frames(self,number_of_frames = 3):
        cap = cv2.VideoCapture(self.image_url)
        list_frames = []
        for i in range(number_of_frames):
            ret, image = cap.read()
            if not ret:
                raise Exception("Failure at reading frames")
            list_frames.append(image)
            if i != number_of_frames-1:
                sleep(0.001)
        cap.release()
        return list_frames

    def get_frames_delayed(self, number_of_frames, delay=0.5):
        cap = cv2.VideoCapture(self.image_url)
        list_frames = []
        for _ in range(number_of_frames):
            t0 = time()
            while (time() - t0) < delay:
                ret, image = cap.read()
                if not ret:
                    raise Exception("Failure at reading frames")
            list_frames.append(image)
        cap.release()
        return list_frames
    