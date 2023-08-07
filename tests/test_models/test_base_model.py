#!/usr/bin/python3
"""It's Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_i
    TestBaseModel_s
    TestBaseModel_td
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_i(unittest.TestCase):
    """It's Unittests for test instantiation of the BaseModel class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(BaseModel().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def testTwoModelsUniqueIds(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def testTwoModelsDifferentCreatedAt(self):
        b1 = BaseModel()
        sleep(0.05)
        b2 = BaseModel()
        self.assertLess(b1.created_at, b2.created_at)

    def testTwoModelsDifferentUpdatedAt(self):
        b1 = BaseModel()
        sleep(0.05)
        b2 = BaseModel()
        self.assertLess(b1.updated_at, b2.updated_at)

    def testStrRepresentation(self):
        d = datetime.today()
        d_repr = repr(d)
        b = BaseModel()
        b.id = "123456"
        b.created_at = b.updated_at = d
        bstr = b.__str__()
        self.assertIn("[BaseModel] (123456)", bstr)
        self.assertIn("'id': '123456'", bstr)
        self.assertIn("'created_at': " + d_repr, bstr)
        self.assertIn("'updated_at': " + d_repr, bstr)

    def testArgsUnused(self):
        b = BaseModel(None)
        self.assertNotIn(None, b.__dict__.values())

    def testInstantiationWithKwargs(self):
        d = datetime.today()
        d_iso = d.isoformat()
        b = BaseModel(id="345", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(b.id, "345")
        self.assertEqual(b.created_at, d)
        self.assertEqual(b.updated_at, d)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def testInstantiationWithArgsAndKwargs(self):
        d = datetime.today()
        d_iso = d.isoformat()
        b = BaseModel("12", id="345", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(b.id, "345")
        self.assertEqual(b.created_at, d)
        self.assertEqual(b.updated_at, d)


class TestBaseModel_s(unittest.TestCase):
    """It's Unittests for test save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        b = BaseModel()
        sleep(0.05)
        first_updated_at = b.updated_at
        b.save()
        self.assertLess(first_updated_at, b.updated_at)

    def testTwoSaves(self):
        b = BaseModel()
        sleep(0.05)
        first_updated_at = b.updated_at
        b.save()
        second_updated_at = b.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        b.save()
        self.assertLess(second_updated_at, b.updated_at)

    def testSaveWithArg(self):
        b = BaseModel()
        with self.assertRaises(TypeError):
            b.save(None)

    def testSaveUpdatesFile(self):
        b = BaseModel()
        b.save()
        bid = "BaseModel." + b.id
        with open("file.json", "r") as f:
            self.assertIn(bid, f.read())


class TestBaseModel_td(unittest.TestCase):
    """It's Unittests for test to_dict method of the BaseModel class."""

    def testToDictType(self):
        b = BaseModel()
        self.assertTrue(dict, type(b.to_dict()))

    def testToDictContainsCorrectKeys(self):
        b = BaseModel()
        self.assertIn("id", b.to_dict())
        self.assertIn("created_at", b.to_dict())
        self.assertIn("updated_at", b.to_dict())
        self.assertIn("__class__", b.to_dict())

    def testToDictContainsAddedAttributes(self):
        b = BaseModel()
        b.name = "Holberton"
        b.my_number = 98
        self.assertIn("name", b.to_dict())
        self.assertIn("my_number", b.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        b = BaseModel()
        b_dict = b.to_dict()
        self.assertEqual(str, type(b_dict["created_at"]))
        self.assertEqual(str, type(b_dict["updated_at"]))

    def testToDictOutput(self):
        dt = datetime.today()
        b = BaseModel()
        b.id = "123456"
        b.created_at = b.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(b.to_dict(), tdict)

    def testContrastToDictDunderDict(self):
        b = BaseModel()
        self.assertNotEqual(b.to_dict(), b.__dict__)

    def testToDictWithArg(self):
        b = BaseModel()
        with self.assertRaises(TypeError):
            b.to_dict(None)


if __name__ == "__main__":
    unittest.main()
