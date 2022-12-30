#!/usr/bin/env python3

import asyncio
import fire

from api.leetcode.leetcode_cli import LeetcodeCLI

class CLI:
  def __init__ (self):
    self.leetcode = LeetcodeCLI()

if __name__ == '__main__':
  fire.core.Display = lambda lines, out: print(*lines, file = out)
  fire.Fire(CLI())

# if __name__ == '__main__':
#   async def main ():
#     api = leetcode.LeetcodeAPI()
    
#     # problem = await api.question_data(title = 'divide-two-integers')
#     problem = await api.question_data(title = 'minimum-obstacle-removal-to-reach-corner')
#     print(problem.to_markdown())

#     await api.session.close()
  
#   asyncio.run(main())
