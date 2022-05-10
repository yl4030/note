# Docker容器技术

### 1.Docker概述

Docker的官方文档内容很全面：https://docs.docker.com/

#### 1.Docker和虚拟机的区别

- 传统虚拟机：虚拟出一套硬件，运行完整的操作系统。
- Docker：直接应用宿主机的内核，也不需要虚拟硬件，每个容器互相隔离。

#### 2.Docker的作用

- 更快的交付和部署
- 更便捷升级和扩缩容
- 更简单的系统运维
- 更高效的资源利用

#### 3.Docker的基本组成

![img](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimage.mamicode.com%2Finfo%2F201807%2F20180715122259940087.png&refer=http%3A%2F%2Fimage.mamicode.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1630025712&t=83094c562fe2c19bad519ae44397dae2)

- 镜像：Docker 镜像（Image），就相当于是一个 root 文件系统。比如官方镜像 ubuntu:16.04 就包含了完整的一套 Ubuntu16.04 最小系统的 root 文件系统。类似项目的映像，可以通过镜像来创建容器服务，镜像-->run-->容器（提供服务）
- 容器：镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中的类和实例一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。
- 仓库：可看成一个代码控制中心，用来保存镜像。

#### 4.Docker安装

Centos安装：https://docs.docker.com/engine/install/centos/

##### 1.删除旧版本

```bash
 sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

##### 2.从远程仓库安装

```bash
sudo yum install -y yum-utils
 sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

##### 3.安装docker引擎

```bash
 sudo yum install docker-ce docker-ce-cli containerd.io
```

##### 4.启动docker

```bash
sudo systemctl start docker					#启动docker
sudo systemctl stop docker 					#停止dockers
sudo systemctl restart docker				#重启docker
```

##### 5.卸载docker

```bash
#1. 卸载依赖
yum remove docker-ce docker-ce-cli containerd.io
#2. 删除资源
rm -rf /var/lib/docker
# /var/lib/docker 是docker的默认工作路径！
```

##### 6.配置镜像加速

配置阿里云镜像加速：https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors

##### 7.Docker底层原理

Docker是怎么工作的？

Docker是一个Client-Server结构的系统，Docker的守护进程运行在主机上。通过Socket从客户端访 问！ Docker-Server接收到Docker-Client的指令，就会执行这个命令！

==Docker为什么比VM快==

1、docker有着比虚拟机更少的抽象层。由于docker不需要Hypervisor实现硬件资源虚拟化,运行在 docker容器上的程序直接使用的都是实际物理机的硬件资源。因此在CPU、内存利用率上docker将会在 效率上有明显优势。

 2、docker利用的是宿主机的内核,而不需要Guest OS。 GuestOS： VM（虚拟机）里的的系统（OS）; HostOS：物理机里的系统（OS）；

![img](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimage.520mwx.com%2Fstatic%2F60e7b4fe44f90880e58d3c32db2eb38d.png&refer=http%3A%2F%2Fimage.520mwx.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1630027942&t=9a742f1ee92d287f6196eaa15add2b5f)

因此,当新建一个 容器时，docker不需要和虚拟机一样重新加载一个操作系统内核。然而避免引导、加 载操作系统内核是个比较费时费资源的过程，当新建一个虚拟机时，虚拟机软件需要加载GuestOS，返 个新建过程是分钟级别的。而docker由于直接利用宿主机的操作系统,则省略了这个复杂的过程，因此 新建一个docker容器只需要几秒钟。

### 2.Docker命令

Docker的官方文档有所有命令的详细介绍：https://docs.docker.com/engine/reference/run/

#### 1.帮助命令

```bash
docker version				#显示docker版本
docker info					#显示docker的系统信息
docker [op] --help			#查看命令帮助文档
```

#### 2.镜像命令

```bash
docker images						#查看主机镜像
docker search [images]				#从docker-hub上查找镜像
docker pull [images]				#从docker-hub上拉取镜像
docker rmi [images]					#删除镜像
```

**docker images** 查看镜像

```bash
[root@Curry czb]# docker images
REPOSITORY                                            TAG          IMAGE ID       CREATED        SIZE
comtest_web                                           latest       6641d00fb2ed   8 days ago     53.6MB
composetest_web                                       latest       1d64be41014c   8 days ago     197MB
testcentos                                            1.0          dd8d97b28202   8 days ago     299MB
mytomcat                                              latest       ea1f9a1a040f   2 weeks ago    648MB
registry.cn-hangzhou.aliyuncs.com/chenzb/chenzb1017   1.0          ea1f9a1a040f   2 weeks ago    648MB
chenzb/mytomcat                                       1.0          ea1f9a1a040f   2 weeks ago    648MB
testos                                                1.0          fa84387658d0   2 weeks ago    209MB
nginx                                                 <none>       4cdc5dd7eaad   3 weeks ago    133MB
redis                                                 alpine       500703a12fa4   3 weeks ago    32.3MB
tomcat                                                latest       36ef696ea43d   3 weeks ago    667MB
wordpress                                             latest       b77ea6f8ecf7   3 weeks ago    551MB
python                                                3.6-alpine   e5d44943603f   4 weeks ago    40.8MB
python                                                3.7-alpine   93ac4b41defe   4 weeks ago    41.9MB
mysql                                                 <none>       09361feeb475   4 weeks ago    447MB
centos                                                latest       300e315adb2f   7 months ago   209MB
#解释
#REPOSITORY # 镜像的仓库源
#TAG # 镜像的标签
#IMAGE ID # 镜像的id
#CREATED # 镜像的创建时间
#SIZE # 镜像的大小
# 可选项
Options:
-a, --all Show all images (default hides intermediate images) #列出
所有镜像
-q, --quiet Only show numeric IDs # 只显示镜像的id

[root@Curry czb]# docker images -aq			 ＃显示所有镜像的id
6641d00fb2ed
a5501991e944
0a7fa653f871
7284c78f38b9
1d64be41014c
f285b7fdfa85
c0b5965648b1
```

**docker pull** 下载镜像

```bash
#下载镜像 docker pull 镜像名[:tag]   tag表示版本，默认为latest
```

**docker rmi** 删除镜像

```bash
#删除相同id的镜像时，要使用tag标签，并附上版本号信息 eg：docker rmi -f tag标签：TAG
docker rmi -f 镜像id 							  #删除指定的镜像
docker rmi -f 镜像id 镜像id 镜像id 镜像id		 #删除指定的镜像
docker rmi -f $(docker images -aq) 				#删除全部的镜像
```

#### 3.容器命令

常用命令：

```bash
docker run 镜像id  		  		#新建容器并启动
docker ps						  #列出所有运行的容器 docker container list
docker rm 容器id 					#删除指定容器
docker start 容器id 				#启动容器
docker restart容器id 				#重启容器
docker stop 容器id 				#停止当前正在运行的容器
docker kill 容器id 				#强制停止当前容器
```

查看容器命令：

```bash
Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  inspect     Display detailed information on one or more containers
  kill        Kill one or more running containers
  logs        Fetch the logs of a container
  ls          List containers
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  prune       Remove all stopped containers
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  run         Run a command in a new container
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes

Run 'docker container COMMAND --help' for more information on a command.
```

##### 运行容器

```bash
docker run [可选参数] image 
#参数说明
--name="Name" 			#容器名字 tomcat01 tomcat02 用来区分容器
-d 						#后台方式运行
-it 					#使用交互方式运行，进入容器查看内容
-p 						#指定容器的端口 -p 8080(宿主机):8080(容器)
	-p ip:主机端口:容器端口
	-p 主机端口:容器端口(常用)
	-p 容器端口：容器端口
-P(大写) 				  #随机指定端口
-v						#挂载数据卷
		-v 容器内路径 					  		#匿名挂载
		-v 卷名：容器内路径 					  #具名挂载
		-v /宿主机路径：容器内路径 			   #指定路径挂载 docker volume ls 是查看不到的
-e 
```

##### 查看容器

```bash
docker ps [OPTIONS]
#参数说明
--all , -a				#Show all containers (default shows just running)
--filter , -f			#Filter output based on conditions provided
--format				#Pretty-print containers using a Go template
--last , -n	-1			#Show n last created containers (includes all states)
--latest , -l			#Show the latest created container (includes all states)
--no-trunc				#Don't truncate output
--quiet , -q			#Only display container IDs
--size , -s				#Display total file sizes
```

##### 退出容器

```bash
#第一种办法
exit		#进入容器后，exit退出，容器停止
#第二种方法
ctrl+q+p	#进入容器后，同时按下ctrl+q+p，容器不停止退出
```

##### 删除容器

```bash
docker rm 容器id 					   #删除指定的容器，不能删除正在运行的容器，如果要强制删除 rm -rf
docker rm -f $(docker ps -aq) 		#删除指定的容器
docker ps -a -q|xargs docker rm 	#删除所有的容器
```

##### 容器操作

```bash
docker start 容器id 				#启动容器
docker restart 容器id 			#重启容器
docker stop 容器id 				#停止当前正在运行的容器
docker kill 容器id 				#强制停止当前容器
```

##### 查看容器内进程信息

```bash
docker top 容器id
```

##### 查看镜像的详细信息

```bash
docker inspect 容器id
```

##### 进入容器

```bash
#第一种方法 exec进入容器开启一个新的终端
docker exec -it 容器id /bin/bash
#第二种方法 attach 进入容器正在执行的终端
docker attach 容器id
```

##### 从容器内拷贝文件到主机

```bash
docker cp 容器id:容器内路径 主机目的路径
```

#### 4.其他命令

##### 查看日志

```bash
[root@localhost ~]# docker logs --help

Usage:  docker logs [OPTIONS] CONTAINER

Fetch the logs of a container

Options:
      --details        Show extra details provided to logs
  -f, --follow         Follow log output
      --since string   Show logs since timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)
  -n, --tail string    Number of lines to show from the end of the logs (default "all")
  -t, --timestamps     Show timestamps
      --until string   Show logs before a timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)
```

#### docker命令大全

![img](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fupload-images.jianshu.io%2Fupload_images%2F3407216-793f99f91ef5e76f.png&refer=http%3A%2F%2Fupload-images.jianshu.io&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1630033576&t=a2193956ce1b11ad4a18fc54ed03844e)

### 3.Docker镜像

- 镜像是什么

镜像是一种轻量级、可执行的独立软件包，用来打包软件运行环境和基于运行环境开发的软件，他包含运行某 个软件所需的所有内容，包括**代码、运行时库、环境变量和配置文件**。 将所有的应用和环境，直接打包为docker镜像，就可以直接运行。

#### 1.Docker镜像加载原理

- UnionFs （联合文件系统）

```
UnionFs（联合文件系统）：Union文件系统（UnionFs）是一种分层、轻量级并且高性能的文件系统，他支 持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下（ unite several directories into a single virtual filesystem)。Union文件系统是 Docker镜像的基础。镜像可以通过分层来进行继承，基于基础镜像（没有父镜像），可以制作各种具体的应 用镜像。
```

- Docker 镜像加载原理

```
docker的镜像实际上由一层一层的文件系统组成，这种层级的文件系统UnionFS。
boot file system （bootfs）：包含操作系统bootloader和kernel。bootloader主要是引导加 kernel,Linux刚启动时会加bootfs文件系统，在 Docker镜像的最底层是 boots。这一层与我们典型的Linux/Unix系统是一样的，包含boot加載器和内核。当boot加载完成之后整个内核就都在内存中了，此时内存的使用权已由 bootfs转交给内核，此时系统也会卸载bootfs。

root file system （rootfs）：包含典型的目录结构，包括 /dev, /proc, /bin, /etc, /lib, /usr, and /tmp
rootfs就是各种不同的操作系统发行版，比如 Ubuntu,Centos等等。

对于精简的OS，rootfs可以很小，只需要包合最基本的命令，工具和程序库就可以了，因为底层直接用Host的kernel，自己只需要提供rootfs就可以了。由此可见对于不同的Linux发行版， boots基本是一致的， rootfs会有差別，因此不同的发行版可以公用bootfs。所以镜像就可以只包含OS的rootfs文件，文件很小，所以启动容器速度会很快。
```

#### 2.Docker分层

```bash
#从官网拉取一个镜像
[root@Curry ~]# docker pull nginx
Using default tag: latest
latest: Pulling from library/nginx
33847f680f63: Pull complete 
dbb907d5159d: Pull complete 
8a268f30c42a: Pull complete 
b10cf527a02d: Pull complete 
c90b090c213b: Pull complete 
1f41b2f2bf94: Pull complete 
Digest: sha256:8f335768880da6baf72b70c701002b45f4932acae8d574dedfddaf967fc3ac90
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest
```

可以看到，Docker镜像下载时是一层一层的下载的

```bash
33847f680f63: Pull complete 
dbb907d5159d: Pull complete 
8a268f30c42a: Pull complete 
b10cf527a02d: Pull complete 
c90b090c213b: Pull complete 
1f41b2f2bf94: Pull complete 
```

最大的好处，我觉得莫过于资源共享了！比如有多个镜像都从相同的Base镜像构建而来，那么宿主机 只需在磁盘上保留一份base镜像，同时内存中也只需要加载一份base镜像，这样就可以为所有的容器 服务了，而且镜像的每一层都可以被共享。

所有的 Docker镜像都起始于一个基础镜像层，当进行修改或培加新的内容时，就会在当前镜像层之 上，创建新的镜像层。 举一个简单的例子，假如基于 Ubuntu Linux16.04创建一个新的镜像，这就是新镜像的第一层；如果在 该镜像中添加 Python包， 就会在基础镜像层之上创建第二个镜像层；如果继续添加一个安全补丁，就会创健第三个镜像层该像当 前已经包含3个镜像层，如下图所示（这只是一个用于演示的很简单的例子）。

![image-20210728114100207](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210728114100207.png)

在添加额外的镜像层的同时，镜像始终保持是当前所有镜像的组合，理解这一点非常重要。下图中举了 一个简单的例子，每个镜像层包含3个文件，而镜像包含了来自两个镜像层的6个文件。

![image-20210728114129141](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210728114129141.png)

上图中的镜像层跟之前图中的略有区別，主要目的是便于展示文件 下图中展示了一个稍微复杂的三层镜像，在外部看来整个镜像只有6个文件，这是因为最上层中的文件7 是文件5的一个更新版文种情況下，上层镜像层中的文件覆盖了底层镜像层中的文件。这样就使得文件的更新版本作为一个新镜像层添加到镜像当中。

![image-20210728132554331](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210728132554331.png)

Docker通过存储引擎（新版本采用快照机制）的方式来实现镜像层堆栈，并保证多镜像层对外展示为统 一的文件系统。Linux上可用的存储引撃有AUFS、 Overlay2、 Device Mapper、Btrfs以及ZFS。顾名思义，每种存储引擎都基于 Linux中对应的文件系统或者块设备技术，井且每种存储引擎都有其独有的性能特点。 Docker在 Windows上仅支持 windowsfilter一种存储引擎，该引擎基NTFS文件系统之上实现了分层和CoW [1]。 下图展示了与系统显示相同的三层镜像。所有镜像层堆并合井，对外提供统一的视图。

![image-20210728133114623](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210728133114623.png)

Docker 镜像都是只读的，当容器启动时，一个新的可写层加载到镜像的顶部。这一层就是我们通常说的容器层，容器之下的都叫镜像层！

#### 3.修改提交镜像

```bash
docker commit			#提交容器成为一个新的副本
docker commit -m="描述信息" -a="作者" 容器id 目标镜像名：[TAG]
```

范例：

```shell
#从docker-hub上pull一个centos的镜像
[root@Curry ~]# docker pull centos
Using default tag: latest
latest: Pulling from library/centos
7a0437f04f83: Pull complete 
Digest: sha256:5528e8b1b1719d34604c87e11dcd1c0a20bedf46e83b5632cdeac91b8c04efc1
Status: Downloaded newer image for centos:latest
docker.io/library/centos:latest
[root@Curry ~]# docker images
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    08b152afcfae   5 days ago     133MB
centos       latest    300e315adb2f   7 months ago   209MB
#创建镜像并且进入镜像
[root@Curry ~]# docker run -it --name mycentos centos /bin/bash
#该镜像是最简版本，缺乏很多功能
[root@d4bd058e5a1f /]# clear                                          
bash: clear: command not found
[root@d4bd058e5a1f /]# vim
bash: vim: command not found
#下载创建相关服务，创建一个比较完全的OS
[root@d4bd058e5a1f /]# yum -y install ncurses			#安装clear功能
[root@d4bd058e5a1f /]# yum install vim					#安装vim
[root@d4bd058e5a1f /]# yum install tree					#安装tree
[root@d4bd058e5a1f /]# yum-config-manager \    			#安装docker
>     --add-repo \
>     https://download.docker.com/linux/centos/docker-ce.repo
Failed to set locale, defaulting to C.UTF-8
Adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
[root@d4bd058e5a1f /]# yum install docker-ce docker-ce-cli containerd.io
[root@d4bd058e5a1f home]# vim commitmsg.txt				#保留测试信息
[root@d4bd058e5a1f home]# cat commitmsg.txt 
I can do all things


------------------------
#提交镜像
[root@Curry ~]# docker commit -m="my test centos" -a="chenzb" d4bd058e5a1f testcentos:1.0
sha256:037bc29a99d2b8409c48dea2bb8428b6699193d2ec5c8fe2f82d2f4d37ca793d
[root@Curry ~]# docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
testcentos   1.0       037bc29a99d2   12 seconds ago   797MB
nginx        latest    08b152afcfae   5 days ago       133MB
centos       latest    300e315adb2f   7 months ago     209MB
[root@Curry ~]# docker inspect testcentos:1.0			#查看镜像相关信息
[
    {
        "Id": "sha256:037bc29a99d2b8409c48dea2bb8428b6699193d2ec5c8fe2f82d2f4d37ca793d",
        "RepoTags": [
            "testcentos:1.0"
        ],
        "DockerVersion": "20.10.7",
        "Author": "chenzb",
        "Metadata": {
            "LastTagTime": "2021-07-28T17:08:05.509207807+08:00"
        }
    }
]
```



### 4.Dcoker数据卷

#### 1.什么是数据卷

容器之间可以有一个数据共享的技术！Docker容器中产生的数据，同步到本地！ 这就是卷技术！目录的挂载，将我们容器内的目录，挂载到Linux上面！

#### 2.使用数据卷

- 方式一：在启动容器时，通过参数-v挂载

```bash
docker run -it -v 主机目录:容器内目录 -p 主机端口:容器内端口

[root@localhost ~]# docker run -d -it --name centos1 -v /home/roo/test:/home centos /bin/bash
755a585b1f5008b12b4869329725e36b4931dd0c0e737feb0bb5623f0436411f

[root@localhost ~]# docker inspect centos1
        "Mounts": [
            {
                "Type": "bind",
                "Source": "/home/roo",
                "Destination": "/home",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            }

```

查看文件同步：

![image-20210728143718540](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210728143718540.png)



```shell
#测试：
#1. 停止容器
#2. 宿主机修改文件
#3. 再启动容器
#4. 查看容器内文件信息

[root@26200e85e4e8 home]# ls -la
total 4
drwxr-xr-x. 2 root root 70 Jul 28 07:10 .
drwxr-xr-x. 1 root root 62 Jul 28 06:28 ..
-rw-r--r--. 1 root root 21 Jul 28 07:10 guazaiceshi.aqa
-rw-r--r--. 1 root root  0 Jul 28 06:30 guazaiceshi.qaq
-rw-r--r--. 1 root root  0 Jul 28 06:36 hhhhhh.com
[root@26200e85e4e8 home]# cat guazaiceshi.aqa 
I can do all things
```

发现宿主机上做出的修改即使停止容器也能使用,保证了数据的实时和同步。

![image-20210728151337352](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210728151337352.png)

```bash
#测试：将容器删除，查看数据卷是否还存在

[root@localhost test]# ls
guazaiceshi.aqa  guazaiceshi.qaq  hhhhhh.com
[root@localhost test]# docker ps
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS          PORTS     NAMES
26200e85e4e8   centos    "/bin/bash"   53 minutes ago   Up 11 minutes             centos1
[root@localhost test]# docker rm -f 26200e85e4e8
26200e85e4e8
[root@localhost test]# docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@localhost test]# ls
guazaiceshi.aqa  guazaiceshi.qaq  hhhhhh.com

###发现数据还是存在，没有丢失，这就实现了容器数据的持久化
```

#### 3.具名挂载和匿名挂载

```bash
#匿名挂载
[root@localhost test]# docker run -d -P --name niming -v /etc/nginx nginx
[root@localhost test]# docker volume ls
DRIVER    VOLUME NAME
local     88ad4785c5b013cf52d78cd64953a12574855a1dba00eb2e9d24ed5494445345
#这里发现，这种就是匿名挂载，我们在 -v只写了容器内的路径，没有写容器外的路径！
#具名挂载
[root@localhost test]# docker run -d -P --name jumingming -v juming:/etc/nginx nginx
b63acd756f10bb2d0d16c5edc3987c633ddc7a84832aa2b6e1ecfbb08d257b38
[root@localhost test]# docker volume ls
DRIVER    VOLUME NAME
local     88ad4785c5b013cf52d78cd64953a12574855a1dba00eb2e9d24ed5494445345
local     juming
#指定目录挂载
[root@localhost test]# docker run -d -P --name zhiding -v /home/roo/guazai_test:/etc/nginx nginx
68d8d61c3fa1789475ec9500967c304b5ef3bd6eae33f3e34bcf41f42feaf0aa
[root@localhost test]# docker volume list                       #volume list查看不到挂载路径，默认查看/var/lib/docker/volumes/xxxx/_data 下
DRIVER    VOLUME NAME
local     88ad4785c5b013cf52d78cd64953a12574855a1dba00eb2e9d24ed5494445345
local     juming
[root@localhost test]# docker inspect zhiding
        "Mounts": [
            {
                "Type": "bind",
                "Source": "/home/roo/guazai_test",
                "Destination": "/etc/nginx",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            }
        ],
```

所有的docker容器内的卷，没有指定目录的情况下都是在 /var/lib/docker/volumes/xxxx/_data 下 如果指定了目录，docker volume ls 是查看不到的。

拓展：

```bash
# 通过 -v 容器内路径： ro rw 改变读写权限
ro #readonly 只读
rw #readwrite 可读可写
docker run -d -P --name nginx05 -v juming:/etc/nginx:ro nginx
docker run -d -P --name nginx05 -v juming:/etc/nginx:rw nginx
# ro 只要看到ro就说明这个路径只能通过宿主机来操作，容器内部是无法操作！
```

#### 4.数据卷容器

多个容器之间相互挂载数据卷

![image-20210728155326774](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210728155326774.png)



### 5.Dockerfile

#### 1.Dockerfile概述

Dockerfile就是用来构建docker镜像的构建文件、命令脚本。

#### 2.Dokcerfile 构建过程

##### 基础知识：

1. 每个保留关键字(指令）都是必须是大写字母 
2. 执行从上到下顺序 
3. #表示注释 
4. 每一个指令都会创建提交一个新的镜像层，并提交！

![image-20210729084958482](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210729084958482.png)

##### 常见指令

```bash
#FROM:指定基础镜像，必须为第一个命令
#格式：
	FROM <image>
　　FROM <image>:<tag>
　　FROM <image>@<digest>
#示例：
　　FROM mysql:5.6	

#MAINTAINER:维护者信息
#格式：
    MAINTAINER <name>
#示例：
    MAINTAINER Jasper Xu
    MAINTAINER sorex@163.com
    MAINTAINER Jasper Xu <sorex@163.com>
    
#RUN：构建镜像时执行的命令，有两种方式
#shell执行
#格式：
    RUN <command>
exec执行
#格式：
    RUN ["executable", "param1", "param2"]
#示例：
    RUN ["executable", "param1", "param2"]
    RUN apk update
    RUN ["/etc/execfile", "arg1", "arg1"]
#注：RUN指令创建的中间镜像会被缓存，并会在下次构建中使用。如果不想使用这些缓存镜像，可以在构建时指定--no-cache参数，如：docker build --no-cache

#ADD:将本地文件添加到容器中，tar类型文件会自动解压，可以访问网络资源。
#格式：
    ADD <src>... <dest>
    ADD ["<src>",... "<dest>"] 用于支持包含空格的路径
#示例：
    ADD hom* /mydir/          # 添加所有以"hom"开头的文件
    ADD hom?.txt /mydir/      # ? 替代一个单字符,例如："home.txt"
    ADD test relativeDir/     # 添加 "test" 到 `WORKDIR`/relativeDir/
    ADD test /absoluteDir/    # 添加 "test" 到 /absoluteDir/
    
#COPY：功能类似ADD，但是不会解压文件

#CMD：构建容器后调用，也就是在容器启动时才进行调用只执行最后一条
#格式：
    CMD ["executable","param1","param2"] (执行可执行文件，优先)
    CMD ["param1","param2"] (设置了ENTRYPOINT，则直接调用ENTRYPOINT添加参数)
    CMD command param1 param2 (执行shell内部命令)
#示例：
    CMD echo "This is a test." | wc -
    CMD ["/usr/bin/wc","--help"]
#注：CMD不同于RUN，CMD用于指定在容器启动时所要执行的命令，而RUN用于指定镜像构建时所要执行的命令。
    
#ENTRYPOINT：配置容器，使其可执行化。配合CMD可省去"application"，只使用参数
#格式：
    ENTRYPOINT ["executable", "param1", "param2"] (可执行文件, 优先)
    ENTRYPOINT command param1 param2 (shell内部命令)
#示例：
    FROM ubuntu
    ENTRYPOINT ["top", "-b"]
    CMD ["-c"]
#注：ENTRYPOINT与CMD非常类似，不同的是通过docker run执行的命令不会覆盖ENTRYPOINT，而docker run命令中指定的任何参数，都会被当做参数再次传递给ENTRYPOINT。Dockerfile中只允许有一个ENTRYPOINT命令，多指定时会覆盖前面的设置，而只执行最后的ENTRYPOINT指令。

#LABEL：用于为镜像添加元数据
#格式：
    LABEL <key>=<value> <key>=<value> <key>=<value> ...
#示例：
　　LABEL version="1.0" description="这是一个Web服务器" by="IT笔录"
#注：使用LABEL指定元数据时，一条LABEL指定可以指定一或多条元数据，指定多条元数据时不同元数据之间通过空格分隔。推荐将所有的元数据通过一条LABEL指令指定，以免生成过多的中间镜像。
　　
#ENV：设置环境变量
#格式：
    ENV <key> <value>  #<key>之后的所有内容均会被视为其<value>的组成部分，因此，一次只能设置一个变量
    ENV <key>=<value> ...  #可以设置多个变量，每个变量为一个"<key>=<value>"的键值对，如果<key>中包含空格，可以使用\来进行转义，也可以通过""来进行标示；另外，反斜线也可以用于续行
#示例：
    ENV myName John Doe
    ENV myDog Rex The Dog
    ENV myCat=fluffy

#EXPOSE：指定于外界交互的端口
#格式：
    EXPOSE <port> [<port>...]
#示例：
    EXPOSE 80 443
    EXPOSE 8080    EXPOSE 11211/tcp 11211/udp
#注：EXPOSE并不会让容器的端口访问到主机。要使其可访问，需要在docker run运行容器时通过-p来发布这些端口，或通过-P参数来发布EXPOSE导出的所有端口

#VOLUME：用于指定持久化目录，挂载目录
#格式：
    VOLUME ["/path/to/dir"]
#示例：
    VOLUME ["/data"]
    VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
#注：一个卷可以存在于一个或多个容器的指定目录，该目录可以绕过联合文件系统，并具有以下功能：
1.卷可以容器间共享和重用
2.容器并不一定要和其它容器共享卷
3.修改卷后会立即生效
4.对卷的修改不会对镜像产生影响
5.卷会一直存在，直到没有任何容器在使用它

#WORKDIR：工作目录，类似于cd命令
#格式：
    WORKDIR /path/to/workdir
#示例：
    WORKDIR /a  (这时工作目录为/a)
    WORKDIR b  (这时工作目录为/a/b)
    WORKDIR c  (这时工作目录为/a/b/c)
#注：通过WORKDIR设置工作目录后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT、ADD、COPY等命令都会在该目录下执行。在使用docker run运行容器时，可以通过-w参数覆盖构建时所设置的工作目录。

#USER:指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户。使用USER指定用户时，可以使用用户名、UID或GID，或是两者的组合。当服务不需要管理员权限时，可以通过该命令指定运行用户。并且可以在之前创建所需要的用户
#格式:
　　USER user
　　USER user:group
　　USER uid
　　USER uid:gid
　　USER user:gid
　　USER uid:group
#示例：
　　USER www
#注：使用USER指定用户后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT都将使用该用户。镜像构建完成后，通过docker run运行容器时，可以通过-u参数来覆盖所指定的用户。

#ARG：用于指定传递给构建运行时的变量
#格式：
    ARG <name>[=<default value>]
#示例：
    ARG site
    ARG build_user=www

#ONBUILD：用于设置镜像触发器
#格式：
　　ONBUILD [INSTRUCTION]
#示例：
　　ONBUILD ADD . /app/src
　　ONBUILD RUN /usr/local/bin/python-build --dir /app/src
#注：当所构建的镜像被用做其它镜像的基础镜像，该镜像中的触发器将会被钥触发
```

范例：

```bash
#first_dockerfile 					#体现了分层的思想，每条命令就是一层
FROM centos

VOLUME [" volume01 "," volume02 "]

CMD echo "================I can do all things=============="
CMD /bin/bash

[root@localhost test]# docker build -t first_dockerfile:2.0 ./first_dockerfile  .
"docker build" requires exactly 1 argument.
See 'docker build --help'.

Usage:  docker build [OPTIONS] PATH | URL | -

Build an image from a Dockerfile

###命令 docker build -f 文件路径 -t 镜像名:[tag] .        通过指定文件创建镜像 
###若没有-f文件路径的话，默认找当前文件夹下的Dockerfile文件
[root@localhost test]# docker build -t first_dockerfile:2.0 -f ./first_dockerfile  .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM centos
 ---> 300e315adb2f
Step 2/4 : VOLUME [" volume01 "," volume02 "]
 ---> Using cache
 ---> 9bf24c32af66
Step 3/4 : CMD echo "================I can do all things=============="
 ---> Using cache
 ---> 9920c4b5112a
Step 4/4 : CMD /bin/bash
 ---> Using cache
 ---> c97e09ae0bcf
Successfully built c97e09ae0bcf
Successfully tagged first_dockerfile:2.0

[root@localhost test]# docker images
REPOSITORY         TAG       IMAGE ID       CREATED         SIZE
first_dockerfile   1.0       c97e09ae0bcf   2 minutes ago   209MB
first_dockerfile   2.0       c97e09ae0bcf   2 minutes ago   209MB

```

#### 3.发布镜像

```bash
#登录docker-hub
[root@Curry home]# docker login --help
Usage:  docker login [OPTIONS] [SERVER]
Log in to a Docker registry.
If no server is specified, the default is defined by the daemon.
Options:
  -p, --password string   Password
      --password-stdin    Take the password from stdin
  -u, --username string   Username
[root@Curry home]# docker login -u chenzb1017 
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[root@localhost test]# docker tag c97e09ae0bcf chenzb/myfirst_dockerfile:1.0
[root@localhost test]# docker images
REPOSITORY                  TAG       IMAGE ID       CREATED        SIZE
chenzb/myfirst_dockerfile   1.0       c97e09ae0bcf   24 hours ago   209MB
first_dockerfile            1.0       c97e09ae0bcf   24 hours ago   209MB
first_dockerfile            2.0       c97e09ae0bcf   24 hours ago   209MB
nginx                       latest    08b152afcfae   6 days ago     133MB
hello-world                 latest    d1165f221234   4 months ago   13.3kB
centos                      latest    300e315adb2f   7 months ago   209MB
[root@localhost test]# docker push chenzb/myfirst_dockerfile:1.0
The push refers to repository [docker.io/chenzb/myfirst_dockerfile]
2653d992f4ef: Preparing 
denied: requested access to the resource is denied
###在push tag镜像时，镜像的tag一定要是用户名/镜像名：[TAG],否则会被拒绝。
[root@localhost test]# docker tag c97e09ae0bcf chenzb1017/myfirst_dockerfile:1.0
[root@localhost test]# docker images
REPOSITORY                      TAG       IMAGE ID       CREATED        SIZE
chenzb1017/myfirst_dockerfile   1.0       c97e09ae0bcf   24 hours ago   209MB
first_dockerfile                1.0       c97e09ae0bcf   24 hours ago   209MB
first_dockerfile                2.0       c97e09ae0bcf   24 hours ago   209MB
nginx                           latest    08b152afcfae   6 days ago     133MB
hello-world                     latest    d1165f221234   4 months ago   13.3kB
centos                          latest    300e315adb2f   7 months ago   209MB
[root@localhost test]# docker push chenzb1017/myfirst_dockerfile:1.0
The push refers to repository [docker.io/chenzb1017/myfirst_dockerfile]
2653d992f4ef: Pushed 
1.0: digest: sha256:7866241d1c78e80278bf6bb5f10ef4fc4da1ef8260f96439810b0193489c2ae3 size: 529
```

### 6.Docker 网络

#### 1.原理

我们每启动一个docker容器，docker就会给docker容器分配一个ip，我们只要按照了docker， 就会有一个docker0桥接模式，使用的技术是veth-pair技术！ 

https://www.cnblogs.com/bakari/p/10613710.html

范例：

```bash
[root@localhost test]# docker run -d -P --name nginx01 nginx
f60555253abd8c3f4ac71f1adcd1ea449c7472969fcacc3be2fc5753160dff69
[root@localhost test]# docker run -d -P --name nginx02 nginx
c63b88961c62dc539e82de9f641e991d84e4772f21e636f66c6e9917e46ed493
[root@localhost test]# ip add
5: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:2d:5a:b8:a9 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:2dff:fe5a:b8a9/64 scope link 
       valid_lft forever preferred_lft forever
7: vetha5b4af9@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default 
    link/ether aa:57:c4:e4:53:ff brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::a857:c4ff:fee4:53ff/64 scope link 
       valid_lft forever preferred_lft forever
9: veth82fe7bf@if8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default 
    link/ether 06:d6:2c:96:03:36 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::4d6:2cff:fe96:336/64 scope link 
       valid_lft forever preferred_lft forever
#创建一个容器就多一个ip，if6和if8
       
#测试两个容器是否能ping通
[root@localhost test]# docker exec -it centos02 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
12: eth0@if13: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:11:00:04 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.4/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
[root@localhost test]# docker exec -it centos01 ping 172.17.0.4			#ip能ping通
PING 172.17.0.4 (172.17.0.4) 56(84) bytes of data.
64 bytes from 172.17.0.4: icmp_seq=1 ttl=64 time=0.123 ms
64 bytes from 172.17.0.4: icmp_seq=2 ttl=64 time=0.065 ms
[root@localhost test]# docker exec -it centos01 ping centos02			#名字ping不同
ping: centos02: Name or service not known

```

docker使用的是Linux的桥接，宿主机是Docker容器的网桥 docker0。Docker中所有网络接口都是虚拟的，虚拟的转发效率高（内网传递文件） 只要容器删除，对应的网桥一对就没了！

![image-20210729104942530](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210729104942530.png)

#### 2.-link

为了能够通过名字来访问容器，可以在创建容器的时候为容器增加-link选项。

```bash
[root@localhost test]# docker run -d -it --name centos03 --link centos02 centos
946e9f46106978f9c5207a317c6d2d1e12c4a6cb1d2d076bdb95e0fbf007594b
[root@localhost test]# docker inspect 946e9f461069
"Links": [
    "/centos02:/centos03/centos02"
],
[root@localhost test]# docker exec -it centos03 cat /etc/hosts
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
ff00::0	ip6-mcastprefix
ff02::1	ip6-allnodes
ff02::2	ip6-allrouters
172.17.0.4	centos02 088e6260bb10  				#centos02的主机
172.17.0.3	946e9f461069
[root@localhost test]# docker exec -it centos03 ping centos02				#此时ping容器名可以ping通
PING centos02 (172.17.0.4) 56(84) bytes of data.
64 bytes from centos02 (172.17.0.4): icmp_seq=1 ttl=64 time=0.100 ms
64 bytes from centos02 (172.17.0.4): icmp_seq=2 ttl=64 time=0.061 ms

#反过来ping却ping不通
[root@localhost test]# docker exec -it centos02 ping centos03
ping: centos03: Name or service not known

```

#### 3.自定义网络

```bash
#docker 网络的基本命令
[root@localhost test]# docker network --help
Usage:  docker network COMMAND
Manage networks
Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks
```

**查看网络**

```bash
[root@localhost test]# docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
77fce4d7e4b3   bridge    bridge    local
c3eb3d9ccb8a   host      host      local
76499429cc0a   none      null      local
```

**网络模式**

- bridge ：桥接 docker（默认，自己创建也是用bridge模式） 

- none ：不配置网络，一般不用

-  host ：和所主机共享网络 

- container ：容器网络连通（用得少！局限很大）

**创建自己的网络**

```bash
[root@localhost test]# docker network create --driver bridge --subnet 192.168.0.0/16 --gateway 192.168.0.1 mynet
a81d18f87b407bf2bac3c535abebddb2ca66125b38dc81ed166f80c165f840bd
[root@localhost test]# docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
77fce4d7e4b3   bridge    bridge    local
c3eb3d9ccb8a   host      host      local
a81d18f87b40   mynet     bridge    local
76499429cc0a   none      null      local
[root@localhost test]# docker network inspect mynet						#inspect查看网络配置
[
    {
        "Name": "mynet",
        "Id": "a81d18f87b407bf2bac3c535abebddb2ca66125b38dc81ed166f80c165f840bd",
        "Created": "2021-07-29T19:21:32.025454026+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "192.168.0.0/16",
                    "Gateway": "192.168.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
```

**添加容器到网络**

```bash
#在启动容器的时候加--net参数，选择网络
[root@localhost test]# docker run -d -P -it --name test02 --net mynet centos /bin/bash
4e962c199e67f5e7474f9cffbb8e56766006577964b24880e23c8060e8c8978c
[root@localhost test]# docker run -d -P -it --name test01 --net mynet centos /bin/bash
628282e0902fa91f1f6246e32bb2e8ba16f8f8fc8094d367e8a55178fb3159f3
[root@localhost test]# docker network inspect mynet
[
    {
        "Name": "mynet",
        "Id": "a81d18f87b407bf2bac3c535abebddb2ca66125b38dc81ed166f80c165f840bd",
        "Created": "2021-07-29T19:21:32.025454026+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "192.168.0.0/16",
                    "Gateway": "192.168.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "4e962c199e67f5e7474f9cffbb8e56766006577964b24880e23c8060e8c8978c": {
                "Name": "test02",
                "EndpointID": "4d28ee10a6f288423ffe3bc0ebef2630476eb7ba57fa969bf5a0449197ce819c",
                "MacAddress": "02:42:c0:a8:00:02",
                "IPv4Address": "192.168.0.2/16",
                "IPv6Address": ""
            },
            "628282e0902fa91f1f6246e32bb2e8ba16f8f8fc8094d367e8a55178fb3159f3": {
                "Name": "test01",
                "EndpointID": "0c7a020611d2bf5502a7a7ab3ea6c10378ee10c25a0b7c23d6a43ccba2f69e6c",
                "MacAddress": "02:42:c0:a8:00:03",
                "IPv4Address": "192.168.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

**自定义网络的好处**

1. 同个网络内的可以相互ping通，不管是通过ip还是容器名

```bash
[root@localhost test]# docker exec -it test01 ping test02
PING test02 (192.168.0.2) 56(84) bytes of data.
64 bytes from test02.mynet (192.168.0.2): icmp_seq=1 ttl=64 time=0.097 ms
64 bytes from test02.mynet (192.168.0.2): icmp_seq=2 ttl=64 time=0.065 ms
--- test02 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 2ms
rtt min/avg/max/mdev = 0.065/0.081/0.097/0.016 ms
[root@localhost test]# docker exec -it test02 ping test01
PING test01 (192.168.0.3) 56(84) bytes of data.
64 bytes from test01.mynet (192.168.0.3): icmp_seq=1 ttl=64 time=0.048 ms
64 bytes from test01.mynet (192.168.0.3): icmp_seq=2 ttl=64 time=0.063 ms
--- test01 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1ms
rtt min/avg/max/mdev = 0.048/0.055/0.063/0.010 ms
```

2. 不同集群使用不同的网络，保证了安全性



### 7.Docker Compose

#### 1.Compose概念

Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。借助 Compose，您可以使用 YAML 文件来配置应用程序的服务。然后，使用单个命令，从配置中创建并启动所有服务

Compose 具有用于管理应用程序整个生命周期的命令：

- 启动、停止和重建服务
- 查看正在运行的服务的状态
- 流式传输正在运行的服务的日志输出
- 对服务运行一次性命令

作用：批量容器编排

Compose中一些重要的概念：

- 服务services：容器、应用。（web、redis、mysql）
- 项目project：一句相关联的容器：博客、web等

#### 2.安装

看官方文档：https://docs.docker.com/compose/install/

#### 3.测试案例

1. 编写网页app应用

```python
#app.py 
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

2. 编写docker-compose.yml

```yaml
#docker-compose.yml 
version: "3.9"						#版本号
services:							#服务
  web:								#web服务	
    build: .						#build Dockerfile
    ports:							#开放端口
      - "5000:5000"
  redis:							#redis服务
    image: "redis:alpine"			#pull或者run指定镜像
```

3. 编写web服务的Dockerfile

```dockerfile
#Dockerfile 
# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

4. 编写需求文档

```bash
#requirements.txt 
flask
redis
```

5. 运行项目

```bash
[root@Curry composetest]# docker-compose up		 				#启动项目,-d后台启动
Creating network "composetest_default" with the default driver	#创建network
Building web													#根据yml先执行webbuilding
Sending build context to Docker daemon  5.632kB
Step 1/10 : FROM python:3.7-alpine								#根据Dockerfile build web镜像
3.7-alpine: Pulling from library/python
5843afab3874: Pull complete 
1174600ee52d: Pull complete 
437edbe431b9: Pull complete 
1416265535ec: Pull complete 
2ef7f525363f: Waiting 
3.7-alpine: Pulling from library/python
5843afab3874: Pull complete 
1174600ee52d: Pull complete 
437edbe431b9: Pull complete 
1416265535ec: Pull complete 
2ef7f525363f: Pull complete 
Digest: sha256:acef36b54cdb2db1d27cd36c6d9cfe1b975b3282e5503c50bf27ac17f3ec11c4
Status: Downloaded newer image for python:3.7-alpine
 ---> dc24f57a9e79
Step 2/10 : WORKDIR /code
 ---> Running in 9df2e2a0ec0e
Removing intermediate container 9df2e2a0ec0e
 ---> 8b765660001d
Step 3/10 : ENV FLASK_APP=app.py
 ---> Running in 4bfe0bfc1f9e
Removing intermediate container 4bfe0bfc1f9e
 ---> 3ee1c57d4129
Step 4/10 : ENV FLASK_RUN_HOST=0.0.0.0
 ---> Running in 245e7f6b701c
Removing intermediate container 245e7f6b701c
 ---> 1192cbafc79c
Step 5/10 : RUN apk add --no-cache gcc musl-dev linux-headers
 ---> Running in bee8e2fdf938
fetch https://dl-cdn.alpinelinux.org/alpine/v3.14/main/x86_64/APKINDEX.tar.gz
fetch https://dl-cdn.alpinelinux.org/alpine/v3.14/community/x86_64/APKINDEX.tar.gz
(1/13) Installing libgcc (10.3.1_git20210424-r2)
(2/13) Installing libstdc++ (10.3.1_git20210424-r2)
(3/13) Installing binutils (2.35.2-r2)
(4/13) Installing libgomp (10.3.1_git20210424-r2)
(5/13) Installing libatomic (10.3.1_git20210424-r2)
(6/13) Installing libgphobos (10.3.1_git20210424-r2)
(7/13) Installing gmp (6.2.1-r0)
(8/13) Installing isl22 (0.22-r0)
(9/13) Installing mpfr4 (4.1.0-r0)
(10/13) Installing mpc1 (1.2.1-r0)
(11/13) Installing gcc (10.3.1_git20210424-r2)
(12/13) Installing linux-headers (5.10.41-r0)
(13/13) Installing musl-dev (1.2.2-r3)
Executing busybox-1.33.1-r2.trigger
OK: 140 MiB in 48 packages
Removing intermediate container bee8e2fdf938
 ---> cdaf1da4a6a0
Step 6/10 : COPY requirements.txt requirements.txt
 ---> 91ff347889fa
Step 7/10 : RUN pip install -r requirements.txt
 ---> Running in 98570b88b8c7
Collecting flask
  Downloading Flask-2.0.1-py3-none-any.whl (94 kB)
Collecting redis
  Downloading redis-3.5.3-py2.py3-none-any.whl (72 kB)
Collecting itsdangerous>=2.0
  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting Werkzeug>=2.0
  Downloading Werkzeug-2.0.1-py3-none-any.whl (288 kB)
Collecting click>=7.1.2
  Downloading click-8.0.1-py3-none-any.whl (97 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.1-py3-none-any.whl (133 kB)
Collecting importlib-metadata
  Downloading importlib_metadata-4.6.1-py3-none-any.whl (17 kB)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1.tar.gz (18 kB)
Collecting typing-extensions>=3.6.4
  Downloading typing_extensions-3.10.0.0-py3-none-any.whl (26 kB)
Collecting zipp>=0.5
  Downloading zipp-3.5.0-py3-none-any.whl (5.7 kB)
Building wheels for collected packages: MarkupSafe
  Building wheel for MarkupSafe (setup.py): started
  Building wheel for MarkupSafe (setup.py): finished with status 'done'
  Created wheel for MarkupSafe: filename=MarkupSafe-2.0.1-cp37-cp37m-linux_x86_64.whl size=14614 sha256=98fc43bfe14d187f915660b202f0dabaa659281e1f74c8cd53462adbe5f71fb2
  Stored in directory: /root/.cache/pip/wheels/1a/18/04/e3b5bd888f000c2716bccc94a565239f9defc47ef93d9e7bea
Successfully built MarkupSafe
Installing collected packages: zipp, typing-extensions, MarkupSafe, importlib-metadata, Werkzeug, Jinja2, itsdangerous, click, redis, flask
Successfully installed Jinja2-3.0.1 MarkupSafe-2.0.1 Werkzeug-2.0.1 click-8.0.1 flask-2.0.1 importlib-metadata-4.6.1 itsdangerous-2.0.1 redis-3.5.3 typing-extensions-3.10.0.0 zipp-3.5.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container 98570b88b8c7
 ---> 870c632812e4
Step 8/10 : EXPOSE 5000
 ---> Running in db48e749344d
Removing intermediate container db48e749344d
 ---> c87973504cbf
Step 9/10 : COPY . .
 ---> 8ea48a667963
Step 10/10 : CMD ["flask", "run"]
 ---> Running in 34cea4f3d0e2
Removing intermediate container 34cea4f3d0e2
 ---> 3595cefc0166
Successfully built 3595cefc0166
Successfully tagged composetest_web:latest
WARNING: Image for service web was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Pulling redis (redis:alpine)...									#拉取redis镜像
alpine: Pulling from library/redis
5843afab3874: Already exists
9db2305878ef: Pull complete
3558750a1d54: Pull complete
425b6ad3558b: Pull complete
638bf2557b6e: Pull complete
c3553f307e8f: Pull complete
Digest: sha256:420c98f3fedeb9a1d6d2bcdfe19b15fa8e1382e73559ea69e21aee7dbce23da3
Status: Downloaded newer image for redis:alpine
Creating composetest_redis_1 ... done						#启动redis服务
Creating composetest_web_1   ... done						#启动web服务
Attaching to composetest_redis_1, composetest_web_1
redis_1  | 1:C 29 Jul 2021 06:04:12.646 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis_1  | 1:C 29 Jul 2021 06:04:12.646 # Redis version=6.2.5, bits=64, commit=00000000, modified=0, pid=1, just started
redis_1  | 1:C 29 Jul 2021 06:04:12.646 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis_1  | 1:M 29 Jul 2021 06:04:12.647 * monotonic clock: POSIX clock_gettime
redis_1  | 1:M 29 Jul 2021 06:04:12.648 * Running mode=standalone, port=6379.
redis_1  | 1:M 29 Jul 2021 06:04:12.648 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
redis_1  | 1:M 29 Jul 2021 06:04:12.648 # Server initialized
redis_1  | 1:M 29 Jul 2021 06:04:12.648 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis_1  | 1:M 29 Jul 2021 06:04:12.648 * Ready to accept connections
web_1    |  * Serving Flask app 'app.py' (lazy loading)
web_1    |  * Environment: production
web_1    |    WARNING: This is a development server. Do not use it in a production deployment.
web_1    |    Use a production WSGI server instead.
web_1    |  * Debug mode: off
web_1    |  * Running on all addresses.
web_1    |    WARNING: This is a development server. Do not use it in a production deployment.
web_1    |  * Running on http://172.19.0.2:5000/ (Press CTRL+C to quit)
web_1    | 172.19.0.1 - - [29/Jul/2021 06:04:57] "GET / HTTP/1.1" 200 -
web_1    | 172.19.0.1 - - [29/Jul/2021 06:05:00] "GET / HTTP/1.1" 200 -
web_1    | 172.19.0.1 - - [29/Jul/2021 06:05:01] "GET / HTTP/1.1" 200 -
web_1    | 172.19.0.1 - - [29/Jul/2021 06:05:02] "GET / HTTP/1.1" 200 -
web_1    | 183.251.103.230 - - [29/Jul/2021 06:07:39] "GET / HTTP/1.1" 200 -
web_1    | 183.251.103.230 - - [29/Jul/2021 06:07:39] "GET /favicon.ico HTTP/1.1" 404 -
web_1    | 183.251.103.230 - - [29/Jul/2021 06:07:40] "GET / HTTP/1.1" 200 -
[root@Curry ~]# docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS         PORTS                    NAMES
fca053e00a70   composetest_web   "flask run"              4 minutes ago   Up 4 minutes   0.0.0.0:5000->5000/tcp   composetest_web_1
1e17f42879ee   redis:alpine      "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes   6379/tcp                 composetest_redis_1
d4bd058e5a1f   centos            "/bin/bash"              25 hours ago    Up 25 hours                             mycentos
[root@Curry ~]# docker network ls
NETWORK ID     NAME                  DRIVER    SCOPE
5d46928281dc   bridge                bridge    local
03cdc206b8b3   composetest_default   bridge    local
42c398fbb8e4   host                  host      local
bc2f15329096   none                  null      local

[root@Curry ~]# curl localhost:5000
Hello World! I have been seen 1 times.
[root@Curry ~]# curl localhost:5000
Hello World! I have been seen 2 times.
```

![image-20210729140808774](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210729140808774.png)

6. 停止项目

```bash
docker-compose stop
```

### 8.Docker Swarm

#### 1.工作模式

![Swarm mode cluster](https://docs.docker.com/engine/swarm/images/swarm-diagram.png)

有两种类型的节点：managers和workers

操作都在manager

Raft算法

#### 2.搭建集群

##### swarm基本命令：

```bash
[root@sgyt ~]# docker swarm --help
Usage:  docker swarm COMMAND
Manage Swarm
Commands:
  ca          Display and rotate the root CA
  init        Initialize a swarm
  join        Join a swarm as a node and/or manager
  join-token  Manage join tokens
  leave       Leave the swarm
  unlock      Unlock swarm
  unlock-key  Manage the unlock key
  update      Update the swarm
```

###### 初始化集群

```bash
[root@sgyt ~]# docker swarm init --help

Usage:  docker swarm init [OPTIONS]

Initialize a swarm

Options:
      --advertise-addr string                  Advertised address (format: <ip|interface>[:port])
#--advertise配置入口      

[root@Curry composetest]# docker swarm init --advertise-addr 172.17.19.254
Swarm initialized: current node (27oknwybhfzz3x77cg0xrt4gm) is now a manager.
To add a worker to this swarm, run the following command:			#加入节点
    docker swarm join --token SWMTKN-1-5sf5k8vjtnah42wdwpcr50g1asx2n9b5s5r4vm6avc9yi4h98u-d0n2lyr4i6gicx0imbd19tf1f 172.17.19.254:2377							#加入管理节点
To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

```

##### 加入集群

```bash
#从主节点获取的命令中，加入工作节点或管理节点
docker swarm join --token SWMTKN-1-5sf5k8vjtnah42wdwpcr50g1asx2n9b5s5r4vm6avc9yi4h98u-d0n2lyr4i6gicx0imbd19tf1f 172.17.19.254:2377
[root@sgyt ~]# docker swarm join --token SWMTKN-1-4jhj4zvas5np6dm1qtwyne8ng9q1jhtp5ub91z803xpsd4alaf-93yd1wk1h799yd4n6mhkuqz0k 192.168.83.100:2377
This node joined a swarm as a worker.
[root@localhost ~]# docker node ls					#查看节点信息
ID                            HOSTNAME                STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
qk9vhzs1rrxrazn0slbqx4yax *   localhost.localdomain   Ready     Active         Leader           20.10.7
d1tic8hbwoxmh70bl68ecbskv     node2.chen.com          Ready     Active                          20.10.7
ky7vmebrdptoo5o1vdqio5wb9     sgyt                    Ready     Active                          20.10.7
#获取管理员的token
[root@localhost ~]# docker swarm join-token manager
To add a manager to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-4jhj4zvas5np6dm1qtwyne8ng9q1jhtp5ub91z803xpsd4alaf-ckyyw045ltbs7dthq0xodrvlh 192.168.83.100:2377
#加入为管理员节点
[root@node2 ~]# docker swarm join --token SWMTKN-1-4jhj4zvas5np6dm1qtwyne8ng9q1jhtp5ub91z803xpsd4alaf-ckyyw045ltbs7dthq0xodrvlh 192.168.83.100:2377
This node joined a swarm as a manager.
[root@host1 ~]# docker node ls
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
23usstudfosdxbkzn6w6firig *   host1      Ready     Active         Leader           20.10.7
2ykuk9dinyojqr19d5u9mjmce     host2      Ready     Active         Reachable        20.10.7
shjl0wxmbrddw94dkfhxskbke     host3      Ready     Active         Reachable        20.10.7
y8hz2tokah9lyjxzounfkvyc7     host3      Ready     Active                          20.10.7
#关闭Leaders节点，host2成为leaders
[root@host2 ~]# docker node ls
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
23usstudfosdxbkzn6w6firig     host1      Unknown   Active         Unreachable      20.10.7
2ykuk9dinyojqr19d5u9mjmce *   host2      Ready     Active         Leader           20.10.7
shjl0wxmbrddw94dkfhxskbke     host3      Ready     Active         Reachable        20.10.7
y8hz2tokah9lyjxzounfkvyc7     host3      Unknown   Active                          20.10.7
#关闭两个管理节点后。集群不可用

```



#### 3.Raft协议

Raft协议：保证大多数节点存活才可用。只要>1,集群至少大于3台。高可用

#### 4.集群作用

弹性、扩缩容

容器 =>服务 =>副本

 体验：创建服务，动态扩展服务、动态更新服务

```bash
[root@host1 composetest]# docker service --help

Usage:  docker service COMMAND

Manage services

Commands:
  create      Create a new service
  inspect     Display detailed information on one or more services
  logs        Fetch the logs of a service or task
  ls          List services
  ps          List the tasks of one or more services
  rm          Remove one or more services
  rollback    Revert changes to a service's configuration
  scale       Scale one or multiple replicated services
  update      Update a service

Run 'docker service COMMAND --help' for more information on a command.
```

灰度发布：金丝雀发布

```shell
#创建服务
[root@host1 composetest]# docker service create -p 8888:80 --name my-nginx nginx:latest
wkiwx2awkcbxu75aubjausroo
overall progress: 1 out of 1 tasks 
1/1: running   [==================================================>] 
verify: Service converged 
#查看服务
[root@host1 composetest]# docker service ps my-nginx 
ID             NAME         IMAGE          NODE      DESIRED STATE   CURRENT STATE            ERROR     PORTS
mr24uq8ukn6g   my-nginx.1   nginx:latest   host1     Running         Running 40 seconds ago             
[root@host1 composetest]# docker service ls
ID             NAME       MODE         REPLICAS   IMAGE          PORTS				#副本数REPLICAS为1
wkiwx2awkcbx   my-nginx   replicated   1/1        nginx:latest   *:8888->80/tcp
#查看服务在哪个节点上执行，可以看到nginx服务运行在了host1主机上，但所有主机都能访问nginx
[root@host1 test]# ansible vm -a 'docker ps'
192.168.83.102 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
192.168.83.103 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
192.168.83.101 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
192.168.83.100 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS     NAMES
e239b31f746c   nginx:latest   "/docker-entrypoint.…"   41 minutes ago   Up 41 minutes   80/tcp    my-nginx.1.mr24uq8ukn6g7mzv533nvprcp

#创建副本
[root@host1 swarm]# docker service update --replicas 2 my-nginx
my-nginx
overall progress: 2 out of 2 tasks 
1/2: running   [==================================================>] 
2/2: running   [==================================================>] 
verify: Service converged 
[root@host1 swarm]# docker service ls
ID             NAME       MODE         REPLICAS   IMAGE          PORTS
wkiwx2awkcbx   my-nginx   replicated   2/2        nginx:latest   *:8888->80/tcp
[root@host1 swarm]# ansible vm -a 'docker ps'
192.168.83.102 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS     NAMES
0c32d1e6b49d   nginx:latest   "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   80/tcp    my-nginx.2.21b0ki653r0w5es3myatm211w
192.168.83.103 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
192.168.83.101 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
192.168.83.100 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS     NAMES
e239b31f746c   nginx:latest   "/docker-entrypoint.…"   59 minutes ago   Up 59 minutes   80/tcp    my-nginx.1.mr24uq8ukn6g7mzv533nvprcp

docker run 		#容器启动，不具有扩缩容的功能
docker service 	#服务，具有扩缩容、滚动更新的功能
```

![image-20210730141539144](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210730141539144.png)
