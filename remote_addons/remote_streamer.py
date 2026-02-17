import cv2
import threading
import time
import socket
from flask import Flask, Response

# turn off flask start logs
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


class RemoteStreamer:
    def __init__(self, port=5000):
        self.output_frame = None
        self.lock = threading.Lock()
        self.port = port
        self.init_stream()

    def _get_ip_address(self):
        """
        Creates temporary connection to check ip address of raspberry.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # check something idk
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "[Error]: Adres not known."

    def init_stream(self):
        ip_addr = self._get_ip_address()
        print(
            f"[REMOTE-STREAMER] Preview available on:"
            + f" http:{ip_addr}:{self.port}\n"
        )
        self.remote_stream = True

        self.app = Flask(__name__)
        self.setup_routes()

        t = threading.Thread(target=self.run_server, daemon=True)
        t.start()

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return HTML_TEMPLATE
        
        @self.app.route("/video_feed")
        def video_feed():
            return Response(
                self.generate(), mimetype="multipart/x-mixed-replace; boundary=frame"
            )

    def run_server(self):
        self.app.run(host="0.0.0.0", port=self.port, debug=False, threaded=True)

    def generate(self):
        while True:
            with self.lock:
                if self.output_frame is None:
                    time.sleep(0.01)
                    continue

                (flag, encodedImage) = cv2.imencode(".jpg", self.output_frame)
                if not flag:
                    continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + bytearray(encodedImage) + b"\r\n"
            )

    def show(self, frame, window_name="BlueSpark"):
        if self.remote_stream:
            with self.lock:
                self.output_frame = frame.copy()
        else:
            cv2.imshow(window_name, frame)


# vibe 
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BlueSpark Vision</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html { 
            margin: 0; 
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #000;
            overflow: hidden; 
        }
        
        img { 
            display: block;
            width: 100vw;   
            height: 100vh;  
            
            object-fit: contain; 
        }
    </style>
</head>
<body>
    <img src="/video_feed" id="stream">
    
    <script>
        document.getElementById('stream').addEventListener('dblclick', function() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    console.log("Error attempting to enable full-screen mode: " + err.message);
                });
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        });
    </script>
</body>
</html>
"""