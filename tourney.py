import sys
import itertools
import random
from collections import defaultdict
from pprint import pprint

def combo_list(combos, prior_pairs):
  print "prior pairs " + str(prior_pairs)
  combo_list = defaultdict(list)
  for combo in combos:
    first, second = combo
    if [first, second] in prior_pairs or [second, first] in prior_pairs:
      continue
    combo_list[first].append(second)
    combo_list[second].append(first)
  return combo_list

def remove_value(mydict, myvalue):
  ''' The dictionary's values must be lists'''
  for key in mydict:
    if myvalue in mydict[key]:
      mydict[key].remove(myvalue)

def pick_pair(combo_list, first):
  if not first in combo_list:
    return None
  if not combo_list[first]:
    return None 
  second = random.choice(combo_list[first])
  
  del combo_list[first]
  remove_value(combo_list, second)
  remove_value(combo_list, first)
  if second in combo_list:
    del combo_list[second]
  return second
  
def generate_round(pairs):
  round = {}
  for i in range(len(pairs)/2):
    first = random.choice(pairs)
    pairs.remove(first)
    pairs = [pair for pair in pairs if first not in pair]
    second = random.choice(pairs)
    pairs.remove(second)
    pairs = [pair for pair in pairs if second not in pair]
    round[tuple(first)] = second
  return round

def gen_rounds(people, num_rounds):
  rounds = []
  prior_pairs = []
  combos = itertools.combinations(people, 2)
  combos = list(combos)
  for round_num in range(num_rounds):
    pairs = []
    round_combo_list = combo_list(combos, prior_pairs)
    print len(round_combo_list)
    for person in round_combo_list.keys():
      first = person
      second = pick_pair(round_combo_list, first)
      if not second:
        continue
      pairs.append([first, second])
      prior_pairs.append([first, second])
    print "%d pairs for round %d are: %s" % (len(pairs), round_num, str(pairs))
    round = generate_round(pairs) 
    rounds.append(round) 
  return rounds

def verify(rounds, people):
  pair_map = defaultdict(int)
  for round in rounds:
    hit_map = defaultdict(int)
    for (left1, left2), (right1, right2) in round.iteritems():
      hit_map[left1] += 1
      hit_map[left2] += 1
      hit_map[right1] += 1
      hit_map[right2] += 1
      pair_map[(left1, left2)] += 1
      pair_map[(right1,right2)] += 1
    for person, hc in hit_map.iteritems():
      assert(hc == 1)
    for pair in pair_map:
      assert(pair_map[pair] == 1)
    # these checks mean the randomness of the picking made somebody left out. 
    bad_round = False
    for person in people:
      if (hit_map[person] != 1):
        print person + " was not included in this round. :("
        bad_round = True
    if not bad_round:
      pprint(round)

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "Usage: tourney.py <file of people> <number of rounds>"
    sys.exit()
  people = open(sys.argv[1]).readlines()
  people = [person.strip() for person in people]

  rounds = gen_rounds(people, int(sys.argv[2]))

  print "Done generating rounds. Will now verify the rounds, and print all rounds that include everybody."

  verify(rounds, people)

