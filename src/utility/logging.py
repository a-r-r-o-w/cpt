#!/usr/bin/env python3

import sys

from colors import Color

class Logger:
  def __init__ (self, stream = sys.stderr):
    self.stream = stream

  def info (self, message):
    colors = [
      (Color.background_rgb, (0, 192, 0)),
      (Color.foreground_rgb, (0, 0, 0)),
      (Color.bold, ())
    ]

    m = '[INFO]'
    for color in colors:
      m = color[0](*color[1], m)
    m = m + ': ' + Color.foreground_rgb(160, 220, 160, message)
    print(m, file = self.stream)
  
  def error (self, message):
    colors = [
      (Color.background_rgb, (192, 0, 0)),
      (Color.foreground_rgb, (0, 0, 0)),
      (Color.bold, ())
    ]

    m = '[ERROR]'
    for color in colors:
      m = color[0](*color[1], m)
    m = m + ': ' + Color.foreground_rgb(220, 160, 160, message)
    print(m, file = self.stream)
  
  def debug (self, message):
    colors = [
      (Color.background_rgb, (0, 128, 192)),
      (Color.foreground_rgb, (0, 0, 0)),
      (Color.bold, ())
    ]

    m = '[DEBUG]'
    for color in colors:
      m = color[0](*color[1], m)
    m = m + ': ' + Color.foreground_rgb(160, 160, 220, message)
    print(m, file = self.stream)

if __name__ == '__main__':
  log = Logger()

  log.info('INFO is to display information related messages')
  log.error('ERROR is to display error related messages')
  log.debug('DEBUG is to display debugging related messages')
