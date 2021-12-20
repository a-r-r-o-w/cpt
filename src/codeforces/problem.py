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
from utility.colors  import Color

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
    id: int = None,
    index: str = None,
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
    self.url = url
    self.id = id
    self.index = index
    self.name = name,
    self.time_limit = time_limit,
    self.memory_limit = memory_limit,
    self.input_file = input_file,
    self.output_file = output_file,
    self.statement = statement,
    self.input_specification = input_specification,
    self.output_specification = output_specification,
    self.notes = notes
  
  def brief_info (self):
    pretty = f"""
               Problem {self.id}/{self.index}
         Name: {self.name}
         Link: {self.url}
        Input: {self.input_file}
       Output: {self.output_file}
   Time Limit: {self.time_limit}
 Memory Limit: {self.memory_limit}
"""
    return pretty
  
  def markdown (self):
    md = f"""
# [{self.id}/{self.index} {self.name}]({self.url})

**Input file: {self.input_file}**

**Output file: {self.output_file}**

**Time limit: {self.time_limit}**

**Memory limit: {self.memory_limit}**

### Statement

{self.statement}

### Input

{self.input_specification}

### Output

{self.output_specification}

### Notes

{self.notes}
"""
    return md

class ProblemScraper:
  """Problem Scraper for https://codeforces.com"""

  def __init__ (self, url: str):
    self.url = url
    self.problem = Problem()

    self.scraped_content: element.Tag = None
  
  def scrape (self) -> Problem:
    log.info(f'Sending request to {self.url}')
    r = requests.get(self.url)
    s = BeautifulSoup(r.text, features = 'lxml')

    if r.status_code != 200:
      log.error(f'Request to {self.url} failed with status code: {r.status_code}')
    
    log.info('Parsing scraped content')

    self.scraped_content = s.find('div', {'class': 'problem-statement'})
    self.parse()

    pretty_info = Color.bold(
      Color.foreground_rgb(120, 200, 250, self.problem.brief_info())
    )

    log.info('Problem Info:\n' + pretty_info)
  
  def parse (self):
    self.problem.index = self._get_index()
    self.problem.url = self.url
    self.problem.id = self._get_id()
    self.problem.name = self._get_name()
    self.problem.time_limit = self._get_time_limit()
    self.problem.memory_limit = self._get_memory_limit()
    self.problem.input_file = self._get_input_file()
    self.problem.output_file = self._get_output_file()
    self.problem.statement = self._get_statement()
    self.problem.input_specification = self._get_input_specification()
    self.problem.output_specification = self._get_output_specification()
  
  def _get_name (self) -> str:
    name_div = self.scraped_content.find('div', { 'class': 'title' })
    title = name_div.text
    name = ' '.join(title.split()[1:])
    return name
  
  def _get_id (self) -> str:
    return int(self.url.split('/')[-2])
  
  def _get_index (self) -> str:
    index_div = self.scraped_content.find('div', { 'class': 'title' })
    title = index_div.text
    index = title.split()[0][:-1]
    return index
  
  def _get_time_limit (self) -> str:
    tl_div = self.scraped_content.find('div', { 'class': 'time-limit' })
    tl = tl_div.text.strip()
    tl = tl[len('time limit per test'):] # remove prefix
    return tl
  
  def _get_memory_limit (self) -> str:
    ml_div = self.scraped_content.find('div', { 'class': 'memory-limit' })
    ml = ml_div.text.strip()
    ml = ml[len('memory limit per test'):] # remove prefix
    return ml
  
  def _get_input_file (self) -> str:
    inputfile_div = self.scraped_content.find('div', { 'class': 'input-file' })
    inputfile = inputfile_div.text.strip()
    inputfile = inputfile[len('input'):] # remove prefix
    return inputfile
  
  def _get_output_file (self) -> str:
    outputfile_div = self.scraped_content.find('div', { 'class': 'output-file' })
    outputfile = outputfile_div.text.strip()
    outputfile = outputfile[len('output'):] # remove prefix
    return outputfile
  
  def _get_statement (self) -> str:
    statement_div = self.scraped_content.find_all('div')[10]
    md = markdownify(str(statement_div)).strip()
    return ProblemScraper._latexify(md)
  
  def _get_input_specification (self) -> str:
    inputspec_div = self.scraped_content.find('div', { 'class': 'input-specification' })
    md = markdownify(str(inputspec_div)).strip()
    md = md[len('Input'):] # remove prefix
    return ProblemScraper._latexify(md)
  
  def _get_output_specification (self) -> str:
    outputspec_div = self.scraped_content.find('div', { 'class': 'output-specification' })
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
  print(scraper.problem.markdown())
