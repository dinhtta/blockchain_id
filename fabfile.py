import json
import requests
import pickle
from config import *
from gen import *

def get_nodes():
  x = open(HOSTSFILE, "r")
  lines = x.readlines()
  nodes = []
  for l in lines:
    nodes.append(l.strip())
  return nodes

# n = 3*f+1
def start_servers(f=0,run=0):
  nodes = get_nodes() 
  root_node = nodes[0]
  
  n = 3*int(f)+1
  cmds=[]
  for i in range(n):
    env = ENV_TEMPLATE.format(i, "false", n, f) #since we run only 1 opt: a2m_separate_q
    if i > 0:
      env = "{} {}".format(env, ENV_EXTRA.format(root_node))

    peer_log = PEER_LOG.format(LOG_PATH.format(run), n) 
    cmds.append(CMD.format(peer_log, DEPLOY_PATH, LOG_PATH.format(run), BUILD_PATH, env, LOGGING_LEVEL, peer_log))

  # now run them
  for i in range(n):
    cmd = "ssh {} {}".format(nodes[i], cmds[i])
    execute(cmd)

def stop_servers():
  nodes = get_nodes()
  for node in nodes:
    cmd = "ssh {} {}".format(node, KILL_SERVER_CMD)
    execute(cmd)

# path must be inside $GOPATH/src
def deploy(endpoint, path):
    deploy_request = {}
    params = {}
    chaincodeID = {}
    ctorMsg = {}

    deploy_request["jsonrpc"] = "2.0"
    deploy_request["method"] = "deploy"

    params["type"] = 1
    chaincodeID["path"] = path 

    params["chaincodeID"] = chaincodeID

    ctorMsg["function"] = "Init"
    ctorMsg["args"] = []

    params["ctorMsg"] = ctorMsg

    deploy_request["params"] = params
    deploy_request["id"] = "1"

    response = requests.post("http://{}:7050/chaincode".format(endpoint), data=json.dumps(deploy_request), headers=HEADERS)
    res_json = response.json()
    print(res_json)

    if res_json["result"]["status"] == "OK":
        chaincodeID = res_json["result"]["message"]
        f = open(CHAINCODEPATH, "w")
        f.write(chaincodeID)
        f.close()
    else:
        print("Deployment Failed with msg", res_json)
        return False, ""


def invoke(endpoint, chaincodeID, func, args):
  invoke_req = {}
  invoke_req["jsonrpc"] = "2.0"
  invoke_req["method"] = "invoke"
  params = {}
  params["type"] = 1

  chaincodeID_json = {}
  chaincodeID_json["name"] = chaincodeID

  params["chaincodeID"] = chaincodeID_json

  ctorMsg = {}
  ctorMsg["function"] = func
  ctorMsg["args"] = args
  params["ctorMsg"] = ctorMsg

  invoke_req["params"] = params
  invoke_req["id"] = "3"

  invoke_url = "http://{}:7050/chaincode".format(endpoint)

  response = requests.post(invoke_url, data=json.dumps(invoke_req), headers=HEADERS)
  print(response.json())

def hello():
  print("Hello world")

def load_data(endpoint):
  pubkeys = pickle.load(open("pubkeys", "rb"))
  hashkeys = pickle.load(open("hashkeys", "rb"))
  f = open(format(CHAINCODEPATH), 'r')
  chaincodeID = f.read()
  f.close()
  for pk in pubkeys:
    hk = hashkeys[pk]
    invoke(endpoint, chaincodeID, "register", [str(hk), str(pk)])


# test some random ID
def query_contract(endpoint, n=0):
    query_req = {}

    query_req["jsonrpc"] = "2.0"
    query_req["method"] = "query"

    params = {}
    params["type"] = 1

    chaincodeID_json = {}
    f = open(format(CHAINCODEPATH), 'r')
    chaincodeID = f.read()
    f.close()
    chaincodeID_json["name"] = chaincodeID

    params["chaincodeID"] = chaincodeID_json

    hashkeys = pickle.load(open("hashkeys", "rb"))
    pubkeys = pickle.load(open("pubkeys", "rb"))
    
    ctorMsg = {}
    ctorMsg["function"] = "none" 
    ctorMsg["args"] = [str(hashkeys[pubkeys[int(n)]])] 

    print("expecting: ", pubkeys[int(n)])

    params["ctorMsg"] = ctorMsg
    query_req["params"] = params
    query_req["id"] = "3"

    print(json.dumps(query_req))
    response = requests.post("http://{}:7050/chaincode".format(endpoint), data=json.dumps(query_req), headers=HEADERS)
    print(response.json())


