## Introduction to Mel Spectrograms

Read [this](https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53) and [this](https://towardsdatascience.com/getting-to-know-the-mel-spectrogram-31bca3e2d9d0) link

Additionally, if you're interested in learning further on DSP, see [this](https://www.youtube.com/watch?v=NA0TwPsECUQ)

## Experimental (Optional Setup)

Make a downloads folder to save the deb files (After setting up the VM in the main setup)
```
mkdir downloads
cd downloads
```

#### CUDA and CUDNN Setup

Note the instructions have been derived from [here](https://gist.github.com/matheustguimaraes/43e0b65aa534db4df2918f835b9b361d)

Also note that the VMs we provision are on Ubuntu 16.04 vs 18. Most instructions out there are specific to Ubuntu 18, which may or may not work for us.

By default the VMs provisioned are already equipped with CUDA. For example the V100 VM comes with CUDA 10.1. Can be confirmed with `/usr/local/cuda/bin/nvcc --version` or `nvidia-smi`

CUDNN needs to be manually installed. Here are the ready download links to the run time, dev sdk and code samples (for testing CUDNN), and the CUDA toolkit:

```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1zu2Vbed6fUcizWb3E726E3uZKx2uVnNv' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1zu2Vbed6fUcizWb3E726E3uZKx2uVnNv" -O libcudnn7_7.6.5.32-1+cuda10.1_amd64.deb && rm -rf /tmp/cookies.txt
```
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=16vZc8UgKkyJRgRGm8JuO0GOYWCdhEGMu' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=16vZc8UgKkyJRgRGm8JuO0GOYWCdhEGMu" -O libcudnn7-dev_7.6.5.32-1+cuda10.1_amd64.deb && rm -rf /tmp/cookies.txt
```

```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1FWXRwsNqPEflCmVIyPrDiBb2_dVGRPrr' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1FWXRwsNqPEflCmVIyPrDiBb2_dVGRPrr" -O libcudnn7-doc_7.6.5.32-1+cuda10.1_amd64.deb && rm -rf /tmp/cookies.txt
```

```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1pO2rzX4S0RLH0H9m78YTC4WhQjGVtQnv' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1pO2rzX4S0RLH0H9m78YTC4WhQjGVtQnv" -O cuda_10.1.105_418.39_linux.run && rm -rf /tmp/cookies.txt
```

After downloading, we install the deb packages for each
```
sudo dpkg -i libcudnn7_7.6.5.32-1+cuda10.1_amd64.deb
sudo dpkg -i libcudnn7-dev_7.6.5.32-1+cuda10.1_amd64.deb
sudo dpkg -i libcudnn7-doc_7.6.5.32-1+cuda10.1_amd64.deb
```

Export some path variables and refresh the bashrc file
```
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda-10.1/bin:$PATH
source ~/.bashrc 
```

For testing we will run MNIST code sample to run with CUDNN
```
# Copy code samples to downloads folder for convenience

cp -a /usr/src/cudnn_samples_v7/ ~/downloads/cudnn_samples_v7/
cd ~/downloads/cudnn_samples_v7/mnistCUDNN
make clean && make
./mnistCUDNN
```

Can verify libcudnn version here
```
/sbin/ldconfig -N -v $(sed 's/:/ /' <<< $LD_LIBRARY_PATH) 2>/dev/null | grep libcudnn
# output would be like	libcudnn.so.7 -> libcudnn.so.7.6.5
```

If you see no errors from the above sample, CUDNN is installed on the machine.

Alternatively, [Verify](https://medium.com/@changrongko/nv-how-to-check-cuda-and-cudnn-version-e05aa21daf6c) if CUDA and CUDNN are installed on the VM

#### Tensor RT Setup (On Jetson only, for inference)


For convenience, here is the deb package link for TensorRT: 
```
https://drive.google.com/file/d/1TiF7wxK_14ZetBBxO-4voHAg9db3pWcT/view?usp=sharing
```

Follow the steps in this [link](https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt_301/tensorrt-install-guide/index.html) to install Tensor RT
But to summarize, from downloads folder created

```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1TiF7wxK_14ZetBBxO-4voHAg9db3pWcT' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1TiF7wxK_14ZetBBxO-4voHAg9db3pWcT" -O nv-tensorrt-repo-ubuntu1604-cuda10.0-trt7.0.0.11-ga-20191216_1-1_amd64.deb && rm -rf /tmp/cookies.txt
```

```
sudo dpkg -i nv-tensorrt-repo-ubuntu1604-cuda10.0-trt7.0.0.11-ga-20191216_1-1_amd64.deb
sudo apt-get update
sudo apt-get install python3-libnvinfer

# If that doesnt work, try
sudo apt-get install -y --no-install-recommends python3-libnvinfer=7.0.0-1+cuda10.0 python3-libnvinfer-dev=7.0.0-1+cuda10.0 libnvinfer7=7.0.0-1+cuda10.0 libnvinfer-dev=7.0.0-1+cuda10.0
```

With sudo apt-get update, If you see an error like "The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 6ED91CA3AC1160CD"
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6ED91CA3AC1160CD
```

## Setup

Start a P100 VM - Change ssh key (optionally change location if Vm not available)

You can alternatively start a V100 VM by changing `--flavor AC1_8X60X100` to `--flavor AC2_8X60X100`

```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100 --domain=ucb.com --image=2263543 --billing=hourly  --network 1000 --key=<KeyID> --flavor AC1_8X60X100 --san
```

SSH into the VM, then setup s3fs to mount IBM cloud storage.

```
sudo apt-get update
sudo apt-get install automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
git clone https://github.com/s3fs-fuse/s3fs-fuse.git

cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install

```
Create cos creds file for IBM storage

```
echo "bf87c595976145c386349f53e2517493:a61ba4b36c06b17ce4a5cf1cb087821b79fb293c42b1e617" > $HOME/.cos_creds
chmod 600 $HOME/.cos_creds
```
Go back to root directory. Clone this repo and mount to IBM Object storage

```
# after going to root dir
git clone https://github.com/hoichunlaw/w251-project.git
cd w251-project
mkdir data

sudo s3fs audiodata /root/w251-project/data -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.jp-tok.cloud-object-storage.appdomain.cloud
```

Build docker container

```
# copy the ipynb files to the docker folder for building the container
cp *.ipynb ~/w251-project/docker
cd docker
docker build -t tf/w251-project -f Dockerfile.tf-w251-project .
```

Run docker container

```
nvidia-docker run -d --name w251-project -p 8888:8888 -v /root/w251-project:/project tf/w251-project
```

Then you can access the notebook by looking at the public IP of the VM and navigating to the jupyter server.
```
# get public ip address of the vm
ifconfig
# get the jupyter token from docker logs and navigate to IP.Address:8888?token=<tokenId>
docker logs w251-project
```

