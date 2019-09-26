from config import *
import os
import time
from stop import *

# starting server of 1 shard index
def start_one_shard(setup_opt, shards, shard_idx, nodes, f, n, nclients, threads, txrate, run):
  shard_nodes = nodes[shard_idx*n : (shard_idx+1)*n]
  root_node = shard_nodes[0]
  
  cmds=[]
  for i in range(n):
    if SETUP_OPTS[setup_opt].startswith("noa2m"):
      env = ENV_TEMPLATE.format(i, "false", n, f) #since we run only 1 opt: a2m_separate_q
    else:
      env = ENV_TEMPLATE.format(i, "true", n, f)
    if i > 0:
      env = "{} {}".format(env, ENV_EXTRA.format(root_node))

    peer_log = PEER_LOG.format(LOG_PATH.format(shards, nclients, run), "{}_hl_log".format(SETUP_OPTS[setup_opt]), shard_nodes[i], f, threads, txrate) 
    cmds.append(CMD.format(peer_log, DEPLOY_PATH, LOG_PATH.format(shards, nclients, run), DEPLOY_PATH, BUILD_PATH, env, LOGGING_LEVEL, peer_log))

  # now run them
  for i in range(n):
    cmd_prepare = "ssh {} {}".format(shard_nodes[i], DEPLOY_FABRIC_CMD.format(SRC_PATH, SRC_PATH, SETUP_OPTS[setup_opt], SRC_PATH))
    execute(cmd_prepare)
    cmd = "ssh {} {}".format(shard_nodes[i], cmds[i])
    execute(cmd)

def start_shards(setup_opt, shards, f, n, nclients, threads, txrate, run):
  # workout nodes, f, n, threads, txrate from config file
  fn = open(HOSTSFILE)
  nodes=[]
  for l in fn.readlines():
    nodes.append(l.strip())
  fn.close()

  print nodes

  for s in range(int(shards)):
    start_one_shard(int(setup_opt), shards, s, nodes, int(f), int(n), int(nclients), threads, txrate, run)

def deploy_contract(shards, n):
  fn = open(HOSTSFILE)
  nodes = []
  for l in fn.readlines():
    nodes.append(l.strip())
  fn.close()

  # go to each leader from the shard to deploy
  for s in range(int(shards)):
    endpoint = nodes[s*int(n)]
    deploy_cmd = "ssh {} \"{}\"".format(endpoint, FAB_DEPLOY.format(CONTRACT_GOPATH, CONTRACT_PATH, GO_DIR, HOME_DIR, "endpoint={},index={}".format(endpoint, s)))
    execute(deploy_cmd)


# each clients connect to ALL shards, one node per shard
# in round robin for all nodes per shard
def client_endpoints(shards, nodes, n, client_idx):
  # which node in the shard
  node_idx = int(client_idx) % int(n)
  endpoints = []
  for i in range(int(shards)):
    endpoints.append("{}:7050/chaincode".format(nodes[i*int(n)+node_idx]))
  
  ep = "\\\"{}\\\"".format(';'.join(endpoints))
  return ep

def start_clients(setup_opt, shards, f, n, clients, clients_per_server, threads, txrate, ops, run):
  nodes = []
  fn = open(HOSTSFILE)
  for l in fn.readlines():
    nodes.append(l.strip())
  fn.close()

  chaincodeIDPath = "{}_0".format(CHAINCODEPATH)
  log = CLIENT_LOG.format(CLIENT_LOG_DIR.format(shards, clients, run), "logs_{}".format(SETUP_OPTS[int(setup_opt)]), f) 
 
  for c in range(int(clients)):
    client_node = nodes[int(n)*int(shards)+c/int(clients_per_server)]
    client_cmd = CLIENT_CMD.format(log, CLIENT_PATH, threads, ops, client_endpoints(shards,nodes,n,c), txrate, chaincodeIDPath, shards, OPERATION, RECORD_COUNT, CLIENT_TYPE, REQUEST_DISTRIBUTION, ZIPF, c, (int(clients))/shards, PRE_QUERY, log, c, threads, txrate)
#    client_cmd = CLIENT_CMD.format(log, CLIENT_PATH, threads, ops, client_endpoints(shards,nodes,n,c), txrate, CHAINCODE_LOCAL_PATH, shards, OPERATION, RECORD_COUNT, CLIENT_TYPE, REQUEST_DISTRIBUTION, ZIPF, c, n, PRE_QUERY, log, c, threads, txrate)

    cmd = "ssh {} {}".format(client_node, client_cmd)
    execute(cmd)

  time.sleep(SLEEP_TIME)
  stop()
