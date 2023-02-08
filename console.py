#!/usr/bin/python3
"""A entry point into the command interpreter"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel


def parse(line):
    curly_brackets = re.search(r"\{(.*?)\}", line)
    brackets = re.search(r"\[(.*?)\]", line)
    if curly_brackets is None:
        if brackets is None:
            return [i.strip(",") for i in split(line)]
        else:
            lexer = split(line[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(line[:curly_brackets.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_brackets.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """The class for the command interpreter"""

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

    def do_EOF(self, line):
        """Handle end of line character"""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER"""
        pass

    def do_create(self, line):
        """Creating an instance od BaseModel"""

        lineParse = parse(line)
        if len(lineParse) == 0:
            print("** class name missing **")
        elif lineParse[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(lineParse[0])().id)
            storage.save()

    def do_show(self, line):
        """
        Prints the string representation of an
        instance based on the class name and id
        """

        lineParse = parse(line)
        objAll = storage.all()
        if len(lineParse) == 0:
            print("** class name missing **")
        elif lineParse[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(lineParse) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(lineParse[0], lineParse[1]) not in objAll:
            print("** no instance found **")
        else:
            print(objAll["{}.{}".format(lineParse[0], lineParse[1])])

    def do_destory(self, line):
        """
        Deletes an instance based on the class name and id
        """

        lineParse = parse(line)
        objAll = storage.all()
        if len(lineParse) == 0:
            print("** class name missing **")
        elif lineParse[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(lineParse) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(lineParse[0], lineParse[1]) not in objAll:
            print("** no instance found **")
        else:
            del objAll["{}.{}".format(lineParse[0], lineParse[1])]
            storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all
        instances based or not on the class name
        """

        lineParse = parse(line)
        if len(lineParse) > 0 and lineParse[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objExtract = []
            for obj in storage.all().values():
                if len(lineParse) > 0\
                 and lineParse[0] == obj.__class__.__name__:
                    objExtract.append(obj.__str__())
                elif len(lineParse) == 0:
                    objExtract.append(obj.__str__())
            print(objExtract)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by
        adding or updating attribute (save the change into the JSON file)
        """

        lineParse = parse(line)
        objAll = storage.all()
        if len(lineParse) == 0:
            print("** class name missing **")
            return False
        if lineParse[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(lineParse) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(lineParse[0], lineParse[1]) not in objAll:
            print("** no instance found **")
            return False
        if len(lineParse) == 2:
            print("** attribute name missing **")
            return False
        if len(lineParse) == 3:
            try:
                type(eval(lineParse[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(lineParse) == 4:
            objExtract = objAll["{}.{}".format(lineParse[0], lineParse[1])]
            if lineParse[2] in objExtract.__class__.__dict__.keys():
                valueType = type(objExtract.__class__.__dict__[lineParse[2]])
                objExtract.__dict__[lineParse[2]] = valueType
            else:
                objExtract.__dict__[lineParse[2]] = lineParse[3]
        elif type(eval(lineParse[2])) == dict:
            objExtract = objAll["{}.{}".format(lineParse[0], lineParse[1])]
            for k, v in eval(lineParse[2]).items():
                if (k in objExtract.__class__.__dict__.keys() and
                        type(objExtract.__class__.__dict__[k]) in {
                            str, int, float}):
                    valueType = type(objExtract.__class__.__dict__[k])
                    objExtract.__dict__[k] = valueType(v)
                else:
                    objExtract.__dict__[k] = v
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
