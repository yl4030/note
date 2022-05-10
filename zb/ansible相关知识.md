# yealink.cloud_docker项目ansible相关知识

## 1.项目编排

在整个cloud项目中，ansible起到了对每个服务，每项业务进行编排的作用，使整个项目在我们的需求下进行部署，能够更直观地了解整个项目的部署流程。

### 1.1playbook

在项目编排中，playbook至关重要，是整个项目编排的核心。

**简介：**Playbooks 提供了一个可重复、可重用、简单的配置管理和多机部署系统，非常适合部署复杂的应用程序。

**核心元素**：

- Hosts：主机列表。相应的主机目录保存在inventory/hosts 中
- Tasks：任务集，包含功能模块，实现服务。
- tags：标签，指定某条任务执行，用于选择运行playbook中的部分代码，在部署中可以用来指定相应的服务进行部署或者升级。

### 1.2 roles

**简介：**roles是用来组织每项服务的playbook

**核心元素：**

- defaults：常用于配置服务中涉及到的默认变量。
- files：存放服务需要的文件。
- handlers：触发器，在特定条件下，执行某项操作，例如更改了变量值，重启相应服务。
- meta：配置每项服务的相关依赖。
- templates：存放任务中的模板文件。
- vars：存放服务中相关的自定义变量

### 1.3 编排方式

在cloud项目中，总共包含了9个业务，每个业务被封装为一个大的roles，每个业务中还包括不同的服务，每一个服务也是一个小roles，每项服务中不同的功能是由playbook构成。整个项目的业务则是通过playbook来调用，最后再由一个playbook进行编排。

cloud项目编排流程图：

![](E:\个人资料\Cloud\yealink.cloud_docker项目知识梳理总结\resource\img\编排方式流程图.png)

### 1.4.Inventory文件

主机配置清单文件，用于配置主机信息，每项服务对应各自的主机地址。同时定义每个服务配置信息，例如名字、端口等。将这些信息按组分类，方便我们维护。



## 2.使用模块

`become`：更改权限，类似linux里的sudo

`tags`：给playbook做标签，用于指定执行某项任务，在编排部署中，可以用于指定升级或部署某项服务

`files`：文件模块，可以用于创建文件夹，配置文件权限、属性、属主等

`slurp`：用于获取远程主机中文件数据的base64编码

`debug`：调试模块，用于输出调试信息。

`notify`：触发器，当task发生改变时调用handlers中相应的模块。

`docker_container`：重要模块，详见2.1介绍。

`import_playbook`：在当前playbook中导入其他playbook，这是编排项目的一个基础。

### 2.1 docker_container

**简介：**docker_container是ansible中用于管理docker容器生命周期的一个模块。有很多参数，以下列举一些常用以及项目中运用到的参数。

```shell
capabilities			#要从容器中增加的功能列表
cap_drop				#要从容器中删除的功能列表	
command					#在容器启动时执行的命令
comparisons				#指定将现有容器的属性与模块选项进行比较，以决定是否应重新创建/更新容器。
						#ignore 该选项发生改变则忽略
						#strict 该选项发生改变则重启
						#allow_more_present 	仅允许用于列表、集合和字典。如果为列表或集合指定了它，则仅当模块选项包含容器选项中不存在的值时，才会更新或重新启动容器。如果为 dict 指定了选项，则仅当模块选项包含容器选项中不存在的键，或者存在的键的值不同时，才会更新或重新启动容器。
devices					#要添加到容器中的主机设备，以字典的方式<path_on_host>:<path_in_container>:<cgroup_permissions>.
device_read_bps 		#设备路径和设备读取速率（每秒字节数）的列表。
						#path 设备路径
						#rate 速率，格式为 <number>[<unit>] 的设备读取限制。 数字是一个正整数。单位可以是 B、K、M、G、T或 P之一。 省略单位默认为字节
device_read_iops		#设备和从设备读出速率（每秒IO）的列表。
						#path 设备路径
						#rate 速率，为正整数
device_requests			#允许请求额外的资源，例如 GPU。	
						#capabilities			请求功能的字符串列表列表。
                        #count					请求号码或设备
                        #device_ids				设备id列表 
                        #driver					用于此设备的驱动程序
                        #options				驱动选项
entrypoint				#相对于docker中Dockerfile的ENTRYPOINT
env						#配置环境变量
env_file				#指定环境变量目录
healthcheck				#配置运行的检查以确定此服务的容器是否“健康”。
hostname				#容器主机名
image					#指明构建的镜像
links					#链接容器的名称别名列表，格式为 container_name:alias。 设置此项将强制重新启动容器。
log_driver				#指定日志驱动程序
log_options				#所选 log_driver 的选项字典。
name					#创建容器名，相当于docker的--name
network					#配置容器网络选项
						#相关参数
						#name，网络名称，网络必须被创建
						#ipv4_address，配置容器在网络中的ipv4地址，要符合网络子网
						#ipv6_address，配置容器在网络中的ipv6地址，要符合网络子网
						#links，链接其他容器
						#aliases，别名，可以通过别名访问容器
network_mode			#网络模式，选项包括bridge、host、none、container：<name|id>、<network_name>、default
ports					#配置容器端口，和docker -p类似
pull					#如果为true，则始终拉取最新镜像，否则只在丢失时拉取镜像。  
purge_networks			#删除于容器相关联的网络，除了networks中指定的网络
restart					#和state的start状态一起使用，可以重启容器
restart_policy          #容器重启政策：
						#no						不重启
						#on-failure				错误时重启
						#always					总是重启
						#unless-stopped 
state					#设置容器状态
						#absent：与指定名称匹配的容器将被停止并删除。使用 force_kill杀死容器而不是停止它。使用 keep_volumes保留与删除的容器关联的匿名卷。
						#present：创建容器，创建后容器状态为created，若容器存在则skip
						#stopped：暂停容器，容器未启动则skip
						#started：启动容器，没有容器会自动创建。
volume					#指定挂载卷，挂载模式ro、rw、consistent、delegate、cached、rprivate、private、rshared、shared、rslave、slave 和 nocopy
volume_from   			#从其他容器中获取卷
```

### 2.2 file模块

file模块可以用于创建文件夹，配置文件权限、属性、属主等，在项目中被用来创建每项服务的配置相关文件夹。在每个roles中的config.yml中常被调用。

介绍一下file模块常见参数：

```shell
path		#必须参数，用于指定要操作的文件或目录，在之前版本的ansible中，使用dest参数或者name参数指定要操作的文件或目录，为了兼容之前的版本，使用dest或name也可以。
state：	   #设置文件状态。
-directory		#如果目录不存在，创建目录
-file 			#文件不存在，则不会被创建，存在则返回文件的信息 （常用于检查文件是否存在）
-link 			#创建软链接
-hard 			#创建硬链接
-touch 			#如果文件不存在，则会创建一个新的文件，如果文件或目录（已存在，则更新其最后修改时间）
-absent 		#删除目录、文件或者取消链接文件
src			#当state设置为link或者hard时，表示我们想要创建一个软链或者硬链，所以，我们必须指明软链或硬链链接的哪个文件，通过src参数即可指定链接源。
force  		#当state=link的时候，可配合此参数强制创建链接文件，当force=yes时，表示强制创建链接文件。不过强制创建链接文件分为三种情况。情况一：当要创建的链接文件指向的源文件并不存在时，使用此参数，可以先强制创建出链接文件。情况二：当要创建链接文件的目录中已经存在与链接文件同名的文件时，将force设置为yes，会将同名文件覆盖为链接文件，相当于删除同名文件，创建链接文件。情况三：当要创建链接文件的目录中已经存在与链接文件同名的文件，并且链接文件指向的源文件也不存在，这时会强制替换同名文件为链接文件。
owner		#用于指定被操作文件的属主，属主对应的用户必须在远程主机中存在，否则会报错。
group		#用于指定被操作文件的属组，属组对应的组必须在远程主机中存在，否则会报错。
mode		#用于指定被操作文件的权限，比如，如果想要将文件权限设置为"rw-r-x---"，则可以使用mode=650进行设置，或者使用mode=0650，效果也是相同的。如果想要设置特殊权限，比如为二进制文件设置suid，则可以使用mode=4700。
recurse		#当要操作的文件为目录，将recurse设置为yes，可以递归的修改目录中文件的属性。
```

### 2.3 import_playbook模块

在上文1.3中的流程图中可以看到，项目中引入一个site.yml来对其他项目进行编排部署，我们可以认为site.yml就是整个项目的主playbook，而其中依靠的就是import_playbook模块。

site.yml：

```yaml
---
- import_playbook: gather-facts.yml
  tags:
    - always

# - name: pre config
#   hosts: all
#   gather_facts: false
#   roles:
#     - role: host-config
#   tags:
#     - host-config

- import_playbook: site-base.yml
- import_playbook: site-devops.yml
- import_playbook: site-ybdp.yml
- import_playbook: site-ybsp-upgrade-script.yml
- import_playbook: site-ybsp.yml
- import_playbook: site-phone.yml
- import_playbook: site-rtn.yml
- import_playbook: site-im-upgrade-script.yml
- import_playbook: site-im.yml
- import_playbook: site-mediation.yml
- import_playbook: site-meeting-upgrade-script.yml
- import_playbook: site-meeting.yml
- import_playbook: site-web.yml
- import_playbook: site-operation-upgrade-script.yml
- import_playbook: site-operation.yml
- import_playbook: site-operation-frontend.yml

- name: echo ylyun user info
  hosts: all
  connection: local
  gather_facts: false
  tasks:
    - name:  echo ylyun user info
      local_action:
        module: debug
        msg: 
          - "User realm:   {{ user_manager_top_level_domain }}"
          - "index         address: {{ external_ip }}"
          - "portal        address: {{ cloud_nginx_portal_domain }}"
          - "meeting       address: {{ cloud_nginx_meeting_domain }}"
          - "partner       address: {{ cloud_nginx_partner_domain }}"
          - "yealink admin address: {{ cloud_nginx_yealink_domain }}"
          - "scheduler     address: {{ cloud_nginx_scheduler_domain }}"
          - "rocketmq         port: {{ rocketmq_namesrv_port }}"
          - "framework-nredis port: {{ framework_nredis_port }}"
          - "framework-pgsql  port: {{ framework_pgsql_pgport }}"
          - "common-nredis    port: {{ common_nredis_port }}"
          - "common-pgsql     port: {{ common_pgsql_pgport }}"
      run_once: True
  tags:
    - info
```

从代码中可以看到，我们将期望的服务启动顺序依次通过import_playbook依次导入，使得每个playbook按照顺序依次运行，这就起到了编排的作用，这个方法比常规方法要简洁方便，不用依次在每项服务结束后再调取另一个服务启动。



## 3.role文件结构

在本文1.2中介绍到了ansible中的roles，role是ansible中用来组织playbook的一种工具，roles能够根据文件结构，自动加载相关变量、文件、任务和其他ansible工作，能够让逻辑结构更清晰，更好地对playbook进行维护。

### 3.1目录结构

role目录下主要包括以下的文件夹

- `tasks`
- `handlers` 
- `defaults`
- `vars`
- `files` 
- `templates` 
- `meta`

#### 3.1.1 tasks文件夹

tasks文件夹是roles目录中最重要的文件夹，是role的执行目录，通常把role的工作任务都放在该文件夹下。

