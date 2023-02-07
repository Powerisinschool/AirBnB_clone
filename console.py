#!/usr/bin/python3

import cmd
import sys

from models.base_model import BaseModel
from models import storage
from models.classes import classes

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def quit(self, code: int):
        'Quit the console'
        sys.exit(code)

    def parse(self, s: str) -> list[str]:
        result = [""]
        pause = False
        s = s.strip()
        for char in s:
            if char == '"' or char == "'":
                pause = not pause
                continue
            if char == " " and not pause:
                result.append("")
                continue
            result[-1] += char
        return result

    def do_quit(self, args):
        'Exit the program'
        self.quit(0)

    def do_EOF(self, args):
        'Exit the program'
        self.quit(0)

    def do_create(self, args):
        'Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id. Ex: `$ create BaseModel`'
        if len(args) < 0:
            print("** class name missing **")
            return
        if args not in classes:
            print("** class doesn't exist **")
            return
        new = classes[args]()
        new.save()
        print(new.id)

    def do_show(self, args):
        'Prints the string representation of an instance based on the class name and id. Ex: `$ show BaseModel 1234-1234-1234`'
        args = self.parse(args)
        if args[0] == '':
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
        except:
            print("** no instance found **")

    def do_destroy(self, args):
        'Deletes an instance based on the class name and id (saves the change into the JSON file)'
        args = self.parse(args)
        if args[0] == '':
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
        except:
            print("** no instance found **")

    def do_all(self, args):
        'Prints all string representation of all instances based or not on the class name'
        instances = []
        if args == "":
            for k, v in storage.all().items():
                instances.append(str(v))
        elif args not in classes:
            print("** class doesn't exist **")
            return
        else:
            for k, v in storage.all().items():
                if isinstance(v, classes[args]): instances.append(str(v))
        print(instances)

    def do_update(self, args):
        'Updates an instance based on the class name and id by adding or updating attribute (saves the change into the JSON file)'
        args = self.parse(args)
        # args = args.split(" ")
        if args[0] == '':
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


if __name__ == '__main__':
    HBNBCommand().cmdloop()