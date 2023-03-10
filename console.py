#!/usr/bin/python3
"""
AirBnB console
"""
import shlex
import cmd
import json
import sys
from typing import List

from models import storage
from models.classes import classes


class HBNBCommand(cmd.Cmd):
    """
    The entry point for the command interpreter
    """
    prompt = "(hbnb) "

    @staticmethod
    def quit(code: int):
        'Quit the console'
        sys.exit(code)

    def parse(self, s: str) -> List[str]:
        # result = [""]
        # pause = False
        # s = s.strip()
        # for char in s:
        #     if char == '"' or char == "'":
        #         pause = not pause
        #         continue
        #     if char == " " and not pause:
        #         result.append("")
        #         continue
        #     result[-1] += char
        # return result
        return shlex.split(s)

    @staticmethod
    def fetch_instances(caller: str = "") -> List[any]:
        instances = []
        if caller == "":
            for k, v in storage.all().items():
                instances.append(str(v))
        else:
            for k, v in storage.all().items():
                if isinstance(v, classes[caller]):
                    instances.append(str(v))
        return instances

    def do_quit(self, args):
        """Exit the program"""
        print()
        self.quit(0)

    def do_EOF(self, args):
        """Exit the program"""
        self.quit(0)

    def do_create(self, args):
        'Creates a new instance and prints the id. Ex: `$ create BaseModel`'
        if len(args) < 1:
            print("** class name missing **")
            return
        if args not in classes:
            print("** class doesn't exist **")
            return
        new = classes[args]()
        new.save()
        print(new.id)

    def do_show(self, args):
        'Prints the repr of an instance e.g `$ show BaseModel 1234-1234-1234`'
        args = self.parse(args)
        if args == []:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        try:
            print(storage.all()[f"{args[0]}.{args[1]}"])
        except Exception as _:
            print("** no instance found **")

    def do_destroy(self, args):
        'Deletes an instance based on the class name and id'
        args = self.parse(args)
        if args == []:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        try:
            storage.all().pop(f"{args[0]}.{args[1]}")
            storage.save()
        except Exception as _:
            print("** no instance found **")

    def do_all(self, args: str):
        """Print string repr of all instances based or not on the class name"""
        args = args.strip()
        if args not in classes and args != "":
            print("** class doesn't exist **")
            return
        print(f"[{', '.join(self.fetch_instances(args))}]")

    def do_update(self, args):
        """Updates an instance by adding or updating attribute"""
        args = self.parse(args)
        if args == []:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        try:
            setattr(storage.all()[key], args[2], args[3])
            storage.save()
        except Exception as e:
            print(e)

    def handle_args(self, args, caller: str):
        if args == ".all()":
            self.do_all(caller)
        if args == ".count()":
            print(len(self.fetch_instances(caller)))
        if args[:6] == ".show(" and args[-1] == ")":
            id = args[6:-1]
            self.do_show(f"{caller} {id}")
        if args[:9] == ".destroy(" and args[-1] == ")":
            id = args[9:-1]
            self.do_destroy(f"{caller} {id}")
        if args[:8] == ".update(" and args[-1] == ")":
            if len(args) < 10:
                self.do_update(caller)
                return
            fargs = args[8:-1]
            if fargs[0] == "{" and len(fargs) > 2:
                try:
                    attr_dict = json.loads(fargs)
                except Exception as e:
                    print(e)
                    return
                print(attr_dict)
                for k, v in attr_dict.items():
                    setattr(storage.all()[f"{caller}.{fargs[0]}"], k, v)
                    # self.do_update(f"{caller} {fargs[0]} {k} {v}")
                return
            fparse = " ".join([caller, *(fargs.split(", "))])
            self.do_update(fparse)

    def do_BaseModel(self, args):
        """Base Model"""
        self.handle_args(args, "BaseModel")

    def do_User(self, args):
        """User Model"""
        self.handle_args(args, "User")

    def do_State(self, args):
        """State Model"""
        self.handle_args(args, "State")

    def do_City(self, args):
        """City Model"""
        self.handle_args(args, "City")

    def do_Amenity(self, args):
        """Amenity Model"""
        self.handle_args(args, "Amenity")

    def do_Place(self, args):
        """Place Model"""
        self.handle_args(args, "Place")

    def do_Review(self, args):
        """Review Model"""
        self.handle_args(args, "Review")

    def emptyline(self):
        """Empty line should do nothing"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
