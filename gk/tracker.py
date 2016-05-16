from collections import namedtuple
import cv2

# copied and adapted from
# http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
def find_colored_contours(frame, lower, upper):
    # take the frame, blur it, and convert it to the HSV
    # color space
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
    return cnts


class BallTracker(object):

    Ball = namedtuple('Ball', ['center', 'radius'])

    def __init__(self, lower, upper, show=False):
        self.lower = lower
        self.upper = upper
        self.show = show
        self.ball = None

    @classmethod
    def fromconf(cls, show, conf):
        lower = tuple(conf['lower'])
        upper = tuple(conf['upper'])
        return cls(lower, upper, show)

    def toconf(self):
        return dict(lower = self.lower,
                    upper = self.upper)

    def process(self, frame):
        cnts = find_colored_contours(frame, self.lower, self.upper)
	if len(cnts) <= 0:
            self.ball = None
            return frame
        #
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        x = int(x)
        y = int(y)
        self.ball = self.Ball((x, y), int(radius))
        if self.show:
            ball = self.ball
            yellow = (0, 255, 255)
            cv2.circle(frame, ball.center, ball.radius, yellow, 2)
        return frame


if __name__ == '__main__':
    from gk.camera import CVCamera
    from gk.video import Video
    camera = CVCamera(640, 480)
    video = Video(camera)
    balltracker = BallTracker(lower=(0, 0, 60),
                              upper=(7, 255, 255),
                              show=True)
    video.process = balltracker.process
    video.run()

