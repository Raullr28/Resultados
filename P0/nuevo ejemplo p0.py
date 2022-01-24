data = [1, 4, 2, 4, 2, 5, 6, 7, 4, 76, 3, 2, 5, 6, 7]
import numpy as np
np.mean(data)

np.median(data)


from scipy.stats import describe
describe(data)

np.quantile(data, 0.9)

np.unique(data, return_counts = True)



np.var(data, ddof=1)


np.std(data, ddof=1)


otra = [1, 5, 3, 5, 3, 65, 4, 6, 3, 6, 3, 12, 4, 23]

len(otra)

len(data)


otra += [2, 4]
np.corrcoef(data, [1, 5, 3, 5, 3, 65, 4, 6, 3, 6, 3, 56, 4, 2, 4])[0,1]

