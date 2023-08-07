#!/usr/bin/python3
"""It's Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def prs(arg):
    cb = re.search(r"\{(.*?)\}", arg)
    bk = re.search(r"\[(.*?)\]", arg)
    if cb is None:
        if bk is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lx = split(arg[:bk.span()[0]])
            rl = [i.strip(",") for i in lx]
            rl.append(bk.group())
            return rl
    else:
        lx = split(arg[:cb.span()[0]])
        rl = [i.strip(",") for i in lx]
        rl.append(cb.group())
        return rl


class HBNBCommand(cmd.Cmd):
    """It's Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): It's The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def lnempty(self):
        """It's Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """It's Default behavior for cmd module when input is invalid"""
        agd = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        mt = re.search(r"\.", arg)
        if mt is not None:
            ag = [arg[:mt.span()[0]], arg[mt.span()[1]:]]
            mt = re.search(r"\((.*?)\)", ag[1])
            if mt is not None:
                command = [ag[1][:mt.span()[0]], mt.group()[1:-1]]
                if command[0] in agd.keys():
                    cl = "{} {}".format(ag[0], command[1])
                    return agd[command[0]](cl)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """It's Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """It's EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """It's Usage: create <class>
        Create a new class instance and print its id.
        """
        ag = prs(arg)
        if len(ag) == 0:
            print("** class name missing **")
        elif ag[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(ag[0])().id)
            storage.save()

    def do_show(self, arg):
        """It's Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        ag = prs(arg)
        objt = storage.all()
        if len(ag) == 0:
            print("** class name missing **")
        elif ag[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(ag) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(ag[0], ag[1]) not in objt:
            print("** no instance found **")
        else:
            print(objt["{}.{}".format(ag[0], ag[1])])

    def do_destroy(self, arg):
        """It's Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        ag = prs(arg)
        objt = storage.all()
        if len(ag) == 0:
            print("** class name missing **")
        elif ag[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(ag) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(ag[0], ag[1]) not in objt.keys():
            print("** no instance found **")
        else:
            del objt["{}.{}".format(ag[0], ag[1])]
            storage.save()

    def do_all(self, arg):
        """It's Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        ag = prs(arg)
        if len(ag) > 0 and ag[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(ag) > 0 and ag[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(ag) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """It's Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        ag = prs(arg)
        count = 0
        for obj in storage.all().values():
            if ag[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update for class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        ag = prs(arg)
        objt = storage.all()

        if len(ag) == 0:
            print("** class name missing **")
            return False
        if ag[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(ag) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(ag[0], ag[1]) not in objt.keys():
            print("** no instance found **")
            return False
        if len(ag) == 2:
            print("** attribute name missing **")
            return False
        if len(ag) == 3:
            try:
                type(eval(ag[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(ag) == 4:
            obj = objt["{}.{}".format(ag[0], ag[1])]
            if ag[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[ag[2]])
                obj.__dict__[ag[2]] = valtype(ag[3])
            else:
                obj.__dict__[ag[2]] = ag[3]
        elif type(eval(ag[2])) == dict:
            obj = objt["{}.{}".format(ag[0], ag[1])]
            for k, v in eval(ag[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
