# -*- coding: utf-8 -*-

# Universidade Federal da Bahia
# Estrutura de Dados e Algoritmos II
# Author: @marciovicente
# Email: marciovicente.filho@gmail.com

import sys, struct, os, pickle
sys.path.insert(0, 'libs/')

class Record(object):

  def __init__(self):
    self.value = None
    self.label = None
    self.age = None
    super(Record, self).__init__()


class Node(object):

  def __init__(self):
    self.records = [] # 2*ORDER
    self.pointers = [] # 2*ORDER + 1
    super(Node, self).__init__()


class Application(object):
  """ Main Application Class """

  def __init__(self):
    self.filename = 'file.dat'
    self.file = None
    self.ORDER = 2
    self.STRUCT_SIZE = 2
    super(Application, self).__init__()

  def init_file(self):
    self.open_file()
    self.set_struct_size()
    self.file.seek(self.STRUCT_SIZE)
    self.close_file()

  def create_file(self):
    self.file = file(self.filename, 'w+b')

  def set_struct_size(self):
    r = Record()
    r.value = r.age = 1
    r.label = 'A'*20

    # CREATING A NEW NODE (THE ROOT)
    n = Node()
    n.records = [r] * (2 * self.ORDER)
    n.pointers = [0] * (2 * self.ORDER + 1)

    dumpped = pickle.dumps(n)
    self.STRUCT_SIZE = sys.getsizeof(dumpped)

  def main(self):
    if not os.path.exists(self.filename):
      self.create_file()
      self.init_file()

    operation = raw_input()
    while operation is not 'e':
      if operation is 'i':
        self.insert_record()
      elif operation is 'c':
        self.query()
      elif operation is 'r':
        value = raw_input()
        self.remove(value=value)
      elif operation is 'p':
        self.print_file()
      operation = raw_input()
    return

  def insert_record(self):
    value = raw_input()
    label = raw_input()
    age = raw_input()

    r = Record()
    r.value = int(value)
    r.label = label
    r.age = int(age)

    self.open_file()
    self.file.seek(0)
    obj = None
    try:
      obj = pickle.loads(self.file.read())
    except Exception:
      pass

    if isinstance(obj, Node): # IF RETRIEVE THE ROOT
      print 'is instance'
    else:
      # CREATE THE ROOT
      node = Node()
      node.records.append(r)
      node.pointers.append(0)
      self.file.seek(0)
      self.file.write(pickle.dumps(node))
      self.close_file()
      return True

  def open_file(self):
    self.file = open(self.filename, 'r+b')

  def close_file(self):
    if self.file:
      self.file.close()

app = Application()
app.main()
