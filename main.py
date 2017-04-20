import csv
import json
import gzip
import pickle
from collections import defaultdict


def readGz(f):
    for l in gzip.open(f):
        yield eval(l)

original_data = []
for l in readGz("./data/line_players.json.gz"):
    original_data.append(l)

data = original_data

