import numpy as np 
import multiprocessing as mp 
  
  
def multiply_elements(array): 
    return array * 2
  
  
if __name__ == '__main__': 
    np.random.seed(0) 
    arr = np.random.randint(0, 100, (100,)) 
    print(arr) 
    print('------------------------------------------') 
    pool = mp.Pool(mp.cpu_count()) 
    result = pool.map(multiply_elements, [arr[i:i+1] 
                                          for i in range(0, 100, 1)]) 
    print(result) 