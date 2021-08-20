import secrets
import os
import matplotlib.pyplot as plt
import warnings
import cv2
from fer import FER
from PIL import Image
import numpy as np, pandas as pd


from flask import url_for, current_app

def detect_mood(pic_upload):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(pic_upload.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(current_app.root_path,'static/mood_uploads',picture_fn)
    output_size=(125,125)
    i=Image.open(pic_upload)
    i.thumbnail(output_size)
    i.save(picture_path)


    detector=FER(mtcnn=True)

    img = cv2.imread(picture_path)
    img=plt.imread(picture_path)
    try:
        mood = detector.top_emotion(img)
    except:
        mood = ('',0)
    

    return (picture_fn,mood)
