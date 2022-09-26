from flask import Flask, request,session,abort, redirect,render_template, jsonify
from flask_cors import CORS, cross_origin

from Mongo import mongo_pdf, download
import base64
import json


app = Flask(__name__)
app.secret_key = "One-Time-Share"
CORS(app)

name_of_pdf = "not_defined"

@app.route('/', methods=['GET','POST'])
def pdf_send():    
    return render_template('Upload_page.html') 


@app.route('/upload_pdf', methods=['GET','POST'])
def show():
    global name_of_pdf
    if request.method == 'POST':
        pdf_base64 = request.get_json()
    
        # decode = open(pdf_base64['pdf_name'], 'wb')
        # decode.write(base64.b64decode(pdf_base64['pdf']))
        
        encoded_pdf = 'data:application/pdf;base64,' + pdf_base64['pdf']
        # print(encoded_pdf)
        
        name_of_pdf = pdf_base64['pdf_name']
        
        encoded_pdf_utf = encoded_pdf.encode('utf-8')
        enc_pdf = pdf_base64['pdf'].encode('utf-8')
        
        mongo_pdf(encoded_pdf_utf, pdf_base64['pdf_name'])
    
    return redirect("/show_link")
        

@app.route("/show_link",methods= ["GET","POST"])
def gen_link():
    
    if request.method == 'POST':
        pointer = request.get_data()
        
        pointer = pointer.decode('utf-8')
            
        pdf_download_data = download(name_of_pdf[pointer])
        return pdf_download_data
    return render_template('link.html',current_name = name_of_pdf)


if __name__ == '__main__':
    app.run()