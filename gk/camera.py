import cv2
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except ImportError:
    PiCamera = None


class CVCamera(object):

    def __init__(self, width, height, deviceno=0):
        CAP_PROP_FRAME_WIDTH = 3
        CAP_PROP_FRAME_HEIGHT = 4
        camera = cv2.VideoCapture(deviceno)
        camera.set(CAP_PROP_FRAME_WIDTH, width)
        camera.set(CAP_PROP_FRAME_HEIGHT, height)
        self.camera = camera

    def read(self):
        (grabbed, frame) = self.camera.read()
        if not grabbed:
            raise IOError("could not read from camera")
        return frame

    def close(self):
        self.camera.release()

    def __enter__(self):
        pass

    def __exit__(self, etype, evalue, tb):
        self.release()


class MyPiCamera(object):

    def __init__(self, width, height):
        if PiCamera is None:
            raise ValueError("PiCamera not available")
        self.camera = PiCamera()
        self.camera.resolution = (width, height)
        self.output = PiRGBArray(self.camera)

    def read(self):
        self.output.truncate(0)
        self.camera.capture(self.output, format="bgr")
        return self.output.array

    def close(self):
        self.camera.close()

    def __enter__(self):
        pass

    def __exit__(self, etype, evalue, tb):
        self.close()
