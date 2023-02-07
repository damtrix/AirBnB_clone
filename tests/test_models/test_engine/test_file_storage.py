#!/usr/bin/python3
"""Unittest module for the FileStorage class."""

import unittest
from datetime import datetime
import time
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import re
import json
import os


class TestFileStorage(unittest.TestCase):
    """Test Cases for the FileStorage class."""

    def setUp(self):
        """Sets up test methods."""
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def test_5_instantiation(self):
        """Tests instantiation of storage class."""
        self.assertEqual(type(storage).__name__, "FileStorage")

    def test_3_init_no_args(self):
        """Tests __init__ with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.__init__()
        msg = "descriptor '__init__' of 'object' object needs an argument"
        self.assertEqual(str(e.exception), msg)

    def test_3_init_many_args(self):
        """Tests __init__ with many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            b = FileStorage(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        msg = "FileStorage() takes no arguments"
        self.assertEqual(str(e.exception), msg)

    def test_5_attributes(self):
        """Tests class attributes."""
        self.resetStorage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(getattr(FileStorage, "_FileStorage__objects"), {})

    def help_test_all(self, classname):
        """Helper tests all() method for classname."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        o = storage.classes()[classname]()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], o)

    def help_test_all_multiple(self, classname):
        """Helper tests all() method with many objects for classname."""
        self.resetStorage()
        self.assertEqual(storage.all(), {})

        cls = storage.classes()[classname]
        objs = [cls() for i in range(1000)]
        [storage.new(o) for o in objs]
        self.assertEqual(len(objs), len(storage.all()))
        for o in objs:
            key = "{}.{}".format(type(o).__name__, o.id)
            self.assertTrue(key in storage.all())
            self.assertEqual(storage.all()[key], o)

    def test_5_all_no_args(self):
        """Tests all() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.all()
        msg = "FileStorage.all() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_5_all_excess_args(self):
        """Tests all() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.all(self, 98)
        msg = "FileStorage.all() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def help_test_new(self, classname):
        """Helps tests new() method for classname."""
        self.resetStorage()
        cls = storage.classes()[classname]
        o = cls()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        self.assertTrue(key in FileStorage._FileStorage__objects)
        self.assertEqual(FileStorage._FileStorage__objects[key], o)

    def test_5_new_no_args(self):
        """Tests new() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            storage.new()
        msg = "FileStorage.new() missing 1 required positional argument: 'obj'"
        self.assertEqual(str(e.exception), msg)

    def test_5_new_excess_args(self):
        """Tests new() with too many arguments."""
        self.resetStorage()
        b = BaseModel()
        with self.assertRaises(TypeError) as e:
            storage.new(b, 98)
        msg = "FileStorage.new() takes 2 positional arguments but 3 were given"
        self.assertEqual(str(e.exception), msg)

    def help_test_save(self, classname):
        """Helps tests save() method for classname."""
        self.resetStorage()
        cls = storage.classes()[classname]
        o = cls()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        d = {key: o.to_dict()}
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as f:
            self.assertEqual(len(f.read()), len(json.dumps(d)))
            f.seek(0)
            self.assertEqual(json.load(f), d)

    def test_5_save_no_args(self):
        """Tests save() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.save()
        msg = "FileStorage.save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_5_save_excess_args(self):
        """Tests save() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.save(self, 98)
        msg = "FileStorage.save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def help_test_reload(self, classname):
        """Helps test reload() method for classname."""
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})
        cls = storage.classes()[classname]
        o = cls()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        storage.save()
        storage.reload()
        self.assertEqual(o.to_dict(), storage.all()[key].to_dict())

    def help_test_reload_mismatch(self, classname):
        """Helps test reload() method for classname."""
        self.resetStorage()
        storage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})

        cls = storage.classes()[classname]
        o = cls()
        storage.new(o)
        key = "{}.{}".format(type(o).__name__, o.id)
        storage.save()
        o.name = "Laura"
        storage.reload()
        self.assertNotEqual(o.to_dict(), storage.all()[key].to_dict())

    def test_5_reload_no_args(self):
        """Tests reload() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.reload()
        msg = "FileStorage.reload() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_5_reload_excess_args(self):
        """Tests reload() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            FileStorage.reload(self, 98)
        msg = "FileStorage.reload() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)


if __name__ == '__main__':
    unittest.main()
