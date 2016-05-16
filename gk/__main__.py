"""
Usage: gk [options]

Options:
  -c --conf=FILE  Path to the configuration file [Default: gk.conf]
  --noload        Don't load the config file
  --nosave        Don't save the config file
  --iball         Display interactive controls to adjust the ball thresholds
                  (imply --show)
  --show          Display the frames
  -h --help       show this
"""

import os.path
import json
from gk.camera import CVCamera
from gk.video import Video
from gk.tracker import BallTracker
from gk.perspective import Perspective

class Conf(object):

    camera = dict(
        width = 640,
        height = 480
    )

    field = dict(
        width = 200,
        points = None
    )

    ball = dict(
        lower = (0,   0,  60), # HSV
        upper = (7, 255, 255)  # HSV
    )

    def __init__(self, filename=None):
        if filename is not None and os.path.exists(filename):
            with open(filename) as f:
                conf = json.load(f)
            self.__dict__.update(conf)

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.__dict__, f)


class GoalKeeper(Video):

    def __init__(self, conf, show=False, iball=False):
        camera = CVCamera(conf.camera['width'], conf.camera['height'])
        winname = 'frame'
        Video.__init__(self, camera, winname, show)
        self.conf = conf
        self.perspective = Perspective.fromconf(winname, show=show,
                                                conf=conf.field)
        self.tracker = BallTracker.fromconf(show=show, interactive=iball,
                                            conf=conf.ball)

    def process(self, frame):
        frame = self.perspective.process(frame)
        frame = self.tracker.process(frame)
        return frame

    def end(self):
        self.conf.field = self.perspective.toconf()
        self.conf.ball = self.tracker.toconf()

def main():
    import docopt
    args = docopt.docopt(__doc__)
    configfile = args['--conf']
    if args['--noload']:
        conf = Conf()
    else:
        conf = Conf(configfile)
    #
    show = args['--show']
    iball = args['--iball']
    if iball:
        show = True
    gk = GoalKeeper(conf, show=show, iball=iball)
    gk.run()
    #
    if not args['--nosave']:
        conf.save(configfile)


if __name__ == '__main__':
    main()
