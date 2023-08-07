#!/usr/bin/python3
"""It's Defines unittests for models/state.py.

Unittest classes:
    TestState_i
    TestState_s
    TestState_td
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_i(unittest.TestCase):
    """It's Unittests for test instantiation of the State class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(State, type(State()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(State(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(State().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def testNameIsPublicClassAttribute(self):
        s = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(s))
        self.assertNotIn("name", s.__dict__)

    def testTwoStatesUniqueIds(self):
        s1 = State()
        s2 = State()
        self.assertNotEqual(s1.id, s2.id)

    def testTwoStatesDifferentCreatedAt(self):
        s1 = State()
        sleep(0.05)
        s2 = State()
        self.assertLess(s1.created_at, s2.created_at)

    def testTwoStatesDifferentUpdatedAt(self):
        s1 = State()
        sleep(0.05)
        s2 = State()
        self.assertLess(s1.updated_at, s2.updated_at)

    def testStrRepresentation(self):
        d = datetime.today()
        d_repr = repr(d)
        s = State()
        s.id = "123456"
        s.created_at = s.updated_at = d
        strstr = s.__str__()
        self.assertIn("[State] (123456)", strstr)
        self.assertIn("'id': '123456'", strstr)
        self.assertIn("'created_at': " + d_repr, strstr)
        self.assertIn("'updated_at': " + d_repr, strstr)

    def testArgsUnused(self):
        s = State(None)
        self.assertNotIn(None, s.__dict__.values())

    def testInstantiationWithKwargs(self):
        d = datetime.today()
        d_iso = d.isoformat()
        s = State(id="345", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(s.id, "345")
        self.assertEqual(s.created_at, d)
        self.assertEqual(s.updated_at, d)

    def testInstantiationithNoneKwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_s(unittest.TestCase):
    """It's Unittests for test save method of the State class."""

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
        s = State()
        sleep(0.05)
        first_updated_at = s.updated_at
        s.save()
        self.assertLess(first_updated_at, s.updated_at)

    def testTwoSaves(self):
        s = State()
        sleep(0.05)
        first_updated_at = s.updated_at
        s.save()
        second_updated_at = s.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        s.save()
        self.assertLess(second_updated_at, s.updated_at)

    def testSaveWithArg(self):
        s = State()
        with self.assertRaises(TypeError):
            s.save(None)

    def testSaveUpdatesFile(self):
        s = State()
        s.save()
        std = "State." + s.id
        with open("file.json", "r") as f:
            self.assertIn(std, f.read())


class TestState_td(unittest.TestCase):
    """It's Unittests for test to_dict method of the State class."""

    def testToDictType(self):
        self.assertTrue(dict, type(State().to_dict()))

    def testToDictContainsCorrectKeys(self):
        s = State()
        self.assertIn("id", s.to_dict())
        self.assertIn("created_at", s.to_dict())
        self.assertIn("updated_at", s.to_dict())
        self.assertIn("__class__", s.to_dict())

    def testToDictContainsAddedAttributes(self):
        s = State()
        s.middle_name = "Holberton"
        s.my_number = 98
        self.assertEqual("Holberton", s.middle_name)
        self.assertIn("my_number", s.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        s = State()
        s_dict = s.to_dict()
        self.assertEqual(str, type(s_dict["id"]))
        self.assertEqual(str, type(s_dict["created_at"]))
        self.assertEqual(str, type(s_dict["updated_at"]))

    def testToDictOutput(self):
        d = datetime.today()
        s = State()
        s.id = "123456"
        s.created_at = s.updated_at = d
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': d.isoformat(),
            'updated_at': d.isoformat(),
        }
        self.assertDictEqual(s.to_dict(), tdict)

    def testContrastToDictDunderDict(self):
        s = State()
        self.assertNotEqual(s.to_dict(), s.__dict__)

    def testToDictWithArg(self):
        s = State()
        with self.assertRaises(TypeError):
            s.to_dict(None)


if __name__ == "__main__":
    unittest.main()
