from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    #Ensure that flask was set up correctly
    def test_index(self):
        tester=app.test_client(self)
        response=tester.get('/',content_type='html/text')
        self.assertEqual(response.status_code,200)

    #ensure that login page load correctly
    def test_login_page_loads(self):
        tester=app.test_client(self)
        response=tester.get('/',content_type='html/text')
        self.assertTrue(b'SmartMedi' in response.data)

    # view patient detail
    def test_correct_login(self):
        tester=app.test_client(self)
        response=tester.post(
            '/validateLogin',
            data=dict( _NIC="942033740v"),
            follow_redirects=True
        )
        self.assertIn(b'',response.data)

    #ensure login behaves correctly given the incorrect username password
    def test_incorrect_login(self):
        tester=app.test_client(self)
        response=tester.post(
            '/validateLogin',
            data=dict(inputEmail="jarsi@gmail.com",inputPassword="12"),
            follow_redirects=True
        )
        self.assertIn(b'SmartMedi Error',response.data)

    #ensure home page load correctly
    def test_home_page_loads(self):
        tester=app.test_client(self)
        response=tester.get('/show',content_type='html/text')
        self.assertTrue(b'We Provide the Best Medical Services.' in response.data)

    # ensure collect image page error because of session var
    def test_collectImage_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/showWebCam', content_type='html/text')
        self.assertTrue(b'you need to capture more than ten patient face images' in response.data)

    # ensure recognice page load correctly
    def test_recognice_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/showRecogPatient', content_type='html/text')
        self.assertTrue(b'Unauthorized Access' in response.data)

    #ensure logout behave correctly
    def test_logout(self):
        tester=app.test_client(self)
        tester.post(
            '/validateLogin',
            data=dict(inputEmail="jarsi@gmail.com",inputPassword="123"),
            follow_redirects=True
        )
        response=tester.get('/logout',follow_redirects=True)
        self.assertIn(b'SIGN UP WITH',response.data)

    if __name__=='__main__':
        unittest.main()