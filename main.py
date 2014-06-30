# -*- coding: utf-8 -*-

# Universidade Federal da Bahia
# Estrutura de Dados e Algoritmos II
# Author: @marciovicente
# Email: marciovicente.filho@gmail.com

import sys
import struct
import os
import pickle
import math

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
    self.count = 0
    self.parent = None
    super(Node, self).__init__()


class Application(object):
  """ Main Application Class """

  def __init__(self):
    self.filename = 'file.dat'
    self.file = None
    self.ORDER = 2
    self.STRUCT_SIZE = 2
    self.SLOTS = 0
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
        value = raw_input()
        self.query(value)
      elif operation is 'r':
        value = raw_input()
        self.remove(value=value)
      elif operation is 'p':
        self.print_file()
      operation = raw_input()
    return

  def insert_record(self, value=None, index=None):
    value = int(raw_input())
    label = raw_input()
    age = int(raw_input())

    r = Record()
    r.value = value
    r.label = label
    r.age = age

    self.open_file()
    self.file.seek((index or 0) * self.STRUCT_SIZE)
    obj = None
    try:
      obj = pickle.loads(self.file.read())
    except Exception:
      pass

    if isinstance(obj, Node): # IF RETRIEVE THE ROOT
      node = obj
      if node.count < (2 * self.ORDER): # ONLY IF HAS SPACE IN NODE
        for idx,n in enumerate(node.records):
          if value == n.value:
            print 'chave ja existente: %s' % value
            return False

          if value < n.value and node.pointers[idx] == 0:
            # tenho que inserir antes
            node.records.insert(idx-1 if idx > 0 else idx, r)
            node.pointers.insert(idx, 0)
            node.count += 1
            self.SLOTS += 1
            self.file.seek(0)
            self.file.write(pickle.dumps(node))
            self.close_file()
            return True
          if value > n.value and value < node.records[idx + 1 if idx+1 < node.count else idx].value and node.pointers[idx] == 0:
            node.records.insert(idx, r)
            node.pointers.insert(idx, 0)
            node.count += 1
            self.SLOTS += 1
            self.file.seek(0)
            self.file.write(pickle.dumps(node))
            self.close_file()
            return True
          elif node.pointers[idx] != 0: # ou seja, caso exista um nó filho
            node_to_insert = node.pointers[idx]
            return self.insert_record(value=value, index=node_to_insert) # chamo a recursão para a proxima pagina
          # return True
      else:
        # primeiro tenho que inserir pra achar o do meio
        # tenho que percorrer todo a lista pra achar a posição
        aux_node = node.records
        for idx,n in enumerate(node.records):
          if value < node.records[idx].value:
            aux_node.insert(idx, r) # insiro temporariamente para achar o meio
            break
        medium = aux_node[len(node.records)/2 + 1] # esse é o nó que vira raiz
        self.split_tree(aux_node[:self.ORDER], medium, aux_node[-self.ORDER:], parent=True if node.parent else False)

    else:
      # CREATE THE ROOT
      node = Node()
      node.records.append(r)
      node.pointers.append(0)
      node.count += 1
      self.SLOTS += 1
      self.file.seek(0)
      self.file.write(pickle.dumps(node))
      self.close_file()
      return True
      # else: tem q criar outro no pra inserir

  def split_tree(self, left_child, medium, right_child, parent=False):
    # a pagina que tiver left_child e right_child deve ter o parent apontando median
    # mas antes tenho que testar se posso inserir median em alguma outra raiz
    left_node = right_node = Node()

    left_node.records = left_child
    left_node.count = right_node.count = len(left_child) # Considerando que ambos tem o mesmo tamanho
    right_node.records = right_child
    left_node.parent = right_node.parent = medium # setando o pai
    # primeiro tenho que verificar se o pai vai virar um novo nó ou será inserido em algum outro nó
    if parent:
      # tenho que tentar passar ele pra o pai
        # e aqui dentro case tenha pai terei q chamar a recursao
      pass
    else:
      # ou seja, eu vou substituir a atual raiz pelo node_root (overriding)
      node_root = Node()
      node_root.records = medium
      node_root.count += 1

      node_root.pointers.insert(0, self.SLOTS) # inserindo o da esquerda
      self.SLOTS += 1
      node_root.pointers.insert(1, self.SLOTS) # inserindo o da direita
      self.file.seek(0)
      self.file.write(pickle.dumps(node_root))
      self.close_file()

  def query(self, value, position=None):
    self.open_file()
    self.file.seek((position or 0) * self.STRUCT_SIZE)
    node = None
    try:
      node = pickle.loads(self.file.read())
    except Exception:
      pass
    if node:
      for n,idx in enumerate(node.records):
        if value == n.value:
          print 'chave: %s' % n.value
          print n.label
          print n.age
          return True

        if value < n.value:
          if not n.pointers[idx]: # ou seja, caso não tenha filho
            print 'chave não encontrada: %s' % value
          else: # tenho que descer pra o filho à esquerda
            index = n.pointers[idx]
            return self.query(value=value, position=index) # chamando a recursão para o outro nó

        if value > n.value and value < node.records[idx + 1 if idx+1 < node.count else idx].value:
          # ou seja, cheguei no intervalo do numero desejado mas n achei um filho
          if node.pointers[idx] == 0:
            print 'chave não encontrada: %s' % value
            return False
          index = n.pointers[idx]
          return self.query(value=value, position=index) # chamando a recursão para o outro nó

  def open_file(self):
    self.file = open(self.filename, 'r+b')

  def close_file(self):
    if self.file:
      self.file.close()

app = Application()
app.main()
