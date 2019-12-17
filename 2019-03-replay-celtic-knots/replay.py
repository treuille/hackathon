import sys
import os

commits = [
    '5f4055e01cfbad12e7fd6a9cdbbdaa785f591cce',
    'dda1b475ae13538c5b32608fccfc49f9134a9ba9',
    'bfd05b9806c0e90b8d36541274cb93dd2f5a1761',
    '54975cf0d66d6fce815c9b0306c5c2a8d22288ee',
    'bfa38c9dcb45dca0f62c51522c6c99c81a8d130f',
    'd391d41cea0485f7ee9e6f45918094aaf7e30e32',
    'bfa00d9a1d71f53bfe95a98c599b89a3e3a1937a',
    '4085f55cf69651df9318486b2defb3640a24c4f0',
    'bc640eae11bc7d6d0047febb8ffff0f6a285c137',
    'a4d759d2861b577e3a489589057f60c2b748aa2e',
    'a1c0c8584efcb402a485f00494049d6aa6a075fd',
]
commits.reverse()

try:
    commit = commits[int(sys.argv[1])]
    print('The commit is', commit)
    os.system('git checkout %s' % commit)
    os.system('python ./celtic.py')

except IndexError:
    print('Must have 0 <= commit_num < %i.' % len(commits))
