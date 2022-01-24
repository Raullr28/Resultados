data = [1, 4, 2, 4, 2, 5, 6, 7, 4, 76, 3, 2, 5, 6, 7]
import numpy as np
print (np.mean(data))

print(np.median(data))


from scipy.stats import describe
describe(data)

print(np.quantile(data, 0.9))

np.unique(data, return_counts = True)



print(np.var(data, ddof=1))


print (np.std(data, ddof=1))


otra = [1, 5, 3, 5, 3, 65, 4, 6, 3, 6, 3, 12, 4, 23]

print (len(otra))

print (len(data))


otra += [2, 4]
print  (np.corrcoef(data, [1, 5, 3, 5, 3, 65, 4, 6, 3, 6, 3, 56, 4, 2, 4])[0,1])

