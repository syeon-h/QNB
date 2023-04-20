from seleniumbase import BaseCase 
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndHomePageTest(BaseCase):
    def test_r1_1_user_regiser(self, *_): 
        '''
        Testing R1-1 : email and password cannot be empty 
        Uses Black Box method of input coverage testing (input partition)
        '''
        # open register page
        self.open(base_url + '/register') 

        # Fill email with empty field and password non empty
        self.type("#email", "")
        self.type("#name", "user2022")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration failed cause the email field is empty
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 

        # Fill password with empty field and email non empty
        self.type("#email", "test1@test.com")
        self.type("#name", "u00")
        self.type("#password", "")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration can't be completed cause the pass 
        # field is empty
        self.assert_element("#message")
        self.assert_text("The passwords do not match", "#message")

        # open register page
        self.open(base_url + '/register') 

        # Fill email and password with empty field 
        self.type("#email", "")
        self.type("#name", "user2022")
        self.type("#password", "")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration failed cause the email field is empty
        self.assert_element("#message")
        self.assert_text("The passwords do not match", "#message")

        # Fill email and password with non empty field
        self.type("#email", "testtest123@email.com")
        self.type("#name", "user2022")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # see if it successfully registered
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testtest123@email.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome user2022 !", "#welcome-header")

    def test_r1_3_user_regiser(self, *_): 
        '''
        Testing R1-3 : the email has to follow RFC5322 
        Using Black Box method of output coverage testing 
        '''
        # open register page
        self.open(base_url + '/register') 
        # email that doesn't follow RFC5322
        self.type("#email", "notworkingemail")
        self.type("#name", "slamcode")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # email that doesn't work should output registration failed
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # email that doesn't follow RFC5322
        self.type("#email", "workingEmail@outlook.com")
        self.type("#name", "slamcodeee")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # email that does work should be able to login and output welcome 
        # message as the header
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "workingEmail@outlook.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome slamcodeee !", "#welcome-header")

    def test_r1_4_user_regiser(self, *_): 
        '''
        Testing R1-4 : password has to meet the required complexity 
        minimum length 6
        at least one upper case, lower case, and special charcter 
        Using Black Box method of output coverage testing 
        '''
        # open register page
        self.open(base_url + '/register') 
        # password that doesn't follow requirements
        self.type("#email", "workingEmail123@hotmail.com")
        self.type("#name", "slamcodeProject")
        self.type("#password", "1")
        self.type("#password2", "1")
        # click enter button
        self.click('input[type="submit"]')

        # password doesn't follow required complexity, 
        # should output error message
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # password that does follow requirements
        self.type("#email", "workingEmail123@hotmail.com")
        self.type("#name", "slamcodeProject")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # password that does work should output no error 
        # message and be allowed to login
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "workingEmail123@hotmail.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome slamcodeProject !", "#welcome-header")

    def test_r1_5_user_regiser(self, *_): 
        '''
        Testing R1-5 : user name has to be non-empty
        alphanumeric-only 
        space is not allowed as the prefix or suffix 
        Using Black Box method of Input Partition Testing
        '''
        # open register page
        self.open(base_url + '/register') 
        # user name being empty
        self.type("#email", "testingemail123@test.com")
        self.type("#name", "")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration didn't go through
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testingemail123@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("login failed", "#message")

        # open register page
        self.open(base_url + '/register') 
        # user name not being alphanumeric
        self.type("#email", "testingemail123@test.com")
        self.type("#name", "slamcode!")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration didn't go through
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # user name being alphanumeric
        self.type("#email", "testingemail123@test.com")
        self.type("#name", "slamcode")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration went through
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testingemail123@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome slamcode !", "#welcome-header")

        # open register page
        self.open(base_url + '/register') 
        # user name have space has prefix
        self.type("#email", "testingemail1234@test.com")
        self.type("#name", " slamcode")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration didn't go through
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # user name have space has suffix
        self.type("#email", "testingemail1234@test.com")
        self.type("#name", "slamcode ")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration didn't go through
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # user name being alphanumeric
        self.type("#email", "testingemail1234@test.com")
        self.type("#name", "slam code")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration went through
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testingemail1234@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome slam code !", "#welcome-header")

    def test_r1_6_user_register(self, *_): 
        '''
        Testing R1-6 : user name has to be longer than 2 less than 20
        Using Black Box method of input boundary testing (robustness)
        '''
        # open register page
        self.open(base_url + '/register') 
        # user name of length 1
        self.type("#email", "test101@test.com")
        self.type("#name", "u")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration failed 
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # user name of length 2
        self.type("#email", "test101@test.com")
        self.type("#name", "u0")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration failed 
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # user name of length 3
        self.type("#email", "test101@test.com")
        self.type("#name", "u01")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration succeeded
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test101@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome u01 !", "#welcome-header")

        # open register page
        self.open(base_url + '/register') 
        # user name of length 19
        self.type("#email", "test102@test.com")
        self.type("#name", "1234567891234567891")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration succeeded
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test102@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome 1234567891234567891 !", "#welcome-header")

        # open register page
        self.open(base_url + '/register') 
        # user name of length 20
        self.type("#email", "test101@test.com")
        self.type("#name", "12345678912345678910")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration failed 
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # open register page
        self.open(base_url + '/register') 
        # user name of length 21
        self.type("#email", "test101@test.com")
        self.type("#name", "123456789123456789101")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration failed 
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        
    def test_r1_7_user_register(self, *_): 
        '''
        Testing R1-7: If the email has been used, the operation failed.
        This test uses input partitioning: registered and not registered
        '''
        # open register page
        self.open(base_url + '/register') 
        # fill email that already been registered 
        self.type("#email", "test1@test.com")
        self.type("#name", "u00")

        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the registeration failed 
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # fill email that never used 
        self.type("#email", "test99@test.com")
        self.type("#name", "u99")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        self.click('input[type="submit"]') 

        # test if the registeration succeed 
        self.assert_element("#message")
        self.assert_text("Please login", "#message") 

    def test_r1_8_user_register(self, *_): 
        '''
        Testing R1-8 : shipping adress is empty at the regisration. 
        This test uses output partitioning: empty and edited address 
        '''
        # open login page
        self.open(base_url + '/login')
        self.type("#email", "test99@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]') 

        # open home page
        self.open(base_url) 
        # test if the shipping address is empty  
        self.assert_element("#profile")
        self.assert_text("shipping address: empty", "#profile") 
        
        # open login page
        self.open(base_url + '/profileupdate') 
        self.type("#name", "u99") 
        self.type("#postal_code", "A1A 1A1") 
        self.type("#billing_address", "200 Test Billing Address") 
        self.click('input[type="submit"]') 
        # test if the shipping address is not empty 
        self.assert_element("#profile")
        self.assert_text(
            "shipping address: 200 Test Billing Address", "#profile") 

    def test_r1_9_user_register(self, *_): 
        '''
        Testing R1-9 : postal code is empty at the regisration.    
        This test uses output partitioning: empty and edited postal code
        '''
        # open login page
        self.open(base_url + '/login')
        self.type("#email", "test99@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]') 
        
        # open home page
        self.open(base_url) 
        # test if the postal code is empty 
        self.assert_element("#profile")
        self.assert_text("postal code: A1A 1A1", "#profile") 

        self.open(base_url + '/logout')

        # open home page
        self.open(base_url + '/login')
        self.type("#email", "test1@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]') 
        # test if the postal code is empty 
        self.assert_element("#profile")
        self.assert_text("postal code: empty", "#profile") 

    def test_r1_10_user_register(self, *_): 
        '''
        Testing R1-10 : balance should be initialized as 100. 
        This test uses exhaustive output testing: 100
        ''' 
        # open login page
        self.open(base_url + '/login')
        self.type("#email", "test1@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]') 

        # open home page 
        self.open(base_url) 
        # test if the balance is 100.0  
        self.assert_element("#profile")
        self.assert_text("balance: 100.0", "#profile")

    def test_r2_1_login_success(self, *_):
        '''
        Testing R2-1: A user can log in using her/his email address 
          and the password.
        This test uses input partitioning: registered and not registered
        '''
        self.open(base_url + '/login') 
        # fill not registered email and password
        self.type("#email", "notregistered1@test.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # test if the login attempt failed 
        self.assert_element("#message")
        self.assert_text("login failed", "#message")

        # fill registered email and password
        self.type("#email", "test1@test.com")
        self.type("#password", "123@Aa")
        self.click('input[type="submit"]')

        # after clicking on the browser (the line above)
        # the front-end code is activated
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value. However, here we only want to test the
        # front-end, without running the backend logics.
        # so we patch the backend to return a specific user instance,
        # rather than running that program. (see @ annotations above)

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome u00 !", "#welcome-header")

    def test_r2_2_login_success(self, *_):
        '''
        Testing R2-2: The login function should check 
          if the supplied inputs meet the same email/password 
          requirements as above, before checking the database. 
        This test uses input boundary testing 
        '''
        # open login page
        self.open(base_url + '/login')
        # fill with incorrect email format 
        self.type("#email", "invalidemail")
        self.type("#password", "123@Aa")
        self.click('input[type="submit"]')

        # test if the login failed 
        self.assert_element("#message")
        self.assert_text("login failed", "#message") 

        # fill with empty email  
        self.type("#email", "")
        self.type("#password", "123@Aa")
        self.click('input[type="submit"]')

        # test if the login failed 
        self.assert_element("#message")
        self.assert_text("login failed", "#message") 

        # fill with incorrect password format 
        self.type("#email", "test1@test.com")
        self.type("#password", "invalidpass")
        self.click('input[type="submit"]')

        # test if the login failed 
        self.assert_element("#message")
        self.assert_text("login failed", "#message") 

        # fill with empty password  
        self.type("#email", "test1@test.com")
        self.type("#password", "")
        self.click('input[type="submit"]')

        # test if the login failed 
        self.assert_element("#message")
        self.assert_text("login failed", "#message") 
        
