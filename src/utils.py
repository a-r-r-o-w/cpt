import os
import typing
import urllib.parse

class cd:
  def __init__ (self, new_path: str):
    self.path = new_path

  def __enter__ (self):
    self.saved_path = os.getcwd()
    os.chdir(self.path)
    return self

  def __exit__ (self, exc_type, exc_val, exc_tb):
    os.chdir(self.saved_path)
