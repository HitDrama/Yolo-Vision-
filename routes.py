from flask import Blueprint
from controllers.opencv_controller import home

from controllers.video_controller import video_feed,video_page,record_video
from controllers.license_controller import license_plate
from controllers.Bienso_controller import Biensoxe
from controllers.image_controller import image_to_text
from controllers.yolocoban_controller import yolocoban


opencv=Blueprint("opencv",__name__)

#định nghĩa router
opencv.route("/",methods=["GET","POST"])(home)
opencv.route("/image-to-text", methods=["GET", "POST"])(image_to_text)

opencv.route("/yolo-co-ban", methods=["GET", "POST"])(yolocoban)

