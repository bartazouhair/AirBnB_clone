#!/usr/bin/python3
"""It's a Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_i
    TestFileStorage_m
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_i(unittest.TestCase):
    """It's Unittests for test instantiation of the FileStorage class."""

    def testFileStorageInstantiationNoArgs(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def testFileStorageInstantiationWithArg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def testFileStorageFilePathIsPrivateStr(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorageObjectsIsPrivateDict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def testStorageInitializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_m(unittest.TestCase):
    """It's Unittests for test methods of the FileStorage class."""

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
        FileStorage._FileStorage__objects = {}

    def testAll(self):
        self.assertEqual(dict, type(models.storage.all()))

    def testAllWithArg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def testNew(self):
        b = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        self.assertIn("BaseModel." + b.id, models.storage.all().keys())
        self.assertIn(b, models.storage.all().values())
        self.assertIn("User." + u.id, models.storage.all().keys())
        self.assertIn(u, models.storage.all().values())
        self.assertIn("State." + s.id, models.storage.all().keys())
        self.assertIn(s, models.storage.all().values())
        self.assertIn("Place." + p.id, models.storage.all().keys())
        self.assertIn(p, models.storage.all().values())
        self.assertIn("City." + c.id, models.storage.all().keys())
        self.assertIn(c, models.storage.all().values())
        self.assertIn("Amenity." + a.id, models.storage.all().keys())
        self.assertIn(a, models.storage.all().values())
        self.assertIn("Review." + r.id, models.storage.all().keys())
        self.assertIn(r, models.storage.all().values())

    def testNewWithArgs(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def testNeWith_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def testSave(self):
        b = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        models.storage.save()
        st = ""
        with open("file.json", "r") as f:
            st = f.read()
            self.assertIn("BaseModel." + b.id, st)
            self.assertIn("User." + u.id, st)
            self.assertIn("State." + s.id, st)
            self.assertIn("Place." + p.id, st)
            self.assertIn("City." + c.id, st)
            self.assertIn("Amenity." + a.id, st)
            self.assertIn("Review." + r.id, st)

    def testSaveWithArg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def testReload(self):
        b = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        models.storage.save()
        models.storage.reload()
        ob = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + b.id, ob)
        self.assertIn("User." + u.id, ob)
        self.assertIn("State." + s.id, ob)
        self.assertIn("Place." + p.id, ob)
        self.assertIn("City." + c.id, ob)
        self.assertIn("Amenity." + a.id, ob)
        self.assertIn("Review." + r.id, ob)

    def testReloadWithArg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
