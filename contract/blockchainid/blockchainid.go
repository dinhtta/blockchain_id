package main

import (
	"fmt"
  "strconv"
	"github.com/hyperledger/fabric/core/chaincode/shim"
  "crypto/x509"
  "crypto/ecdsa"
  "encoding/base64"
  "math/big"
)

type BlockchainID struct {}

var MAX_USERS int = 1000
var counterTab string = "count"
var pubkeyTab string = "pubkey"
func main() {
	err := shim.Start(new(BlockchainID))
	if err != nil {
		fmt.Printf("Error starting BlockchainID: %s", err)
	}
}

func (t *BlockchainID) Init(stub shim.ChaincodeStubInterface, function string, args []string) ([]byte, error) {
  // preload MAX_USERS

  // preload MAX_ACCOUNTS
  /*
  for i:=0 ; i< MAX_ACCOUNTS; i++ {
    stub.PutState(checkingTab + "_" + strconv.Itoa(i), []byte("100000"))
    stub.PutState(savingTab + "_" + strconv.Itoa(i), []byte("100000"))
  }
  */
	return nil, nil
}

func (t *BlockchainID) Invoke(stub shim.ChaincodeStubInterface, function string, args []string) ([]byte, error) {

  switch function {
    case "register":
      return t.register(stub, args)
    case "update":
      return t.incrementCounter(stub, args)
  }
  return nil, nil

}

func (t *BlockchainID) Query(stub shim.ChaincodeStubInterface, function string, args []string) ([]byte, error) {
  counter_key := counterTab + "_"+ args[0]

  if val, _ := stub.GetState(counter_key); val == nil {
    return nil, fmt.Errorf("Key does not exist %v" + args[0])
  } else {
    return []byte(val), nil
  }
	//valAsbytes, err := stub.GetState(checkingTab+"_"+args[0])
	//return valAsbytes, err
}

func (t *BlockchainID) register(stub shim.ChaincodeStubInterface, args []string) ([]byte, error) {
  key := pubkeyTab + "_" + args[0]
  counter_key := counterTab + "_" + args[0]
  if val, _:= stub.GetState(key); val != nil {
    return nil, fmt.Errorf("already registered, val %v", val)
  }
  stub.PutState(key, []byte(args[1]))
  stub.PutState(counter_key, []byte(strconv.Itoa(0)))
  
  /*
  // checking that we can actually get the Public Key back
  raw, _ := base64.StdEncoding.DecodeString(args[1])
  _, err := x509.ParsePKIXPublicKey(raw)
  if (err!=nil) {
    return nil, fmt.Errorf("Error converting back to public key %v", err)
  }
  */
  return nil, nil
}

func (t *BlockchainID) verifySignature(pubKey *ecdsa.PublicKey, value, raw_r, raw_s string) bool {
  // parse raw_r, raw_s back to bigInt
  rbytes, _ := base64.StdEncoding.DecodeString(raw_r)
  sbytes, _ := base64.StdEncoding.DecodeString(raw_s)
  r,s := big.NewInt(0), big.NewInt(0)
  r.UnmarshalText(rbytes)
  s.UnmarshalText(sbytes)
  return ecdsa.Verify(pubKey, []byte(value), r, s)
}

// argumments are: <hashkey>, <r>, <s> 
// (r,s) are signatures of the counter+1 value
func (t *BlockchainID) incrementCounter(stub shim.ChaincodeStubInterface, args []string) ([]byte, error) {
  key := pubkeyTab + "_" + args[0]
  counter_key := counterTab + "_" + args[0]

  if val, err := stub.GetState(counter_key); err!=nil {
    return nil, fmt.Errorf("No key exists %v\n", args[0])
  } else{
    count,_ := strconv.Atoi(string(val))
    // verify signature
    pub_raw, _ := stub.GetState(key)
    raw, _ := base64.StdEncoding.DecodeString(string(pub_raw))
    pub, _ := x509.ParsePKIXPublicKey(raw)

    count = count + 1
    //expected := strconv.Itoa(count) 
    expected := "0"
    if t.verifySignature(pub.(*ecdsa.PublicKey), expected, args[1], args[2]) {
      // update counter
      stub.PutState(counter_key, []byte(expected))
      return []byte("successful"), nil
    } else {
      return []byte("wrong signature"), fmt.Errorf("Signature cannot be verified")
    }
  }
}

