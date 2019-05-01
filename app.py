from flask import Flask, render_template, json, request,redirect,session,url_for,g
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
import cv2
import numpy as np
import time



mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'smartmedi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showDoctorHome')
def showDoctorHome():
    return render_template('doctorhome.html')


@app.route('/showAddPatient')
def showAddPatient():
    return render_template('addpatientmode.html')

@app.route('/showAddMember')
def showAddMember():
    return render_template('addpatient.html')

@app.route('/showRegisterDoctor')
def showRegisterDoctor():
    return render_template('registerDoctor.html')


@app.route('/showAddDrug')
def showAddDrug():
    return render_template('addDrug.html')

@app.route('/show')
def show():
    return render_template('indexnew.html')





@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')

@app.route('/userHome')
def userHome():
    return render_template('userHome.html')
    #if session.get('user'):
        #return render_template('userHome.html')
    #else:
        #return render_template('error.html',error = 'Unauthorized Access')


@app.route('/showViewPatient')
def showviewPatient():
    return render_template('viewpatient.html')






@app.route('/showViewHome')
def showviewHome():
    return render_template('viewHome.html')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        

        
        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        #print data
        #print
        


        if len(data) > 0:
            if (str(data[0][3])==_password):
                #session['user'] = data[0][0]
                return redirect('/showDoctorHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
            

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            #_hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()


@app.route('/registerDoctor',methods=['POST','GET'])
def registerDoctor():
    print "Its ok"
    try:
        _name = request.form['inputName']
        #print("heloo 1")
       # _email = request.form['inputEmail']
        print("heloo 2")
        _field = request.form['field']
        print("heloo 3")
        print("hel 4")
        _day = request.form.get('day')
        _month = request.form.get('month')
        _year = request.form['year']
        print("heloo 5")
        _dob = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        print ('fff')
        _address = request.form['address']
        _mobile = request.form['mobile_number']
        _email=request.form['email']
        print("kkkkkkkkk")
        #_password=request.form['password1']
       # _con_password=request.form['password2']
        print(_name,_field,_dob,_address,_mobile,_email)
        print(_email)


        # validate the received values
        if _name and _email:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            print("hhhhhhhhhhhhhhhhhh")
            #cursor.callproc('sp_registerDoctor', (_name,_field,_dob,_address,_mobile,_email))
            #cursor.callproc('sp_registerDoctor', ("a","b","c","d",_mobile,_email))
            # cursor.callproc('sp_addPatient', (_name, _gender, _dob, _NIC, _mobile, _address, _info, _bloodgroup))
            # data = cursor.fetchall()
            query = "insert into doctor (name,field,dob,address,mobile,email) values (%s,%s,%s,%s,%s,%s)"

            cursor.execute(query, (_name,_field,_dob,_address,_mobile,_email))
            data = cursor.fetchall()
            print("gggggggggg")
            ##################################################



            ########################################################
            print("hello 1111")
            #cursor.execute("INSERT INTO 'patientdemo'('name','email','gender') VALUES (%s,%s,%s)",(_name,_email,_gender))
            print("wwwwwwwww")

            print("xxxxxxxxx")

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'Doctor Register successfully !'})
            else:
                print("111111111")
                return json.dumps({'error': str(data[0])})
        else:
            print("gooooooo")
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        print("purijala")
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/addMember',methods=['POST','GET'])
def addMember():
    print("hello")
    try:
        patientName = request.form['patient_name']
        gender = request.form.get('gender')
        print(str(gender))
        mobile = request.form['mobile_number']
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form['year']
        dob=str(day)+"-"+str(month)+"-"+str(year)
        print(dob)
        address = request.form['address']
        email = request.form['email']
        info = request.form['textarea']
        typeofapp=[]
        if request.form.get('test1'):
            typeofapp.append[str.test1]

            # match with pairs
        if request.form.get('test1'):
            typeofapp.append[str.test2]

        if request.form.get('test1'):
            typeofapp.append[str.test3]

        if request.form.get('test1'):
            typeofapp.append[str.test4]

        print(typeofapp)

        # validate the received values
        if patientName and gender and mobile:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()

            query = "insert into patient (fullname,gender,,mobileno,address,email) values (%s,%s,%s,%s,%s)"

            cursor.execute(query, (patientName,gender,mobile,address,email))

            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()




@app.route('/addPatient', methods=['POST', 'GET'])
def addPatient():

    try:
        _name = request.form['inputName']
        print("heloo 1")
       # _email = request.form['inputEmail']
        print("heloo 2")
        _gender = request.form['gender']
        print("heloo 3")
        print(_gender)
        _bloodgroup=request.form['bloodgroup']
        print(_bloodgroup)
        print("hel4")
        _day = request.form.get('day')
        _month = request.form.get('month')

        _year = request.form['year']
        print("heloo 5")
        _dob = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        print ('fff')
        _NIC=request.form['inputNIC']
        print _NIC[:-1]

        print "vaani"
        _address = request.form['address']
        _mobile = request.form['mobile_number']
        _info = request.form['textarea']



        # validate the received values
        if _name and  _gender and _dob and _mobile and _NIC and _address:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            #_hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_addPatient', (_name,_gender,_dob,_NIC,_mobile,_address,_info,_bloodgroup))
            data = cursor.fetchall()

            ##################################################

            #import cv2
            #import numpy as np

            faceDetect = cv2.CascadeClassifier("C:\Python27\Scripts\SMARTMEDI\static\js\haarcascade_frontalface_default.xml");
            cam = cv2.VideoCapture(0);


            sampleNum = 0

            while (True):
                ret, img = cam.read();
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5);
                for (x, y, w, h) in faces:
                    sampleNum += 1
                    cv2.imwrite("C:/Python27/Scripts/SMARTMEDI/dataSet/User." +_NIC[:-1] + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)
                    cv2.waitKey(100);

                cv2.imshow("Face", img);
                cv2.waitKey(1);
                if (sampleNum > 20):
                    break

            cam.release()

            # cv2.destroyAllWindow()

            # cam.release()
            # cv2.destroyAllWindow()

            ########################################################
            print("hello 1111")
            #cursor.execute("INSERT INTO 'patientdemo'('name','email','gender') VALUES (%s,%s,%s)",(_name,_email,_gender))
            print("wwwwwwwww")

            print("xxxxxxxxx")

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'Patient created successfully !'})
            else:
                print("111111111")
                return json.dumps({'error': str(data[0])})
        else:
            print("gooooooo")
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()



@app.route('/addDrug', methods=['POST', 'GET'])
def addDrug():
    try:
        _drugname = request.form['drugName']
        _brandname=request.form['brandName']
        _day = request.form.get('day')
        _month = request.form.get('month')
        _year = request.form['year']
        _expire = str(str(_year) + "-" + str(_month) + "-" + str(_day))
        print _expire
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
                print("111111111")
                return json.dumps({'error': str(data[0])})
        else:
            print("gooooooo")
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/viewHome',methods=['POST','GET'])
def viewHome():
    # print "jjjjjj"

    #print _name
    # session['my_var'] = _name
    #g.a="sangi"
    # return redirect(url_for('viewPatient'))
    try:

        ################################################################


        #############################################################
            #print g.a
            # my_var = session.get('my_var', None)
            # print my_var
            #print g.a
            #_user = session.get('user')
            #print(k)
            #_name = request.form['patient_name']
            #print _name
            #print "j1"
            _name = request.form['inputNIC']
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetPatient',(_name,))
            #print "j2"
            wishes = cursor.fetchall()

            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'id': wish[0],
                        'name': wish[1],
                        'gender': wish[2],
                        'dob': wish[3],
                        'mobile': wish[4],
                        'address': wish[5],
                        'email': wish[6],
                        'info': wish[7],
                    'blood': wish[9]}
                wishes_dict.append(wish_dict)

            print(wishes_dict)
            #jsondata=str(wish_dict)
            #print jsondata
            session['data'] = wish_dict
            #print session['data']
            return json.dumps(wishes_dict)
            #return render_template('view.html')
           #return redirect('/dataRender')


    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/dataRender')
def dataRender():
    print "hello"
    print session['data']
    return render_template('view.html')




@app.route('/viewPatient', methods=['POST', 'GET'])
def viewPatient():
    try:
            #print g.a
            my_var = session.get('my_var', None)
            print my_var
            #print g.a
            #_user = session.get('user')
            #print(k)
            #_name = request.form['patient_name']
            #print _name
            #print "j1"
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetPatient',(my_var,))
            #print "j2"
            wishes = cursor.fetchall()

            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'id': wish[0],
                        'name': wish[1],
                        'gender': wish[2],
                        'dob': wish[3],
                        'mobile': wish[4],
                        'address': wish[5],
                        'email': wish[6],
                        'info': wish[7],
                    'blood': wish[9]}
                wishes_dict.append(wish_dict)

            print(wishes_dict)

            return json.dumps(wishes_dict)

    except Exception as e:
        return render_template('error.html', error = str(e))





if __name__ == "__main__":
    app.run(port=5002)
