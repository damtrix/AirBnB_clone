#!/usr/bin/python3
"""A entry point into the command interpreter"""
import cmd
import re
from shlex import split
from models import storage
import json
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
        """Creating an instance of BaseModel"""

        lineParse = parse(line)
        if len(lineParse) == 0:
            print("** class name missing **")
        elif lineParse[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            data = storage.classes()[lineParse[0]]()
            print(data.id)
            storage.save()

    def do_show(self, line):
        """Prints the string representation of an instance based on the class name and id"""

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

    def do_destroy(self, line):
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
        """Updates an instance by adding or updating attribute.
        """
        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_count(self, line):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""

        lineParse = parse(line)
        count = 0
        if len(lineParse) == 0:
            print("** class name missing **")
        elif lineParse[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            for obj in storage.all().values():
                if lineParse[0] == obj.__class__.__name__:
                    count += 1
            print(count)

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""

        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
