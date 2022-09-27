from flask import Flask, request, redirect,render_template
from flask_cors import CORS

from Mongo import delete, mongo_pdf, download
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
        
        with open('./static/json/pdf_name.json', 'r') as v:
         data_name = json.load(v)
     
        
        data_length = len(data_name)
        
        data_name[data_length] = name_of_pdf
        
        with open('./static/json/pdf_name.json', 'w') as o:
         json.dump(data_name, o)
    
    return render_template('Upload_page.html') 
        

@app.route("/show_link",methods= ['GET','POST'])
def gen_link():
    print("OK")
    if request.method == 'POST':
        pointer = request.get_data()
        
        pointer = pointer.decode('utf-8')
        with open('./static/json/pdf_name.json', 'r') as u:
            name_of_pdf = json.load(u)
           
        pdf_download_data = download(name_of_pdf[pointer])
        
        return pdf_download_data
    return render_template('link.html')


@app.route("/del_link",methods= ['GET','POST'])
def del_link():
    
    delete(name_of_pdf)
    
    return render_template('info.html')


if __name__ == '__main__':
    app.run()