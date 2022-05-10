具有 AWS 管理控制台访问权限的用户可在以下位置登录: https://yldevops.signin.aws.amazon.com/console

用户：xuzc
访问密钥 ID：AKIAXTVISUCWOJKKOC6H 
私有访问密钥：zoP0JTK2YC2rD7oXQOSqi7u38Ce47HtrfMtRhCtq

用户:  xuzc
密码：au*-(@Hy#nYm8}^

1.下载安装

```shell
#https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-chap-welcome.html 
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
unzip awscliv2.zip 
sudo ./aws/install
```

2.配置

```shell
#https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-configure-quickstart.html
[root@yl4030-test home]# aws configure
AWS Access Key ID [None]: AKIAXTVISUCWOJKKOC6H
AWS Secret Access Key [None]: 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
Default region name [None]: eu-central-1
Default output format [None]: json
[root@yl4030-test ~]# aws eks --region eu-central-1 update-kubeconfig --name staging-eks-eu-central-1
Added new context arn:aws:eks:eu-central-1:523265810604:cluster/staging-eks-eu-central-1 to /root/.kube/config
[root@yl4030-test ~]# less /root/.kube/config
```

