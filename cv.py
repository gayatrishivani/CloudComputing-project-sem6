import os
from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import random
from PIL import Image
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sketch',methods=['POST'])
def sketch():
    target = os.path.join(APP_ROOT, 'static/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    
    file = request.files.get("file")
    
    jc =  file.filename
    jcp = str(random.randint(0,22)) + jc
    destination = "/".join([target, jcp])
    file.save(destination)
    
    fol = "static/"+jcp
    print(fol)
    jcs = cv2.imread(fol)
    
    scale_percent = 0.60
    
    width = int(jcs.shape[1]*scale_percent)
    height = int(jcs.shape[0]*scale_percent)

    dim = (width,height)
    resized = cv2.resize(jcs,dim,interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    kernel_sharpening = np.array([[-1,-1,-1], 
                                [-1, 9,-1],
                                [-1,-1,-1]])
    sharpened = cv2.filter2D(gray,-1,kernel_sharpening)



    
    inv = 255-gray
    gauss = cv2.GaussianBlur(inv,ksize=(9,9),sigmaX=0,sigmaY=0)

    def dodgeV2(image,mask):
        return cv2.divide(image,255-mask,scale=256)

    pencil_jc = dodgeV2(sharpened,gauss)

    print(pencil_jc)
    img = Image.fromarray(pencil_jc)
    fole = "static/"+"copy"+jcp
    img.save(fole)
    imge = "copy"+jcp
    return render_template("sketch.html", img_name=jcp,ps_name=imge)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)
