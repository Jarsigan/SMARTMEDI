from flask import Flask, render_template, json, request,redirect,session,url_for,g
from flaskext.mysql import MySQL
from datetime import datetime
import cv2
import datetime
import numpy as np
import time
import os
import cStringIO
from PIL import Image,ImageEnhance

global index_add_counter
import base64
import re
import cStringIO
index_add_counter = 0
userNic="unknown"


mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'smartmedi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


#call signup and signin template
@app.route('/')
def main():
    return render_template('signup.html',)

#call home window
@app.route('/show')
def show():
    if session.get('user'):
        return render_template('indexnew.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#call collect image data
@app.route('/showWebCam')
def showWebCam():
    return render_template('view.html')
    # if session.get('user'):
    #     return render_template('view.html')
    # else:
    #     return render_template('error.html',error = 'Unauthorized Access')


#call face recognation window
@app.route('/showRecogPatient')
def showRecogPatient():
    if session.get('user'):
        return render_template('recogPatient.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#call create patient window
@app.route('/showAddPatient')
def showAddPatient():
    if session.get('user'):
        return render_template('addpatientmode.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#call doctor registation window
@app.route('/showRegisterDoctor')
def showRegisterDoctor():
    if session.get('user'):
        return render_template('registerDoctor.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#call doctor view update window
@app.route('/showViewUpdateDoctor')
def ViewUpdateDoctor():
    if session.get('user'):
        return render_template('viewUpdateDoctor.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


#call drug
@app.route('/showAddDrug')
def showAddDrug():
    if session.get('user'):
        return render_template('addDrug.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#caal view update drug
@app.route('/showViewUpdateDrug')
def showViewUpdateDrug():
    if session.get('user'):
        return render_template('viewUpdateDrug.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

#call patient report home
@app.route('/showPatientReport')
def showPatientReport():
    if session.get('user'):
        return render_template('patientReport.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#call create medical report
@app.route('/showCreateMedReport')
def showCreateMedReport():
    if session.get('user'):
        return render_template('medReport.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#call view patient report page
@app.route('/showViewMedReport')
def showViewMedReport():
    if session.get('user'):
        return render_template('viewMedReport.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#view and update patient detail
@app.route('/showViewHome')
def showviewHome():
    if session.get('user'):
        return render_template('viewHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')



#logout
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


#upload face image models from user end
@app.route('/upload',methods=['POST'])
def upload():
    #get face image data from user as base64 format and change to jpeg and save the detected images
    NIC=session["userNIC"]
    imageData = request.form['file']
    myName = request.form['myName']
    i=str(imageData)
    imgstr=i.split("data:image/jpeg;base64,")[1]
    global index_add_counter
    index_add_counter+=1
    image_64_decode = base64.decodestring(imgstr)
    s="C:/Python27/Scripts/SMARTMEDI/dataSet/jarsi"+"."+str(index_add_counter)+".jpeg"
    # create a writable image and write the decoding result
    image_result = open(s, 'wb')
    # save image
    image_result.write(image_64_decode)
    #face detect and save detect faces
    faceDetect = cv2.CascadeClassifier(
        "C:\Python27\Scripts\SMARTMEDI\static\js\haarcascade_frontalface_default.xml");
    img = cv2.imread(s)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5);
    if faces!=():
        for (x, y, w, h) in faces:
            cv2.imwrite(
                "C:/Python27/Scripts/SMARTMEDI/dataSet/detect/"+NIC +".dtc"+ str(index_add_counter)+ ".jpg",
                gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.waitKey(100);



        return  json.dumps({'message': 'Uploaded sucessfully'})
    else:
        return json.dumps({'message': 'Fault Image!'})

#recognize face and fetch details from database
@app.route('/recogFace',methods=['POST'])
def recogFace():
    ### train image models
    recognizer = cv2.createLBPHFaceRecognizer();
    path = 'C:/Python27/Scripts/SMARTMEDI/dataSet/detect'

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L');
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[0])
            faces.append(faceNp)
            IDs.append(ID)

        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    # set path to trained xml file
    recognizer.save('C:/Python27/Scripts/SMARTMEDI/static/js/recognizer/trainingData.yml')


    ###get image data from user end and change as jpeg image
    imageData = request.form['file']
    myName = request.form['myName']
    i = str(imageData)
    imgstr = i.split("data:image/jpeg;base64,")[1]

    image_64_decode = base64.decodestring(imgstr)
    s = "C:/Python27/Scripts/SMARTMEDI/dataSet/recog/demo" + ".jpeg"

    # create a writable image and write the decoding result
    image_result = open(s, 'wb')
    # save image
    image_result.write(image_64_decode)

    ###recog face
    faceDetect = cv2.CascadeClassifier("C:\Python27\Scripts\SMARTMEDI\static\js\haarcascade_frontalface_default.xml");
    rec = cv2.createLBPHFaceRecognizer();
    rec.load('C:/Python27/Scripts/SMARTMEDI/static/js/recognizer/trainingData.yml');
    id = 0
    font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL, 4, 1, 0, 4)

    img = cv2.imread(s)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceDetect.detectMultiScale(gray, 1.3, 5);
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)
        id, conf = rec.predict(gray[y:y + h, x:x + w])
        cv2.cv.PutText(cv2.cv.fromarray(img), str(id), (x, y + h), font, 255);
    print(id)

    if id!=0:
        NICNumber=id

        #mysql connection
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_viewPatientNIC', (NICNumber,))
        wishes = cursor.fetchall()

        # remove perivious userID session variable
        session.pop("userID", None)
        patientID = wishes[0][0]
        session['userID'] = patientID
        dob=wishes[0][3]
        year = dob.split("-")[0]
        month = dob.split("-")[1]
        day = dob.split("-")[2]

       #set data as a json format
        for wish in wishes:
            wish_dict = {
                'id': wish[0],
                'name': wish[1],
                'gender': wish[2],
                'dob': wish[3],
                'year': year,
                'month': month,
                'day': day,
                'nic': wish[4],
                'mobile': wish[5],
                'address': wish[6],
                'email': wish[7],
                'info': wish[8],
                'typeofapp': wish[9],
                'notification':"",
                'blood': wish[10]}

        session['data'] = wish_dict
        return json.dumps(wish_dict)
    else:
        return json.dumps({'notification': 'Patient is not find'})

#signin
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        #connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if (str(data[0][3])==_password):
                session['user'] =str(data[0][0])
                print str(data[0][0])
                return redirect('/show')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

        #its use for testing
        # if _username == "jarsi@gmail.com" and _password == "1234":
        #     # return redirect('/show')
        #     return render_template('indexnew.html')

    except Exception as e:
        return render_template('error.html',error = str(e))



#signup
@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['name']
        _email = request.form['email']
        _password = request.form['password']


        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            # _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps('User created successfully !')
            else:
                return json.dumps(str(data[0]))
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

#register patient
@app.route('/addPatient', methods=['POST', 'GET'])
def addPatient():

    try:
        #get form data
        session.pop("userNIC", None)
        _name = request.form['inputName']
       # _email = request.form['inputEmail']
        _gender = request.form['gender']
        _bloodgroup=request.form['bloodgroup']
        _day = request.form.get('day')
        _month = request.form.get('month')
        _year = request.form['year']
        _dob = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        _NIC=request.form['inputNIC']
        _address = request.form['address']
        _mobile = request.form['mobile_number']
        _info = request.form['textarea']

        #set userNIC value
        session['userNIC']=_NIC[:-1]

        # validate the received values
        if _name and  _gender and _dob and _mobile and _NIC and _address:

            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addPatient', (_name,_gender,_dob,_NIC,_mobile,_address,_info,_bloodgroup))
            data = cursor.fetchall()


            if len(data) is 0:
                conn.commit()
                return redirect('/showWebCam')
            else:
                return render_template('error.html', error=str(data[0]))
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

#view patient using nic number
@app.route('/viewHome',methods=['POST','GET'])
def viewHome():
    try:
            _NIC = request.form['NICnumber']
            # _NIC="942033740v"

            #database connection
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetPatient',(_NIC,))
            wishes = cursor.fetchall()

            # remove perivious session variable
            session.pop("userID", None)

            patientID=wishes[0][0]
            session['userID'] =patientID
            dob=wishes[0][3]
            year=dob.split("-")[0]
            month=dob.split("-")[1]
            day=dob.split("-")[2]

            #set database value as a json format
            for wish in wishes:
                wish_dict = {
                        'id': wish[0],
                        'name': wish[1],
                        'gender': wish[2],
                        'dob': wish[3],
                        'year':year,
                        'month':month,
                        'day':day,
                        'nic':wish[4],
                        'mobile': wish[5],
                        'address': wish[6],
                        'email': wish[7],
                        'info': wish[8],
                    'typeofapp':wish[9],
                    'blood': wish[10]}

            session['data'] = wish_dict
            return json.dumps(wish_dict)

    except Exception as e:
        return render_template('error.html', error = str(e))

#update patient
@app.route('/updatePatient', methods=['POST', 'GET'])
def updatePatient():

    try:
        session.pop("userNIC", None)
        _name = request.form['inputName']
        _patientid = request.form['patientid']
        _day = request.form['day']
        _month = request.form['month']
        _gender = request.form['gender']
        _year = request.form['year']
        _dob = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        _address = request.form['address']
        _mobile = request.form['mobile_number']
        _info = request.form['textarea']
        _bloodgroup = request.form['bloodgroup']
        nic=request.form['NICnumber']


        session['userNIC'] = nic[:-1]

        # validate the received values
        if _name and _dob and _mobile and nic and _address:

            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "update patient set fullname=%s,gender=%s,dateofbirth=%s,NIC=%s,mobileno=%s,address=%s,bloodgroup=%s,otherinformation=%s where patientid=%s"

            cursor.execute(query, (_name,_gender,_dob,nic,_mobile,_address,_bloodgroup,_info,_patientid))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'Patient update successfully !'})
                # return redirect('/showWebCam')


            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


#register doctor
@app.route('/registerDoctor',methods=['POST','GET'])
def registerDoctor():
    try:
        _name = request.form['inputName']
        _NIC=request.form['inputNIC']
        _field = request.form['field']
        _day = request.form.get('day')
        _month = request.form.get('month')
        _year = request.form['year']
        _dob = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        _address = request.form['address']
        _mobile = request.form['mobile_number']
        _email=request.form['email']

        # validate the received values
        if _name and _email:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into doctor (name,NIC,field,dob,address,mobile,email) values (%s,%s,%s,%s,%s,%s,%s)"

            cursor.execute(query, (_name,_NIC,_field,_dob,_address,_mobile,_email))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                # return json.dumps({'message': 'Doctor Register successfully !'})
                return redirect('/showRegisterDoctor')
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


#view doctor
@app.route('/viewDoctor',methods=['POST','GET'])
def viewDoctor():
    try:
            _NIC = request.form['NICnumber']

            # All Good, let's call MySQL
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetDoctor',(_NIC,))
            wishes = cursor.fetchall()

            dob=wishes[0][4]

            #set values as json format
            for wish in wishes:
                wish_dict = {
                        'id': wish[0],
                        'name': wish[1],
                        'nic': wish[2],
                        'field': wish[3],
                        'year':dob.year,
                        'month':dob.month,
                        'day':dob.day,
                        'address': wish[5],
                        'mobile': wish[6],
                        'email': wish[7]}

            return json.dumps(wish_dict)

    except Exception as e:
        return render_template('error.html', error = str(e))

#update doctor
@app.route('/updateDoctor', methods=['POST', 'GET'])
def updateDoctor():
    try:
        _id=request.form["id"]
        _name = request.form['name']
        _field = request.form['field']
        _day = request.form['day']
        _month = request.form['month']
        _year = request.form['year']
        _dob = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        _address = request.form['address']
        _mobile = request.form['mobile_number']
        _email = request.form['email']

        # validate the received values
        if _name and _email and _field and _address:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "update doctor set name=%s,field=%s,dob=%s,address=%s,mobile=%s,email=%s where doctorID=%s;"


            cursor.execute(query, (_name,_field,_dob,_address,_mobile,_email,_id))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/showViewUpdateDoctor')
            else:
                print("111111111")
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


#create medical report
@app.route('/createMedReport', methods=['POST', 'GET'])
def createMedReport():
    try:
        #fetch form data
        _doctorName = request.form['doctorId']
        _doctorId=0
        _illCategory=request.form['illCategory']
        _illDetail=request.form['illDetail']
        _drugDetail=request.form['drugDetail']
        now = datetime.datetime.now()
        _date=now.strftime("%Y-%m-%d")
        _time=now.strftime("%H:%M")
        _patientId = session["userID"]

        # validate the received values
        if _patientId and  _illCategory and _date and _time:

            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createReport', (_patientId,_doctorId,_doctorName,_illCategory,_illDetail,_drugDetail,_date,_time))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/showPatientReport')
            else:
                return render_template('error.html', error=str(data[0]))
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

#view report
@app.route('/viewReport',methods=['POST','GET'])
def viewReport():

    try:
        #fetch form data
            _patientId = session["userID"]
            _reportId=request.form['reportID']
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_viewReport',(_reportId,))
            wishes = cursor.fetchall()
            wishes_dict = []

            #set data as json format
            for wish in wishes:
                wish_dict = {
                        'id': wish[0],
                        'patienID': wish[1],
                        'doctorID': wish[2],
                        'doctorName': wish[3],
                        'IllnessCategory':wish[4],
                        'Date': wish[5],
                        'time': wish[6],
                        'IllnessDetail': wish[7],
                        'DrugDetail': wish[8],
                    }
                wishes_dict.append(wish_dict)

            session['data'] = wish_dict
            return json.dumps(wish_dict)

    except Exception as e:
        return render_template('error.html', error = str(e))




@app.route('/addDrug', methods=['POST', 'GET'])
def addDrug():
    try:
        _drugname = request.form['drugName']
        _brandname=request.form['brandName']
        _day = request.form.get('day')
        _month = request.form.get('month')
        _year = request.form['year']
        _expire = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        _amount = request.form['amount']
        _price = request.form['price']



        # validate the received values
        if _drugname and  _brandname and _expire and _amount and _price:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            #_hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_addDrug', (_drugname,_brandname,_expire,_amount,_price))
            data = cursor.fetchall()


            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'Drug added successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/viewDrug',methods=['POST','GET'])
def viewDrug():

    try:
        #fetch form data

            _drugname = request.form['drugName']
            con = mysql.connect()
            cursor = con.cursor()
            query = "select * from drug where drugName=%s;"

            cursor.execute(query, (_drugname))
            wishes = cursor.fetchall()
            wishes_dict = []
            # year=wishes[0][3].year
            # print year

            #set data as json format
            for wish in wishes:
                wish_dict = {
                        'id': wish[0],
                        'drugName': wish[1],
                        'drugBrand': wish[2],
                        'year': wish[3].year,
                        'month':wish[3].month,
                        'day':wish[3].day,
                        'amount':wish[4],
                        'price': wish[5],
                    }
                wishes_dict.append(wish_dict)
            print wish_dict
            session['data'] = wish_dict
            return json.dumps(wish_dict)

    except Exception as e:
        return render_template('error.html', error = str(e))

#update drug detail
@app.route('/updateDrug', methods=['POST', 'GET'])
def updateDrug():
    try:
        _drugname = request.form['drugName']
        _brandname=request.form['brandName']
        _day = request.form.get('day')
        _month = request.form.get('month')
        _year = request.form['year']
        _expire = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        _amount = request.form['amount']
        _price = request.form['price']



        # validate the received values
        if _drugname and  _brandname and _expire and _amount and _price:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            query = "update drug set brandName=%s,expireDate=%s,amount=%s,price=%s where drugName=%s;"

            cursor.execute(query, (_brandname, _expire, _amount, _price,_drugname))
            data = cursor.fetchall()


            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'Drug updated successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()



#get doctor name from database for fetch in dropdown button
@app.route('/getDoctor', methods=['POST', 'GET'])
def getDoctor():
    try:

        # All Good, let's call MySQL
            con = mysql.connect()
            cursor = con.cursor()
            query = "SELECT name FROM doctor;"

            cursor.execute(query)
            wishes = cursor.fetchall()
            wishes_dict = [{}]
            count=0
            for wish in wishes:
                count+=1
                k="doc"+str(count)
                wishes_dict[0][k] = wish[0]

            return json.dumps(wishes_dict[0])

    except Exception as e:
        return render_template('error.html', error = str(e))

#get doctor NIC number to fetch data in dropdown button
@app.route('/getDoctorNIC', methods=['POST', 'GET'])
def getDoctorNIC():
    try:
        # All Good, let's call MySQL
            con = mysql.connect()
            cursor = con.cursor()
            # cursor.callproc('sp_GetDoctor' )
            query = "SELECT NIC FROM doctor;"

            cursor.execute(query)
            wishes = cursor.fetchall()
            wishes_dict = [{}]
            count=0
            for wish in wishes:
                count+=1
                k="doc"+str(count)
                wishes_dict[0][k] = wish[0]


            return json.dumps(wishes_dict[0])

    except Exception as e:
        return render_template('error.html', error = str(e))

#get patient NIC number for fetch in dropdown
@app.route('/getNICNumber', methods=['POST', 'GET'])
def getNICNumber():
    try:
        # All Good, let's call MySQL
            con = mysql.connect()
            cursor = con.cursor()
            # cursor.callproc('sp_GetDoctor' )
            query = "SELECT NIC FROM patient;"

            cursor.execute(query)
            wishes = cursor.fetchall()

            wishes_dict = [{}]
            count=0
            for wish in wishes:
                count+=1
                k="doc"+str(count)
                wishes_dict[0][k] = wish[0]


            return json.dumps(wishes_dict[0])

    except Exception as e:
        return render_template('error.html', error = str(e))

#get report id to fetch in dropdown
@app.route('/getReportID', methods=['POST', 'GET'])
def getReportID():
    try:
            patientid=session['userID']

            # All Good, let's call MySQL
            con = mysql.connect()
            cursor = con.cursor()
            # cursor.callproc('sp_GetDoctor' )
            query = "SELECT reportID FROM report where patientID=%s"

            cursor.execute(query, (patientid))

            # cursor.execute(query)
            wishes = cursor.fetchall()
            wishes_dict = [{}]
            count=0
            for wish in wishes:
                count+=1
                k="doc"+str(count)
                wishes_dict[0][k] = wish[0]
            return json.dumps(wishes_dict[0])

    except Exception as e:
        return render_template('error.html', error = str(e))

#get Drug name to fetch in dropdown
@app.route('/getDrugName', methods=['POST', 'GET'])
def getDrugName():
    try:
            # All Good, let's call MySQL
            con = mysql.connect()
            cursor = con.cursor()
            query = "SELECT drugName FROM drug"

            cursor.execute(query,)
            wishes = cursor.fetchall()
            wishes_dict = [{}]
            count=0
            for wish in wishes:
                count+=1
                k="doc"+str(count)
                wishes_dict[0][k] = wish[0]
            return json.dumps(wishes_dict[0])

    except Exception as e:
        return render_template('error.html', error = str(e))



if __name__ == "__main__":
    app.run(port=5002)
