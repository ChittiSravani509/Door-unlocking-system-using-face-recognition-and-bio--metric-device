# python recognize_faces_video.py --encodings encodings.pickle
# python recognize_faces_video.py --encodings encodings.pickle --output
import datetime
import MySQLdb
import cv2
import time
import pickle
import imutils
import argparse
import face_recognition
from imutils.video import VideoStream
output/jurassic_park_trailer_output.avi - -display
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
                help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
                help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
writer = None
time.sleep(2.0)
while True:
    frame = vs.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(frame, width=750)
    r = frame.shape[1] / float(rgb.shape[1])
    boxes = face_recognition.face_locations(rgb,
                                            model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}
    for i in matchedIdxs:
        name = data["names"][i]
        counts[name] = counts.get(name, 0) + 1
        name = max(counts, key=counts.get)
        names.append(name)
        str = name
        t = datetime.datetime.now()
        print("identified faces:", str)
        print("date:", datetime.datetime.now())
db = MySQLdb.connect("localhost", "phpmyadmin", "sai518", "facerecognition")
Mycursor = db.cursor()
mycursor.execute(
    "insert IGNORE into recognizedfaces values(%s,%s,%s,%s)", (str, t, t, 'present'))
db.commit()
mycursor.execute("select rollno,status from student")
rs = mycursor.fetchall()
for i in rs:
    x = i[0]
    y = i[1]
    mycursor.execute("""insert into attendance values(%s,%s,%s)""", (x, t, y))
    mycursor.execute(
        "update attendance inner join recognizedfaces on recognizedfaces.rollno=attendance.rollno set attendance.Status='present'")
    db.commit()
db.close()
for ((top, right, bottom, left), name) in zip(boxes, names):
    top = int(top * r)
    right = int(right * r)
    bottom = int(bottom * r)
    left = int(left * r)
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)
    if writer is None and args["output"] is not None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 20,
                                 (frame.shape[1], frame.shape[0]), True)
    if writer is not None:
        writer.write(frame)
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    cv2.destroyAllWindows()
    vs.stop()
    if writer is not None:
        writer.release()
