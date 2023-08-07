#!/usr/bin/python3
"""It's Defines unittests for models/amenity.py.
Unittest classes:
    TestAmenity_i
    TestAmenity_s
    TestAmenity_td
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_i(unittest.TestCase):
    """It's Unittests for test instantiation of the Amenity class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(Amenity().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def testNameIsPublicClassAttribute(self):
        a = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", a.__dict__)

    def testTwoAmenitiesUniqueIds(self):
        a1 = Amenity()
        a2 = Amenity()
        self.assertNotEqual(a1.id, a2.id)

    def testTwoAmenitiesDifferentCreatedAt(self):
        a1 = Amenity()
        sleep(0.05)
        a2 = Amenity()
        self.assertLess(a1.created_at, a2.created_at)

    def testTwoAmenitiesDifferentUpdatedAt(self):
        a1 = Amenity()
        sleep(0.05)
        a2 = Amenity()
        self.assertLess(a1.updated_at, a2.updated_at)

    def testStrRepresentation(self):
        d = datetime.today()
        d_repr = repr(d)
        a = Amenity()
        a.id = "123456"
        a.created_at = a.updated_at = d
        astr = a.__str__()
        self.assertIn("[Amenity] (123456)", astr)
        self.assertIn("'id': '123456'", astr)
        self.assertIn("'created_at': " + d_repr, astr)
        self.assertIn("'updated_at': " + d_repr, astr)

    def testArgsUnused(self):
        a = Amenity(None)
        self.assertNotIn(None, a.__dict__.values())

    def testInstantiationWithKwargs(self):
        """It's a instantiation with kwargs test method"""
        d = datetime.today()
        d_iso = d.isoformat()
        a = Amenity(id="345", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(a.id, "345")
        self.assertEqual(a.created_at, d)
        self.assertEqual(a.updated_at, d)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_s(unittest.TestCase):
    """It's Unittests for test save method of the Amenity class."""

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
        a = Amenity()
        sleep(0.05)
        first_updated_at = a.updated_at
        a.save()
        self.assertLess(first_updated_at, a.updated_at)

    def testTwoSaves(self):
        a = Amenity()
        sleep(0.05)
        first_updated_at = a.updated_at
        a.save()
        second_updated_at = a.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        a.save()
        self.assertLess(second_updated_at, a.updated_at)

    def testSaveWithArg(self):
        a = Amenity()
        with self.assertRaises(TypeError):
            a.save(None)

    def testSaveUpdatesFile(self):
        a = Amenity()
        a.save()
        amd = "Amenity." + a.id
        with open("file.json", "r") as f:
            self.assertIn(amd, f.read())


class TestAmenity_td(unittest.TestCase):
    """It's Unittests for test to_dict method of the Amenity class."""

    def testToDictType(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def testToDictContainsCorrectKeys(self):
        a = Amenity()
        self.assertIn("id", a.to_dict())
        self.assertIn("created_at", a.to_dict())
        self.assertIn("updated_at", a.to_dict())
        self.assertIn("__class__", a.to_dict())

    def testToDictContainsAddedAttributes(self):
        a = Amenity()
        a.middle_name = "Holberton"
        a.my_number = 98
        self.assertEqual("Holberton", a.middle_name)
        self.assertIn("my_number", a.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        a = Amenity()
        a_dict = a.to_dict()
        self.assertEqual(str, type(a_dict["id"]))
        self.assertEqual(str, type(a_dict["created_at"]))
        self.assertEqual(str, type(a_dict["updated_at"]))

    def testToDictOutput(self):
        d = datetime.today()
        a = Amenity()
        a.id = "123456"
        a.created_at = a.updated_at = d
        tdt = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': d.isoformat(),
            'updated_at': d.isoformat(),
        }
        self.assertDictEqual(a.to_dict(), tdt)

    def testContrastToDictDunderDict(self):
        a = Amenity()
        self.assertNotEqual(a.to_dict(), a.__dict__)

    def testToDictWithArg(self):
        a = Amenity()
        with self.assertRaises(TypeError):
            a.to_dict(None)


if __name__ == "__main__":
    unittest.main()
