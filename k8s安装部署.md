# K8s安装部署

 https://www.yisu.com/zixun/23228.html 

## 一．环境准备

| 主机名 | ip             |
| ------ | -------------- |
| master | 192.168.37.110 |
| node01 | 192.168.37.111 |
| node02 | 192.168.37.112 |



## 二．部署前操作

### 1.借助ntp服务设置各节点的时间同步

```shell
yum -y install chrony #下载
systemctl start chronyd && systemctl enable chronyd #启动
chronyc sources #检测
```

### 2.通过DNS完成各节点名称解析，测试环境主机，测试用hosts文件代替

```shell
hostnamectl  set-hostname  master # node01 node02
bash
```

### 3.配置各节点的hosts

```bash
vim /etc/hosts

127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.37.110 master
192.168.37.111 node01
192.168.37.112 node02
```

### 4.配置master免密登入

```shell
ssh-keygen -t rsa
ssh-copy-id node01
ssh-copy-id node02
```

### 5.如有firewalld服务或iptables规则关闭各节点iptables和firewalld服务

```shell
systemctl stop firewalld && systemctl disable firewalld
iptables -F
```

### 6.禁用SELinux

```shell
setenforce 0 # 临时关闭
# 永久关闭
/etc/sysconfig/selinux 中改SELINUX=disabled 
#或 
sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
```

### 7.禁用Swap设备

```shell
free
swapoff -a # 临时关闭
sed -ri 's/.*swap.*/#&/' /etc/fstab # 永久关闭
```

### 8.打开iptables桥接功能及路由转发

**各节点开启桥接**

```shell
[root@master ~]# sysctl -a |grep bridge 
sysctl: reading key "net.ipv6.conf.all.stable_secret"
sysctl: reading key "net.ipv6.conf.default.stable_secret"
sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
sysctl: reading key "net.ipv6.conf.lo.stable_secret"
sysctl: reading key "net.ipv6.conf.virbr0.stable_secret"
sysctl: reading key "net.ipv6.conf.virbr0-nic.stable_secret"
[root@master ~]# modprobe br_netfilter
[root@master ~]# sysctl -a |grep bridge
net.bridge.bridge-nf-call-arptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-filter-pppoe-tagged = 0
net.bridge.bridge-nf-filter-vlan-tagged = 0
net.bridge.bridge-nf-pass-vlan-input-dev = 0
sysctl: reading key "net.ipv6.conf.all.stable_secret"
sysctl: reading key "net.ipv6.conf.default.stable_secret"
sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
sysctl: reading key "net.ipv6.conf.lo.stable_secret"
sysctl: reading key "net.ipv6.conf.virbr0.stable_secret"
sysctl: reading key "net.ipv6.conf.virbr0-nic.stable_secret"
[root@master ~]# cat >> /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
[root@master ~]# cat /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
[root@master ~]# sysctl -p /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
```

## 三．k8s集群

### k8s部署

#### 1.部署docker

```shell
yum install -y yum-utils
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum -y install docker-ce docker-ce-cli containerd.io
docker --version
systemctl start docker
```

#### 2.部署kubernetes

**获取yum**

```shell
[root@master ~]# cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
[root@master ~]# cat /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
```

**安装、开机自启kubelet**

```shell
yum install -y kubelet-1.18.0 kubeadm-1.18.0 kubectl-1.18.0
systemctl enable kubelet
```

#### 3.配置Master节点初始化

```shell
kubeadm version #查看安装的版本
kubeadm init --apiserver-advertise-address=192.168.37.110 --image-repository registry.aliyuncs.com/google_containers --kubernetes-version v1.18.0 --service-cidr=10.96.0.0/12  --pod-network-cidr=10.244.0.0/16

# 执行初始化中提示必要步骤
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

#kubectl查看节点状态
kubectl get nodes
```

#### 4.在master中安装flannel插入

```shell
# 如果节点状态是NotReady，安装flannel插件
wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml # 如果wget下载有问题就用其他方法把yml文件下载下来
kubectl apply -f kube-flannel.yml
```

#### 5.将node节点添加到kubernetes集群(node节点执行)

```shell
$ kubeadm join --token 5p5lsl.dmwdsgrosh5w9zjl 192.168.37.110:6443
```

如果出现以下错误，说明需要进行ca校验可以使用

```shell
--discovery-token-unsafe-skip-ca-verification
```

参数忽略校验
discovery.bootstrapToken: Invalid value: "": using token-based discovery without caCertHashes can be unsafe. Set unsafeSkipCAVerification to continue
这里指定的--token来自前面kubeadm init执行后输出的信息。如果没有记录可以通过kubeadm token list进行查看。最后一个参数是指定master节点的ip和k8s api(https)端口
**默认token 24小时就会过期，后续的机器要加入集群需要使用以下命令重新生成token**

```shell
kubeadm token create
```

**查看token**

```shell
kubeadm token list
```



### 部署 nginx

1. 创建监听 80 端口的 Nginx Pod（Kubernetes 运行容器的最小单元)

```shell
kubectl run nginx --image=nginx --port=80
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210723110602032.png" alt="image-20210723110602032" style="width:100%;" />

2. 查看deployment

```shell
kubectl get deployment
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210723111312155.png" alt="image-20210723111312155" style="width:100%;" />

3. 问题就出现了，的确没有，那我们就需要手动创建

```shell
kubectl create deployment nginx --image=nginx
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210723111551611.png" alt="image-20210723111551611" style="width:100%;" />

4. 再次查看deployment

```shell
kubectl get deployment
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210723111703180.png" alt="image-20210723111703180" style="width:100%;" />



### 发布服务

1. 使用负载均衡模式发布服务

```shell
kubectl expose deployment nginx --port=80 --type=LoadBalancer
```

2. 查看服务详情

```shell
kubectl describe service nginx
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210723111959206.png" alt="image-20210723111959206" style="width:100%;" />

3. 这里我就可以利用 节点的ip+暴露出来的端口 检测服务是否访问成功

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210723112329775.png" alt="image-20210723112329775" style="width:100%;" />

## 四．yum安装etcd集群

### 安装

1.yum安装

```shell
yum -y install etcd
```

2.修改etcd配置文件

```shell
vim /etc/etcd/etcd.conf
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210726140306323.png" alt="image-20210726140306323" style="width:100%;" />

3.修改etcd启动配置文件

```shell
vim /usr/lib/systemd/system/etcd.service 
```

```shell
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
WorkingDirectory=/var/lib/etcd/
EnvironmentFile=-/etc/etcd/etcd.conf
User=etcd
# set GOMAXPROCS to number of processors
ExecStart=/bin/bash -c "GOMAXPROCS=$(nproc) /usr/bin/etcd --name=\"${ETCD_NAME}\" --data-dir=\"${ETCD_DATA_DIR}\" --listen-client-urls=\"${ETCD_LISTEN_CLIENT_URLS}\" --listen-peer-urls=\"${ETCD_LISTEN_PEER_URLS}\" --advertise-client-urls=\"${ETCD_ADVERTISE_CLIENT_URLS}\" --initial-cluster-token=\"${ETCD_INITIAL_CLUSTER_TOKEN}\" --initial-cluster=\"${ETCD_INITIAL_CLUSTER}\" --initial-cluster-state=\"${ETCD_INITIAL_CLUSTER_STATE}\" "
Restart=on-failu
LimitNOFILt=65536

[Install]
WantedBy=multi-user.target
```

5.启动etcd服务

```shell
systemctl start etcd	#启动etcd服务
systemctl status etcd	#查看启动状态
```

如若出现如下错误，处理方法：

```shell
systemctl stop avahi-daemon
systemctl disable avahi-daemon
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210726135724152.png" alt="image-20210726135724152" style="width:100%;" />

6.查看cluster状态

```shell
etcdctl cluster-health
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210726145442229.png" alt="image-20210726145442229" style="width:100%;" />

7.列出etcd服务状态

```shell
etcdctl member list
#从列出信息可以看出，目前是etcd为主节点。
#查看etcd服务启动日志，可通过 tail -f /var/log/message 动态查看
```

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210726145945872.png" alt="image-20210726145945872" style="width:100%;" />

8.至此，etcd集群已配置完成。接下来可以对kubernetes集群apiserver配置文件进行修改，使其指向etcd集群

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```shell
 1 #修改master节点，apiserver配置文件
 2 [root@master ~]# cat /etc/kubernetes/apiserver 
 3 ###
 4 ## kubernetes system config
 5 KUBE_API_ADDRESS="--address=0.0.0.0"
 6 KUBE_API_PORT="--port=8080"
 7 KUBELET_PORT="--kubelet-port=10250"
 8 KUBE_ETCD_SERVERS="--etcd-servers=http://192.168.20.71:2379,http://192.168.20.72:2379,http://192.168.20.73:2379"
 9 KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"
10 KUBE_API_ARGS="--service_account_key_file=/etc/kubernetes/serviceaccount.key"
11 KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"
12 KUBE_API_ARGS=""
13 
14 #k8s集群做任何调整后，都需要重启服务
15 #重启master各组件，可连起来写
16 systemctl restart kube-apiserver kube-controller-manager kube-scheduler
17 #重启node1、node2各组件
18 systemctl restart kubelet kube-proxy
19 
20 #再次在master节点查看etcd、node集群状态
21 #测试，可关闭一台etcd服务，创建一个pod，无异常
22 #通过测试可以得出，etcd集群至少需要2个etcd节点才可以正常工作。
```

# k8s

## 一．环境准备

### kubectx和kubens

```shell
#轻松进行上下文和命名空间切换（kubectx和kubens工具）
wget https://raw.githubusercontent.com/ahmetb/kubectx/master/kubectx
wget https://raw.githubusercontent.com/ahmetb/kubectx/master/kubens
chmod +x kubectx kubens
sudo mv kubens kubectx /usr/local/bin
```

### fzf

```shell
git clone --depth 1 https://github.com/junegunn/fzf.git && cd fzf/ && ./install
source ~/.bashrc
```

### Kubectl autocomplete（自动补全）

```bash
source <(kubectl completion bash) 
echo "source <(kubectl completion bash)" >> ~/.bashrc 
#如果出现  -bash: _get_comp_words_by_ref: command not found
yum install bash-completion -y
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash) 
```



## 二．k8s架构

<img src="https://jimmysong.io/kubernetes-handbook/images/kubernetes-high-level-component-archtecture.jpg" alt="Kuberentes 架构（图片来自于网络）" style="width:100%;" />

Kubernetes 主要由以下几个核心组件组成：

- etcd 保存了整个集群的状态；
- apiserver 提供了资源操作的唯一入口，并提供认证、授权、访问控制、API 注册和发现等机制；
- controller manager 负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
- scheduler 负责资源的调度，按照预定的调度策略将 Pod 调度到相应的机器上；
- kubelet 负责维护容器的生命周期，同时也负责 Volume（CSI）和网络（CNI）的管理；
- Container runtime 负责镜像管理以及 Pod 和容器的真正运行（CRI）；
- kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡；

除了核心组件，还有一些推荐的插件，其中有的已经成为 CNCF 中的托管项目：

- CoreDNS 负责为整个集群提供 DNS 服务
- Ingress Controller 为服务提供外网入口
- Prometheus 提供资源监控
- Dashboard 提供 GUI
- Federation 提供跨可用区的集群

## 三．集群

### 1.Pod概览

**在 Kubernetes 集群中 Pod 两种使用方式：**

- 一个 Pod 中运行一个容器。“每个 Pod 中一个容器” 的模式是最常见的用法；在这种使用方式中，你可以把 Pod 想象成是单个容器的封装，kuberentes 管理的是 Pod 而不是直接管理容器。
- 在一个 Pod 中同时运行多个容器。一个 Pod 中也可以同时封装几个需要紧密耦合互相协作的容器，它们之间共享资源。这些在同一个 Pod 中的容器可以互相协作成为一个 service 单位 —— 一个容器共享文件，另一个 “sidecar” 容器来更新这些文件。Pod 将这些容器的存储资源作为一个实体来管理。

**Pod 中可以共享两种资源：网络和存储**

* 网络： 每个 Pod 都会被分配一个唯一的 IP 地址。Pod 中的所有容器共享网络空间，包括 IP 地址和端口。Pod 内部的容器可以使用 `localhost` 互相通信。Pod 中的容器与外界通信时，必须分配共享网络资源（例如使用宿主机的端口映射）。
* 存储： 可以为一个 Pod 指定多个共享的 Volume。Pod 中的所有容器都可以访问共享的 volume。Volume 也可以用来持久化 Pod 中的存储资源，以防容器重启后文件丢失

```shell
# 注意：重启 Pod 中的容器跟重启 Pod 不是一回事。Pod 只提供容器的运行环境并保持容器的运行状态，重启容器不会造成 Pod 重启。
```

**Pod phase**

- 挂起（Pending）：Pod 已被 Kubernetes 系统接受，但有一个或者多个容器镜像尚未创建。等待时间包括调度 Pod 的时间和通过网络下载镜像的时间，这可能需要花点时间。
- 运行中（Running）：该 Pod 已经绑定到了一个节点上，Pod 中所有的容器都已被创建。至少有一个容器正在运行，或者正处于启动或重启状态。
- 成功（Succeeded）：Pod 中的所有容器都被成功终止，并且不会再重启。
- 失败（Failed）：Pod 中的所有容器都已终止了，并且至少有一个容器是因为失败终止。也就是说，容器以非0状态退出或者被系统终止。
- 未知（Unknown）：因为某些原因无法取得 Pod 的状态，通常是因为与 Pod 所在主机通信失败。

### 2.Deployment

Deployment 为 Pod 和 ReplicaSet 提供了一个声明式定义（declarative）方法。

相比于job，默认单个job成功运行后即结束

比如一个简单的 nginx 应用可以定义为：

```yaml
apiVersion: apps/v1 #apiVersion 是当前配置格式的版本（通过命令 kubectl api-version 查看）
kind: Deployment #要创建的资源类型
metadata: #资源的元数据（name 是必需的元数据项）
  name: nginx-deployment
spec: #描述Deployment 的规格
  replicas: 3 #副本数量，默认为 1
  selector: #过滤规则的定义（匹配过滤携带label的pods）
   matchLabels:
    app: nginx
  template:  #定义 Pod 的模板（配置文件的重要部分）
    metadata: #定义 Pod 的元数据（至少要定义一个 label。label 的 key 和 value 可以任意指定）
      labels:
        app: nginx
    spec: #描述 Pod 的规格（定义 Pod 中每一个容器的属性，name 和 image 是必需的）
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

创建Deployment

```shell
# kubectl create命令，是先删除所有现有的东西，重新根据yaml文件生成新的。
# kubectl apply命令，根据配置文件里面列出来的内容，升级现有的。所以yaml文件的内容可以只写需要升级的属性。
[root@master home]# kubectl create -f nginx-deployment.yaml --record
[root@master home]# kubectl apply -f nginx-deployment.yaml --record
deployment.apps/nginx-deployment created
#------------------------------------ --record ------------------------------------
#将 kubectl 的--record的 flag 设置为true 可以在 annotation 中记录当前命令创建或者升级了该资源。
#----查看roll 历史
[root@master home]# kubectl rollout history deployment nginx-deployment    
deployment.apps/nginx-deployment
REVISION  CHANGE-CAUSE
1         kubectl apply --filename=nginx-deployment.yaml --record=true
2         kubectl apply --filename=nginx-deploymentnew.yaml --record=true
#----回退版本
[root@master home]# kubectl rollout undo deployment/nginx-deployment
deployment.apps/nginx-deployment rolled back
[root@master home]# kubectl rollout undo deployment nginx-deployment --to-revision=1  #回退到指定版本
deployment.apps/nginx-deployment rolled back
[root@master home]# kubectl rollout history deployment nginx-deployment    
deployment.apps/nginx-deployment
REVISION  CHANGE-CAUSE
2         kubectl apply --filename=nginx-deploymentnew.yaml --record=true
3         kubectl apply --filename=nginx-deployment.yaml --record=true
#----------------------------------------------------------------------------------
[root@master home]# kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           12m
[root@master home]# kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-6dd8bc586b-kndcj   1/1     Running   0          3m44s
nginx-deployment-6dd8bc586b-mv9ps   1/1     Running   0          3m44s
nginx-deployment-6dd8bc586b-vxs4h   1/1     Running   0          3m44s
[root@master home]# kubectl get rs
NAME                          DESIRED   CURRENT   READY   AGE
nginx-deployment-6dd8bc586b   3         3         3       156m
```

扩容：

```bash
[root@master home]# kubectl scale deployment nginx-deployment --replicas 5
deployment.apps/nginx-deployment scaled
[root@master home]# kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   5/5     5            5           157m
[root@master home]# kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-6dd8bc586b-bdrqm   1/1     Running   0          23s
nginx-deployment-6dd8bc586b-gwwbr   1/1     Running   0          23s
nginx-deployment-6dd8bc586b-kndcj   1/1     Running   0          157m
nginx-deployment-6dd8bc586b-mv9ps   1/1     Running   0          157m
nginx-deployment-6dd8bc586b-vxs4h   1/1     Running   0          157m
```

如果集群支持 horizontal pod autoscaling 的话，还可以为 Deployment 设置自动扩展：

```shell
[root@master home]# kubectl autoscale deployment nginx-deployment --min=4 --max=10 --cpu-percent=80 #使Pod的数量介于4和10之间，CPU使用率维持在80%
horizontalpodautoscaler.autoscaling/nginx-deployment autoscaled
[root@master home]# kubectl get horizontalpodautoscaler.autoscaling
NAME               REFERENCE                     TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
nginx-deployment   Deployment/nginx-deployment   <unknown>/80%   4         10        6          15s
[root@master home]# kubectl get pods 
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-6dd8bc586b-bt5dl   1/1     Running   0          5m20s
nginx-deployment-6dd8bc586b-f7cn7   1/1     Running   0          5m13s
nginx-deployment-6dd8bc586b-fvhsr   1/1     Running   0          5m20s
nginx-deployment-6dd8bc586b-rkj4q   1/1     Running   0          5m13s
nginx-deployment-6dd8bc586b-wn6mp   1/1     Running   0          5m20s
nginx-deployment-6dd8bc586b-zdbmr   1/1     Running   0          5m13s
#删除autoscale(两种方法)
[root@master home]# kubectl delete horizontalpodautoscalers.autoscaling nginx-deployment 
horizontalpodautoscaler.autoscaling "nginx-deployment" deleted

[root@master home]# kubectl get hpa
NAME               REFERENCE                     TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
nginx-deployment   Deployment/nginx-deployment   <unknown>/80%   4         10        0          2s
[root@master home]# kubectl delete hpa nginx-deployment
horizontalpodautoscaler.autoscaling "nginx-deployment" deleted
```

更新镜像：

```shell
[root@master home]# kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
deployment.apps/nginx-deployment image updated
[root@master home]# kubectl describe deployments
  Containers:
   nginx:
    Image:        nginx:1.9.1
```

### 3.node

```shell
#---------------------------指定节点上创建容器---------------------------
[root@master home]# kubectl label nodes node01 label=test    #创建标签（name=node01）
node/node01 labeled
[root@master home]# kubectl label nodes node01 label-   #删除标签
node/node01 labeled
[root@master home]# kubectl get nodes --show-labels    #查看标签
NAME     STATUS   ROLES    AGE   VERSION   LABELS
master   Ready    master   24d   v1.18.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=master,kubernetes.io/os=linux,node-role.kubernetes.io/master=
node01   Ready    <none>   22d   v1.18.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux,label=test
node02   Ready    <none>   22d   v1.18.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node02,kubernetes.io/os=linux
[root@master home]# vim nginxW-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: http-deployment
spec:
  replicas: 3
  selector:
   matchLabels:
    app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
      nodeSelector:  #指定node标签
        label: test
[root@master home]# kubectl get pod -o wide
NAME                                READY   STATUS    RESTARTS   AGE    IP            NODE     NOMINATED NODE   READINESS GATES
http-deployment-67b77c64f-62s49     1/1     Running   0          6s     10.244.1.24   node01   <none>           <none>
http-deployment-67b77c64f-9x5rm     1/1     Running   0          6s     10.244.1.25   node01   <none>           <none>
http-deployment-67b77c64f-zzs77     1/1     Running   0          6s     10.244.1.23   node01   <none>           <none>
#---------------------------过滤标签---------------------------
$ kubectl get pods -l environment=production,tier=frontend
$ kubectl get pods -l 'environment in (production),tier in (frontend)'
$ kubectl get pods -l 'environment in (production, qa)'
$ kubectl get pods -l 'environment,environment notin (frontend)'
[root@master home]# kubectl get node -l label=test 
NAME     STATUS   ROLES    AGE   VERSION
node01   Ready    <none>   23d   v1.18.0

```

node管理

```shell
===================cordon========================
#禁止 Pod 调度到该节点上。
kubectl cordon node01 
# 影响最小，只会将node调为SchedulingDisabled
# 之后再发创建pod，不会被调度到该节点
# 旧有的pod不会受到影响，仍正常对外提供服务

#恢复调度
kubectl uncordon node01
===================drain=========================
#驱逐节点
kubectl drain node01
#命令会删除该节点上的所有 Pod（DaemonSet 除外），在其他 node 上重新启动它们，通常该节点需要维护时使用该命令。直接使用该命令会自动调用`kubectl cordon <node>`命令。
#接着，该节点调为SchedulingDisabled

#恢复调度
kubectl uncordon node01
===================delete========================
kubectl delete node01
#首先，驱逐node上的pod，其他节点重新创建
#然后，从master节点删除该node，master对其不可见，失去对其控制，master不可对其恢复

#恢复调度，需进入node节点，重启kubelet
#基于node的自注册功能，节点重新恢复使用
systemctl restart kubelet
================================================
```

### 4.annotation

Annotation，顾名思义，就是注解。Annotation 可以将 Kubernetes 资源对象关联到任意的非标识性元数据。

Label 和 Annotation 都可以将元数据关联到 Kubernetes 资源对象。Label 主要用于选择对象，可以挑选出满足特定条件的对象。相比之下，annotation 不能用于标识及选择对象。annotation 中的元数据可多可少，可以是结构化的或非结构化的，也可以包含 label 中不允许出现的字符。

Annotation 和 label 一样都是 key/value 键值对映射结构：

```
json"annotations": {"key1":"value1","key2":"value2"}
```

以下列出了一些可以记录在 annotation 中的对象信息：

- 声明配置层管理的字段。使用 annotation 关联这类字段可以用于区分以下几种配置来源：客户端或服务器设置的默认值，自动生成的字段或自动生成的 auto-scaling 和 auto-sizing 系统配置的字段。
- 创建信息、版本信息或镜像信息。例如时间戳、版本号、git 分支、PR 序号、镜像哈希值以及仓库地址。
- 记录日志、监控、分析或审计存储仓库的指针

- 可以用于 debug 的客户端（库或工具）信息，例如名称、版本和创建信息。
- 用户信息，以及工具或系统来源信息、例如来自非 Kubernetes 生态的相关对象的 URL 信息。
- 轻量级部署工具元数据，例如配置或检查点。
- 负责人的电话或联系方式，或能找到相关信息的目录条目信息，例如团队网站。

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: istio-manager
spec:
  replicas: 1
  template:
    metadata:
      annotations:  #控制是否自动向 pod 中注入 sidecar 
        alpha.istio.io/sidecar: ignore
      labels:
        istio: manager
    spec:
      serviceAccountName: istio-manager-service-account
      containers:
      - name: discovery
        image: harbor-001.jimmysong.io/library/manager:0.1.5
        imagePullPolicy: Always
        args: ["discovery", "-v", "2"]
        ports:
        - containerPort: 8080
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
```

### 5.namespace

在一个 Kubernetes 集群中可以使用 namespace 创建多个 “虚拟集群”，这些 namespace 之间可以完全隔离，也可以通过某种方式，让一个 namespace 中的 service 可以访问到其他的 namespace 中的服务。

集群中默认会有 `default` 和 `kube-system` 这两个 namespace。用户的普通应用默认是在 `default` 下，与集群管理相关的为整个集群提供服务的应用一般部署在 `kube-system` 的 namespace 下，例如我们在安装 kubernetes 集群时部署的 `kubedns`、`heapseter`、`EFK` 等都是在这个 namespace 下面。

另外，并不是所有的资源对象都会对应 namespace，`node` 和 `persistentVolume` 就不属于任何 namespace。

```shell
kubectl get ns #获取集群中有哪些 namespace
kubectl -n #定操作的 namespace
```

### 6.affinity、taint、toleration、固定节点

node/pod affinity

- requiredDuringSchedulingIgnoredDuringExecution
  表示pod必须部署到满足条件的节点上，如果没有满足条件的节点，就不停重试。其中IgnoreDuringExecution表示pod部署之后运行的时候，如果节点标签发生了变化，不再满足pod指定的条件，pod也会继续运行。
- requiredDuringSchedulingRequiredDuringExecution
  表示pod必须部署到满足条件的节点上，如果没有满足条件的节点，就不停重试。其中RequiredDuringExecution表示pod部署之后运行的时候，如果节点标签发生了变化，不再满足pod指定的条件，则重新选择符合要求的节点。
- preferredDuringSchedulingIgnoredDuringExecution
  表示优先部署到满足条件的节点上，如果没有满足条件的节点，就忽略这些条件，按照正常逻辑部署。
- preferredDuringSchedulingRequiredDuringExecution
  表示优先部署到满足条件的节点上，如果没有满足条件的节点，就忽略这些条件，按照正常逻辑部署。其中RequiredDuringExecution表示如果后面节点标签发生了变化，满足了条件，则重新调度到满足条件的节点。
- 这里的匹配逻辑是label在某个列表中，可选的操作符有：
  - In: label的值在某个列表中
  - NotIn：label的值不在某个列表中
  - Exists：某个label存在
  - DoesNotExist：某个label不存在
  - Gt：label的值大于某个值（字符串比较）
  - Lt：label的值小于某个值（字符串比较）

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
#################### node affinity
spec:
  containers:
  - name: with-node-affinity
    image: gcr.io/google_containers/pause:2.0
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname  #要求pod 运行在node01的节点
            operator: In
            values:
            - node01
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1 #权重（权重越大亲和性越高）
        preference:
          matchExpressions:
          - key: kubernetes.io/hostname #希望节点pod 运行在node01的节点
            operator: In
            values:
            - node01
#################### pod affinity
apiVersion: v1
kind: Pod
metadata:
  name: with-pod-affinity
  labels: 
   app: with-pod-affinity
spec:
  containers:
  - name: with-pod-affinity
    image: gcr.io/google_containers/pause:2.0
  affinity:
    podAffinity:  #亲和
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchExpressions:
              - key: app  #要求pod 与标签为app：pod-1的pod运行在同一个节点上
                operator: In
                values:
                - pod-1
          topologyKey: kubernetes.io/hostname #判断条件
    podAntiAffinity:   #排斥
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1 #权重（权重越大亲和性越高）
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app  #要求pod 与标签为app：pod-1的pod运行在不同节点上
                operator: In
                values:
                - pod-1
          topologyKey: kubernetes.io/hostname #判断条件
```

taint、toleration

Taint（污点）和 Toleration（容忍）可以作用于 node 和 pod 上，其目的是优化 pod 在集群间的调度，这跟节点亲和性类似，只不过它们作用的方式相反，具有 taint 的 node 和 pod 是互斥关系，而具有节点亲和性关系的 node 和 pod 是相吸的。

Taint 和 toleration 相互配合，可以用来避免 pod 被分配到不合适的节点上。每个节点上都可以应用**一个或多个** taint ，这表示对于那些不能容忍这些 taint 的 pod，是不会被该节点接受的。如果将 toleration 应用于 pod 上，则表示这些 pod 可以（但不要求）被调度到具有相应 taint 的节点上。

```shell
# =================== 为 node 设置 taint =====================
--------为 node01 设置 taint：
kubectl taint nodes node01 key1=value1:NoSchedule
kubectl taint nodes node01 key1=value1:NoExecute
kubectl taint nodes node01 key2=value2:NoSchedule
--------删除上面的 taint：
kubectl taint nodes node01 key1:NoSchedule-
kubectl taint nodes node01 key1:NoExecute-
kubectl taint nodes node01 key2:NoSchedule-
--------查看 node01 上的 taint：
kubectl describe nodes node01
# ================= 为 pod 设置 toleration ===================
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"  
  effect: "NoSchedule"   #可以为 NoSchedule、PreferNoSchedule 或 NoExecute
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
- key: "node.alpha.kubernetes.io/unreachable"
  operator: "Exists"
  effect: "NoExecute"
  tolerationSeconds: 6000  #当 pod 需要被驱逐时，可以继续在 node 上运行的时间
```

固定节点

- nodeName:
- nodeSelector:

```yaml
# ================= nodeName ===================
apiVersion: apps/v1 
kind: Deployment
metadata: 
  name: nginx-deployment
spec:
  replicas: 3 
  selector:
   matchLabels:
    app: nginx
  template: 
    metadata: 
      labels:
        app: nginx
    spec: 
      nodeName: node01 #强制固定到node01节点
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
# ================= nodeSelector ===================      
apiVersion: apps/v1 
kind: Deployment
metadata: 
  name: nginx-deployment
spec:
  replicas: 3 
  selector:
   matchLabels:
    app: nginx
  template: 
    metadata: 
      labels:
        app: nginx
    spec: 
      nodeSelector:
        disk: ssd  #强制选择标签有 disk：ssd 的节点（如果有多个，随机选择）
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

### 7.DaemonSet

*DaemonSet* 确保全部（或者一些）Node 上运行一个 Pod 的副本。当有 Node 加入集群时，也会为他们新增一个 Pod 。当有 Node 从集群移除时，这些 Pod 也会被回收。删除 DaemonSet 将会删除它创建的所有 Pod。

### 8.CronJob

*Cron Job* 管理基于时间的 [Job](https://kubernetes.io/docs/concepts/jobs/run-to-completion-finite-workloads/)，即：

- 在给定时间点只运行一次
- 周期性地在给定时间点运行

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"  #调度，必需字段，指定任务运行周期
  jobTemplate:  #Job 模板，必需字段，指定需要运行的任务
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            args:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

### 9.StatefulSet

StatefulSet是为了解决有状态服务的问题（对应Deployments和ReplicaSets是为无状态服务而设计），其应用场景包括：

- 稳定的持久化存储，即Pod重新调度后还是能访问到相同的持久化数据，基于PVC来实现
- 稳定的网络标志，即Pod重新调度后其PodName和HostName不变，基于Headless Service（即没有Cluster IP的Service）来实现
- 有序部署，有序扩展，即Pod是有顺序的，在部署或者扩展的时候要依据定义的顺序依次依次进行（即从0到N-1，在下一个Pod运行之前所有之前的Pod必须都是Running和Ready状态），基于init containers来实现
- 有序收缩，有序删除（即从N-1到0）

```yaml
---                 
apiVersion: v1
kind: Service   #定义网络标志（DNS domain）的Headless Service，用于控制网络域
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---                     
apiVersion: apps/v1beta1
kind: StatefulSet   #定义具体应用的StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 2
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: gcr.io/google_containers/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:          #使用 PersistentVolume Provisioner 提供的 PersistentVolumes 作为稳定存储。自动创建PVC（kubectl get pvc）
  - metadata:
      name: www
      annotations:
        volume.alpha.kubernetes.io/storage-class: anything
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

### 10.HPA

Horizontal Pod Autoscaling(HPA),顾名思义就是使Pod水平自动缩放，仅适用于Deployment和ReplicaSet，由API server和controller共同实现。

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210901145231521.png" alt="image-20210901145231521" style="width:100%;" />

```yaml
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: hello-world
spec:
  scaleTargetRef:
    apiVersion: extensions/v1beta1
    kind: Deployment
    name: hello-world
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      targetAverageUtilization: 50
  - type: Resource
    resource:
      name: memory
      targetAverageValue: 100Mi
```

```shell
kubectl autoscale deployment hello-world --min=2 --max=5 --cpu-percent=50
[root@master home]# kubectl create -f hpa.yaml
horizontalpodautoscaler.autoscaling/hello-world created
[root@master home]# kubectl get hpa hello-world
NAME          REFERENCE                TARGETS                          MINPODS   MAXPODS   REPLICAS   AGE
hello-world   Deployment/hello-world   <unknown>/100Mi, <unknown>/50%   1         10        0          16s
[root@master home]# kubectl describe hpa
Name:                                                  hello-world
Namespace:                                             default
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Wed, 01 Sep 2021 15:05:02 +0800
...
[root@master home]# kubectl delete hpa hello-world
horizontalpodautoscaler.autoscaling "hello-world" deleted
```

在不同版本的API中，HPA autoscale时可以根据以下指标来判断：

- autoscaling/v1
  - CPU
- autoscaling/v1alpha1
  - 内存
  - 自定义metrics
    - kubernetes1.6起支持自定义metrics，但是必须在kube-controller-manager中配置如下两项：
      - `--horizontal-pod-autoscaler-use-rest-clients=true`
      - `--api-server`指向[kube-aggregator](https://github.com/kubernetes/kube-aggregator)，也可以使用heapster来实现，通过在启动heapster的时候指定`--api-server=true`。查看[kubernetes metrics](https://github.com/kubernetes/metrics)
  - 多种metrics组合
    - HPA会根据每个metric的值计算出scale的值，并将最大的那个值作为扩容的最终结果。

设置自定义指标

```bash
# kubernetes1.6
在设置定义指标HPA之前需要先进行如下配置：

- 将heapster的启动参数 `--api-server` 设置为 true

- 启用custom metric API
- 将kube-controller-manager的启动参数中`--horizontal-pod-autoscaler-use-rest-clients`设置为true，并指定`--master`为API server地址，如`--master=http://172.20.0.113:8080`
# kuberentes1.7+
修改以下配置：
	将kube-controller-manager的启动参数中--horizontal-pod-autoscaler-use-rest-clients设置为true，并指定--master为API server地址，如--master=http://172.20.0.113:8080
	修改kube-apiserver的配置文件apiserver，增加一条配置--requestheader-client-ca-file=/etc/kubernetes/ssl/ca.pem --requestheader-allowed-names=aggregator --requestheader-extra-headers-prefix=X-Remote-Extra- --requestheader-group-headers=X-Remote-Group --requestheader-username-headers=X-Remote-User --proxy-client-cert-file=/etc/kubernetes/ssl/kubernetes.pem --proxy-client-key-file=/etc/kubernetes/ssl/kubernetes-key.pem，用来配置aggregator的CA证书。
```

## 四．服务发现与路由
