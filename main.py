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
    self.prev = None
    self.next  = None
    super(Record, self).__init__()

  def __repr__(self):
      return repr((self.prev,self.value,self.next))

class Node(object):

  def __init__(self):
    self.records = [] # 2*ORDER
    self.pointers = [] # 2*ORDER + 1
    self.x = 0
    self.parent = None
    super(Node, self).__init__()

  def __repr__(self):
      return repr((self.records))


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

    r = Record()
    r.value = r.age = r.label = r.next = r.prev = None

    n = Node()
    n.records = [r] * (2 * self.ORDER)
    n.pointers = [None] * (2 * self.ORDER + 1)


    dumpped = pickle.dumps(n)

    self.file.seek(0)
    self.file.write(dumpped)

    self.close_file()

  def create_file(self):
    self.file = file(self.filename, 'w+b')

  def set_struct_size(self):
    r = Record()
    r.value = r.age = 1
    r.label = 'A'*20
    r.next =  999
    r.prev = 999

    # CREATING A NEW NODE (THE ROOT)
    n = Node()
    n.records = [r] * (2 * self.ORDER)
    n.pointers = [0] * (2 * self.ORDER + 1)

    dumpped = pickle.dumps(n)
    self.STRUCT_SIZE = sys.getsizeof(dumpped * 50)

  def main(self):
    if not os.path.exists(self.filename):
      self.create_file()
      self.init_file()

    operation = raw_input()
    while operation is not 'e':
      if operation is 'i':
        value = raw_input()
        label = raw_input()
        age = raw_input()
        r = Record()
        r.value = int(value)
        r.label = str(label)
        r.age = int(age)
        r.prev = None
        r.next = None
        self.insert_record(0,r,None)
      elif operation is 'c':
        value = raw_input()
        self.consulta_chave(int(value))
      elif operation is 'r':
        value = raw_input()
        self.remove(value)
      elif operation is 'p':
        self.print_nodes()
      elif operation is 'o':
        self.print_asc_tree();
      operation = raw_input()
    return

  def insert_record(self, pont, node_ins, index):
    # self.print_all()
    if pont == None:
      index = node_ins
      return index
    else:
      node = self.get_node(pont)
      v_ext = self.value_check(node_ins.value,node)
      pos = self.node_next(node,node_ins.value)

    if v_ext:
      print("chave ja existente: %s" % node_ins.value)
      return None

    flag_r = self.insert_record(pos,node_ins,index)

    if flag_r == None:
      return

    else:
      index = flag_r
      if not self.node_is_full(node):
        node = self.get_node(pont)
        node_s = self.insert_node(node,index)
        self.save_node(node_s,pont)
        return None
      else:

        mn = self.make_overflow(node,index)
        mobj = mn.records[len(mn.records)/2]
        mobj.prev = pont
        mobj.next = pont+1
        node.records.pop(len(mn.records)/2)
        mn = self.refreshing(mn,pont)

        for x in range((len(mn.records)/2),len(mn.records)) :
          if not self.is_leaf(mn):
            if(mn.records[x].prev != None):
              mn.records[x].prev = mn.records[x].prev + 1
            if(mn.records[x].next != None):
              mn.records[x].prev = mn.records[x].next + 1
        newnode = Node()

        for x in range((len(mn.records)/2),len(mn.records)) :
          newnode.records.append(mn.records[x])
        for x in range(len(node.records)/2,len(node.records)) :
          r = Record()
          r.value = r.age = r.label = r.next = r.prev = None
          newnode.records.append(r)

        self.p_node(pont+1)

        self.save_node(newnode,pont+1)

        for x in range(len(node.records)/2,len(node.records)) :
          r = Record()
          r.value = r.age = r.label = r.next = r.prev = None
          node.records[x] = r
        self.save_node(node,pont)

        if pont == 0:
          self.p_node(0)
          mobj.prev = 1
          mobj.next = 2

          n_root = Node()

          for x in range(0,len(node.records)):
            r = Record()
            r.value = r.age = r.label = r.next = r.prev = None
            n_root.records.append(r)

          n_root.records[0] = mobj
          self.save_node(n_root,0)
        return mobj


  def get_node(self,index):
    self.open_file()
    self.file.seek(index * self.STRUCT_SIZE)
    line = self.file.readline(self.STRUCT_SIZE)
    if len(line) > 0 :
      self.file.seek(self.STRUCT_SIZE * index)
      obj = pickle.loads(self.file.read())
    else:
      obj = None
      self.close_file()
    self.close_file()
    return obj


  def split_tree(self, left_child, medium, right_child, parent=False):
    # a node[records]ina que tiver left_child e right_child deve ter o parent apontando median
    # mas antes tenho que testar se posso inserir median em alguma outra raiz
    left_node = right_node = Node()

    left_node.records = left_child
    left_node.x = right_node.x = len(left_child) # Considerando que ambos tem o mesmo tamanho
    right_node.records = right_child
    left_node.parent = right_node.parent = medium # setando o father
    # primeiro tenho que verificar se o father vai virar um novo nó ou será inserido em algum outro nó
    if parent:
      # tenho que tentar passar ele pra o father
        # e aqui dentro case tenha father terei q chamar a recursao
      pass
    else:
      # ou seja, eu vou substituir a atual raiz pelo node_root (overriding)
      node_root = Node()
      node_root.records = medium
      node_root.x += 1

      node_root.pointers.insert(0, self.SLOTS) # inserindo o da esquerda
      self.SLOTS += 1
      node_root.pointers.insert(1, self.SLOTS) # inserindo o da direita
      self.file.seek(0)
      self.file.write(pickle.dumps(node_root))
      self.close_file()

  def remove(self,val):
    node_val = self.search_value(val,0)
    if(node_val != None):
      node_key = self.get_node(node_val)
      n_k = self.g_node(val,node_key)

      if n_k.next != None:
        n_rig = self.find_smaller(n_k.next)
        node_s = self.get_node(n_rig)
        self.change_nds(n_rig,node_val,val)
        node_removed = self.get_node(n_rig)
        node_val = n_rig
      else:
        node_removed = self.r_val_node(node_val,val)

      if self.is_underflow(node_removed):
        node_f = self.father_nd(node_val)
        nodes_bro = self.join_br(node_f,node_val)
        if nodes_bro != None:
          remove_rec(nodes_bro)

  def remove_rec(node_val):
    node_removed = fileFunctions.get_node(node_val)
    if fileFunctions.is_underflow(node_removed):

      node_f = fileFunctions.father_nd(node_val)

      nodes_bro = fileFunctions.join_br(node_f,node_val)

      if nodes_bro != None:
        remove_rec(nodes_bro)

  def print_tree(self, position=0):
    self.file.seek(position * self.STRUCT_SIZE)
    obj = None
    try:
      obj = pickle.loads(self.file.read())
    except Exception:
      return

    while obj:
      for idx,record in enumerate(obj.records):
        print record[idx].value
        # aqui tenho que printar no formato que ele quer
      position += 1
      return self.print_file(position)
    return

  def print_asc(self, pont = 0):
    if(pont == None):
      return
    node_root = self.get_node(pont)
    for x in range(0,self.ORDER * 2):
      ult = (self.ORDER * 2) - 1
      print_asc(node_root.records[x].prev)
      if(node_root.records[x].value != None):
        print(str(node_root.records[x].value))
      else:
        ult = x-1
        break
    self.print_asc(node_root.records[x].next)

  def open_file(self):
    self.file = open(self.filename, 'r+b')

  def query_value(value):
    pos_chave = self.search_chave(value, 0)
    if(pos_chave != None):
      registro = self.print_node(pos_chave, value)
    else:
      print("chave nao encontrada: %s" % value)

  def search_chave(chave,pos):
    result = None
    while(pos != None and result == None):
      pag = self.get_node(pos)
      chave_exst = self.verify_val(chave,pag)
      if chave_exst:
        result = pos
      else:
        if chave < pag.records[0].value:
          pos = pag.records[0].prev
        else:
          for count in range(0,self.ORDER * 2):
            if(pag.records[count].value != None):
              if count == (self.ORDER * 2)-1:
                pos = pag.records[count].next
              else:
                if chave > pag.records[count].value:
                  if pag.records[count+1].value != None:
                    if(chave < pag.records[count+1].value):
                      pos = pag.records[count].next
                  else:
                    pos = pag.records[count].next
            else:
              break
      return result

  def close_file(self):
    if self.file:
      self.file.close()

  def value_check(self,value,node):
    for x in range(2 * self.ORDER):
      if node.records[x].value != None:
        if node.records[x].value == value:
          return True
    return False

  def node_next(self,node,value):
    if value < node.records[0].value:
      return node.records[0].prev
    for x in range(0,2 * self.ORDER):
      if x == (2 * self.ORDER)-1:
        return node.records[x].next
      if value > node.records[x].value:
        if node.records[x+1].value != None:
          if(value < node.records[x+1].value):
            return node.records[x].next
        else:
          return node.records[x].next

  def node_is_full(self,n):
    for x in range(0,self.ORDER * 2):
      if n.records[x].value == None:
        return False
    return True

  def insert_node(self,n,rec):
    rec_e = self.find_rec_e(n)
    n.records[rec_e] = rec
    node = self.sorting(n,n.records[rec_e].value)
    return node


  def find_rec_e(self,n):
    for x in range(0,self.ORDER * 2):
      if n.records[x].value == None:
          return x

  def save_node(self,n,index):
    self.open_file()
    dumpped = pickle.dumps(n)
    self.file.seek(self.STRUCT_SIZE * index)
    self.file.write(dumpped)
    self.close_file()

  def sorting(self,node,rec):
        for x in xrange(0,len(node.records)):
            if(node.records[x].value != None):
                for i in xrange(x+1, len(node.records)):
                    if(node.records[i].value != None):
                        if node.records[i].value < node.records[x].value:
                            node.records[i], node.records[x] = node.records[x], node.records[i]
                    else:
                        break
            else:
                break
        for x in xrange(0,len(node.records)-1):
            if(node.records[x].value == rec):
                if(node.records[x+1] != None):
                    if(node.records[x+1].value != None):
                        node.records[x+1].prev = node.records[x].next
        return node

  def make_overflow(self,node,new_rec):
    node.records.append(new_rec)
    for x in xrange(0,len(node.records)):
      if(node.records[x].value != None):
          for i in xrange(x+1, len(node.records)):
              if(node.records[i].value != None):
                  if node.records[i].value < node.records[x].value:
                      node.records[i], node.records[x] = node.records[x], node.records[i]
              else:
                  break
      else:
          return node
    return node

  def refresh(self,node,y):
    for x in range(0,self.ORDER * 2):
      if(node[x].value != None):
        if(node[x].prev > y):
          node[x].prev = node[x].prev + 1
        if(node[x].next > y):
          node[x].next = node[x].next + 1
      else:
        break
    return node

  def is_leaf(self,node):
    for x in range(0,self.ORDER * 2):
      if node.records[x].value != None:
        if node.records[x].prev != "null" or node.records[x].next != "null":
          return False
    return True

  def p_node(self,i):
    index = 0
    node = self.get_node(index)
    while(node != None):
      self.atualize_ponts(node,index,i-1)
      index = index +1
      node = self.get_node(index)
    node = self.get_node(i)
    while(node != None):
      n_aux = self.get_node(i+1)
      self.save_node(node,i+1)
      node = n_aux
      i = i+1
    return

  def print_nodes(self):
    pnodes = []
    int_pnodes = 0
    line = []

    root = self.get_node(0)

    pnodes.append(0)
    int_pnodes = int_pnodes + 1
    self.print_node(root,int_pnodes)

    line.append(0)

    while len(line) > 0:
      first_node = line[0]
      f_node = self.bro_recs(self.get_node(first_node))

      for p in range(0,len(f_node)) :
        if(f_node[p] not in pnodes):
          pnodes.append(f_node[p])
          int_pnodes = int_pnodes + 1
          self.print_node(self.get_node(f_node[p]),int_pnodes)
          line.append(f_node[p])
      line.pop(0)
    return

  def print_node(self,node,y):
    print("No: %s:" % y),
    print("apontador:"),
    if(node.records[0].prev != None):
      print(int(node.records[0].prev) + 1),
    else:
      print("null"),
    for x in range(0,self.ORDER * 2):
      print("chave:"),
      if(node.records[x].value != None):
        print(node.records[x].value),
      else:
        print("null"),
      print("apontador:"),
      if(node.records[x].next != None):
        print(int(node.records[x].next)+1),
      else:
        print("null"),
    print('\n'),

  def bro_recs(self,father):
    bro_recs = []
    if(father == None):
      return bro_recs
    if(father.records[0].prev != None):
      bro_recs.append(father.records[0].prev)
    for x in range(0,self.ORDER * 2):
      if(father.records[x].next != None):
        bro_recs.append(father.records[x].next)
    return bro_recs

  def refreshing(self,node,x):
    for x in range(0,self.ORDER * 2):
      if(node.records[x].value != None):
        if(node.records[x].prev > x):
          node.records[x].prev = node.records[x].prev + 1
        if(node.records[x].next > x):
          node.records[x].next = node.records[x].next + 1
      else:
        break
    return node

  def atualize_ponts(self,node,pos,x):
    for count in range(0,self.ORDER * 2):
      if(node.records[count].value != None):
        if(node.records[count].prev > x):
          node.records[count].prev = node.records[x].prev + 1
          self.save_node(node,pos)
        if(node.records[count].next > x):
          node.records[count].next = node.records[x].next + 1
          self.save_node(node,pos)

      else:
        break
    return

  def find_val(self,val):
    for x in range(0,TAMANHO_ARQUIVO):
      node = self.get_node(val)
      if node != None:
        if node.records.value == val:
          return node
    return None

  def find_smaller(self,n_root):
    node_ret = None
    ind = n_root
    node = self.get_node(n_root)
    while (node[0].prev != None):
      ind = node[0].prev
      node = get_node(node[0].prev)
    return ind

  def change_nds(self,n_sub,n_prev,val):
    n_sub.records[0].value
    ind = n_prev
    pos_folha = n_sub
    n_sub = self.get_node(n_sub)
    n_prev = self.get_node(n_prev)
    for x in range(0,self.ORDER * 2):
      if(n_prev.records[x].value == val):
        n_prev.records[x].value = n_sub.records[0].value
        n_prev.records[x].label = n_sub.records[0].label
        n_prev.records[x].age = n_sub.records[0].age
        save_object(n_prev,ind)

    for x in range(0,self.ORDER * 2):
      if(x == (self.ORDER * 2)-1):
        r = Record()
        r.value = r.age = r.label = r.next = r.prev = None
        n_sub.records[x] = r
      else:
        n_sub.records[x] = n_sub.records[x+1]
    self.save_node(n_sub,pos_folha)

  def print_all(self):
    i=0
    node = self.get_node(i)
    while(node != None):
      print(str(node))
      i = i+1
      node = self.get_node(i)

  def r_val_node(self,node,val):
    pos = node
    node = self.get_node(node)
    ret = False
    for x in range(0,self.ORDER * 2):
      if(x == (self.ORDER * 2)-1):
        r = Record()
        r.value = r.age = r.label = r.next = r.prev = None
        node.records[x] = r
      else:
        if(node.records[x].value != None):
          if(int(node.records[x].value) == int(val)):
            r = Record()
            r.value = r.age = r.label = r.next = r.prev = None
            node.records[x] = node.records[x+1]
            ret = True
          if ret:
            node.records[x] = node.records[x+1]
    self.save_node(node,pos)

    return node

  def is_underflow(self,node):
    underflow = True
    values = 0
    for x in range(0,self.ORDER * 2):
      if(node.records[x].value != None):
        values = values+1
    if values >= self.ORDER:
      underflow = False

    return underflow

  def father_nd(self,val,nRoot,nFat):
    if(nRoot == None):
      return nFat
    else:
      node = self.get_node(nRoot)
      v_ext = self.verify_val(val,node)
      if v_ext:
        return nFat
      else:
        if val < node.records[0].value:
          father_nd(node.records[0].prev,val,node)
        for x in range(0,(self.ORDER * 2)):
          if val > node.records[x].value:
            if node.records[x+1].value != None:
              if(val < node.records[x+1].value):
                father_nd(node.records[x].next,val,node)
            else:
              father_nd(node.records[x].next,val,node)

  def verify_val(self,val,node):
    for x in range(0,self.ORDER * 2):
      if node.records[x].value != None:
        if int(node.records[x].value) == int(val):
          return True
    return False

  def search_value(self,val,pos):
    retorno = None
    while(pos != None and retorno == None):
      node = self.get_node(pos)
      chave_exst = self.verify_val(val,node)
      if chave_exst:
        retorno = pos
      else:
        if val < node.records[0].value:
          pos = node.records[0].prev
        else:
          for count in range(0,self.ORDER * 2):
            if(node.records[count].value != None):
              if count == (self.ORDER * 2)-1:
                pos = node.records[count].next
              else:
                if val > node.records[count].value:
                  if node.records[count+1].value != None:
                    if(val < node.records[count+1].value):
                      pos = node.records[count].next
                  else:
                    pos = node.records[count].next
            else:
              break
    return retorno

  def g_node(self,val,node):
    for x in range(0,self.ORDER * 2):
      if(int(node.records[x].value) == int(val)):
        return node.records[x]
    return None

  def join_br(father,index):
    p_father = father
    father = self.get_node(father)

    x_brof = None
    x_bros = None
    bf = None
    bs = None
    for x in range(0,self.ORDER * 2):
      if(father.records[x].value != None):
        if(father[x].records.next == index):
          bf = father.records[x].prev
          x_brof = x
          x_pai = x
        if(father.records[x].prev == index):
          bs = father[x].prox
          x_bros = x
          x_pai = x
    if bf != None:

      is_big = is_big(self.get_node(bf))
      if is_big:
        bf_node = self.get_node(bf)
        n_son = self.get_node(index)
        n_son = self.psh_n(n_son)
        r = Record()
        r.value = r.age = r.label = r.next = r.prev = None
        n_son.records[0] = r
        n_son.records[0].value = father.records[x_brof].value
        n_son.records[0].age = father.records[x_brof].age
        n_son.records[0].label = father.records[x_brof].label

        save_object(n_son,father.records[x_brof].next)

        father.records[x_brof].value = higher_node(father.records[x_brof].ant)
        save_object(father,p_father)
        return None

    if bs != None:
      is_big = is_big(self.get_node(bs))
      if(is_big):

        bf_node = self.get_node(bs)
        n_son = self.get_node(index)
        r = Record()
        r.value = r.age = r.label = r.next = r.prev = None
        n_son.records[self.ORDER-1] = r
        n_son.records[self.ORDER-1].value = father.records[x_bros].value
        n_son.records[self.ORDER-1].age = father.records[x_bros].age
        n_son.records[self.ORDER-1].label = father.records[x_bros].label

        n_son.records[self.ORDER-1].next = self.get_node(father.records[x_bros].prox)[0].prev
        n_son.records[self.ORDER-1].prev = n_son.records[self.ORDER-2].next
        save_object(n_son,father.records[x_bros].prev)

        father.records[x_bros].value = self.get_node(father.records[x_bros].next)[0].value
        puxa_node(father.records[x_bros].next)
        save_object(father,p_father)
        return None
    n_son = self.get_node(index)
    if bf != None:
      bf_node = self.get_node(bf)
      reg_save = register.Registro()
      reg_save.value = father.records[x_brof].value
      reg_save.age = father.records[x_brof].age
      reg_save.label = father.records[x_brof].label
      bf_node.records[self.ORDER] = reg_save
      father = ret_value_pag(p_father,father.records[x_brof].value)
      save_object(father,p_father)
      x = 1
      for x in range(0,self.ORDER-1):
        registro_transf = register.Registro()
        registro_transf.value = n_son.records[x].value
        registro_transf.label = n_son.records[x].label
        registro_transf.age = n_son.records[x].age
        bf_node.records[self.ORDER + x] = registro_transf
      save_object(bf_node,bf)
      pull_from(index)
      return p_father
    if bs != None:
      bs_node = self.get_node(bs)
      i = self.ORDER
      for x in range(0,self.ORDER):
        registro_transf = register.Registro()
        registro_transf.value = bs_node.records[x].value
        registro_transf.label = bs_node.records[x].label
        registro_transf.age = bs_node.records[x].age
        bs_node.records[i] = registro_transf
        i = i+1

      reg_save = register.Registro()
      reg_save.value = father.records[x_bros].value
      reg_save.age = father.records[x_bros].age
      reg_save.label = father.records[x_bros].label
      bs_node.records[self.ORDER-1] = reg_save

      for x in range(0,self.ORDER-1):
        registro_transf = register.Registro()
        registro_transf.value = n_son.records[x].value
        registro_transf.label = n_son.records[x].label
        registro_transf.age = n_son.records[x].age
        bs_node.records[x] = registro_transf

      father = ret_value_pag(p_father,father.records[x_bros].value)
      save_object(father,p_father)
      save_object(bs_node,bs)
      pull_from(index)
      return p_father

  def is_big(node):
    big = False
    values = 0
    for x in range(0,self.ORDER * 2):
      if(node[x].value != None):
        values = values+1
    if values > self.ORDER:
      big = True
    return big

  def psh_n(self,node):
    r = Record()
    r.value = r.age = r.label = r.next = r.prev = None
    node_aux = node.records[0]
    for x in range(1,(self.ORDER * 2)):
      node_t = node.records[x]
      node.records[count] = node_aux
      node_aux = node_t
    node.records[0] = r
    return node

  def higher_node(self,node):
    index = node
    node = get_object(node)
    pos_higher = 0
    v_higher = node.records[0].value
    for x in range(0,self.ORDER * 2):
      if(node.records[x].value != None):
        if(node.records[x].value > v_higher):
          pos_higher = x
          v_higher = node.records[x].value
      else:
        break

    reg_v = register.Registro(None,None,None,None,None)
    node[pos_higher] = reg_v
    self.save_node(node,index)
    return v_higher

  def father_nd(self,node):
    pos = 0
    pag_at = self.get_node(pos)

    while(self.pont_aponta_para(pag_at,node) == False):
      pos = pos + 1
      pag_at = self.get_node(pos)
    return pos

  def pont_aponta_para(self,pag_search,pag):
    for count in range(0,self.ORDER * 2):
      if(pag_search.records[count].value != None):
        if(pag_search.records[count].prev == pag or pag_search.records[count].next == pag):
          return True
      else:
        break
    return False

  def consulta_chave(self,chave):
    pos_chave = self.search_chave(chave,0)
    if(pos_chave != None):
        registro = self.print_uni_node(pos_chave,chave)
    else:
        print("chave nao encontrada: "+str(chave))


  def search_chave(self,chave,pos):
    retorno = None
    while(pos != None and retorno == None):
        pag = self.get_node(pos)
        chave_exst = self.verify_val(chave,pag)
        if chave_exst:
            retorno = pos
        else:   
            if chave < pag.records[0].value:
                pos = pag.records[0].prev
            else:
                for count in range(0,self.ORDER * 2):
                    if(pag.records[count].value != None):
                        if count == (self.ORDER * 2)-1:
                            pos = pag.records[count].next
                        else:
                            if chave > pag.records[count].value:
                                if pag.records[count+1].value != None:
                                    if(chave < pag.records[count+1].value):
                                        pos = pag.records[count].next
                                else:
                                    pos = pag.records[count].next
                    else:
                        break
    return retorno

  def print_uni_node(self,pos,chave):
    node = self.get_node(pos)
    for count in range(0,self.ORDER * 2):
      if(node.records[count].value == chave):
        print("chave: "+str(node.records[count].value))
        print(node.records[count].label)
        print(node.records[count].age)

app = Application()
app.main()
