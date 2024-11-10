from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

def camera():
    cam = cv2.VideoCapture(0)
    r, frame = cam.read()
    ret, jpg = cv2.imencode(".jpg", frame)
    if not ret:
        return None
    return jpg.tobytes()

def stream():
    while True:
        frame = camera()
        if frame is None:
            break
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/api/screen")
def api():
    return Response(
        stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True)
