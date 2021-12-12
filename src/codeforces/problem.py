#!/usr/bin/env python3

import requests
import sys

from bs4 import (
  BeautifulSoup,
  element
)
from markdownify import markdownify

sys.path.insert(0, '../')
sys.path.insert(1, '../utility/')

from utility.logging import Logger

log = Logger()

class TestCase:
  def __init__ (
    self,
    input: str = None,
    output: str = None
  ):
    self.input = input
    self.output = output

class Problem:
  def __init__ (
    self,
    *,
    url: str = None,
    name: str = None,
    statement: str = None,
    time_limit: str = None,
    memory_limit: str = None,
    input_file: str = None,
    output_file: str = None,
    input_specification: str = None,
    output_specification: str = None,
    notes: str = None
  ):
    self.name = None,
    self.time_limit = None,
    self.memory_limit = None,
    self.input_file = None,
    self.output_file = None,
    self.statement = None,
    self.input_specification = None,
    self.output_specification = None,
    self.notes = None

class ProblemScraper:
  """Problem Scraper for https://codeforces.com"""

  def __init__ (self, url: str):
    self.url = url
    self.problem = Problem()
  
  def scrape (self) -> Problem:
    log.info(f'Sending request to {self.url}')
    r = requests.get(self.url)
    s = BeautifulSoup(r.text, features = 'lxml')

    if r.status_code != 200:
      log.error(f'Request to {self.url} failed with status code: {r.status_code}')
    
    problem = s.find('div', {'class': 'problem-statement'})

    self.problem.index = ProblemScraper._index_from_problem(problem)
    self.problem.name = ProblemScraper._name_from_problem(problem)
    self.problem.time_limit = ProblemScraper._time_limit_from_problem(problem)
    self.problem.memory_limit = ProblemScraper._memory_limit_from_problem(problem)
    self.problem.input_file = ProblemScraper._input_file_from_problem(problem)
    self.problem.output_file = ProblemScraper._output_file_from_problem(problem)
    self.problem.statement = ProblemScraper._statement_from_problem(problem)
    self.problem.input_specification = ProblemScraper._input_specification_from_problem(problem)
    self.problem.output_specification = ProblemScraper._output_specification_from_problem(problem)

    print(self.problem.index, self.problem.name)
    print(self.problem.time_limit)
    print(self.problem.memory_limit)
    print(self.problem.input_file)
    print(self.problem.output_file)
    print(self.problem.statement)
    print(self.problem.input_specification)
    print(self.problem.output_specification)
  
  @staticmethod
  def _name_from_problem (problem: element.Tag) -> str:
    return ' '.join(problem.find('div', { 'class': 'title' }).text.strip().split()[1:])
  
  @staticmethod
  def _index_from_problem (problem: element.Tag) -> str:
    return problem.find('div', { 'class': 'title' }).text.strip().split()[0][:-1]
  
  @staticmethod
  def _time_limit_from_problem (problem: element.Tag) -> str:
    return problem.find('div', { 'class': 'time-limit' }).text.strip()[len('time limit per test'):]
  
  @staticmethod
  def _memory_limit_from_problem (problem: element.Tag) -> str:
    return problem.find('div', { 'class': 'memory-limit' }).text.strip()[len('memory limit per test'):]
  
  @staticmethod
  def _input_file_from_problem (problem: element.Tag) -> str:
    return problem.find('div', { 'class': 'input-file' }).text.strip()[len('input'):]
  
  @staticmethod
  def _output_file_from_problem (problem: element.Tag) -> str:
    return problem.find('div', { 'class': 'output-file' }).text.strip()[len('output'):]
  
  @staticmethod
  def _statement_from_problem (problem: element.Tag) -> str:
    return markdownify(str(problem.find_all('div')[10]).strip()).strip()
  
  @staticmethod
  def _input_specification_from_problem (problem: element.Tag) -> str:
    return \
      markdownify(str(problem.find('div', { 'class': 'input-specification' }))
      .strip())[len('Input'):].strip()
  
  @staticmethod
  def _output_specification_from_problem (problem: element.Tag) -> str:
    return \
      markdownify(str(problem.find('div', { 'class': 'output-specification' }))
      .strip())[len('Output'):].strip()

if __name__ == '__main__':
  scraper = ProblemScraper('https://codeforces.com/problemset/problem/4/A')
  scraper.scrape()
