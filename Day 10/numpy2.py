import numpy as np
b = [1,2,3]
print(f"List b: {b},type: {type(b)}")
a = np.array([1,2,3])
print(f"Array a: {a},type: {type(a)},len: {len(a)},shape: {a.shape}")

c = np.array(range(1,10))
print(f"Array c: {c},type: {type(c)},len: {len(c)})")