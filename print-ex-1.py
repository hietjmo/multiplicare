
import random

class S:
  def __init__(self):
    self.data = []

self = S ()

self.columns = 5
self.rows = 20

def create_table ():
  table = []
  for a in range (2,50):
    for b in range (2,50):
      c = a * b
      if 10 <= c <= 99:
        table.append ((a,b,c))
  return table


def lottery (self):
  random.shuffle (self.qs)
  self.questions = {}
  for i in range (0,self.columns):
    for j in range (0,self.rows):
      self.questions [i,j] = self.qs [i*self.rows+j]

self.table = create_table ()
self.qs = self.table [:]

lottery (self)
for j in range (0,self.rows):
  for i in range (0,self.columns):
    a,b,c = self.questions [i,j]
    txt1 = f"{a}×{b}={c}"
    print (f"{txt1:>12}",end="")
  print ()


