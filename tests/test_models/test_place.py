#!/usr/bin/python3
"""It's Defines unittests for models/place.py.

Unittest classes:
    TestPlace_i
    TestPlace_s
    TestPlace_td
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_i(unittest.TestCase):
    """It's Unittests for test instantiation of the Place class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(Place, type(Place()))

    def testNewInstanceStoredIn_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(Place().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def testCityIdIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(p))
        self.assertNotIn("city_id", p.__dict__)

    def testUserIdIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(p))
        self.assertNotIn("user_id", p.__dict__)

    def testNameIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(p))
        self.assertNotIn("name", p.__dict__)

    def testDescriptionIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(p))
        self.assertNotIn("desctiption", p.__dict__)

    def testNumberRoomsIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(p))
        self.assertNotIn("number_rooms", p.__dict__)

    def testNumberBathroomsIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(p))
        self.assertNotIn("number_bathrooms", p.__dict__)

    def testMaxQuestIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(p))
        self.assertNotIn("max_guest", p.__dict__)

    def testPriceByNightIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(p))
        self.assertNotIn("price_by_night", p.__dict__)

    def testLatitudeIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(p))
        self.assertNotIn("latitude", p.__dict__)

    def testLongitudeIsPublicClassAttribute(self):
        p = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(p))
        self.assertNotIn("longitude", p.__dict__)

    def testAmenityIds_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(p))
        self.assertNotIn("amenity_ids", p.__dict__)

    def test_two_placesUniqueIds(self):
        p1 = Place()
        p2 = Place()
        self.assertNotEqual(p1.id, p2.id)

    def testTwoPlacesDifferentCreatedAt(self):
        p1 = Place()
        sleep(0.05)
        p2 = Place()
        self.assertLess(p1.created_at, p2.created_at)

    def testTwoPlacesDifferentUpdatedAt(self):
        p1 = Place()
        sleep(0.05)
        p2 = Place()
        self.assertLess(p1.updated_at, p2.updated_at)

    def testStrRepresentation(self):
        d = datetime.today()
        d_repr = repr(d)
        p = Place()
        p.id = "123456"
        p.created_at = p.updated_at = d
        pstr = p.__str__()
        self.assertIn("[Place] (123456)", pstr)
        self.assertIn("'id': '123456'", pstr)
        self.assertIn("'created_at': " + d_repr, pstr)
        self.assertIn("'updated_at': " + d_repr, pstr)

    def testArgsUnused(self):
        p = Place(None)
        self.assertNotIn(None, p.__dict__.values())

    def testInstantiationWithKwargs(self):
        d = datetime.today()
        d_iso = d.isoformat()
        p = Place(id="345", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(p.id, "345")
        self.assertEqual(p.created_at, d)
        self.assertEqual(p.updated_at, d)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_s(unittest.TestCase):
    """It's Unittests for test save method of the Place class."""

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
        p = Place()
        sleep(0.05)
        first_updated_at = p.updated_at
        p.save()
        self.assertLess(first_updated_at, p.updated_at)

    def testTwoSaves(self):
        p = Place()
        sleep(0.05)
        first_updated_at = p.updated_at
        p.save()
        second_updated_at = p.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        p.save()
        self.assertLess(second_updated_at, p.updated_at)

    def testSaveWithArg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.save(None)

    def testSaveUpdatesFile(self):
        p = Place()
        p.save()
        pid = "Place." + p.id
        with open("file.json", "r") as f:
            self.assertIn(pid, f.read())


class TestPlace_td(unittest.TestCase):
    """It's Unittests for test to_dict method of the Place class."""

    def testToDictType(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def testToDictContainsCorrectKeys(self):
        p = Place()
        self.assertIn("id", p.to_dict())
        self.assertIn("created_at", p.to_dict())
        self.assertIn("updated_at", p.to_dict())
        self.assertIn("__class__", p.to_dict())

    def testToDictContainsAddedAttributes(self):
        p = Place()
        p.middle_name = "Holberton"
        p.my_number = 98
        self.assertEqual("Holberton", p.middle_name)
        self.assertIn("my_number", p.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        p = Place()
        p_dict = p.to_dict()
        self.assertEqual(str, type(p_dict["id"]))
        self.assertEqual(str, type(p_dict["created_at"]))
        self.assertEqual(str, type(p_dict["updated_at"]))

    def testToDictOutput(self):
        d = datetime.today()
        p = Place()
        p.id = "123456"
        p.created_at = p.updated_at = d
        tict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': d.isoformat(),
            'updated_at': d.isoformat(),
        }
        self.assertDictEqual(p.to_dict(), tict)

    def testContrastToDictDunderDict(self):
        p = Place()
        self.assertNotEqual(p.to_dict(), p.__dict__)

    def testToDictWithArg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.to_dict(None)


if __name__ == "__main__":
    unittest.main()
