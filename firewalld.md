详细链接：https://juejin.cn/post/6844903865146425351

# firewalld

## 1. 查看防火墙状态

```
systemctl status firewalld
```

## 2. 开启防火墙

```shell
systemctl start firewalld
(py3) ~ root(k8s: devops-intranet-prod | ns: monitorcenter)# systemctl start firewalld
Failed to start firewalld.service: Unit is masked.
(py3) ~ root(k8s: devops-intranet-prod | ns: monitorcenter)# systemctl unmask firewalld.service
Removed symlink /etc/systemd/system/firewalld.service.
```

## 3. 停止防火墙

```shell
systemctl stop firewalld
```

## 4. 重启防火墙

```shell
systemctl restart firewalld
```

## 5. 查看防火墙开放端口

```shell
firewall-cmd --list-ports
```

## 6. 开放端口

**（开放后需要要重启防火墙才生效）**

```shell
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=8888/tcp --permanent
iptables -A INPUT -p tcp –dport 22 -j ACCEPT
```

## 7. 关闭端口

**（关闭后需要要重启防火墙才生效）**

```shell
firewall-cmd --zone=public --remove-port=80/tcp --permanent
firewall-cmd --zone=public --remove-port=8080/tcp --permanent
```

## 8.设置开机启动

```shell
systemctl enable firewalld
```

## 9.禁用开机启动

```shell
systemctl disable firewalld
```

## 10.重启防火墙

```shell
firewall-cmd --reload
```

