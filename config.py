import os

FS = [1]
NUSERS = 100
KEYFILE = "keys"
HOSTSFILE = 'hosts'
HOSTNAME = 'slave-{}'
ENDPOINT_SUFFIX = ":7050/chaincode"

GO_DIR='/data/dinhtta/src/github.com/'
FAB_DEPLOY='rm -rf {}; cp -r {} {}; cd {}; fab deploy:{} > /data/dinhtta/odeploy 2>&1'

DEPLOY_PATH = '/data/dinhtta/hyperledger'
BUILD_PATH = '/data/dinhtta/src/github.com/hyperledger/fabric/build/bin'
SRC_PATH = '/data/dinhtta/src/github.com/hyperledger'
CHAINCODEPATH = 'chaincodeID'
#CONTRACT_GOPATH = '/data/dinhtta/src/github.com/smallbank'


SLEEP_TIME = 200
LOG_PATH = '/data/dinhtta/blockchain_id_run{}'
PEER_LOG = '{}/log_n_{}'

LOGGING_LEVEL = 'warning:consensus/pbft,consensus/executor,consensus/handler=info'
ENV_TEMPLATE = 'CORE_PEER_ID=vp{} CORE_PEER_ADDRESSAUTODETECT=true CORE_PEER_NETWORK=blockbench CORE_PEER_VALIDATOR_CONSENSUS_PLUGIN=pbft CORE_PEER_VALIDATOR_CONSENSUS_BUFFERSIZE=2000 CORE_PEER_FILESYSTEMPATH=/data/dinhtta/hyperledger CORE_VM_ENDPOINT=http://localhost:2375 CORE_PBFT_GENERAL_MODE=batch CORE_PBFT_GENERAL_TIMEOUT_REQUEST=10s CORE_PBFT_GENERAL_TIMEOUT_VIEWCHANGE=10s CORE_PBFT_GENERAL_TIMEOUT_RESENDVIEWCHANGE=10s CORE_PBFT_GENERAL_SGX={} CORE_PBFT_GENERAL_N={} CORE_PBFT_GENERAL_F={} '
ENV_EXTRA = 'CORE_PEER_DISCOVERY_ROOTNODE={}:7051'
CMD = '"sudo ntpdate -b clock-1.cs.cmu.edu; rm -rf {}; rm -rf {}; mkdir -p {}; cd {}/; {} nohup ./peer node start --logging-level={} > {} 2>&1 &"'
KILL_SERVER_CMD = 'killall -KILL peer'

DEPLOY_FABRIC_CMD = '"rm -rf {}/fabric; cp -r {}/fabric_{} {}/fabric"'

HEADERS = {'content-type': 'application/json'}

def execute(cmd):
  os.system(cmd)
  print(cmd)

