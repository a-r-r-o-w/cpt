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
    name_div = problem.find('div', { 'class': 'title' })
    title = name_div.text
    name = ' '.join(title.split()[1:])
    return name
  
  @staticmethod
  def _index_from_problem (problem: element.Tag) -> str:
    index_div = problem.find('div', { 'class': 'title' })
    title = index_div.text
    index = title.split()[0][:-1]
    return index
  
  @staticmethod
  def _time_limit_from_problem (problem: element.Tag) -> str:
    tl_div = problem.find('div', { 'class': 'time-limit' })
    tl = tl_div.text.strip()
    tl = tl[len('time limit per test'):] # remove prefix
    return tl
  
  @staticmethod
  def _memory_limit_from_problem (problem: element.Tag) -> str:
    ml_div = problem.find('div', { 'class': 'memory-limit' })
    ml = ml_div.text.strip()
    ml = ml[len('memory limit per test'):] # remove prefix
    return ml
  
  @staticmethod
  def _input_file_from_problem (problem: element.Tag) -> str:
    inputfile_div = problem.find('div', { 'class': 'input-file' })
    inputfile = inputfile_div.text.strip()
    inputfile = inputfile[len('input'):] # remove prefix
    return inputfile
  
  @staticmethod
  def _output_file_from_problem (problem: element.Tag) -> str:
    outputfile_div = problem.find('div', { 'class': 'output-file' })
    outputfile = outputfile_div.text.strip()
    outputfile = outputfile[len('output'):] # remove prefix
    return outputfile
  
  @staticmethod
  def _statement_from_problem (problem: element.Tag) -> str:
    statement_div = problem.find_all('div')[10]
    md = markdownify(str(statement_div)).strip()
    return ProblemScraper._latexify(md)
  
  @staticmethod
  def _input_specification_from_problem (problem: element.Tag) -> str:
    inputspec_div = problem.find('div', { 'class': 'input-specification' })
    md = markdownify(str(inputspec_div)).strip()
    md = md[len('Input'):] # remove prefix
    return ProblemScraper._latexify(md)
  
  @staticmethod
  def _output_specification_from_problem (problem: element.Tag) -> str:
    outputspec_div = problem.find('div', { 'class': 'output-specification' })
    md = markdownify(str(outputspec_div)).strip()
    md = md[len('Output'):] # remove prefix
    return ProblemScraper._latexify(md)
  
  @staticmethod
  def _latexify (s: str) -> str:
    return s.replace('$$$', '$').replace('$$', '$')

if __name__ == '__main__':
  # scraper = ProblemScraper('https://codeforces.com/problemset/problem/4/A')
  scraper = ProblemScraper('https://codeforces.com/problemset/problem/1614/E')
  scraper.scrape()
