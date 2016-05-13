from goalkeeper.video import Video
from goalkeeper.tracker import BallTracker
from goalkeeper.perspective import Perspective

class GoalKeeper(Video):

    def __init__(self, src, winname='frame', show=True):
        Video.__init__(self, src, winname, show)
        self.perspective = Perspective(winname, 200, show=show)
        self.tracker = BallTracker(lower=(0, 0, 60),
                                   upper=(7, 255, 255),
                                   show=show)

    def process(self, frame):
        frame = self.perspective.process(frame)
        frame = self.tracker.process(frame)
        return frame
    
    

if __name__ == '__main__':
    from goalkeeper.camera import CVCamera
    camera = CVCamera(640, 480)
    gk = GoalKeeper(camera)
    gk.run()

