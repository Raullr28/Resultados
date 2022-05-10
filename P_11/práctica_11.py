import numpy as np
from scipy import stats
import pandas as pd
from itertools import compress
from random import randint, random
import matplotlib.pyplot as plt

def poli(maxdeg, varcount, termcount):
    f = []
    for t in range(termcount):
        var = randint(0, varcount - 1)
        deg = randint(1, maxdeg)
        f.append({'var': var, 'coef': random(), 'deg': deg})
    return pd.DataFrame(f)
  
def evaluate(pol, var):
    return sum([t.coef * var[pol.at[i, 'var']]**t.deg for i, t in pol.iterrows()])
 
 
def domin_by(target, challenger):
    if np.any(challenger < target):
        return False
    return np.any(challenger > target)
 
vc = 4
md = 3
tc = 5
#k = 2 # cuantas funciones objetivo

replicas=50
CV=[]
for k in range(2,6):
    rep=[]
    for r in range(replicas):
        obj = [poli(md, vc, tc) for i in range(k)]
        minim = np.random.rand(k) > 0.5
        n = 250 # cuantas soluciones aleatorias
        sol = np.random.rand(n, vc)
        val = np.zeros((n, k))
        for i in range(n): # evaluamos las soluciones
            for j in range(k):
                val[i, j] = evaluate(obj[j], sol[i])
        sign = [1 + -2 * m for m in minim]
        dom = []
        for i in range(n):
            d = [domin_by(sign * val[i], sign * val[j]) for j in range(n)]
            dom.append(sum(d)) 
        frente = val[[d == 0 for d in dom], :]
        rep.append((len(frente)*100)/n)
    CV.append(rep)
##############################################################################
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(4, 12))
plt.ylabel('Porcentajes soluciones de pareto')
parts = ax.violinplot(CV, showmeans=False, showmedians=False, showextrema=False)
for p in parts['bodies']:
    p.set_facecolor('orange')
    p.set_edgecolor('red')
    p.set_alpha(1)
c='blue'
plt.boxplot([CV[0], CV[1], CV[2], CV[3]],
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color='lime'),widths=(0.15, 0.15, 0.15, 0.15))
plt.subplots_adjust(bottom = 0.5, wspace = 0.02)
plt.xticks([1,2,3,4], ['2','3','4','5'])
plt.xlabel('Funciones objetivo (k)')
plt.savefig('p11p_violin.png', bbox_inches = 'tight')
plt.close()

result = stats.kruskal(CV[0], CV[1], CV[2], CV[3])
print(result)














