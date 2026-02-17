import argparse
import sys

from .camera import UniversalCamera
from .remote_streamer import RemoteStreamer
from .exceptions import CameraError

class VisionControl:
    """
    Represents controller responsible for parsing arguments, creating
    and calling appriopriate objects responsible for handling these
    arguments.
    """

    def __init__(self, cam_height: int = 320, cam_width: int = 640):
        self.cam_width = cam_width
        self.cam_height = cam_height
        self.args = self.parse_arguments()
        self.handle_args(self.args)        

    def parse_arguments(self):
        parser = argparse.ArgumentParser()

        # remote streamer arguments
        parser.add_argument(
            "--remote-preview",
            action="store_true",
            help="Stream preview remotely on local http addres"
            + ", default port is 5000.",
        )
        parser.add_argument(
            "--stream-port",
            type=int,
            default=5000,
            help="Custom port on which preview should be streamed.",
        )

        # camera hardware handling arguments
        parser.add_argument(
            "--cam",
            type=str,
            default="auto",
            choices=["auto", "rpi", "usb"],
            help="Camera Selection: usb, rpi CSI cable or auto deteciton",
        )

        # parse only own arguments, delete them from argv to prevent conflict
        args, unknown_args = parser.parse_known_args()
        sys.argv = [sys.argv[0]] + unknown_args

        return args

    def handle_args(self, args):
        """Handle all given arguments automatically."""
        try:
            self.camera = UniversalCamera(self.cam_width, self.cam_height, args.cam)
            port = args.stream_port
            self.streamer = RemoteStreamer(port=port)
            self.streamer.remote_stream = args.remote_preview # FIXME
        except CameraError as e:
            raise CameraError(e)
        

    def read(self):
        return self.camera.read()
    
    def update(self, frame):
        """Send updated frame to video/stream."""
        self.streamer.show(frame)

    def stop(self):
        """Stop started functionality"""
        if self.camera:
            self.camera.release()
