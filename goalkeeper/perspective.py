import cv2
import numpy as np
from imutils.perspective import order_points

class Perspective(object):

    def __init__(self, winname, width, show=False):
        self.winname = winname
        self.width = width
        self.show = show
        self.points = []
        cv2.setMouseCallback(winname, self.onclick)

    def onclick(self, event, x, y, flags, param):
        if len(self.points) == 4:
            return
        if event == cv2.EVENT_LBUTTONUP:
            point = (x, y)
            print 'x = %s' % (point,)
            self.points.append(point)
            if len(self.points) == 4:
                # automatically sort the points
                points = np.array(self.points, dtype = "float32")
                self.points = order_points(points)

    def process(self, frame):
        if len(self.points) < 4:
            if self.show:
                for point in self.points:
                    cv2.circle(frame, point, 5, (255, 0, 0))
            return frame
        else:
            return self.warp(frame)

    def warp(self, frame):
        dst = np.array([
            [0, 0],
            [self.width-1, 0],
            [self.width-1, self.width-1],
            [0, self.width-1]
        ], dtype=np.float32)
        M = cv2.getPerspectiveTransform(self.points, dst)
        return cv2.warpPerspective(frame, M, (self.width, self.width))
    


if __name__ == '__main__':
    from goalkeeper.camera import CVCamera
    from goalkeeper.video import Video
    camera = CVCamera(640, 480)
    video = Video(camera)
    perspective = Perspective(video.winname, 400, show=True)
    video.process = perspective.process
    video.run()

