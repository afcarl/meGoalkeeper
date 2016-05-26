import cv2
import time

class Video(object):

    def __init__(self, src, winname='frame', show=True, dstfile=None,
                 singlestep=False, framename='/tmp/frame.png'):
        self.src = src
        self.winname = winname
        self.show = show
        self.singlestep = singlestep
        self.dstfile = dstfile
        self.framename = framename
        cv2.namedWindow(winname)

    def process(self, frame):
        return frame

    def end(self):
        pass

    def iterframes(self):
        if self.dstfile is not None:
            fourcc = cv2.VideoWriter_fourcc(*'X264')
            dstvideo = cv2.VideoWriter(self.dstfile, fourcc, 30, (200, 200))
        else:
            dstvideo = None

        save_next = False
        t1 = time.time()
        i = 0
        wait_time = 1
        if self.singlestep:
            wait_time = 0 # wait until we click or press a key
        while True:
            frame = self.src.read()
            if frame is None:
                break
            if save_next:
                print 'Saving frame to', self.filename
                cv2.imwrite(self.framename, frame)
                save_next = False
            #
            frame = self.process(frame)
            yield frame
            i += 1
            if i == 30:
                fps = 30/(time.time() - t1)
                print 'fps: %.2f' % fps
                t1 = time.time()
                i = 0
            #
            if self.show:
                cv2.imshow(self.winname, frame)
                key = cv2.waitKey(wait_time) & 0xFF
                if key == ord("q"):
                    break
                if key == ord('s'):
                    save_next = True
            #
            if dstvideo:
                dstvideo.write(frame)
        #
        if dstvideo:
            dstvideo.release()
        self.end()

    def run(self):
        for frame in self.iterframes():
            pass


if __name__ == '__main__':
    from gk.camera import CVCamera
    camera = CVCamera(640, 480)
    player = Player(camera)
    player.run()
