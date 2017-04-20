import pickle
f = open('hero_names.csv','r')

hero_type = {}
for line in f.readlines():
    line = line.strip()
    attr = line.split(",")
    id = int(attr[1])
    type = attr[3]
    hero_type[id] = str(type)

print hero_type
pickle.dump(hero_type, open('hero_type.pkl','wb'))


feat = {}

i = 0
for r in range(0,6):
    print 'r = ' + str(r)
    for g in range(0,6-r):
        print 'g = ' + str(g)
        b = 5 - r - g
        print 'b = ' + str(b)
        feat[(r,g,b)] = i
        i += 1

print len(feat)
pickle.dump(feat, open('type_feat.pkl','wb'))
