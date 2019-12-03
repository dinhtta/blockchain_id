#!/bin/bash
# installing hyperledger-fabric with docker 

#install docker 

dpkg -s "docker-ce" &> /dev/null

if [ $? -eq 0 ]; then
    echo "Docker installed"
else
    sudo apt update
    sudo apt -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo apt-key fingerprint 0EBFCD88
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt -y install docker-ce docker-ce-cli containerd.io
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
fi


HL_DATA=$HOME

sudo apt install -y libsnappy-dev zlib1g-dev libbz2-dev

ARCH=`uname -m`
if [ $ARCH == "aarch64" ]; then
        ARCH="arm64"
elif [ $ARCH == "x86_64" ]; then
        ARCH="amd64"
fi

if ! [ -d "$HL_DATA" ]; then
	mkdir -p $HL_DATA
fi
cd $HL_DATA

GOTAR="go1.9.3.linux-$ARCH.tar.gz"
wget https://storage.googleapis.com/golang/$GOTAR
sudo tar -C /usr/local -xzf $GOTAR
mkdir -p $HOME/go/src/github.com
echo "export PATH=\"\$PATH:/usr/local/go/bin\"" >> ~/.profile
echo "export GOPATH=\"$HOME/go\"" >> ~/.profile
source ~/.profile
sudo chown -R $USER:$USER $HOME/go

git clone https://github.com/facebook/rocksdb.git

sudo apt install -y make g++ build-essential
cd $HL_DATA
cd rocksdb
git checkout v4.5.1
PORTABLE=1 make shared_lib
sudo INSTALL_PATH=/usr/local make install-shared


#installing hyperledger fabric

set -ue
#sudo ntpdate -b clock-1.cs.cmu.edu
HL_HOME=/home/ubuntu/go/src/github.com/hyperledger
#HL_A2M_OPTIMIZE=fabric_a2m_optimize
#HL_A2M_OPTIMIZE_NOBROADCAST=fabic_a2m_optimize_no_broadcast
#HL_A2M_NOBROADCAST=fabric_a2m_no_broadcast
#HL_A2M_SEPARATE_QUEUE=fabric_a2m_separate_queue
HL_NO_A2M_NOBROADCAST=fabric_noa2m_no_broadcast
#HL_ORIGINAL=fabric_noa2m
#HL_A2M=fabric_a2m
#HL_ORIGINAL_SHARDING=fabric_noa2m_sharding
#HL_A2M_NOBROADCAST_SHARDING=fabric_a2m_no_broadcast_sharding
#HL_A2M_OPTIMIZE_SHARDING=fabric_a2m_optimize_sharding
#HL_A2M_SHARDING=fabric_a2m_sharding
#HL_A2M_SEPARATE_QUEUE_SHARDING=fabric_a2m_separate_queue_sharding

HL=fabric

sudo apt-get install -y fabric

mkdir -p $HL_HOME
cd $HL_HOME && rm -rf fabric*


echo "Installing HL with optimization 1 (no broadcast)"
git clone https://github.com/ug93tad/fabric && cd $HL
git checkout noa2m_no_broadcast && make peer
rm -rf $HL_HOME/$HL_NO_A2M_NOBROADCAST && cp -r $HL_HOME/$HL $HL_HOME/$HL_NO_A2M_NOBROADCAST
cd $HL_HOME && rm -rf $HL


