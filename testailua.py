import numpy as np

# Ludoaan 10x10 Matrixi random datalla
a = np.random.random((10, 10))
# a.sort()
sample_data = []
test_data = []
index = 0

print(len(a)/2)

for x in a:
    for y in x:
        sample_data.append(y)
        ++index
    print(index)
    if index >= (len(a)/2-1):
        test_data.append(y)
    index = index + 1

sample_data.sort()
test_data.sort()
print(sample_data)
print('Test')
print(test_data)
