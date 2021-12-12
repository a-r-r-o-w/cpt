#!/usr/bin/env python3

class Color:
  """Colorful terminal Output"""

  @staticmethod
  def the80s (color: int, content: str) -> str:
    return f'\x1b[{color}m{content}\x1b[0m'
  
  @staticmethod
  def foreground_rgb (r: int, g: int, b: int, content: str) -> str:
    return f'\x1b[38;2;{r};{g};{b}m{content}\x1b[0m'
  
  @staticmethod
  def background_rgb (r: int, g: int, b: int, content: str) -> str:
    return f'\x1b[48;2;{r};{g};{b}m{content}\x1b[0m'
  
  @staticmethod
  def foreground (value: int, content: str) -> str:
    return f'\x1b[38;5;{value}m{content}\x1b[0m'
  
  @staticmethod
  def background (value: int, content: str) -> str:
    return f'\x1b[48;5;{value}m{content}\x1b[0m'
  
  @staticmethod
  def bold (content: str) -> str:
    return Color.the80s(1, content)
  
  @staticmethod
  def faint (content: str) -> str:
    return Color.the80s(2, content)
  
  @staticmethod
  def italic (content: str) -> str:
    return Color.the80s(3, content)
  
  @staticmethod
  def underline (content: str) -> str:
    return Color.the80s(4, content)
  
  @staticmethod
  def slowblink (content: str) -> str:
    return Color.the80s(5, content)

  @staticmethod
  def rapidblink (content: str) -> str:
    return Color.the80s(6, content)
  
  @staticmethod
  def reverse (content: str) -> str:
    return Color.the80s(7, content)
  
  @staticmethod
  def conceal (content: str) -> str:
    return Color.the80s(8, content)

  @staticmethod
  def strikethrough (content: str) -> str:
    return Color.the80s(9, content)
  
  @staticmethod
  def doubleunderline (content: str) -> str:
    return Color.the80s(21, content)

if __name__ == '__main__':
  print('{:^75}'.format(Color.underline('Color Test')), '\n')

  print('{0:^30}{1:^45}'.format('foreground', 'background'), '\n')

  for i in range(0, 256, 6):
    for j in range(i, min(i + 6, 256)):
      print(Color.foreground(j, '{0:^5}'.format(j)), end = ' ');
    
    for j in range(i, min(i + 6, 256)):
      print(Color.background(j, '{0:^5}'.format(j)), end = ' ');
    
    print()
  
  print('\n{:^40}\n'.format('256 random background and foreground colors'))

  import random

  for i in range(256):
    rb = random.randint(0, 255)
    gb = random.randint(0, 255)
    bb = random.randint(0, 255)
    rf = random.randint(0, 255)
    gf = random.randint(0, 255)
    bf = random.randint(0, 255)

    print(Color.background_rgb(rb, gb, bb, Color.foreground_rgb(rf, gf, bf, 'color')), end = ' ')
    
    if (i + 1) % 8 == 0:
      print()
  
  print('\n{:^40}\n'.format('The 80s'))
  for i in range(256):
    print(Color.the80s(i, '{0:^5}'.format(i)), end = '')
    
    if (i + 1) % 8 == 0:
      print()
