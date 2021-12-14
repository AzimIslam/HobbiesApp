# Commented out for deployment
""" from django.test import LiveServerTestCase
from selenium import webdriver
from .models import User, Hobby
from django.contrib.auth.hashers import make_password
import time
from selenium.common.exceptions import NoSuchElementException 

class SeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report = {
            "Creates a user account for the hobby app": "FAILED",
            "User logs in to hobbies app successfully": "FAILED",
            "Editing user date of birth": "FAILED",
            "Adding hobby to hobby list": "FAILED",
            "Removing hobby from hobby list": "FAILED"
        }
        cls.selenium = webdriver.Chrome()
        # cls.selenium = webdriver.Firefox() --> uncomment for Firefox
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        print("\n----------------- Test Report -----------------")
        for key in cls.report:
            print(f"\n{key}\t{cls.report[key]}")
        super().tearDownClass()

    def setUp(self):
        Hobby.objects.create(name="Cars", description="A car (or automobile) is a wheeled motor vehicle used for transportation. Most definitions of cars say that they run primarily on roads, seat one to eight people, have four wheels, and mainly transport people rather than goods.")
        Hobby.objects.create(name="Hiking", description="Hiking is a long, vigorous walk, usually on trails or footpaths in the countryside. Walking for pleasure developed in Europe during the eighteenth century.[1] Religious pilgrimages have existed much longer but they involve walking long distances for a spiritual purpose associated with specific religions. ")
        Hobby.objects.create(name="Video Games", description="A video game[a] or computer game is an electronic game that involves interaction with a user interface or input device – such as a joystick, controller, keyboard, or motion sensing device – to generate visual feedback.")

    def test_removeHobby(self):
        ''' Removing hobby from hobby list '''
        User.objects.create(email="test3@email.com", username="test05", first_name="Test", last_name="User", password=make_password("seleniumtest123"), date_of_birth="2001-08-20")

        self.selenium.get(self.live_server_url)

        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys("test05")
        time.sleep(1)
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys("seleniumtest123")
        time.sleep(1)
        self.selenium.find_element_by_class_name("btn-primary").click()
        time.sleep(1)
        self.selenium.get(self.live_server_url + "/api/hobby/Hiking")
        self.selenium.find_element_by_xpath('//button[text()="Add Hobbie"]').click()
        time.sleep(1)
        self.selenium.get(self.live_server_url + "/api/hobby/Cars")
        self.selenium.find_element_by_xpath('//button[text()="Add Hobbie"]').click()
        time.sleep(1)
        self.selenium.get(self.live_server_url + "/api/hobby/Video%20Games")
        self.selenium.find_element_by_xpath('//button[text()="Add Hobbie"]').click()
        time.sleep(1)

        self.selenium.get(self.live_server_url)

        self.selenium.find_element_by_xpath('//button[text()="Edit Profile"]').click()
        time.sleep(1)

        self.selenium.find_element_by_class_name("btn-danger").click()

        self.selenium.find_element_by_xpath('//button[text()="Save Changes"]').click()
        time.sleep(1)

        rows = self.selenium.find_elements_by_xpath ("//*[@class= 'table']/tbody/tr")

        self.assertEquals(len(rows), 2)
        self.report["Removing hobby from hobby list"] = "PASSED"

    def test_addHobby(self):
        ''' Adding hobby to hobby list '''
        test1 = False
        test2 = False
        test3 = False

        User.objects.create(email="test3@email.com", username="test04", first_name="Test", last_name="User", password=make_password("seleniumtest123"), date_of_birth="2001-08-20")

        self.selenium.get(self.live_server_url)

        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys("test04")
        time.sleep(1)
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys("seleniumtest123")
        time.sleep(1)
        self.selenium.find_element_by_class_name("btn-primary").click()
        time.sleep(1)
        self.selenium.get(self.live_server_url + "/api/hobby/Hiking")
        self.selenium.find_element_by_xpath('//button[text()="Add Hobbie"]').click()
        time.sleep(1)
        self.selenium.get(self.live_server_url)
        time.sleep(1)
        if self.selenium.find_element_by_xpath('//a[text()="Hiking"]').text == "Hiking":
            test1 = True

        self.selenium.get(self.live_server_url + "/api/hobby/Cars")
        self.selenium.find_element_by_xpath('//button[text()="Add Hobbie"]').click()
        time.sleep(1)
        self.selenium.get(self.live_server_url)
        time.sleep(1)
        if self.selenium.find_element_by_xpath('//a[text()="Cars"]').text == "Cars":
            test2 = True

        try:
            self.selenium.find_element_by_xpath('//a[text()="Video Games"]')
        except NoSuchElementException:
            test3 = True

        self.assertTrue(test1 and test2 and test3)
        self.report["Adding hobby to hobby list"] = "PASSED"


    def test_editDOB(self):
        ''' Editing user date of birth '''
        User.objects.create(email="test3@email.com", username="test03", first_name="Test", last_name="User", password=make_password("seleniumtest123"), date_of_birth="2001-08-20")

        self.selenium.get(self.live_server_url)
        time.sleep(1)

        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys("test03")
        time.sleep(1)

        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys("seleniumtest123")
        time.sleep(1)

        self.selenium.find_element_by_class_name("btn-primary").click()
        time.sleep(1)

        self.selenium.find_element_by_xpath('//button[text()="Edit Profile"]').click()
        time.sleep(1)
        self.selenium.execute_script('document.getElementById("date").value = "1999-01-01"')
        time.sleep(1)
        self.selenium.find_element_by_xpath('//button[text()="Save Changes"]').click()
        time.sleep(1)

        self.assertEquals(self.selenium.find_element_by_xpath('//p[text()="1999-01-01"]').text, "1999-01-01")
        self.report["Editing user date of birth"] = "PASSED"
        

    def test_login(self):
        ''' User logs in to hobbies app successfully '''

        User.objects.create(email="test2@email.com", username="test02", first_name="Test", last_name="User", password=make_password("seleniumtest123"), date_of_birth="2001-08-20")

        self.selenium.get(self.live_server_url)
        time.sleep(1)
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys("test02")
        time.sleep(1)
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys("seleniumtest123")
        time.sleep(1)
        self.selenium.find_element_by_class_name("btn-primary").click()
        time.sleep(1)
        self.assertEquals(self.selenium.find_element_by_class_name("navbar-brand").text, "Hobbies App")
        self.report["User logs in to hobbies app successfully"] = "PASSED"
        

    def test_createAccount(self):
        '''Creates a user account for the hobby app'''
        self.selenium.get(self.live_server_url +  "/register/")
        time.sleep(1)
        email_input = self.selenium.find_element_by_id("email")
        email_input.send_keys("test@email.com")
        time.sleep(1)
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys("test")
        time.sleep(1)
        fn_input = self.selenium.find_element_by_id("fName")
        fn_input.send_keys("Test")
        time.sleep(1)
        ln_input = self.selenium.find_element_by_id("surname")
        ln_input.send_keys("User")
        time.sleep(1)
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys("seleniumtest123")
        time.sleep(1)
        self.selenium.execute_script('document.getElementById("birthday").value = "2001-08-20"')
        time.sleep(1)
        self.selenium.find_element_by_class_name("btn-primary").click()
        time.sleep(1)
        self.assertEquals(self.selenium.find_element_by_class_name("navbar-brand").text, "Hobbies App")

        self.report["Creates a user account for the hobby app"] = "PASSED" """