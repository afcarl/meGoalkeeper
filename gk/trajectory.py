import cv2
import math
import numpy as np
from collections import deque

class Trajectory(object):

    def __init__(self, show):
        self.show = show
        self.points = deque(maxlen=4)

    def add_point(self, p):
        self.points.append(p)

    def predict(self, yy):
        if len(self.points) < 2:
            return None

        Xs = [x for x, y in self.points]
        Ys = [y for x, y in self.points]
        # y = kx + m
        # x = (y-m)/k
        (k, m), resids, rank, s, rcond = np.polyfit(Xs, Ys, 1, full=True)
        if rank < 2:
            # this is the equivalent of "RankWarning: Polyfit may be poorly
            # conditioned": this probably means that the ball has gone out of
            # sight, just ignore it
            return None
        xx = int((yy-m)/k)
        if abs(xx) > 500:
            return None
        return xx, yy

    def process(self, frame):
        if not self.show:
            return frame
        p0 = None
        for p1 in self.points:
            cv2.circle(frame, p1, 5, (255, 0, 0), 2)
            if p0 is not None:
                cv2.line(frame, p0, p1, (255, 0, 0))
            p0 = p1
        #
        p1 = self.predict(yy=200)
        if p1 is not None:
            cv2.circle(frame, p1, 5, (255, 255, 0), 2)
            cv2.line(frame, p0, p1, (255, 255, 0))
        return frame
