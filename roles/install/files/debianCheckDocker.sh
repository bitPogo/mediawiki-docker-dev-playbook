#!/bin/bash

dpkg -l docker-ce &> /dev/null

if [ $? -ne 0 ]; then
        #see https://docs.docker.com/install/linux/docker-ce/debian/
        apt-get install -y \
                apt-transport-https \
                ca-certificates \
                curl \
                gnupg2 \
                software-properties-common
        
        curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

        add-apt-repository \
                "deb [arch=amd64] https://download.docker.com/linux/debian \
                $(lsb_release -cs)\
                stable"
fi

