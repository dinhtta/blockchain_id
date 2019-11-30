# Simple benchmark for the blockchainID contract

## Structure
#### The contract

+ Implemented in contract/blokchchainid/blockchainid.go
+ For now, we only verify singature and do not check for increment. The check can be done easily, but would
overly complicate the benchmark driver. Specifically, the driver would need to avoid causing failed txs
because of the race in transaction ordering. 

#### Blockchain
The blockchain is the `fabric_noa2m_no_broadcast` version. Its installation can be found at
[https://github.com/ug93tad/hlpp/tree/develop/benchmark/hyperledger-a2m](https://github.com/ug93tad/hlpp/tree/develop/benchmark/hyperledger-a2m)

To start/stop, use `fab start_servers:f=<..>` and `fab stop_servers` respectively

#### The driver
The driver and related tools are in `client` directory. 

The `hosts` file contains the list of all server nodes

## Run an experiment
0. Generate users' keys. The number of users can be specified in `main.go`

    `./client gen` 

1. Start the blockchain with necessary nodes (by specifying `f`)

2. Deploy the contract

    `./client deploy <server>`
  
    Make sure to wait for it to be deployed (check the log). 

3. Load data (users and their keys)

    `./client load <server>`

4. Run benchmark

    `./client bench <start Idx> <end Idx> <nthreads> <nOutstandingRequests> <nRequestPerSecond> <hostFile> <nRequestServers> <duration>`

    where:

    + `startIdx, endIdx`: range of the user indexes
    + `nThreads`: number of thread per driver
    + `nOutstandingRequests`: maximum of in-flight/outstanding requests per driver
    + `nReqeustPerSecond`: request rate
    + `hostFile`: text file with the list of all servers
    + `nRequestServers`: the driver will only send requests to this number of servers (out of all servers in `hostFile`)
    + `duration`: how long, in seconds, is the expriment

## Invoking external process from smart contract

**Note: pull the latest from noa2m_no_broadcast branch, because there're changes in Hyperledger**

### Change in Hyperledger
There are 3 steps needed to execute an external process from inside smart contract. In step 1, we need to
set up necessary environment inside Docker containers that run the contract. Next, we need to add the
binary/script to be loaded together with the contract. Finally, we need to include the file type to be
uploaded together with the smart contract. *All these steps have been implemented in the latest commit in the
noa2m_no_broadcast branch*. 

1. Change `scripts/provisions/common.sh` to install necessary dependencies, e.g. Python.

2. Make sure the file is in the `$GOPATH/src/github.com/hyperledger/fabric`. Currently, we have `external.py`
as a simple external Python program which does nothing but printing out the input.  

3. Edit `core/container/util/writer.go` to include the file type

### Running it
After running step 0, 1, 2, 3 exactly the same as above, run:

```
./client test <index> <endpoint> 
```

which basically sends 3 binary to the `testExternal` method of the smart contract. The contract then execute
`python external.py <string1> <string2>`, and return the output as Error message in the log. You can see the
error message in the server log contains the same string as what the `./client` process prints.  

### Extending it
The best way to integrate ZkSnark verifier process with this is:
+ The verifier is a executable (whatever its dependencies are, they need to be set up properly in
`scripts/provisions/common.sh` file in Hyperledger)

+ The smart contract should receive input (public key, proof, etc.) as strings, and use them to invoke the
verifier process. 

+ The verifier process should just return "0" or "1" depending whether the proof is correct. 
