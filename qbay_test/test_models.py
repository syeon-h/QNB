from qbay.models import register, login, unique_id, update_user
from qbay.models import create_listing, update_listing, valid_date
from qbay.models import Listing, valid_date
from datetime import datetime


def test_create_listing_title_parameter():
    '''
        Testing the title parameter on each payload 
    '''
    file = open("payload.txt")
    for payload in file.readlines():
        create_listing(payload, "Description", 50, "123@Aa")


def test_create_listing_description_parameter():
    '''
        Testing the desription parameter on each payload 
    '''
    file = open("payload.txt")
    for payload in file.readlines():
        create_listing("House", payload, 50, "123@Aa")


def test_create_listing_price_parameter():
    '''
        Testing the price parameter on each payload 
    '''
    file = open("payload.txt")
    for payload in file.readlines():
        create_listing("House", "Description", payload, "123@Aa")


def test_create_listing_email_parameter():
    '''
        Testing the email parameter on each payload 
    '''
    file = open("payload.txt")
    for payload in file.readlines():
        create_listing("House", "Description", 50, payload)


def test_register_user_parameter():
    '''
        Testing the user parameter on each payload 
    '''
    file = open("payload.txt")
    for payload in file.readlines():
        register(payload, "workingEmail435@email.com", "123@Aa")


def test_register_email_parameter():
    '''
        Testing the email parameter on each payload 
    '''
    file = open("payload.txt")
    for payload in file.readlines():
        register("workingg userr", payload, "123@Aa")


def test_register_password_parameter():
    '''
        Testing the password parameter on each payload 
    '''
    file = open("payload.txt")
    for payload in file.readlines():
        register("workinggg userrr", "workingEmail435@email.com", payload)


def test_r1_1_user_regiser(): 
    '''
    Testing R1-1 : email and password cannot be empty 
    '''
    assert register('u00', '', '123@Aa') is False
    assert register('u00', 'test1@test.com', '') is False
    assert register('name', 'test54@test.com', '123@Aa') is True


def test_r1_2_user_regiser(): 
    '''
    Testing R1-2 : a user is unqiely identified by id.   
    '''

    user = login('test54@test.com', '123@Aa') 
    assert user is not None 
    assert unique_id(user.id) is True 


def test_r1_3_user_regiser(): 
    '''
    Testing R1-3 : the email has to follow RFC5322  
    '''
    assert register('u00', 'test0@test', '123@Aa') is False  
    assert register('u00', 'test0"@test.com', '123@Aa') is False 


def test_r1_4_user_regiser(): 
    '''
    Testing R1-4 : password has to meet the required complexity 
    minimum length 6
    at least one upper case, lower case, and special charcter 
    '''

    assert register('u00', 'test1@test.com', '12@Aa') is False
    assert register('u00', 'test2@test.com', '123@AA') is False 
    assert register('u00', 'test3@test.com', '123@aa') is False 
    assert register('u00', 'test4@test.com', '123Aaa') is False


def test_r1_5_user_regiser(): 
    '''
    Testing R1-5 : user name has to be non-empty
    alphanumeric-only 
    space is not allowed as the prefix or suffix 
    '''

    assert register('', 'test1@test.com', '123@Aa') is False
    assert register('u0@', 'test2@test.com', '123@Aa') is False 
    assert register(' u00', 'test3@test.com', '123@Aa') is False 
    assert register('u00 ', 'test4@test.com', '123@Aa') is False


def test_r1_6_user_register(): 
    '''
    Testing R1-6 : user name has to be logner than 2 less than 20 
    '''

    assert register('u0', 'test1@test.com', '123@Aa') is False
    assert register(
        'u1234567890123456789', 'test2@test.com', '123@Aa') is False


def test_r1_7_user_register(): 
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('u00', 'test0@test.com', 'Testing123!') is True
    assert register('u00', 'test1@test.com', '123@Aa') is True
    assert register('u00', 'test2@test.com', '123@Aa') is True
    assert register('u01', 'test1@test.com', '123@Aa') is False


def test_r1_8_user_regiser(): 
    '''
    Testing R1-8 : shipping adress is empty at the regisration.    
    '''

    user = login('test54@test.com', '123@Aa') 
    assert user is not None 
    assert user.billing_address == ''


def test_r1_9_user_regiser(): 
    '''
    Testing R1-9 : postal code is empty at the regisration.    
    '''

    user = login('test54@test.com', '123@Aa') 
    assert user is not None 
    assert user.postal_code == ''


def test_r1_10_user_regiser(): 
    '''
    Testing R1-10 : balance should be initialized as 100.    
    '''

    user = login('test1@test.com', '123@Aa') 
    assert user is not None 
    assert user.balance == 100.0


def test_r2_2_login():
    '''
    Testing R2-2:The login function should check if the supplied 
      inputs meet the same email/password requirements as above, before 
    checking the database.
      (will be tested after the previous test)
    '''
    user = login('invalidemail', 'validPass!')
    assert user is None

    user = login('validemail@email.com', 'invalidpass!')
    assert user is None

    user = login('invalidemail', 'invalidpass!')
    assert user is None


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    (will be tested after the previous test, so we already have u0, 
      u1 in database)
    '''

    user = login('test0@test.com', 'Testing123!')
    assert user is not None
    assert user.username == 'u00'

    user = login('test0@test.com', 'invalidpass')
    assert user is None

    user = login('invalidemail', 'Testing123!')
    assert user is None


def test_r3_1_update_user():
    '''
    Testing R3-1: A user is only able to update 
      his/her user name, user email, billing address, and postal code
    '''
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'B4A 3A4') is True
    assert update_user(
        1, 'updateduser', 'test54@test.com', '', 'B4A 3A4') is True
    assert update_user(
        1, 'updateduser', '', 
        '200 Test Billing Address', 'B4A 3A4') is True
    assert update_user(
        1, 'updateduser', '', '', 'B4A 3A4') is True


def test_r3_2_update_user():
    '''
    Testing R3-2: postal code should be non-empty, alphanumeric-only, 
      and no special characters such as !
    '''
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', '') is False
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'A2A 42!') is False
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is True


def test_r3_3_update_user():
    '''
    Testing R3-3: Postal code has to be a valid Canadian postal code
    Valid Canadian postcode:
      - in the format A1A 1A1, where A is a letter and 1 is a digit.
      - a space separates the third and fourth characters.
      - do not include the letters D, F, I, O, Q or U.
      - the first position does not make use of the letters W or Z.
    '''
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'B1A 1T1') is True
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'B1A1T1') is False
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'D1F 1Q1') is False
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'W1A 1T1') is False
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'Z1A 1T1') is False


def test_r3_4_update_user():
    '''
    Testing R3-4: User name follows the requirements above
    '''
    assert update_user(
        1, 'updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is True
    assert update_user(
        1, 'updated user', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is True
    assert update_user(
        1, '', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is False
    assert update_user(
        1, 'u', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is False
    assert update_user(
        1, 'updateduserrrrrrrrrrrrr', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is False
    assert update_user(
        1, ' updateduser', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is False
    assert update_user(
        1, 'updateduser ', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is False
    assert update_user(
        1, ' updateduser ', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is False
    assert update_user(
        1, 'updateduser!!!!', 'test54@test.com', 
        '200 Test Billing Address', 'A1A 1A1') is False


def test_r4_1_create_listing():
    '''
    Testing R4-1: The title of the product has to be 
      alphanumeric-only, and space allowed only if it 
        is not as prefix and suffix, and non-empty.
    '''

    assert create_listing('suitable title', 
                          'Suitable description for the listing', 
                          100.00, 'test0@test.com') is True
    assert create_listing('suitable1', 'Suitable description for the listing', 
                          100.00, 'test0@test.com') is True
    assert create_listing('123', 'Suitable description for the listing', 
                          100.00, 'test0@test.com') is True
    assert create_listing('suitable', 'Suitable description for the listing', 
                          100.00, 'test0@test.com') is True
    assert create_listing('', 
                          'Suitable description for the listing', 
                          100.00, 'test0@test.com') is False
    assert create_listing('Hous@', 
                          'Suitable description for the listing', 100.00, 
                          'test0@test.com') is False
    assert create_listing(' ouse', 
                          'Suitable description for the listing', 100.00, 
                          'test0@test.com') is False
    assert create_listing('Hous ', 
                          'Suitable description for the listing', 100.00, 
                          'test0@test.com') is False


def test_r4_2_create_listing():
    '''
    Testing R4-2: The title of the product has to be 
      no longer than 80 characters
    '''
    assert create_listing('This listing title needs \
      to be over 80 characters in order to return false \
        for this test', 'Suitable description for the \
          listing', 100.00, 'test0@test.com') is False
    assert create_listing('suitable2', 'Suitable description for the \
          listing', 100.00, 'test0@test.com') is True


def test_r4_3_create_listing():
    '''
    Testing R4-3: The description can be arbitrary
      characters, with minimum length 20 characters and
        maximum 2000 characters
    '''

    assert create_listing('House', 
                          'unsuitable', 
                          100.00, 'test0@test.com') is False
    assert create_listing('House', 
                          'suitable description of 20 or more characters', 
                          100.00, 'test0@test.com') is True


def test_r4_4_create_listing():
    '''
    Testing R4-4: Description has to be longer than the 
      product's title.
    '''

    assert create_listing('title name of at least 20 characters longer\
                          than description', 'this title is not long enough',
                          100.00, 'test0@test.com') is False
    assert create_listing('suitable3',
                          'this description is longer than the title',
                          100.00, 'test0@test.com') is True


def test_r4_5_create_listing():
    '''
    Testing R4-5: Price has to be of range [10, 10000].
    '''

    assert create_listing('House', 
                          'Suitable description for the listing', 9.00, 
                          'test0@test.com') is False
    assert create_listing('House', 
                          'Suitable description for the listing', 
                          10001.00, 'test0@test.com') is False
    assert create_listing('suitable4', 
                          'Suitable description for the listing', 
                          1000.00, 'test0@test.com') is True


def test_r4_6_create_listing():
    '''
    Testing R4-6: last_modified_date must be after 
      2021-01-02 and before 2025-01-02.
    '''

    d1 = datetime(2020, 1, 2)
    d2 = datetime(2026, 1, 2)
    assert valid_date(datetime.now()) is True
    assert valid_date(d1) is False
    assert valid_date(d2) is False


def test_r4_7_create_listing():
    '''
    Testing R4-7: owner of corresponding product must exist
    '''

    assert create_listing('House', 
                          'Suitable description for the listing', 100.00, 
                          'test5@test.com') is False
    assert create_listing('suitable5', 
                          'Suitable description for the listing', 100.00, 
                          'test0@test.com') is True


def test_r4_8_create_listing():
    '''
    Testing R4-8: user cannot create products with the
      same title
    '''

    assert create_listing('House5', 
                          'Suitable description for the listing', 100.00, 
                          'test1@test.com') is True
    assert create_listing('House5', 
                          'Suitable description for the listing', 100.00, 
                          'test1@test.com') is False


def test_r5_1_update_listing():
    '''
    Testing R5-1: all atributes can be updated except
      owner_id and last_modified date
    '''

    assert update_listing('House', 'House2', 
                          'New Suitable description for the listing', 
                          150.00) is True


def test_r5_2_update_listing():
    '''
    Testing R5-2: price can only be increased, not decreased
    '''

    assert update_listing('House2', 'House2', 
                          'New Suitable description for the listing', 
                          200.00) is True
    assert update_listing('House2', 'House2', 
                          'New Suitable description for the listing', 
                          150.00) is False


def test_r5_3_update_listing():
    '''
    Testing R5-3: last_modified_date should be updated
    '''

    update_listing('House2', 'House2', 
                   'New Suitable description for the listing', 250.00)
    listing = Listing.query.filter_by(title='House2').all()
    
    # ensure date has been updated
    def updated(date):
        if date:
            return True
    assert updated(listing[0].last_modified_date) is True


def test_r5_4_update_listing():
    '''
    Testing R5-4: make sure that attributes follow the same
      requirements as above
    '''

    assert update_listing('House2', '', 
                          'Suitable description for the listing', 
                          250.00) is False
    assert update_listing('House2', 'Hous@', 
                          'Suitable description for the listing', 
                          250.00) is False
    assert update_listing('House2', ' ouse', 
                          'Suitable description for the listing', 
                          250.00) is False
    assert update_listing('House2', 'Hous ', 
                          'Suitable description for the listing', 
                          250.00) is False
    assert update_listing('House2', 
                          'This listing title needs to be over 80 characters \
                          in order to return false for this test', 
                          'Suitable description for the listing', 
                          250.00) is False
    assert update_listing('House2', 'House', 'unsuitable', 
                          250.00) is False
    assert update_listing('House2', 'title name of at least 20 \
                          characters long like the description', 
                          'this title is not long enough', 
                          250.00) is False
    assert update_listing('House2', 'House', 
                          'Suitable description for the listing', 
                          9.00) is False
    assert update_listing('House2', 'House', 
                          'Suitable description for the listing', 
                          10001.00) is False