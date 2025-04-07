
import pygame
import random
from datetime import datetime
import time
import json
import sys
import argparse
import builtins

def print (*xs, log=False,**kwargs):
  if args.log or log:
    return builtins.print(*xs, **kwargs)

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-wx", "--width", type=int, default=1000)
  pad ("-hy", "--height", type=int, default=750)
  pad ("--rows", type=int, default=20)
  pad ("--cols", type=int, default=5)
  pad ("--font", default="fonts/Ubuntu-R.ttf")
  pad ("--fontsize", type=float, default=30)
  pad ("--logkeys", action="store_true")
  pad ("--log", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

numlockkeys = [98,89,90,91,92,93,94,95,96,97]
FASTTICK = pygame.USEREVENT
SLOWTICK = FASTTICK + 1

openmojipalette = {
  'blue': '#92d3f5', 'blueshadow': '#61b2e4', 'red': '#ea5a47',
  'redshadow': '#d22f27', 'green': '#b1cc33', 'greenshadow': '#5c9e31',
  'yellow': '#fcea2b', 'yellowshadow': '#f1b31c', 'white': '#ffffff',
  'lightgrey': '#d0cfce', 'grey': '#9b9b9a', 'darkgrey': '#3f3f3f',
  'slategray': '#4b5563', 'almostwhite': '#f0f0ff',
  'bggrey': '#333333', 'black': '#000000', 'orange': '#f4aa41',
  'orangeshadow': '#e27022', 'pink': '#ffa7c0', 'pinkshadow': '#e67a94',
  'purple': '#b399c8', 'purpleshadow': '#8967aa', 'brown': '#a57939',
  'brownshadow': '#6a462f', 'LightSkinTone': '#fadcbc',
  'MediumLightSkinTone': '#debb90', 'MediumSkinTone': '#c19a65',
  'MediumDarkSkinTone': '#a57939', 'DarkSkinTone': '#6a462f',
  'DarkSkinShadow': '#352318', 'NavyBlue': '#1e50a0',
  'Maroon': '#781e32', 'DarkGreen': '#186648'}

def hex_to_rgb (hex):
  h = hex.lstrip ('#')
  return tuple (int (h[i:i+2], 16) for i in (0, 2, 4))

def om (name,alpha=255):
  return hex_to_rgb (openmojipalette [name]) + (alpha,)

def create_table ():
  table = []
  for a in range (2,50):
    for b in range (2,50):
      c = a * b
      if 10 <= c <= 99:
        table.append ((a,b,c))
  return table

screen_w, screen_h = args.width,args.height

introduce,finalscore,scoreboard,countdown,game,done = (
  "introduce","finalscore","scoreboard","countdown","game","done")

def read_results (self):
  self.filename = f"{self.rows}x{self.columns}-results.json"
  try:
    self.results = json.load (open (self.filename,"r"))
  except:
    self.results = []
  self.logfile = "logfile.json"
  try:
    self.logs = json.load (open (self.logfile,"r"))
  except:
    self.logs = []


def init (self):
  pygame.init ()
  pygame.display.set_caption ("Multiplicare")
  self.screen = pygame.display.set_mode ((screen_w, screen_h))
  self.clock = pygame.time.Clock ()
  self.margin_x,self.margin_y = 40,15
  self.cursor_x,self.cursor_y = 0,0
  if args.font == "None":
    args.font = None
  self.textfont = pygame.font.Font (args.font, args.fontsize)
  self.hugefont = pygame.font.Font (args.font, int(screen_h/2))
  self.finalfont = pygame.font.Font (args.font, int(screen_h/6))
  self.resultfont = pygame.font.Font (args.font, int(args.fontsize/2))
  testtext = "33×3=99"
  img = self.textfont.render (testtext,True,om ("white"))
  self.samplew = img.get_width ()
  self.textheight = img.get_height ()
  img = self.resultfont.render (testtext,True,om ("orange"))
  self.resulth =img.get_height ()
  self.columns = args.cols
  self.rows = args.rows
  self.columnw = (screen_w-2*self.margin_x)/self.columns
  self.rowh = (screen_h-(2*self.margin_y+self.resulth))/self.rows
  self.table = create_table ()
  self.qs = self.table [:]
  self.resultline = ""
  self.running = True
  self.state = introduce
  self.starttime = None
  self.final = None
  self.latest = None
  self.answered = -1
  self.errors,self.corrects,self.hots = {},{},{}
  self.answer = ""
  self.lastlog = []; self.logs = []
  self.countdown = 5
  read_results (self)
  pygame.time.set_timer (SLOWTICK, 5000)

def lottery (self):
  random.shuffle (self.qs)
  self.questions = {}
  for i in range (0,self.columns):
    for j in range (0,self.rows):
      self.questions [i,j] = self.qs [i*self.rows+j]

def draw_screen (self):
  self.screen.fill (om ("slategray"))
  if self.state in [game,done]:
    for i in range (0,self.columns):
      for j in range (0,self.rows):
        x = self.margin_x + i * self.columnw + self.samplew
        y = self.margin_y + self.resulth + j * self.rowh
        a,b,c = self.questions [i,j]
        txt1 = f"{a}×{b}="
        txt2 = f"{a}×{b}={c}"
        img1 = self.textfont.render (txt1,True,om ("white"))
        w1 = img1.get_width() 
        img2 = self.textfont.render (txt2,True,om ("white"))
        cnt = i * self.rows + j
        if self.answered == cnt:
          img3 = self.textfont.render (txt1+self.answer,True,om ("white"))
          self.screen.blit (img3, (x-w1,y))
        if cnt in self.errors:
          txt3 = f"{a}×{b}≠{self.errors[cnt]}"
          img3 = self.textfont.render (txt3,True,om ("red"))
          self.screen.blit (img3, (x-w1,y))
        if cnt in self.corrects and cnt not in self.hots:
          txt3 = "correct"
          img3 = self.textfont.render (txt3,True,om ("green"))
          w1 = img3.get_width() 
          self.screen.blit (img3, (x-w1+15,y))
        if cnt in self.hots:
          txt3 = f"{a}×{b}={a*b}"
          img3 = self.textfont.render (txt3,True,om ("white"))
          self.screen.blit (img3, (x-w1,y))
          self.hots[cnt] = self.hots[cnt] - 1
          if self.hots[cnt] <= 0:
            del self.hots[cnt]
    img = self.resultfont.render (self.resultline,True,om ("white"))
    w2 = img.get_width ()
    self.screen.blit (img, (screen_w - (self.margin_x + w2),1))
  elif self.state == countdown:
      s1 = str (self.countdown)
      img1 = self.hugefont.render (s1,True,om ("white"))
      w1 = img1.get_width() 
      h1 = img1.get_height()
      self.screen.blit (img1,(screen_w/2 - w1/2,screen_h/2 - h1/2))
  elif self.state == finalscore:
      ft = f"{self.final:.2f} s"
      img1 = self.finalfont.render (ft,True,om ("white"))
      w1 = img1.get_width() 
      h1 = img1.get_height()
      self.screen.blit (img1,(screen_w/2 - w1/2,screen_h/2 - h1/2))
  elif self.state == introduce:
      hlp = "s = start, q = quit"
      img = self.resultfont.render (hlp,True,om ("white"))
      w2 = img.get_width ()
      self.screen.blit (img, (screen_w - (self.margin_x + w2),1))
      ft = f"multiplicare"
      img1 = self.finalfont.render (ft,True,om ("white"))
      w1 = img1.get_width() 
      h1 = img1.get_height()
      self.screen.blit (img1,(screen_w/2 - w1/2,screen_h/2 - h1/2))
  elif self.state == scoreboard:
      hlp = "s = start, q = quit"
      img = self.resultfont.render (hlp,True,om ("white"))
      w2 = img.get_width ()
      self.screen.blit (img, (screen_w - (self.margin_x + w2),1))
      for j,res in enumerate (self.results):
        color1 = om ("white")
        if j % 2 == 0:
          color1 = om ("purple")
        x = self.margin_x
        y = self.margin_y + self.resulth + j * self.textheight
        txt5 = f"{res[1]}"
        img5 = self.textfont.render (txt5,True,color1)
        self.screen.blit (img5, (x+20,y))
        txt4 = f"{res[0]:.2f} s"
        img4 = self.textfont.render (txt4,True,color1)
        w4 = img4.get_width() 
        self.screen.blit (img4, (500-w4,y))
        if self.latest and res == self.latest:
          txt5 = "#"
          img5 = self.textfont.render (txt5,True,color1)
          self.screen.blit (img5, (510,y))

def start_game (self):
  self.state = game
  lottery (self)
  self.starttime = time.time ()
  pygame.time.set_timer (FASTTICK, 195)
  print ("Started.")
  self.answered = 0
  self.answer = ""
  self.lastlog = [datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
  self.final = None
  self.errors,self.corrects,self.hots = {},{},{}

def judge (self):
  i,j = divmod (self.answered, self.rows)
  a,b,c = self.questions [i,j]
  if self.answer == f"{c}":
    self.corrects [self.answered] = self.answer
    self.hots [self.answered] = 3
    print ("right")
  else:
    self.errors [self.answered] = self.answer
    print (f"{a}×{b}={c}")
    print ("wrong")
  self.answered = self.answered + 1
  if self.answered >= self.rows * self.columns:
    pygame.time.set_timer (FASTTICK, 0)
    self.resultline = ""
    now = time.time ()
    secs = now - self.starttime
    secs = secs + 20 * (len(self.errors))
    self.final = secs
    self.lastlog.append (secs)
    print (secs)
    self.state = done
    timetext = datetime.today().strftime('%Y-%m-%d %H:%M')
    self.latest = [secs,timetext]
    self.results = self.results [:18]
    self.results.append (self.latest)
    self.results.sort ()
    self.logs = self.logs [:30]
    self.logs.insert (0,self.lastlog)
    pygame.time.set_timer (SLOWTICK, 2000)
  self.answer = ""

def fasttick (self):
  now = time.time ()
  secs = now - self.starttime
  secs = secs + 20 * (len(self.errors))
  self.resultline = f"time: {int(secs)} s"

def logkey (self):
  now = time.time ()
  secs = now - self.starttime
  i,j = divmod (self.answered, self.rows)
  a,b,c = self.questions [i,j]
  question = f"{a}x{b}={c}"
  self.lastlog.append ([round(secs,2),[a,b],self.answer])
  print (self.lastlog,log=args.logkeys)

def handle_key_press (self, event):
  ctrl = event.mod & pygame.KMOD_CTRL
  shift = event.mod & pygame.KMOD_SHIFT
  hw2 = event.scancode
  key = event.key
  keyname = event.unicode
  print ("Pressed:", keyname,hw2,key)
  if hw2 in numlockkeys:
    keyname = str (numlockkeys.index (hw2))
  if "0" <= keyname <= "9":
    if self.state == game:
      self.answer += keyname
      logkey (self)
      if len (self.answer) == 2:
        judge (self)
    else:
      self.countdown = int (keyname) 
      self.state = countdown
      pygame.time.set_timer (SLOWTICK, 1000)

  elif key == pygame.K_BACKSPACE :
    self.answer = self.answer [:-1]
  if key == pygame.K_ESCAPE:
    pygame.time.set_timer (FASTTICK, 0)
    self.state = introduce
  if key == pygame.K_q:
    print ("Q pressed. Quitting.")
    self.running = False
  if key in [pygame.K_s,pygame.K_SPACE,pygame.K_KP_ENTER,pygame.K_RETURN]:
    print ("S pressed. Starting.")
    self.state = countdown
    self.countdown = 5
    pygame.time.set_timer (SLOWTICK, 1000)

def slowtick (self):
  if self.state == countdown:
    if self.countdown == 0:
      pygame.time.set_timer (SLOWTICK, 0)
      start_game (self)
    self.countdown = self.countdown -1
    pygame.time.set_timer (SLOWTICK, 1000)
  if self.state == introduce:
    if len (self.results) > 2:
      self.state = scoreboard
  if self.state == finalscore:
    self.state = scoreboard
  if self.state == done:
    pygame.time.set_timer (SLOWTICK, 0)
    self.state = finalscore
    pygame.time.set_timer (SLOWTICK, 5000)
def do_quit (self):
  self.running = False

class S:
  def __init__(self):
    self.data = []

self = S ()
init (self)

while self.running:
  for event in pygame.event.get ():
    if event.type == pygame.QUIT:
      do_quit (self)
    elif event.type == pygame.KEYDOWN:
      handle_key_press (self, event)
    elif event.type == FASTTICK:
      fasttick (self)
    elif event.type == SLOWTICK:
      slowtick (self)
  draw_screen (self)
  pygame.display.update ()
  print (self.state,log=False)
  self.clock.tick (10)

self.results = self.results [:18]
json.dump (self.results, open (self.filename,"w"))
self.logs = self.logs [:30]
json.dump (self.logs, open (self.logfile,"w"))

