import os
from flask import render_template, request, flash,Response
from werkzeug.utils import secure_filename
from forms.form_opencv import UploadForm
from config import Config
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("models/yolov10n.pt")

def tao_frame(video_file):
    cap = cv2.VideoCapture(video_file)
    while cap.isOpened():
        ret,frame = cap.read()
        if not ret:
            break
            
        results = model(frame)
        annotated_frame = results[0].plot()
        ret,buffer = cv2.imencode(' .jpg',annotated_frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
        
    cap.release()

def yolocoban():
    form=UploadForm()
    dich_vi=""
    dich_eng=""
    if form.validate_on_submit():
        file=request.files.get("file")
        if file and file.filename:
            filename=secure_filename(file.filename)
            filepath=os.path.join(Config.UPLOAD_FOLDER,filename)
            file.save(filepath)
            return Response(tao_frame(filepath),mimetype='multipart/x-mixed-replace; boundary=frame') # Gửi response chứa video đã xử lý

    return render_template("yolocoban.html",form=form)