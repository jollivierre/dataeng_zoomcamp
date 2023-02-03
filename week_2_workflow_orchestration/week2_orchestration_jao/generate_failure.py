# example of generating a faliure

from random import randint

if randint(0,1) > 0:
    raise Exception

print('no error')