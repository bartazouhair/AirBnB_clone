#!/usr/bin/python3
"""It's Defines unittests for models/city.py.

Unittest classes:
    TestCity_i
    TestCity_s
    TestCity_td
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_i(unittest.TestCase):
    """It's Unittests for test instantiation of the City class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(City, type(City()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(City(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(City().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def testStateIdIsPublicClassAttribute(self):
        c = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(c))
        self.assertNotIn("state_id", c.__dict__)

    def testNameIsPublicClassAttribute(self):
        c = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(c))
        self.assertNotIn("name", c.__dict__)

    def testTwoCitiesUniqueIds(self):
        c1 = City()
        c2 = City()
        self.assertNotEqual(c1.id, c2.id)

    def testTwoCitiesDifferentCreated_at(self):
        c1 = City()
        sleep(0.05)
        c2 = City()
        self.assertLess(c1.created_at, c2.created_at)

    def testTwoCitiesDifferentUpdatedAt(self):
        c1 = City()
        sleep(0.05)
        c2 = City()
        self.assertLess(c1.updated_at, c2.updated_at)

    def testStrRepresentation(self):
        d = datetime.today()
        d_repr = repr(d)
        c = City()
        c.id = "123456"
        c.created_at = c.updated_at = d
        ctr = c.__str__()
        self.assertIn("[City] (123456)", ctr)
        self.assertIn("'id': '123456'", ctr)
        self.assertIn("'created_at': " + d_repr, ctr)
        self.assertIn("'updated_at': " + d_repr, ctr)

    def testArgsUnused(self):
        c = City(None)
        self.assertNotIn(None, c.__dict__.values())

    def testInstantiationWithKwargs(self):
        d = datetime.today()
        d_iso = d.isoformat()
        c = City(id="345", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(c.id, "345")
        self.assertEqual(c.created_at, d)
        self.assertEqual(c.updated_at, d)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_s(unittest.TestCase):
    """It's Unittests for test save method of the City class."""

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
        c = City()
        sleep(0.05)
        first_updated_at = c.updated_at
        c.save()
        self.assertLess(first_updated_at, c.updated_at)

    def testTwoSaves(self):
        c = City()
        sleep(0.05)
        first_updated_at = c.updated_at
        c.save()
        second_updated_at = c.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        c.save()
        self.assertLess(second_updated_at, c.updated_at)

    def testSaveWithArg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.save(None)

    def testSaveUpdatesFile(self):
        c = City()
        c.save()
        cid = "City." + c.id
        with open("file.json", "r") as f:
            self.assertIn(cid, f.read())


class TestCity_td(unittest.TestCase):
    """It's Unittests for test to_dict method of the City class."""

    def testToDictType(self):
        self.assertTrue(dict, type(City().to_dict()))

    def testToDictContainsCorrectKeys(self):
        c = City()
        self.assertIn("id", c.to_dict())
        self.assertIn("created_at", c.to_dict())
        self.assertIn("updated_at", c.to_dict())
        self.assertIn("__class__", c.to_dict())

    def testToDictContainsAddeAttributes(self):
        c = City()
        c.middle_name = "Holberton"
        c.my_number = 98
        self.assertEqual("Holberton", c.middle_name)
        self.assertIn("my_number", c.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        c = City()
        c_dict = c.to_dict()
        self.assertEqual(str, type(c_dict["id"]))
        self.assertEqual(str, type(c_dict["created_at"]))
        self.assertEqual(str, type(c_dict["updated_at"]))

    def testToDictOutput(self):
        d = datetime.today()
        c = City()
        c.id = "123456"
        c.created_at = c.updated_at = d
        tict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': d.isoformat(),
            'updated_at': d.isoformat(),
        }
        self.assertDictEqual(c.to_dict(), tict)

    def testContrastToDictDunderDict(self):
        c = City()
        self.assertNotEqual(c.to_dict(), c.__dict__)

    def testToDictWithArg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.to_dict(None)


if __name__ == "__main__":
    unittest.main()
