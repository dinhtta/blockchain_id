package main 

import (
  "io/ioutil"
  "strings"
  "time"
  "fmt"
)

type Client struct {
  startIdx, endIdx int // for the key range
  nThreads int // number of threads
  nOutstandingRequests int // number of outstanding requests
  nRequestsPerSecond int // rate, invert to see the next request
  hosts []string// all host to send requests 
  duration int // how long to run, in seconds

  chaincodeID []byte
  pubkeys, privkeys, hashkeys [][]byte
}

// ns: number of servers
func NewClient(sid, eid, nt, nor, rps int, hostFile string, ns int, duration int) *Client {
  h, _ := ioutil.ReadFile(hostFile)
  hosts := strings.Split(string(h), "\n")
  return &Client{
    startIdx: sid,
    endIdx: eid, 
    nThreads: nt,
    nOutstandingRequests: nor,
    nRequestsPerSecond: rps,
    hosts: hosts[:ns],
    duration: duration,
  }
}

func (c *Client) worker(job chan int, closed chan bool, stats chan int) {
  // receive job, which is id for the next update
  hidx := 0
  nhosts := len(c.hosts)
  count := 0
  for {
    select {
      case idx := <- job: {
        c.update(c.hashkeys[idx], c.privkeys[idx], 0, string(c.chaincodeID), c.hosts[hidx])
        hidx = (hidx + 1)%nhosts
        count++
      }
      case <-closed: {
        stats <- count
        return
      }
    }
  }
}

func (c *Client) Start(filePath, chaincodeIDFile string) {
  // Start main thread
  c.chaincodeID, c.pubkeys, c.privkeys, c.hashkeys = c.load_keys(filePath, chaincodeIDFile)

  buffer := make(chan int, c.nOutstandingRequests)
  done := make(chan bool)
  stats := make(chan int) // see how many were sent
  for i :=0; i < c.nThreads; i++ {
    go c.worker(buffer, done, stats)
  }

  // loop for duration
  t := time.Now()
  t_end := t.Add(time.Duration(c.duration*1000*1000*1000))  // in nanosecond
  idx := 0
  N := len(c.hashkeys)
  for t.Before(t_end) {
    if (time.Now().Before(t)) {
      continue
    }
    buffer <- idx % N
    idx++
    t = c.nextRequest()
  }

  // then close
  nSent := 0
  for i:=0; i<c.nThreads; i++ {
    done <- true
    nSent += <- stats 
  }
  fmt.Printf("Total sent over %v(s): %v\n", c.duration, nSent)
}
