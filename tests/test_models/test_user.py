#!/usr/bin/python3
"""It's a Defines unittests for models/user.py.

Unittest classes:
    TestUser_i
    TestUser_s
    TestUser_td
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_i(unittest.TestCase):
    """It's Unittests for test instantiation of the User class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(User, type(User()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(User(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(User().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def testUpdatedAIsOublicDatetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def testEmailIsPublicStr(self):
        self.assertEqual(str, type(User.email))

    def testPasswordIsPublicStr(self):
        self.assertEqual(str, type(User.password))

    def testFirstNameIsPublicStr(self):
        self.assertEqual(str, type(User.first_name))

    def testLastNameIsPublicStr(self):
        self.assertEqual(str, type(User.last_name))

    def testTwoUsersUniqueIds(self):
        u1 = User()
        u2 = User()
        self.assertNotEqual(u1.id, u2.id)

    def testTwoUsersDifferentCreatedAt(self):
        u1 = User()
        sleep(0.05)
        u2 = User()
        self.assertLess(u1.created_at, u2.created_at)

    def testTwoUsersDifferentUpdatedAt(self):
        u1 = User()
        sleep(0.05)
        u2 = User()
        self.assertLess(u1.updated_at, u2.updated_at)

    def testStrRepresentation(self):
        d = datetime.today()
        d_repr = repr(d)
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = d
        usrstr = usr.__str__()
        self.assertIn("[User] (123456)", usrstr)
        self.assertIn("'id': '123456'", usrstr)
        self.assertIn("'created_at': " + d_repr, usrstr)
        self.assertIn("'updated_at': " + d_repr, usrstr)

    def testArgsUnused(self):
        usr = User(None)
        self.assertNotIn(None, usr.__dict__.values())

    def testInstantiationWithkwargs(self):
        d = datetime.today()
        d_iso = d.isoformat()
        usr = User(id="345", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(usr.id, "345")
        self.assertEqual(usr.created_at, d)
        self.assertEqual(usr.updated_at, d)

    def testInstantiationWithNonekwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_s(unittest.TestCase):
    """It's Unittests for test save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testOneSave(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        self.assertLess(first_updated_at, usr.updated_at)

    def testTwoSaves(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        second_updated_at = usr.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        usr.save()
        self.assertLess(second_updated_at, usr.updated_at)

    def testSaveWithArg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.save(None)

    def testSaveUpdatesFile(self):
        usr = User()
        usr.save()
        usd = "User." + usr.id
        with open("file.json", "r") as f:
            self.assertIn(usd, f.read())


class TestUser_td(unittest.TestCase):
    """It's Unittests for test to_dict method of the User class."""

    def testToDictType(self):
        self.assertTrue(dict, type(User().to_dict()))

    def testToDictContainsCorrectKeys(self):
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())

    def testToDictContainsAddedAttributes(self):
        usr = User()
        usr.middle_name = "Holberton"
        usr.my_number = 98
        self.assertEqual("Holberton", usr.middle_name)
        self.assertIn("my_number", usr.to_dict())

    def tesTodictDatetimeAttributesAreStrs(self):
        usr = User()
        us_dct = usr.to_dict()
        self.assertEqual(str, type(us_dct["id"]))
        self.assertEqual(str, type(us_dct["created_at"]))
        self.assertEqual(str, type(us_dct["updated_at"]))

    def testToDictOutput(self):
        d = datetime.today()
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = d
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': d.isoformat(),
            'updated_at': d.isoformat(),
        }
        self.assertDictEqual(usr.to_dict(), tdict)

    def testContrastToDictDunderDict(self):
        usr = User()
        self.assertNotEqual(usr.to_dict(), usr.__dict__)

    def testToDictWithArg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()
