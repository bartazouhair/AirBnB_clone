#!/usr/bin/python3
"""It's Contains the TestReviewDocs classes
"""

from datetime import datetime
import inspect
from models import review
from models.base_model import BaseModel
import pep8
import unittest
Review = review.Review


class TestReviewD(unittest.TestCase):
    """It's Tests to check the documentation and style of Review class"""
    @classmethod
    def setUpClass(cls):
        """It's Set up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def testPep8ConformanceReview(self):
        """It's Test that models/review.py conforms to PEP8."""
        pps = pep8.StyleGuide(quiet=True)
        rsl = pps.check_files(['models/review.py'])
        self.assertEqual(rsl.total_errors, 0,
                         "Found code style errors (and warnings).")

    def testPep8ConformanceTestReview(self):
        """It's Test that tests/test_models/test_review.py conforms to PEP8."""
        pps = pep8.StyleGuide(quiet=True)
        rsl = pps.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(rsl.total_errors, 0,
                         "Found code style errors (and warnings).")

    def testReviewModuleDocstring(self):
        """It's Test for the review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def testReviewClassDocstring(self):
        """It's Test for the Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def testReviewFuncDocstrings(self):
        """It's Test for the presence of docstrings in Review methods"""
        for fc in self.review_f:
            self.assertIsNot(fc[1].__doc__, None,
                             "{:s} method needs a docstring".format(fc[0]))
            self.assertTrue(len(fc[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(fc[0]))


class TestR(unittest.TestCase):
    """It's Test the Review class"""
    def testIsSC(self):
        """It's Test if Review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def testPlaceIdAttr(self):
        """It's Test Review has attr place_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        self.assertEqual(review.place_id, "")

    def testUserIdAttr(self):
        """It's Test Review has attr user_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        self.assertEqual(review.user_id, "")

    def testTextAttr(self):
        """It's Test Review has attr text, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        self.assertEqual(review.text, "")

    def testToDictCreatesDict(self):
        """It's test to_dict method creates a dictionary with proper attrs"""
        r = Review()
        nw_d = r.to_dict()
        self.assertEqual(type(nw_d), dict)
        for atr in r.__dict__:
            self.assertTrue(atr in nw_d)
            self.assertTrue("__class__" in nw_d)

    def testToDictValues(self):
        """It's test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        r = Review()
        nw_d = r.to_dict()
        self.assertEqual(nw_d["__class__"], "Review")
        self.assertEqual(type(nw_d["created_at"]), str)
        self.assertEqual(type(nw_d["updated_at"]), str)
        self.assertEqual(nw_d["created_at"], r.created_at.strftime(t_format))
        self.assertEqual(nw_d["updated_at"], r.updated_at.strftime(t_format))

    def testStr(self):
        """It's test that the str method has the correct output"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))
