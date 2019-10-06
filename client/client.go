package main 

import (
  "fmt"
  "crypto/ecdsa"
  "crypto/x509"
  "crypto/sha256"
  "crypto/elliptic"
  "crypto/rand"
  "encoding/json"
  "encoding/base64"
  "os"
)

func (c *Client) Gen(n int, filePath string) error {
  var pubkeys [][]byte
  var privkeys [][]byte
  var hashkeys [][]byte
  for i := 0; i<n; i++ {
    privKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
    check(err)
    mk, err := x509.MarshalPKIXPublicKey(privKey.Public())
    check(err)
    pk, err := x509.MarshalECPrivateKey(privKey)
    check(err)
    h := sha256.Sum256(mk)
    pubkeys = append(pubkeys, mk[:])
    privkeys = append(privkeys, pk[:])
    hashkeys = append(hashkeys, h[:])
  }

  dataFile, _ := os.Create(filePath+"_pub")
  encoder := json.NewEncoder(dataFile)
  encoder.Encode(pubkeys)
  dataFile.Close()
  dataFile, _ = os.Create(filePath+"_priv")
  encoder = json.NewEncoder(dataFile)
  encoder.Encode(privkeys)
  dataFile.Close()
  dataFile, _ = os.Create(filePath+"_hash")
  encoder = json.NewEncoder(dataFile)
  encoder.Encode(hashkeys)
  dataFile.Close()

  return nil
}

func (c *Client) Deploy(contractPath, filePath, endpoint string) {
  data := makeDeployRequest("deploy", contractPath, "Init", "") 
  rs := c.postRequest(data, endpoint)
  f, _ := os.Create(filePath)
  defer f.Close()
  f.WriteString(rs.Result.Message)
}

func (c *Client) Load(filePath string, chaincodeIDFile string, endpoint string) error {
  chaincodeID, pubkeys, _, hashkeys := c.load_keys(filePath, chaincodeIDFile)

  for i,v := range(pubkeys) {
    data := makeRequest("invoke", string(chaincodeID), "register",
    base64.StdEncoding.EncodeToString(hashkeys[i]),
    base64.StdEncoding.EncodeToString(v))
    c.postRequest(data, endpoint)
  }
  return nil
}

func (c *Client) Update(filePath, chaincodeIDFile string, index, counter int, endpoint string) error {
  chaincodeID, _, privkeys, hashkeys := c.load_keys(filePath, chaincodeIDFile)

  c.update(hashkeys[index], privkeys[index], counter, string(chaincodeID), endpoint) 
  return nil
}

func (c *Client) Query(filePath, chaincodeIDFile string, index int, endpoint string) error {
  chaincodeID, _, _, hashkeys := c.load_keys(filePath, chaincodeIDFile)

  rs := c.query(hashkeys[index], string(chaincodeID), endpoint) 
  fmt.Printf("%v\n", rs.Result.Message)
  return nil

}

