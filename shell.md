```shell
#---------- 使k8s资源 Terminating
kubectl patch  pod xzc-busybox-1 -p '{"metadata":{"finalizers":["fip.cloud.yealink.com/finalizer"]}}' --type=merge
k delete pod xzc-busybox-1 #Terminating

kubectl patch  pod xzc-busybox-1 -p '{"metadata":{"finalizers":[]}}' --type=merge    #finalizers为空时删除

#---------- cpu测试
dd if=/dev/zero of=/dev/null &
top d1 -c 
uptime 
pkill -9 dd

#---------- 删除命名空间(Terminating)
(py3) ~ root(k8s: qa-europe | ns: monitorcenter)
# 
yum -y install jq
(py3) ~ root(k8s: qa-shanghai | ns: monitorcenter)
# 
(
NAMESPACE=monitorcenter
kubectl proxy &
kubectl get namespace $NAMESPACE -o json |jq '.spec = {"finalizers":[]}' >temp.json
curl -k -H "Content-Type: application/json" -X PUT --data-binary @temp.json 127.0.0.1:8001/api/v1/namespaces/$NAMESPACE/finalize
)

#---------- 端口映射
k port-forward service/thanos-query-global --address 0.0.0.0 80:10902
k port-forward pod/thanos-store-gateway-0  --address 0.0.0.0 :10902

#---------- 查看不为running状态的po
k  get po -A  --field-selector=status.phase!=Running

#---------- 防火墙
firewall-cmd --list-ports
firewall-cmd --zone=public  --add-port=9190/tcp --permanent 
firewall-cmd --zone=public  --remove-port=9190/tcp --permanent 
firewall-cmd --reload
iptables -A INPUT -p tcp –dport 22 -j ACCEPT

#---------- DNS
本地解析：
[root@node01 ~]# vim /etc/hosts
192.168.37.112 www.baidu.com 
[root@node01 ~]# ping www.baidu.com
64 bytes from www.baidu.com (192.168.37.112): icmp_seq=1 ttl=64 time=0.460 ms
DNS解析：
[root@node01 ~]# vim /etc/resolv.conf
nameserver 10.100.1.10   #在这里添加nameserver（从第一行开始解析）
nameserver 114.114.114.114
优先级：
[root@node01 ~]# vim /etc/nsswitch.conf
#hosts:     db files nisplus nis dns 
hosts:      dns files myhostname #files代表本地解析文件，dns代表dns服务器，哪个在前面哪个优先

#---------- ssh
ssh-keygen
ssh-copy-id root@10.120.25.126
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
免密登录：
cmd：“ssh-keygen -t rsa -b 4096”
SET REMOTEHOST=root@10.120.25.126
scp %USERPROFILE%\.ssh\id_rsa.pub %REMOTEHOST%:~/tmp.pub
ssh %REMOTEHOST% "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat ~/tmp.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && rm -f ~/tmp.pub"

#---------- 时间同步
yum -y install chrony #下载
systemctl start chronyd && systemctl enable chronyd #启动
chronyc sources #检测

#---------- conda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh   #官网安装
bash Miniconda3-latest-Linux-x86_64.sh #进入后根据提示安装（回车/yes）
conda create -n python3.6_ansible2.10 python=3.6  #创建python3虚拟环境  
安装环境
pip install ansible==2.10.4 \
kubernetes==11.0.0 \
openshift==0.11.2 \
passlib==1.7.4 \
kubernetes-validate==1.20.0
conda info --env #查看所有虚拟环境
conda activate python3.6_ansible2.10 #启动新建的虚拟环境
conda deactivate #关闭新建的虚拟环境
conda create --name python3（新名字） --clone python3.6_ansible2.10（老名字）
conda remove --name old_name --all

#---------- docker
yum install -y yum-utils
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum -y install docker-ce docker-ce-cli containerd.io
docker --version
systemctl start docker

#---------- k8s
kubelet
yum install -y kubelet-1.18.0 kubeadm-1.18.0 kubectl-1.18.0
systemctl enable kubelet

kubectx和kubens
wget https://raw.githubusercontent.com/ahmetb/kubectx/master/kubectx
wget https://raw.githubusercontent.com/ahmetb/kubectx/master/kubens
chmod +x kubectx kubens
sudo mv kubens kubectx /usr/local/bin

fzf
git clone --depth 1 https://github.com/junegunn/fzf.git && cd fzf/ && ./install
source ~/.bashrc

Kubectl autocomplete（自动补全）
source <(kubectl completion bash) 
echo "source <(kubectl completion bash)" >> ~/.bashrc 
#如果出现  -bash: _get_comp_words_by_ref: command not found
yum install bash-completion -y
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash) 

#---------- ansible
yum install epel-release -y
yum install ansible –y

#---------- aws
下载安装（https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-chap-welcome.html）
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
unzip awscliv2.zip 
sudo ./aws/install

配置（https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-configure-quickstart.html）
[root@yl4030-test home]# aws configure
AWS Access Key ID [None]: AKIAXTVISUCWOJKKOC6H
AWS Secret Access Key [None]: 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
Default region name [None]: eu-central-1
Default output format [None]: json
[root@yl4030-test ~]# aws eks --region eu-central-1 update-kubeconfig --name staging-eks-eu-central-1
Added new context arn:aws:eks:eu-central-1:523265810604:cluster/staging-eks-eu-central-1 to /root/.kube/config
[root@yl4030-test ~]# less /root/.kube/config

#---------- 命令行
~/.bashrc
iNORMAL="\[\033[00m\]"
BLUE="\[\033[01;34m\]"
YELLOW="\[\e[1;33m\]"
GREEN="\[\e[1;32m\]"

source /usr/local/src/kube提示/kube-prompt.sh

export PS1="${BLUE}\W ${GREEN}\u${YELLOW}\$(__kube_ps1)${NORMAL}\n"'\$ '
source <(kubectl completion bash)

alias dk=docker
complete -F _docker dk

alias k=kubectl
complete -F __start_kubectl k

#---------- kube-prompt.sh
#!/bin/bash
KUBE_PS1_NS_COLOR="${KUBE_PS1_NS_COLOR-cyan}"
KUBE_PS1_CONTEXT_COLOR="${KUBE_PS1_CONTEXT_COLOR-red}"
GIT_BRANCH_COLOR="${GIT_BRANCH_COLOR-yellow}"
KUBE_PS1_SHELL="bash"
_kube_ps1_init() {
      _KUBE_PS1_OPEN_ESC=$'\001'
      _KUBE_PS1_CLOSE_ESC=$'\002'
      _KUBE_PS1_DEFAULT_BG=$'\033[49m'
      _KUBE_PS1_DEFAULT_FG=$'\033[39m'
}

_kube_ps1_init


_kube_ps1_color_fg() {
  local KUBE_PS1_FG_CODE
  case "${1}" in
    black) KUBE_PS1_FG_CODE=0;;
    red) KUBE_PS1_FG_CODE=1;;
    green) KUBE_PS1_FG_CODE=2;;
    yellow) KUBE_PS1_FG_CODE=3;;
    blue) KUBE_PS1_FG_CODE=4;;
    magenta) KUBE_PS1_FG_CODE=5;;
    cyan) KUBE_PS1_FG_CODE=6;;
    white) KUBE_PS1_FG_CODE=7;;
    # 256
    [0-9]|[1-9][0-9]|[1][0-9][0-9]|[2][0-4][0-9]|[2][5][0-6]) KUBE_PS1_FG_CODE="${1}";;
    *) KUBE_PS1_FG_CODE=default
  esac

  if [[ "${KUBE_PS1_FG_CODE}" == "default" ]]; then
    KUBE_PS1_FG_CODE="${_KUBE_PS1_DEFAULT_FG}"
    return
  elif [[ "${KUBE_PS1_SHELL}" == "zsh" ]]; then
    KUBE_PS1_FG_CODE="%F{$KUBE_PS1_FG_CODE}"
  elif [[ "${KUBE_PS1_SHELL}" == "bash" ]]; then
    if tput setaf 1 &> /dev/null; then
      KUBE_PS1_FG_CODE="$(tput setaf ${KUBE_PS1_FG_CODE})"
    elif [[ $KUBE_PS1_FG_CODE -ge 0 ]] && [[ $KUBE_PS1_FG_CODE -le 256 ]]; then
      KUBE_PS1_FG_CODE="\033[38;5;${KUBE_PS1_FG_CODE}m"
    else
      KUBE_PS1_FG_CODE="${_KUBE_PS1_DEFAULT_FG}"
    fi
  fi
  echo ${_KUBE_PS1_OPEN_ESC}${KUBE_PS1_FG_CODE}${_KUBE_PS1_CLOSE_ESC}
}

_kube_ps1_color_bg() {
  local KUBE_PS1_BG_CODE
  case "${1}" in
    black) KUBE_PS1_BG_CODE=0;;
    red) KUBE_PS1_BG_CODE=1;;
    green) KUBE_PS1_BG_CODE=2;;
    yellow) KUBE_PS1_BG_CODE=3;;
    blue) KUBE_PS1_BG_CODE=4;;
    magenta) KUBE_PS1_BG_CODE=5;;
    cyan) KUBE_PS1_BG_CODE=6;;
    white) KUBE_PS1_BG_CODE=7;;
    # 256
    [0-9]|[1-9][0-9]|[1][0-9][0-9]|[2][0-4][0-9]|[2][5][0-6]) KUBE_PS1_BG_CODE="${1}";;
    *) KUBE_PS1_BG_CODE=$'\033[0m';;
  esac

  if [[ "${KUBE_PS1_BG_CODE}" == "default" ]]; then
    KUBE_PS1_FG_CODE="${_KUBE_PS1_DEFAULT_BG}"
    return
  elif [[ "${KUBE_PS1_SHELL}" == "zsh" ]]; then
    KUBE_PS1_BG_CODE="%K{$KUBE_PS1_BG_CODE}"
  elif [[ "${KUBE_PS1_SHELL}" == "bash" ]]; then
    if tput setaf 1 &> /dev/null; then
      KUBE_PS1_BG_CODE="$(tput setab ${KUBE_PS1_BG_CODE})"
    elif [[ $KUBE_PS1_BG_CODE -ge 0 ]] && [[ $KUBE_PS1_BG_CODE -le 256 ]]; then
      KUBE_PS1_BG_CODE="\033[48;5;${KUBE_PS1_BG_CODE}m"
    else
      KUBE_PS1_BG_CODE="${DEFAULT_BG}"
    fi
  fi
  echo ${OPEN_ESC}${KUBE_PS1_BG_CODE}${CLOSE_ESC}
}

__kube_ps1()
{
    # Get current context
#    CONTEXT=$(cat ~/.kube/config | grep "current-context:" | sed "s/current-context: //")
    KUBE_PS1=""
    NAMESPACE=$(kubectl config view --minify --output 'jsonpath={..namespace}' 2>/dev/null)
    CONTEXT=$(kubectl config current-context)
    #GIT_BRANCH=$(git describe --contains --all HEAD 2>/dev/null)
    GIT_BRANCH=$(git symbolic-ref HEAD 2>/dev/null  | cut -d/ -f3) 
   if [ -n "$CONTEXT" ]; then
        #echo "(k8s: ${CONTEXT})"
        KUBE_PS1+="$(_kube_ps1_color_fg ${KUBE_PS1_CONTEXT_COLOR})k8s: ${CONTEXT}"
    fi
    if [ -n "${NAMESPACE}" ];then
       KUBE_PS1+=" |$(_kube_ps1_color_fg ${KUBE_PS1_NS_COLOR}) ns: ${NAMESPACE}${KUBE_PS1_RESET_COLOR}"
    fi
   
    if [ -n "${GIT_BRANCH}" ];then
       KUBE_PS1+=" |$(_kube_ps1_color_fg ${GIT_BRANCH_COLOR}) git: ${GIT_BRANCH}${KUBE_PS1_RESET_COLOR}"
    fi
    echo -e "(${KUBE_PS1})"
}

```

