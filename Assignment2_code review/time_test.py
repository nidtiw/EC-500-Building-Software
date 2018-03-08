# Time Test
import testmain
import time

begin = time.time()
testmain.test('Comey',50)
stop = time.time()
print(stop-begin)
