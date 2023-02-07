#!/usr/bin/python3
"""
unittest for base model class
"""
import unittest
from models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    """Test cases for base model class."""

    def setUp(self) -> None:
        """Set up test instances"""
        pass

    def tearDown(self) -> None:
        """Tear down test instances"""
        pass

    def test_instance(self):
        """Test the instance of base model"""

        base = BaseModel()
        self.assertEqual(str(type(base)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(base, BaseModel)

    def test_str(self):
        """Check the official return string (__str__)"""

        base = BaseModel()
        self.assertEqual(base.__str__(), 
        f"[{type(base).__name__}] ({base.id}) {base.__dict__}")

    def test_to_dict(self):
        """Checking the return instance of to-dict() function"""

        base = BaseModel()
        prev_time = base.updated_at
        self.assertDictEqual(base.to_dict(),
        {'__class__': type(base).__name__,
         'updated_at': base.updated_at.isoformat(),
         'id': base.id,
         'created_at': base.created_at.isoformat()
         })
         

    def test_class_attributes(self):
        """Checking the class attributes"""

        base = BaseModel()
        base2 = BaseModel()
        self.assertIsInstance(base.id, str)
        self.assertIsInstance(base.created_at, datetime)
        self.assertIsInstance(base.updated_at, datetime)
        self.assertNotEqual(base.id, base2.id)

    