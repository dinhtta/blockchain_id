# processing throughput
from datetime import datetime

SEARCH_KEY="Batch execution time"
def get_perf(logfile):
  f = open(logfile, "r")
  lines = f.readlines()
  count = 0
  startTime = datetime.now()
  endTime = datetime.now()
  execTime = 0
  txs = 0
  for l in lines:
    if l.find(SEARCH_KEY) != -1:
      ls = l.split(" ")
      count +=1
      if (count <=2):
        continue
      
      endTime = datetime.strptime(ls[0], "%H:%M:%S.%f")
      if (count==3):
        startTime = endTime

      execTime += int(ls[11].strip(","))
      txs += int(ls[13])

  elapsed = (endTime-startTime).seconds
  if elapsed == 0:
    print("Error, no start-end block")
    exit(1)
  tp = txs*1.0/elapsed
  ex = execTime*1.0/txs

  print("Total txs: {}".format(txs))
  print("Throughput: {}".format(tp))
  print("Execution time: {}".format(ex))
  print("Elapsed time: {}".format(elapsed))
