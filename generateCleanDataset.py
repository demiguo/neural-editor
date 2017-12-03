import numpy as np
from datasketch.minhash import MinHash
from datasketch.lsh import MinHashLSH
from itertools import izip


# Create LSH index
lsh = MinHashLSH(threshold=0.5, num_perm=128)

# hash list
hash_list = []
# idx
i = 0
with open("valid.article.filter.txt", 'r') as articles, open("valid.title.filter.txt", 'r') as titles:
    for x, y in izip(articles, titles):
        m = MinHash(num_perm=128)
        # for each tuple minhash the text x 
        for w in x:
            m.update(w.encode('utf8'))
        # and insert in LSH index
        if m not in hash_list:
            lsh.insert((x,y), m)
        hash_list.append(m)
        print i
        i += 1


# neighborhood list
neighborhood_list = []
# idx
i = 0
with open("valid.article.filter.txt", 'r') as articles, open("valid.title.filter.txt", 'r') as titles, open("edit.data.ordered.txt", 'w') as data:
    for x, y in izip(articles, titles):
        # for each tuple query the LSH index and get the neighborhood
        result = lsh.query(hash_list[i])
        for (x_p, y_p) in result:
            data.write(x + '\t' + y + '\t' + x_p + '\t' + y_p + '\n')
        i += 1

