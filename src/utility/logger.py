#!/usr/bin/env python3

import sys

from colors import Color

context = {
  'stream': sys.stderr,
  'info': True,
  'debug': True,
  'error': True
}

def info (message) -> None:
  if not context['info']:
    return
  
  colors = [
    (Color.background_rgb, (0, 192, 0)),
    (Color.foreground_rgb, (0, 0, 0)),
    (Color.bold, ())
  ]

  m = '[INFO]'
  for color in colors:
    m = color[0](*color[1], m)
  m = m + ': ' + Color.foreground_rgb(160, 220, 160, message)
  print(m, file = context['stream'])

def error (message) -> None:
  if not context['error']:
    return
  
  colors = [
    (Color.background_rgb, (192, 0, 0)),
    (Color.foreground_rgb, (0, 0, 0)),
    (Color.bold, ())
  ]

  m = '[ERROR]'
  for color in colors:
    m = color[0](*color[1], m)
  m = m + ': ' + Color.foreground_rgb(220, 160, 160, message)
  print(m, file = context['stream'])

def debug (message):
  if not context['debug']:
    return
  
  colors = [
    (Color.background_rgb, (0, 128, 192)),
    (Color.foreground_rgb, (0, 0, 0)),
    (Color.bold, ())
  ]

  m = '[DEBUG]'
  for color in colors:
    m = color[0](*color[1], m)
  m = m + ': ' + Color.foreground_rgb(160, 160, 220, message)
  print(m, file = context['stream'])

if __name__ == '__main__':
  info('INFO is to display information related messages')
  error('ERROR is to display error related messages')
  debug('DEBUG is to display debugging related messages')
