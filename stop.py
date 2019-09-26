from config import *

def stop():
  # go through all hosts and kill both client and servers
  fn = open(HOSTSFILE)
  nodes = []
  for l in fn.readlines():
    nodes.append(l.strip())

  for c in nodes[::-1]:
    tmp = "ssh {} {}"
    cmd = tmp.format(c, KILL_SERVER_CMD)
    execute(cmd)
    cmd = tmp.format(c, KILL_CLIENT_CMD)
    execute(cmd)
  fn.close()
