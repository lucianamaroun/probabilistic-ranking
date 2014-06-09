#! -*- coding=utf8 -*-
"""""""""""""""""""""""""""
"   Elverton C. Fazzion   "
" elvertoncf@gmail.com.br "
"                         "
"""""""""""""""""""""""""""

from sys import argv,exit
from time import time

"""
Objetivo: Este algoritmo implementa o algoritmo
apriori, descrito na página 234 do livro-base
do curso.
"""

# ------------------------------------------------------------- #
"""
Esta estrutura guarda informações de um subitemset.
"""
class SubItemSet:

    def __init__(self,items,v=0):
        self.items = set()
        self.items = self.items.union(items)
        self.support = v
# ------------------------------------------------------------- #
"""
ADICIONADO: Produz o mapper de uma lista.
"""
def GetMapper(transactions):
    """
    Mapeia cada item da base para um inteiro.
    """
    mapper = dict()
    itemset = set()
    map_transactions = list()

    # Realiza o mapeamento, recupera o itemset e armazena
    # as transações
    id_count = 0
    for transaction in transactions:
        map_transaction = set()
        for item in transaction:
            if item not in mapper:
                mapper[item] = id_count
                id_count += 1
                itemset.add(mapper[item])
            map_transaction.add(mapper[item])
        map_transactions.append(map_transaction)

    # Reverte o mapa, de forma a procurar qual o significado
    # de um inteiro.
    mapper_reverse = dict()
    for decode,encode in mapper.items():
        mapper_reverse[encode] = decode

    return (map_transactions,mapper_reverse,itemset)
# ------------------------------------------------------------- #
"""
Essa função tem por objetivo recuperar todas as transações e o
itemset da base.
Uma otimização é feita, de forma a mapear os itens em números,
garantindo assim pouco volume de espaço em memória, visto
que todas as transações estarão em memória e não precisando
comparar strings.
"""
def GetBasicInfos(file_name,separator):
    """
    Mapeia cada item da base para um inteiro.
    """
    mapper = dict()
    itemset = set()
    transactions = list()

    file_in = open(file_name,"r")

    # Realiza o mapeamento, recupera o itemset e armazena
    # as transações
    id_count = 0
    for line in file_in:
        parts = line.strip().split(separator)
        transactions_mapped = set()
        for part in parts:
            if part not in mapper:
                mapper[part] = id_count
                id_count += 1
                itemset.add(mapper[part])
            transactions_mapped.add(mapper[part])
        transactions.append(transactions_mapped)
    file_in.close()

    # Reverte o mapa, de forma a procurar qual o significado
    # de um inteiro.
    mapper_reverse = dict()
    for decode,encode in mapper.items():
        mapper_reverse[encode] = decode

    return (transactions,mapper_reverse,itemset)
# ------------------------------------------------------------- #
"""
Implementa o algoritmo apriori, citado no livro, pág 234.
"""
def Apriori(mapper,transactions,itemset,min_sup,confidence_min,\
        rare_item,level_max):

    num_transactions = len(transactions)

    # Guarda todos os itens frequentes.
    frequents = list()
    # Guarda os candidatos atuais
    candidates = list()

    # Inicializa o primeiro nível de expansão do apriori.
    for item in itemset:
        temp_set = set()
        temp_set.add(item)
        sub_item_set = SubItemSet(temp_set)
        candidates.append(sub_item_set)

    level = 0
    while(candidates):
    
        # Escolhe o suporte.
        min_support = min_sup[level]

        # Computa o suporte dos itens
        ComputeSupport(transactions,candidates)

        # Guarda os itens frequentes.
        frequents_level = list()

        # Recupera os candidatos frequentes.
        for candidate in candidates:

            # Transforma o suporte de inteiro para porcentagem.
            candidate.support = float(candidate.support)/\
                    num_transactions
            # Se o candidato não tem o suporte mínimo, descarta.
            if (candidate.support >= min_support):
                frequents_level.append(candidate)

        # Imprime os itemsets frequents, em ordem.
        #PrintFrequents(frequents_level,mapper,level)
        #print ""

        # Armazena os itens frequentes deste nível
        if(rare_item):
            frequents.extend(candidates)
        else:
            frequents.extend(frequents_level)
        
        # Verifica se o nível máximo definido foi atingido.
        level += 1
        if(level == level_max):
            break

        # Expande os itens frequentes deste nível, afim de gerar
        # novos candidatos
        candidates = ExtendPrefixTree(frequents_level,level)

    #print "RULES"
    #PrintConfidences(frequents,mapper,confidence_min)
    return GetRules(frequents,mapper,confidence_min)

# ------------------------------------------------------------- #
"""
Calcula o suporte dos candidatos.
"""
def ComputeSupport(transactions,candidates):

    # Para cada transação, verifica se o candidato é um subconjunto
    # dela. Se for, incrementa o suporte em 1.
    for transaction in transactions:
        for candidate in candidates:
            if (candidate.items <= transaction):
                candidate.support += 1
# ------------------------------------------------------------- #
"""
Gera novos candidatos.
"""
def ExtendPrefixTree(candidates,level):

    # Lista dos candidatos já processados.
    processed_candidates = list()

    # Lista de novos candidatos.
    new_candidates = list()

    # Recupera a lista de candidatos do nível de cima, usando set.
    old_candidates = [x.items for x in candidates]

    # Para cada item na lista de candidatos do nível atual, faz a
    # união dele, com cada item posterior a ele
    for leaf_a in range(len(candidates)):
        i=0
        for leaf_b in range(leaf_a+1,len(candidates)):

            i+=1
            union_ab = candidates[leaf_a].items.union(candidates[leaf_b].items)

            # Impõe a regra que os itens gerados devem ser de tamanho 1 a mais
            # que os candidatos atuais e que sejam do mesmo pai.
            if(len(union_ab) > (level+1)) or (union_ab in processed_candidates):
                break

            # Verifica se cada subconjunto, combinado pelo tamanho do nível,
            # existe nos itens frequentes do nível atual. Caso não exista,
            # o item gerado não pode ser frequente.
            valid = 1
            for element in union_ab:
                element_set = set()
                element_set.add(element)
                if ((union_ab - element_set) not in old_candidates):
                    valid = 0
                    break
            if(valid):
                union_ab = SubItemSet(union_ab)
                new_candidates.append(union_ab)
                processed_candidates.append(union_ab.items)

    return new_candidates

# ------------------------------------------------------------- #
"""
Recupera todas as combinações de confiança dos itemsets frequentes.
"""
def PrintConfidences(frequents,mapper,confidence_min):

    # Calcula a confiança de cada regra.
    confidence_rules = dict()
    frequents_num = len(frequents)
    for leaf_a in range(frequents_num):
        for leaf_b in range(leaf_a+1,frequents_num):
            if(frequents[leaf_a].items <= frequents[leaf_b].items):
                confidence = CalculateConfidence(leaf_a,leaf_b,frequents)
                if(confidence < confidence_min):
                    continue
                if(confidence not in confidence_rules):
                    confidence_rules[confidence] = list()
                rule_str_a = ",".join(str(mapper[item]) for item in frequents[leaf_a].items)
                rule_str_b = ",".join(str(mapper[item]) for item in \
                        (frequents[leaf_b].items - frequents[leaf_a].items))
                confidence_rules[confidence].append(rule_str_a + " -> " + rule_str_b)

    confidences = confidence_rules.keys()
    confidences.sort()
    confidences.reverse()

    for confidence in confidences:
        confidence_rules[confidence].sort()
        for rule in confidence_rules[confidence]:
            print rule + " : %.8f"%confidence


# ------------------------------------------------------------- #
"""
ADICIONADO: Retorna uma lista com as regras de associação.
"""
def GetRules(frequents,mapper,confidence_min):

    # Calcula a confiança de cada regra.
    confidence_rules = dict()
    frequents_num = len(frequents)
    for leaf_a in range(frequents_num):
        for leaf_b in range(leaf_a+1,frequents_num):
            if(frequents[leaf_a].items <= frequents[leaf_b].items):
                confidence = CalculateConfidence(leaf_a,leaf_b,frequents)
                if(confidence < confidence_min):
                    continue
                if(confidence not in confidence_rules):
                    confidence_rules[confidence] = list()
                rule_str_a = ",".join(str(mapper[item]) for item in frequents[leaf_a].items)
                rule_str_b = ",".join(str(mapper[item]) for item in \
                        (frequents[leaf_b].items - frequents[leaf_a].items))
                confidence_rules[confidence].append((rule_str_a, rule_str_b))

    confidences = confidence_rules.keys()
    confidences.sort()
    confidences.reverse()

    rules = {}
    for confidence in confidences:
        confidence_rules[confidence].sort()
        for rule in confidence_rules[confidence]:
            if rule[0] not in rules:
                rules[rule[0]] = {}
            rules[rule[0]][rule[1]] = confidence
    return rules


# ------------------------------------------------------------- #
"""
Calcula o suporte. Se leaf_a é [A] e leaf_b é [A,B,C], esse
algoritmo calcula a confiança da regra A -> BC.
"""

def CalculateConfidence(leaf_a,leaf_b,frequents):

    support_a = frequents[leaf_a].support
    support_b = frequents[leaf_b].support

    return support_b/support_a

# ------------------------------------------------------------- #
"""
Imprime todos os itens frequents, de maneira ordenada.
"""
def PrintFrequents(frequents,mapper,level):

    if frequents:
        print "Itemsets of size " + str(level)

    # Ordena os itens.
    frequents_per_support = dict()
    for frequent in frequents:
        if frequent.support not in frequents_per_support:
            frequents_per_support[frequent.support] = list()
        items_str = ",".join(str(mapper[item]) for item in frequent.items)
        frequents_per_support[frequent.support].append(items_str)

    supports = frequents_per_support.keys()
    supports.sort()
    supports.reverse()

    for support in supports:
        frequents_per_support[support].sort()
        for itemset in frequents_per_support[support]:
            print itemset + " %.8f"%support

# ------------------------------------------------------------- #
"""
ADICIONADO: Wrapper.
"""
def run_apriori(transactions, sup_min, confidence_min, level_max):
  rare_item = 0
# Recupera informações básicas.
  transactions,mapper,itemset = GetMapper(transactions)#GetBasicInfos(file_in,separator)
# Inicia o Apriori.
  return Apriori(mapper,transactions,itemset,sup_min,confidence_min,rare_item,level_max)

# ------------------------------------------------------------- #
"""
Trata os parâmetros.
"""
if __name__ == '__main__':
  if(len(argv) == 1):
      print "** Usage **\n"
      print "python apriori.py -d [0] -i [1] -s1 [2] -s2 [2] -c [3] --separator [4] -r [5]\n\n" +\
      "[0] = Nível máximo da árvore gerada pelo apriori.\n" +\
      "[1] = Caminho da base de dados.\n" +\
      "[2] = Suporte mínimo, em decimal percentual (0 a 1).\n" +\
      "[3] = Confiança mínima, em decimal percentual (0 a 1).\n" +\
      "[4] = Separador do arquivo de entrada.\n" +\
      "[5] = OPCIONAL: Usa a implementação da Heurística do Rare Item se igual a 1 e\n" +\
      "não usa, se igual a 0. Caso não informado, ele NÃO usa a implementação da Heurística.\n"

      exit()

  rare_item = 0
  for arg in range(len(argv)):
      if(argv[arg] == "-i"):
          file_in = argv[arg+1]
      elif(argv[arg] == "-s1"):
          support_min1 = float(argv[arg+1])
      elif(argv[arg] == "-s2"):
          support_min2 = float(argv[arg+1])
      elif(argv[arg] == "-c"):
          confidence_min = float(argv[arg+1])
      elif(argv[arg] == "-r"):
          rare_item = int(argv[arg+1])
      elif(argv[arg] == "-d"):
          level_max = int(argv[arg+1])
      elif(argv[arg] == "--separator"):
          separator = argv[arg+1]

  sup_min = [support_min1,support_min2]
# Recupera informações básicas.
  transactions,mapper,itemset = GetMapper(transactions)#GetBasicInfos(file_in,separator)
# Inicia o Apriori.
  Apriori(mapper,transactions,itemset,sup_min,confidence_min,rare_item,level_max)

