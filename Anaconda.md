# Anaconda

## 1.安装Anaconda

```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh   #官网安装
bash Miniconda3-latest-Linux-x86_64.sh #进入后根据提示安装（回车/yes）
```

## 2.创建python3虚拟环境

```shell
conda config --set auto_activate_base false # 启动时不被激活
conda create -n python3.6_ansible2.10 python=3.6  #创建python3虚拟环境  
#安装环境
pip install ansible==2.10.4 \
kubernetes==11.0.0 \
openshift==0.11.2 \
passlib==1.7.4 \
kubernetes-validate==1.20.0

pip install ansible==2.10.4 \
kubernetes==22.6.0 \
openshift==0.13.1 \
passlib==1.7.4 \
kubernetes-validate==1.23.1
```

## 3.虚拟环境

```shell
conda info --env #查看所有虚拟环境
conda activate python3.6_ansible2.10 #启动新建的虚拟环境
conda deactivate #关闭新建的虚拟环境
```

```
其实可以通过克隆一个新的环境，删掉老的环境来解决这个问题。

conda create --name python3（新名字） --clone python3.6_ansible2.10（老名字）

conda remove --name old_name --all
```

