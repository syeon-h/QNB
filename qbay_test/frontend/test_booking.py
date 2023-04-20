from seleniumbase import BaseCase
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User, create_listing

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndHomePageTest(BaseCase):

    def test_booking_1(self, *_):
        """
        Testing first requirement: A user can book
        a listing. Using input partitioning
        input coverage testing.
        """

        # open register page
        self.open(base_url + '/register')
        # register
        self.type("#email", "testtest12348@email.com")
        self.type("#name", "user2022")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # login
        # fill email and password
        self.type("#email", "testtest12348@email.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # open booking page
        self.open(base_url + '/booking')
        # fill in fields with valid values
        self.type("#listing_id", "1")
        self.type("#date", "12-12-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a success
        self.assert_element("#welcome-header")
        self.assert_text("Welcome user2022 !", "#welcome-header")

    def test_booking_2(self, *_):
        """
        Testing second requirement: A user cannot
        book his/her listing. Using input partitioning
        input coverage.
        """

        # open register page
        self.open(base_url + '/register')
        # register
        self.type("#email", "testtest12349@email.com")
        self.type("#name", "user2022")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # login
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testtest12349@email.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # create own listing
        self.open(base_url + '/listcreate')
        # fill in fields with valid values
        self.type("#title", "suitable title new new")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "10")
        self.type("#email", "testtest12349@email.com")
        # click submit
        self.click('input[type="submit"]')

        # book own listing
        self.open(base_url + '/booking')
        # choose newest id
        self.type("#listing_id", "11")
        self.type("#date", "12-13-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a failure
        self.assert_element("#message")
        self.assert_text("Booking failed.", "#message")

        # book different listing
        self.open(base_url + '/booking')
        # choose different id
        self.type("#listing_id", "2")
        self.type("#date", "12-13-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a success
        self.assert_element("#welcome-header")
        self.assert_text("Welcome user2022 !", "#welcome-header")

    def test_booking_3(self, *_):
        """
        Testing third requirement: A user cannot
        book a listing that costs more than
        his/her balance. Using shotgun input
        coverage testing.
        """

        # open register page
        self.open(base_url + '/register')
        # register
        self.type("#email", "testtest123410@email.com")
        self.type("#name", "user2022")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # login
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testtest123410@email.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # book high price listing
        self.open(base_url + '/booking')
        # fill in fields with valid values
        self.type("#listing_id", "8")
        self.type("#date", "12-14-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a failure
        self.assert_element("#message")
        self.assert_text("Booking failed.", "#message")

        # book high price listing
        self.open(base_url + '/booking')
        # fill in fields with valid values
        self.type("#listing_id", "6")
        self.type("#date", "12-14-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a failure
        self.assert_element("#message")
        self.assert_text("Booking failed.", "#message")

        # book lower price listing
        self.open(base_url + '/booking')
        # fill in fields with valid values
        self.type("#listing_id", "3")
        self.type("#date", "12-14-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a success
        self.assert_element("#welcome-header")
        self.assert_text("Welcome user2022 !", "#welcome-header")

    def test_booking_4(self, *_):
        """
        Testing fourth requirement: A user cannot
        book a listing that is already booked with
        the overlapping dates. Using input
        partitioning input coverage.
        """

        # open register page
        self.open(base_url + '/register')
        # register
        self.type("#email", "testtest123411@email.com")
        self.type("#name", "user2022")
        self.type("#password", "123@Aa")
        self.type("#password2", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # login
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testtest123411@email.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # book listing
        self.open(base_url + '/booking')
        # use previous fields
        self.type("#listing_id", "11")
        self.type("#date", "12-12-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a success
        self.assert_element("#welcome-header")
        self.assert_text("Welcome user2022 !", "#welcome-header")

        # book previous booking
        self.open(base_url + '/booking')
        # use different fields
        self.type("#listing_id", "11")
        self.type("#date", "12-12-2024")
        # click submit
        self.click('input[type="submit"]')

        # check if booking was a failure
        self.assert_element("#message")
        self.assert_text("Booking failed.", "#message")

    def test_booking_5(self, *_):
        """
        Testing fifth requirement: A booked listing will 
        show up on the user's home page. Using exhaustive
        input coverage.
        """

        # login
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testtest12348@email.com")
        self.type("#password", "123@Aa")
        # click enter button
        self.click('input[type="submit"]')

        # check if booked listing appears

        self.assert_element("#Booking")
        self.assert_text("id: 1 date: 2024-12-12 00:00:00 update", "#Booking")