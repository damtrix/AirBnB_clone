#!/usr/bin/python3
"""Creates a unique FIleStorage instance of the application"""
from .engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
