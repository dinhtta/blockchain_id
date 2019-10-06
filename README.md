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
