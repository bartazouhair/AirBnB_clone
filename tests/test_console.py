#!/usr/bin/python3
"""It's a Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_p
    TestHBNBCommand_h
    TestHBNBCommand_e
    TestHBNBCommand_c
    TestHBNBCommand_s
    TestHBNBCommand_a
    TestHBNBCommand_d
    TestHBNBCommand_u
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_p(unittest.TestCase):
    """Its Unittests for test prompting of the HBNB command interpreter."""

    def testPromptString(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def testEmptyLine(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_h(unittest.TestCase):
    """Its Unittests for test help messages of the HBNB command interpreter."""

    def testHelpQuit(self):
        hp = "It's Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(hp, output.getvalue().strip())

    def testHelpCreate(self):
        hp = ("It's Usage: create <class>\n        "
              "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(hp, output.getvalue().strip())

    def testHelpEOF(self):
        hp = "It's EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(hp, output.getvalue().strip())

    def testHelpShow(self):
        hp = ("It's Usage: show <class> <id> or <class>.show(<id>)\n        "
              "Display the string representation of a class instance of"
              " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(hp, output.getvalue().strip())

    def testHelpDestroy(self):
        hp = ("It's Usage: destroy <class> <id> or <class>.destroy(<id>)\n"
              "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            output_value = output.getvalue().strip().replace("        ", "")
            self.assertEqual(hp, output_value)

    def testHelpAll(self):
        hp = (
            "It's Usage: all or all <class> or <class>.all()\n        "
            "Display string representations of all instances of a given class"
            ".\n        If no class is specified, displays all instantiated "
            "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(hp, output.getvalue().strip())

    def testHelpCount(self):
        hp = ("It's Usage: count <class> or <class>.count()\n        "
              "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(hp, output.getvalue().strip())

    def testHelpUpdate(self):
        self.maxDiff = None
        hp = (
            "Usage: update <class> <id> <attribute_name> <attribute_value>\n"
            "or <class>.update(<id>, <attribute_name>, <attribute_value>) or\n"
            "<class>.update(<id>, <dictionary>)\n"
            "Update for class instance of a given id by adding or updating\n"
            "- Update for class instance of a given id by adding or updating\n"
            "+ Update for class instance of a given id by adding or updating\n"
            "a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(hp, output.getvalue().strip())

    def test_help(self):
        hp = ("Documented commands (type help <topic>):\n"
              "========================================\n"
              "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(hp, output.getvalue().strip())


class TestHBNBCommand_e(unittest.TestCase):
    """Its Unittests for test exiting from the HBNB command interpreter."""

    def testQuitExits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def testEOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_c(unittest.TestCase):
    """Its Unittests for test create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def testCreateMissingClass(self):
        crr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(crr, output.getvalue().strip())

    def testCreateInvalid_Class(self):
        crr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(crr, output.getvalue().strip())

    def testCreateInvalidSyntax(self):
        crr = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(crr, output.getvalue().strip())
        crr = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testCreateObject(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "User.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "State.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "City.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "Place.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            tk = "Review.{}".format(output.getvalue().strip())
            self.assertIn(tk, storage.all().keys())


class TestHBNBCommand_s(unittest.TestCase):
    """Its Unittests for test show from the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def testShowMissingClass(self):
        crr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testShowInvalidClass(self):
        crr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testShowMissingIdSpaceNotation(self):
        crr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(crr, output.getvalue().strip())

    def testShowMissingIdDotNotation(self):
        crr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testShowNoInstanceFoundSpaceNotation(self):
        crr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(crr, output.getvalue().strip())

    def testShowNoInstanceFoundDotNotation(self):
        crr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(crr, output.getvalue().strip())

    def testShowObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["BaseModel.{}".format(tstID)]
            command = "show BaseModel {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["User.{}".format(tstID)]
            command = "show User {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["State.{}".format(tstID)]
            command = "show State {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Place.{}".format(tstID)]
            command = "show Place {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["City.{}".format(tstID)]
            command = "show City {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Amenity.{}".format(tstID)]
            command = "show Amenity {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Review.{}".format(tstID)]
            command = "show Review {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())

    def testShowObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["BaseModel.{}".format(tstID)]
            command = "BaseModel.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["User.{}".format(tstID)]
            command = "User.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["State.{}".format(tstID)]
            command = "State.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Place.{}".format(tstID)]
            command = "Place.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["City.{}".format(tstID)]
            command = "City.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Amenity.{}".format(tstID)]
            command = "Amenity.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Review.{}".format(tstID)]
            command = "Review.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(o.__str__(), output.getvalue().strip())


class TestHBNBCommand_d(unittest.TestCase):
    """Its Unittests for test destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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
        storage.reload()

    def testDestroyMissingClass(self):
        crr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testDestroyInvalidClass(self):
        crr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testDestroyIdMissingSpaceNotation(self):
        crr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(crr, output.getvalue().strip())

    def testDestroyIdMissingDotNotation(self):
        crr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testDestroyInvalidIdSpaceNotation(self):
        crr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(crr, output.getvalue().strip())

    def testDestroyInvalidIdDotNotation(self):
        crr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(crr, output.getvalue().strip())

    def testDestroyObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["BaseModel.{}".format(tstID)]
            command = "destroy BaseModel {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["User.{}".format(tstID)]
            command = "show User {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["State.{}".format(tstID)]
            command = "show State {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Place.{}".format(tstID)]
            command = "show Place {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["City.{}".format(tstID)]
            command = "show City {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Amenity.{}".format(tstID)]
            command = "show Amenity {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Review.{}".format(tstID)]
            command = "show Review {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())

    def testDestroyObjectsDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["BaseModel.{}".format(tstID)]
            command = "BaseModel.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["User.{}".format(tstID)]
            command = "User.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["State.{}".format(tstID)]
            command = "State.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Place.{}".format(tstID)]
            command = "Place.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["City.{}".format(tstID)]
            command = "City.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Amenity.{}".format(tstID)]
            command = "Amenity.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            o = storage.all()["Review.{}".format(tstID)]
            command = "Review.destory({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(o, storage.all())


class TestHBNBCommand_a(unittest.TestCase):
    """Its Unittests for test all of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def testAllInvalidClass(self):
        crr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testAllObjectsSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def testAllObjectsDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def testAllSingleObjectSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    def testAllSingleObjectDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommand_u(unittest.TestCase):
    """Its Unittests for test update from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def testUpdateMissingClass(self):
        crr = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateInvalidClass(self):
        crr = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateMissingIdSpaceNotation(self):
        crr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateMissingIdDotNotation(self):
        crr = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateInvalidIdSpaceNotation(self):
        crr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateInvalidIdDotNotation(self):
        crr = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateMissingAttrNameSpaceNotation(self):
        crr = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
            tstCmd = "update BaseModel {}".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
            tstCmd = "update User {}".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
            tstCmd = "update State {}".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
            tstCmd = "update City {}".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
            tstCmd = "update Amenity {}".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
            tstCmd = "update Place {}".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateMissingAttrNameDotNotation(self):
        crr = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
            tstCmd = "BaseModel.update({})".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
            tstCmd = "User.update({})".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
            tstCmd = "State.update({})".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
            tstCmd = "City.update({})".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
            tstCmd = "Amenity.update({})".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
            tstCmd = "Place.update({})".format(tstID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateMissingAttrValueSpaceNotation(self):
        crr = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update BaseModel {} attr_name".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update User {} attr_name".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update State {} attr_name".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update City {} attr_name".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update Amenity {} attr_name".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update Place {} attr_name".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update Review {} attr_name".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateMissingAttrValueDotNotation(self):
        crr = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "BaseModel.update({}, attr_name)".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "User.update({}, attr_name)".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "State.update({}, attr_name)".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "City.update({}, attr_name)".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "Amenity.update({}, attr_name)".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "Place.update({}, attr_name)".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "Review.update({}, attr_name)".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(crr, output.getvalue().strip())

    def testUpdateValidStringAttrSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstID = output.getvalue().strip()
        tstCmd = "update BaseModel {} attr_name 'attr_value'".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["BaseModel.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstID = output.getvalue().strip()
        tstCmd = "update User {} attr_name 'attr_value'".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["User.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstID = output.getvalue().strip()
        tstCmd = "update State {} attr_name 'attr_value'".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["State.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstID = output.getvalue().strip()
        tstCmd = "update City {} attr_name 'attr_value'".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["City.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "update Place {} attr_name 'attr_value'".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstID = output.getvalue().strip()
        tstCmd = "update Amenity {} attr_name 'attr_value'".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Amenity.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstID = output.getvalue().strip()
        tstCmd = "update Review {} attr_name 'attr_value'".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Review.{}".format(tstID)].__dict__
        self.assertTrue("attr_value", tstDct["attr_name"])

    def testUpdateValidStringAttrDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tId = output.getvalue().strip()
        tstCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tId = output.getvalue().strip()
        tstCmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tId = output.getvalue().strip()
        tstCmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tId = output.getvalue().strip()
        tstCmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        tstCmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tId = output.getvalue().strip()
        tstCmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tId = output.getvalue().strip()
        tstCmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

    def testUpdateValidIntAttrSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "update Place {} max_guest 98".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual(98, tstDct["max_guest"])

    def testUpdateValidIntAttrDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        tstCmd = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, tstDct["max_guest"])

    def testUpdateValidFloatAttrSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "update Place {} latitude 7.2".format(tstID)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual(7.2, tstDct["latitude"])

    def testUpdateValidFloatAttrDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        tstCmd = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tstDct = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, tstDct["latitude"])

    def testUpdateValidDictionarySpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstID = output.getvalue().strip()
        tstCmd = "update BaseModel {} ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["BaseModel.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstID = output.getvalue().strip()
        tstCmd = "update User {} ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["User.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstID = output.getvalue().strip()
        tstCmd = "update State {} ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["State.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstID = output.getvalue().strip()
        tstCmd = "update City {} ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["City.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "update Place {} ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstID = output.getvalue().strip()
        tstCmd = "update Amenity {} ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Amenity.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstID = output.getvalue().strip()
        tstCmd = "update Review {} ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Review.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

    def testUpdateValidDictionaryDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstID = output.getvalue().strip()
        tstCmd = "BaseModel.update({}".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["BaseModel.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstID = output.getvalue().strip()
        tstCmd = "User.update({}, ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["User.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstID = output.getvalue().strip()
        tstCmd = "State.update({}, ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["State.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstID = output.getvalue().strip()
        tstCmd = "City.update({}, ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["City.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "Place.update({}, ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstID = output.getvalue().strip()
        tstCmd = "Amenity.update({}, ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Amenity.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstID = output.getvalue().strip()
        tstCmd = "Review.update({}, ".format(tstID)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Review.{}".format(tstID)].__dict__
        self.assertEqual("attr_value", tstDct["attr_name"])

    def testUpdateValidDictionaryWithIntSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "update Place {} ".format(tstID)
        tstCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual(98, tstDct["max_guest"])

    def testUpdateValidDictionaryWithIntDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "Place.update({}, ".format(tstID)
        tstCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual(98, tstDct["max_guest"])

    def testUpdateValidDictionaryWithFloatSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "update Place {} ".format(tstID)
        tstCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual(9.8, tstDct["latitude"])

    def testUpdateValidDictionaryWithFloatDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstID = output.getvalue().strip()
        tstCmd = "Place.update({}, ".format(tstID)
        tstCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(tstCmd)
        tstDct = storage.all()["Place.{}".format(tstID)].__dict__
        self.assertEqual(9.8, tstDct["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Its Unittests for test count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def testCountInvalidClass(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", output.getvalue().strip())

    def testCountObject(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
