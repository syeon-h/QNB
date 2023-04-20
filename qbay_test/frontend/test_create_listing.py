from seleniumbase import BaseCase
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndHomePageTest(BaseCase):

    def test_create_listing_r4_1(self, *_):
        """
        Input partitioning black box testing.

        Testing R4-1: The title of the product has to be 
        alphanumeric-only, and space allowed only if it 
        is not as prefix and suffix, and non-empty.
        """

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid title values
        self.type("#title", "suitable titleD")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid title values
        self.type("#title", "suitable12")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid title values
        self.type("#title", "125")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid title values
        self.type("#title", "suitableB")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect title values
        self.type("#title", "")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect title values
        self.type("#title", "Hous@")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect title values
        self.type("#title", " ouse")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect title values
        self.type("#title", "Hous ")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

    def test_create_listing_r4_2(self, *_):
        """
        Input partition black box testing.

        Testing R4-2: The title of the product has to be 
        no longer than 80 characters
        """

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect title values
        self.type("#title", "This listing title needs \
            to be over 80 characters in order to return \
                false for this test")
        self.type("#description", "Suitable \
        description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid title values
        self.type("#title", "suitableD")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    def test_create_listing_r4_3(self, *_):
        """
        Input partitioning black box testing.

        Testing R4-3: The description can be arbitrary
        characters, with minimum length 20 characters and
        maximum 2000 characters
        """

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect description values
        self.type("#title", "House")
        self.type("#description", "unsuitable")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid description values
        self.type("#title", "HouseG")
        self.type("#description", "suitable \
            description of 20 or more characters")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    def test_create_listing_r4_4(self, *_):
        """
        Input partitioning black box testing.

        Testing R4-4: Description has to be longer than the 
        product's title.
        """

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect description values
        self.type("#title", "title name of at least 20 \
            characters longer than description")
        self.type("#description", "this title is not long enough")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid description values
        self.type("#title", "suitableK")
        self.type("#description", "this description \
            is longer than the title")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    def test_create_listing_r4_5(self, *_):
        """
        Shotgun black box testing.

        Testing R4-5: Price has to be of range [10, 10000].
        """

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect price values
        self.type("#title", "House")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "9")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect price values
        self.type("#title", "House")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "10001")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid price values
        self.type("#title", "HouseP")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "1000")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid price values
        self.type("#title", "HouseQ")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "2000")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid price values
        self.type("#title", "HouseW")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "5500")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid price values
        self.type("#title", "HouseE")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "7000")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid price values
        self.type("#title", "HouseR")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "8900")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    def test_create_listing_r4_6(self, *_):
        """
        No frontend testing

        Testing R4-6: last_modified_date must be after 
        2021-01-02 and before 2025-01-02.
        """

    def test_create_listing_r4_7(self, *_):
        """
        Exhaustive black box testing.

        Testing R4-7: owner of corresponding product must exist
        """

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid values with missing owner
        self.type("#title", "House")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test5@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid values with existing owner
        self.type("#title", "suitableT")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    def test_create_listing_r4_8(self, *_):
        """
        Exhaustive black box testing.

        Testing R4-8: user cannot create products with the
        same title
        """

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with valid title values
        self.type("#title", "HouseY")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a success
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

        # open create listing page
        self.open(base_url + '/listcreate')
        # fill in fields with incorrect title values
        self.type("#title", "House5")
        self.type("#description", "Suitable \
            description for the listing")
        self.type("#price", "100")
        self.type("#email", "test1@test.com")
        # click submit
        self.click('input[type="submit"]')

        # check if create listing was a failure
        self.assert_element("#message")
        self.assert_text("Create listing failed.", "#message")