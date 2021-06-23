import numpy as np

result = np.array([90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,
        90,0,150,200,200])
# dht_data = array("B")
dht_data = np.ndarray([])

for i in range(2,44):
        if result[i] <= 90:
            result[i]=0
        else:
            result[i]=1
    
dht_data = result[2:42].reshape((5,8))
b = np.packbits(dht_data)
# byte = dht_data.tobytes()


# print(np.fromstring(byte, dtype='>u4'))
print(b)