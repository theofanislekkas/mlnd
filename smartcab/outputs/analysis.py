#!/usr/local/bin/python

from __future__ import division

import re


asd = open('gamma_9.txt', 'r')

holder = []

for line in asd:
    holder.append(line)

index_list = []

for start in holder:
    if 'Simulator.run():' in start:
        index_list.append(holder.index(start))

totals = []

index_list.pop(0)

for i in index_list:
    k = i - 1
    totals.append(holder[k])

totals.append(holder[-1])

all_rewards = []

for i in totals:
    gh = i
    pattern = re.compile(r"total reward = (\d+)")
    m = re.search(pattern, gh)
    try:
        p = m.groups()
    except:
        print "Trial {} Failed to Pass".format(totals.index(i))
        continue
    all_rewards.append(int(p[0]))

ave_rewards = sum(all_rewards) / len(all_rewards)

print ave_rewards
