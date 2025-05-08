#pip install easyocr pyspellchecker pyvi googletrans==4.0.0-rc1
import os
from flask import render_template, request, flash,redirect,url_for
from werkzeug.utils import secure_filename
from forms.form_opencv import UploadForm
from config import Config
import easyocr
import uuid
from spellchecker import SpellChecker # kiểm tra chính tả eng
from pyvi import ViTokenizer
from googletrans import Translator


def image_to_text():
    form=UploadForm()
    dich_vi=""
    dich_eng=""
    if form.validate_on_submit():
        file=request.files.get("file")
        if file and file.filename:
            filename=secure_filename(file.filename)
            filepath=os.path.join(Config.UPLOAD_FOLDER,filename)
            file.save(filepath)
            reader=easyocr.Reader(['en','vi'])
            full_text=reader.readtext(filepath) #[bbox,text,prob]  
            #văn bản cần dịch ở  full_text
            vanbancandich="\n".join(x[1] for x in full_text ).lower()     
            #sửa lỗi chính tả
            spell=SpellChecker() 
            suachinhta=" ".join((spell.correction(w) or w)  if w.isalpha else w for w in vanbancandich.split())

            #dịch tiếng anh -> việt (ngược lại)
            dich=Translator()
            dich_vi=dich.translate(suachinhta,src="en",dest="vi").text
            dich_eng=dich.translate(dich_vi,src="vi",dest="en").text

    return render_template('image_to_text.html',form=form,dich_vi=dich_vi,dich_eng=dich_eng)