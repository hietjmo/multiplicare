
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


"""
output:

     2×30=60     38×2=76     3×18=54     24×4=96     13×7=91
     12×6=72     3×14=42     15×6=90     5×18=90     2×39=78
     11×5=55     16×3=48      7×2=14     6×16=96      5×8=40
     2×18=36      8×7=56     10×8=80     6×15=90      8×2=16
     2×20=40     14×3=42     15×5=75     11×4=44     24×2=48
      7×5=35     16×4=64     32×3=96     30×3=90     47×2=94
     14×2=28     29×2=58     29×3=87     18×5=90     5×19=95
     8×12=96     2×36=72     4×24=96     45×2=90      6×7=42
     40×2=80     3×31=93     5×17=85     4×17=68      4×8=32
     3×13=39     2×15=30      5×3=15     2×12=24      2×8=16
     17×4=68     2×19=38     13×2=26     3×29=87     2×45=90
     22×4=88     12×4=48      5×2=10     25×3=75     46×2=92
      3×8=24     2×27=54     7×10=70     5×10=50     3×21=63
      6×9=54     14×6=84     2×40=80      9×2=18      2×7=14
     26×2=52     2×14=28     21×2=42      9×7=63     2×49=98
      9×4=36     14×5=70     12×7=84     12×8=96      9×8=72
     33×2=66      8×5=40     14×4=56      6×8=48     2×34=68
     4×22=88     6×14=84     2×24=48      2×6=12     10×5=50
     6×13=78     9×11=99     3×23=69     48×2=96      3×6=18
     23×3=69     2×16=32      8×9=72     3×24=72      7×9=63
"""
