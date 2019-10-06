package main 
import (
  "bytes"
  "reflect"
  "testing"
  "fmt"
  "crypto/ecdsa"
  "crypto/elliptic"
  "crypto/rand"
  "encoding/json"
  "crypto/x509"
  "os"
  "net/http"
  "github.com/hyperledger/fabric/protos"
  "io/ioutil"
)
const N = 100
const ADDR = "http://slave-10:7050/chain/blocks/"
func check(err error) {
  if err != nil {
    panic(err)
  }
}

func TestGet(t *testing.T) {
  res, _ := http.Get(ADDR+"1")
  defer res.Body.Close()
  var x protos.Block
  check(json.NewDecoder(res.Body).Decode(&x))
  fmt.Printf("%v\n",x.Transactions[0]) 
}

// POST request (JSON-RPC 2.0)
func TestRPC(t *testing.T) {
  chaincodeID, _ := ioutil.ReadFile("../chaincodeID")
  data := makeRequest("query", string(chaincodeID), "none", "testdata") 
  fmt.Printf("request: %v\n", string(data))

  res, err := http.Post("http://slave-10:7050/chaincode", "application/json", bytes.NewReader(data))
  check(err)
  defer res.Body.Close()
  var rs rpcResponse
  check(json.NewDecoder(res.Body).Decode(&rs))
  fmt.Printf("%v %v\n", rs.Result, rs.Result.Status)
}

func TestGen(t *testing.T) { 
  fmt.Printf("Testing gen, n=%v\n",N)
  var keys [][]byte
  var origin []*ecdsa.PrivateKey

  for i := 0; i<N; i++ {
    privKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
    if (err != nil) {
      panic(err)
    }
    mk, err := x509.MarshalECPrivateKey(privKey)
    if err != nil {
      panic(err)
    }
    keys = append(keys, mk) 
    origin = append(origin, privKey)
  }
  dataFile, _ := os.Create("keyfile")
  encoder := json.NewEncoder(dataFile)
  encoder.Encode(keys)
  dataFile.Close()

  var res [][]byte
  inFile, _ := os.Open("keyfile")
  decoder := json.NewDecoder(inFile)
  errDecode := decoder.Decode(&res)
  if errDecode != nil {
    panic(errDecode)
  }
  um, umerr := x509.ParseECPrivateKey(res[0])
  if umerr != nil {
    panic(umerr)
  }
  reflect.DeepEqual(um, keys[0])
}
