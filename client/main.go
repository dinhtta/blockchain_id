package main 

import (
  "fmt"
  "os"
  "strconv"
  )

const N=100
const KEYFILE="keyfile"
const CONTRACTPATH="blockchainid"
const CHAINCODEID="chaincodeid"
func main() {
  c := Client{}
  switch os.Args[1] {
    case "gen": {
      c.Gen(N,KEYFILE)
    }
    case "deploy": { // deploy <endpoint>
      c.Deploy(CONTRACTPATH, CHAINCODEID, os.Args[2]) 
    }
    case "load":
      c.Load(KEYFILE, CHAINCODEID, os.Args[2])
    case "update": { // update <key index> counter <endpoint>
      idx, _ := strconv.Atoi(os.Args[2])
      counter, _ := strconv.Atoi(os.Args[3])
      c.Update(KEYFILE, CHAINCODEID, idx, counter, os.Args[4])
    }
    case "query": {
      idx, _ := strconv.Atoi(os.Args[2])
      c.Query(KEYFILE, CHAINCODEID, idx, os.Args[3])
    }
    case "bench": {  // in benchmark mode
      if len(os.Args) != 10 {
        fmt.Printf("client bench <start Idx> <end Idx> <nthreads> <nOutstandingRequests> <nRequestPerSecond> <hostFile> <nRequestServers> <duration>\n")
        return
      }
      newClient := NewClient(toInt(os.Args[2]), toInt(os.Args[3]), toInt(os.Args[4]), toInt(os.Args[5]), toInt(os.Args[6]), os.Args[7], toInt(os.Args[8]), toInt(os.Args[9]))
      newClient.Start(KEYFILE, CHAINCODEID)
    }
  }
  fmt.Printf("Done\n")
}
