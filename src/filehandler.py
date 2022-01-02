#!/usr/bin/env python3

import os
import sys
import typing
import string

if __name__ == '__main__':
  sys.path.insert(0, './codeforces/')
  sys.path.insert(1, './utility/')

import codeforces
from utility.logger import (
  context, info, debug, error
)

def codeforces_testing_script (*, testcase_count):
  script = """\
#!/usr/bin/env python3

import os

os.system('compile main.cpp')

for index in range(1, {testcase_count} + 1):
  os.system(f'./main < {index}.in > {index}.out')
""".format(testcase_count = testcase_count, index = '{index}')

  return script

class cd:
  def __init__ (self, path: str):
    self.old_path = os.getcwd()
    self.new_path = path.encode('ascii', errors = 'ignore').decode()

    allowed_characters = set(string.ascii_letters + string.digits + '.-+_/ ')
    filtered_characters = set(string.printable) - allowed_characters

    for character in filtered_characters:
      self.new_path = self.new_path.replace(character, '_')
  
  def __enter__ (self):
    try:
      debug(f'Creating directory "{self.new_path}"')
      os.makedirs(self.new_path)
    except FileExistsError:
      debug(f'"{self.new_path}" already exists')
    
    os.chdir(self.new_path)
  
  def __exit__ (self, exc_type, exc_val, exc_tb):
    os.chdir(self.old_path)

class FileHandler:
  def __init__ (
    self,
    content: typing.Union[codeforces.Problem, None]
  ):
    self.content = content
  
  def save (self) -> None:
    if self.content.type == 'codeforces.problem':
      self.codeforces_problem_save()
  
  def codeforces_problem_save (self):
    with cd(f'{self.content.id}{self.content.index} - {self.content.name}'):
      # Create README.md file with problem statement
      with open('README.md', 'w') as file:
        file.write(self.content.markdown())
      
      # Create main.cpp file with template
      # TODO: add template support
      with open('main.cpp', 'w') as file:
        pass

      # Create testcase files
      for index, testcase in enumerate(self.content.testcases, 1):
        testcase: codeforces.TestCase = testcase

        with open(f'{index}.in', 'w') as file:
          file.write(testcase.input)
        
        with open(f'{index}-expected.out', 'w') as file:
          file.write(testcase.output)
      
      # Create python file for automating testing
      with open('test.py', 'w') as file:
        file.write(codeforces_testing_script(testcase_count = len(self.content.testcases)))
      
      os.system('chmod +x test.py')
