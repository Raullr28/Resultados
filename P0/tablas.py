import numpy as np

x = np.arange(1, 21)
y = np.sin(x)

import matplotlib.pyplot as plt

plt.plot(x, y)
plt.show()
plt.close()
plt.plot(x, y, 'o')
plt.show()
plt.close()
plt.plot(x, y, '-o')
plt.plot(x, np.cos(x), color ='red')
plt.axhline(y = 0, color = 'lime')
plt.show()
plt.close()
plt.plot(x, y)
plt.plot(x + 1, np.cos(x + 1), marker = 's', color = 'green')
plt.show()
plt.close()
plt.plot(x, y)
plt.title('Texto arriba')
plt.xlabel('Etiqueta')
plt.ylabel('Otra etiqueta')
plt.show()
plt.close()
