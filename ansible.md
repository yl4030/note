# ansible总结
## 修订记录 
| 日期 | 修订版本 | 修改描述 | 作者| 审核|
| --- | --- |--- |--- |--- |
| 2021.07.20| V1.0| 初稿版本 | 许泽超|  |

## **yum安装**

* yum install epel-release -y
* yum install ansible –y
## ansible 配置公私钥
* 1.生成私钥
  * [root@server ~]# ssh-keygen 
* 2.向主机分发私钥
  * [root@server ~]# ssh-copy-id root@192.168.37.122
  * [root@server ~]# ssh-copy-id root@192.168.37.133
## 管理主机清单
* vim /etc/ansible/hosts 
	* [vm]
	* 192.168.37.122
	* 192.168.37.133

## 常用工具

### 1.ansible-doc

查看ansible模块列表和描述

```
ansible-doc [option] [module]
-l --list   		#列出所有模块清单
-s --snippet 		#显示指定模块的playbook片段
```

### 2.ansible-vault

用于加密yml文件

格式：

```shell
ansible-vault [creat|decrypt|edit|encrypt|rekey|view]
```

范例：

```shell
ansible-vault encrypt hello.yml		#加密
ansible-vault decrypt hello.yml		#解密
ansible-vault view hello.yml		#查看
ansible-vault edit hello.yml		#编辑加密文件
ansible-vault rekey hello.yml		#修改口令
ansible-vault crearte hello.yml		#创建新文件
```

### 3.ansible-console

此工具可交互执行命令

提示符格式

```shell
执行用户@当前操作的主机组（当前组的主机数量）[f:并发数]$
```

常用子命令

- 设置并发数：forks n
- 切换组：cd 主机组
- 列出当前主机组列表：list
- 列出所有的内置命令：？或help

范例：

```
[root@localhost home]# ansible-console
Welcome to the ansible console.
Type help or ? to list commands.

root@all (4)[f:5]$ list
10.120.25.126
192.168.37.101
192.168.37.102
192.168.37.104
root@all (4)[f:5]$ cd vm 
root@vm (3)[f:5]$ list
192.168.37.101
192.168.37.102
192.168.37.104
root@vm (3)[f:5]$ 
```



## 常用模块

**获取指定模块的使用帮助 例：ansible-doc -s command**

```
* ping # 主机连通性测试
* command # 在远程主机上执行命令,不支持管道
* shell # 在远程主机上调用shell解析器,支持管道命令个
* copy # 用于将文件复制到远程主机,支持设定内容和修改权限.
* file # 创建文件,创建连接文件,删除文件等
* fetch # 从远程复制文件到本地
* cron # 管理cron计划任务
* yum # 用于模块的安装
* service # 管理服务
* user # 管理用户账号
* group # 用户组管理
* script # 将本地的脚本在远端服务器运行
* setup # 该模块主要用于收集信息，是通过调用facts组件来实现的,以变量形式存储主机上的信息
* script #将主控端的脚本在远程机器上执行后删除
```

### 1.ping模块 
>#### 主机连通性测试 
>
>```
>ansible all -m ping
>```
### 2.command模块 
>#### command模块可以直接在远程主机上执行命令，并将结果返回本主机。
>```shell
>例：ansible web -m command -a 'ss -ntl'
>
>例: ansible web -m command -a 'creates=/data/aaa.jpg ls'</font>
>```
### 3.shell模块

>#### 常用命令
>
>```shell
>chdir　　# 在执行命令之前，先切换到该目录
>
>executable　　# 切换shell来执行命令，需要使用>命令的绝对路径
>
>free_form　　# 要执行的Linux指令，一般使用Ansible的-a参数代替
>
>creates　　# 一个文件名，当这个文件存在，则该命令不执行,可以用来做判断
>
>removes　　#一个文件名，这个文件不存在，则该命令不执行	
>```
>
>shell模块可以在远程主机上调用shell解释器运行命令，支持shell的各种功能，例如管道等。
>
>```shell
>例：ansible web -m shell -a 'cat /home/xzc/test.py'
>```
>
>

### 4.copy模块

>#### copy模块用于将文件复制到远程主机，同时支持给定内容生成文件和修改权限等。
>```shell
>例： ansible web -m copy -a 'src=~/hello dest=/data/hello'　　#复制文件
>```
>
>#### 常用命令
>```shell
>src　　#被复制到远程主机的本地文件。（绝对路径/相对路径）如果路径是一个目录，则会递归复制。
>content　　#用于替换"src"，可以直接指定文件的值
>dest　　#必选项，将源文件复制到的远程主机的绝对路径
>backup　　#当文件内容发生改变后，在覆盖之前把源文件备份，备份文件包含时间信息
>directory_mode　　#递归设定目录的权限，默认为系统默认权限 
>force　　#主机包含该文件且内容不同时，yes：强制覆盖；no：该文件不存在才复制。默认为"yes" 
>others　　#所有的 file 模块中的选项可以在这里使用 
>```
### 5.file模块
>#### file模块主要用于设置文件的属性，比如创建文件、创建链接文件、删除文件等。
>```shell
>例: ansible web -m file -a 'path=/data/a state=touch'　　#创建文件
>```
>
>#### 常用命令
>```shell
>force　　     #需要在两种情况下强制创建软链接，一种是源文件不存在，但之后会建立的情况下；另一种是目标软链接已存在，需要先取消之前的软链，然后创建新               的软链，有两个选项：yes|no
>group　	   　#定义文件/目录的属组。后面可以加上mode：定义文件/目录的权限
>owner　　 	#定义文件/目录的属主。后面必须跟上path：定义文件/目录的路径
>recurse　　 	#递归设置文件的属性，只对目录有效，后面跟上src：被链接的源文件路径，只应用于state=link的情况
>dest　　 		#被链接到的路径，只应用于state=link的情况
>state　 		#状态，有以下选项：
>	directory　　 #如果目录不存在，就创建目录
>	file　　		#即使文件不存在，也不会被创建
>	link　	   　#创建软链接
>	hard　　      #创建硬链接
>	touch　　		#如果文件不存在，则创建一个新文件，如果已存在，则更新其最后修改时间
>	absent　　  	#删除目录、文件或者取消链接文件
>```
### 6.fetch 模块
>#### fetch模块用于从远程某主机获取（复制）文件到本地。
>```shell
>例：ansible web -m fetch -a 'src=/home/test.py dest=/home/xzc' 
>```
>
>#### 常用命令
>```shell
>dest　　#用来存放文件的目录
>src　   #在远程拉取的文件，并且必须是一个file，不能是目录
>```
### 7.cron 模块
>#### cron模块适用于管理cron计划任务的。
>```shell
>例：ansible web -m cron -a 'name="ntp update every 5 min" minute=*/5 job="/sbin/ntpdate 172.17.0.1 &> /dev/null"' #添加计划任务
>```
>
>#### 常用命令
>```
>day=　　 # 日应该运行的工作( 1-31, *, */2, )
>hour=　　# 小时 ( 0-23, *, */2, )
>minute=　# 分钟( 0-59, *, */2, )
>month=　 # 月( 1-12, *, /2, )
>weekday= # 周 ( 0-6 for Sunday-Saturday,, )
>job=　　#指明运行的命令是什么
>name=　　#定时任务描述
>reboot　　# 任务在重启时运行，不建议使用，建议使用special_time
>special_time　　#特殊的时间范围，参数：reboot（重启时），annually（每年），monthly（每月），weekly（每周），daily（每天），hourly（每小时）
>state　　#指定状态，present表示添加定时任务，也是默认设置，absent表示删除定时任务
>user　　# 以哪个用户的身份执行
>```
### 8.yum 模块
>#### cron模块适用于管理cron计划任务的。
>```shell
>例：ansible web -m yum -a 'name=vim state=present' 　　#yum安装vim
>```
>
>#### 常用命令
>```shell
>name=　　#所安装的包的名称
>state=　　#present--->安装， latest--->安装最新的, absent---> 卸载软件。
>update_cache　　#强制更新yum的缓存
>conf_file　　#指定远程yum安装时所依赖的配置文件（安装本地已有的包）。
>disablerepo　　#临时禁止使用yum库。 只用于安装或更新时。
>enablerepo　　#临时使用的yum库。只用于安装或更新时。
>```
### 9.service  模块

>#### service模块用于服务程序的管理。
>
>```shell
>例：ansible web -m service -a 'name=nginx state=started enabled=true' 　　#开机自启动nginx
>```
>
>#### 常用命令
>
>```shell
>arguments　　<font color=blad>#命令行提供额外的参数</font>
>enabled　　<font color=blad>#设置开机启动。</font>
>name=　　<font color=blad>#服务名称</font>
>runlevel　　<font color=blad>#开机启动的级别，一般不用指定。</font>
>sleep　　<font color=blad>#在重启服务的过程中，是否等待。如在服务关闭以后等待2秒再启动。(定义在剧本中。)</font>
>state　　<font color=blad>#started-->启动服务，stopped-->停止服务， restarted-->重启服务， reloaded-->重载配置</font>
>```

### 10.user  模块

>#### user模块主要是用来管理用户账号。
>
>```shell
>例：ansible web -m user -a 'name=keer uid=11111' 　　#添加一个用户并指定其 uid
>```
>
>#### 常用命令
>
>```shell
>comment　　# 用户的描述信息
>createhome　# 是否创建家目录
>force　　# 在使用state=absent时, 行为与userdel –force一致.
>group　　# 指定基本组
>groups　　# 指定附加组，如果指定为(groups=)表示删除所有组
>home　　# 指定用户家目录
>move_home　　# 如果设置为home=时, 试图将用户主目录移动到指定的目录
>name　　# 指定用户名
>password　　# 指定用户密码
>remove　　# 在使用state=absent时, 行为是与userdel –remove一致
>shell　　# 指定默认shell
>state　　# 设置帐号状态，不指定为创建，指定值为absent表示删除
>system　　# 当创建一个用户，设置这个用户是系统用户。这个设置不能更改现有用户
>uid　　# 指定用户的uid
>```

### 11.group 模块

>#### group模块主要用于添加或删除组。
>```shell
>例：ansible web -m group -a 'name=team gid=12222' 　　# 创建组
>```
>
>#### 常用命令
>
>```shell
>gid=　　#设置组的GID号
>name=　　#指定组的名称
>state=　　#指定组的状态，默认为创建，设置值为absent为删除
>system=　#设置值为yes，表示创建为系统组
>```
### 12.script 模块
>#### script模块用于将本机的脚本在被管理端的机器上运行(直接指定脚本的路径即可)。
>> 写一个脚本，并给其加上执行权限：
>* ```shell
>	* vim /tmp/df.sh
>	  * #!/bin/bash
>	  * date >> /tmp/disk_total.log
>	  * df -lh >> /tmp/disk_total.log 
>	* chmod +x /tmp/df.sh
>	```
>>运行命令来实现在被管理端执行脚本
>* ```shell
> ansible web -m script -a '/tmp/df.sh'
### 13.setup 模块
>* setup模块主要用于收集信息，是通过调用facts组件来实现的。
>* facts组件是Ansible用于采集被管机器设备信息的一个功能，我们可以使用setup模块查机器的所有facts信息，可以使用filter来查看指定信息。整个facts信息被包装在一个JSON格式的数据结构中，ansible_facts是最上层的值。
>* facts就是变量，内建变量 。每个主机的各种信息，cpu颗数、内存大小等。会存在facts中的某个变量中。调用后返回很多对应主机的信息，在后面的操作中可以根据不同的信息来做不同的操作。如redhat系列用yum安装，而debian系列用apt来安装软件。
>
>```shell
>例：ansible web -m  -a 'filter="*mem*"'　　#查看内存
>例：ansible web -m setup -a 'filter="*mem*"' --tree /tmp/facts　　#保存我们所筛选的信息至我们的主机上（文件名为我们被管制的主机的IP）
>```

### 14.script 模块

>* 将主控端的脚本在远程机器上执行。
>
>```shell
>例：ansible-doc -s script
>例：ansible vm -m script -a './demo.sh'
>```

### 15.block/rescue/always模块

>* 判断条件（block和rescue只能执行一个）
>
>* ```yml
>  hosts: testB
>  remote_user: root
>  tasks:
>  
>  - block: #当block出错时，才会执行rescue语句
>    - debug:
>      msg: 'I execute normally' 
>    - command: /bin/false
>    - debug:
>      msg: 'I never execute, due to the above task failing'
>      rescue:
>      - debug:
>        msg: 'I caught an error'
>      - command: /bin/false
>      - debug:
>        msg: 'I also never execute'
>        always: #无论block中的任务执行成功还是失败，always中的任务都会被执行
>      - debug:
>        msg: "This always executes"
>
>* <img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210816091646994.png" alt="image-20210816091646994" style="width:100%;" />

## playbook

### 主机与用户

```yaml
---
- hosts: webservers #一个或多个组或主机的 patterns,以逗号为分隔符
  remote_user: root #账户名
```

### Tasks 列表

```yaml
---
- hosts: vm
  remote_user: root
  tasks:
   - name: install httped
     yum: name=httpd state=present
   - name: make sure apache is running
     service: name=httpd state=started
   - name: copy
     copy: src=/home/apahe.yml dest=/home
     ignore_errors: True #
```

### Handlers

当远端系统被人改动时,’notify’ actions 会在 playbook 的每一个 task 结束时被触发,而且即使有多个不同的 task 通知改动的发生, ‘notify’ actions 只会被触发一次.

```yaml
---
- hosts: vm
  remote_user: root
  tasks:
   - name: copy
     copy: src=/home/apache.yml dest=/home
     notify: #对应handlers的name
        - restart apache
   - meta: flush_handlers #立即执行所有的 handler命令
   - name: make sure apache is running
     service: name=httpd state=started
  handlers:
        - name: restart apache
          service: name=httpd state=restarted
```

### Ansible-Pull

Ansible-pull 是一个小脚本,它从 git 上 checkout 一个关于配置指令的 repo,然后以这个配置指令来运行 ansible-playbook.

```shell
ansible-pull --help #获取详细的帮助信息.
```

在执行一个 playbook 之前,想看看这个 playbook 的执行会影响到哪些 hosts：

```yaml
ansible-playbook playbook.yml --list-hosts
```

### Include

```yaml
#nginx.yml: 
---
   - name: make sure nginx is running
     service: name=nginx state=started 
     
#test.yml:
---
- hosts: vm
  remote_user: root
  #Include 语句可以和其他非 include 的 tasks 和 handlers 混合使用。
  tasks:
   - include: /home/nginx.yml #调用nginx.yml
  handlers:
   - name: test
     include: /home/nginx.yml #调用nginx.yml
```

### Tags

在Playbook中，可以同tags组件为特定的task指定标签，当在执行playbook时可以只执行特定的tags的task，而非整个文件。

```yaml
---
- hosts: vm
  remote_user: root
  tasks:
   - include: /home/nginx.yml
   - name: install httped
     yum: name=httpd state=present
     tags: test #标签
   - name: copy
     copy: src=/home/nginx.yml dest=/home
```

```shell
ansible-playbook -t test shell.yml #指定运行test
```

### 变量

变量名：仅能由字母、数S字和下划线组成，且只能字母开头

**变量定义：**

```shell
variable=value
```

**变量调用**：

通过{{ variable_name }}调用变量，且变量名前后建议加空格，有时需要“{{variable_name}}”才生效

**变量来源：**

1.ansible的setup facts远程主机的所用变量都是可以直接调用

```yaml
---
- hosts: appserver
  remote_user: root
  
  tasks:
    - name: creat log file
      file: name=/home/ansible/{{ ansible_fqdn }}.log state=touch #ansible_fqdn为setup里的变量
```

2.通过命令行指定变量，优先级最高

```shell
ansible-playbook -e varname=value
```

```yaml
#shell.yml
---
- hosts: '{{ hosts }}'
  remote_user: '{{ user }}'

  tasks:
        - name: placeholder
          command: /bin/echo foo
```

```shell
ansible-playbook shell.yml -e "hosts=vm user=root"
```

3.在playbook中定义

```
---
- hosts: dbserver
  remote_user: root
  vars:
   - username: user1
     groupname: group1
  tasks:
    - name: creat group
      group: name={{ groupname }} state=present
    - name: creat user
      user: name={{ username }} group={{ groupname }} state=present
```

4.变量文件

```yaml
#vars.yml
---
#variables file
package_name: vsftpd
service_name: vsftpd

#shell.yml
---
- hosts: dbserver
  remote_user: root
  vars_files:  #使用变量文件
    - vars.yml
  tasks:
    - name: install package
      yum: name={{ package_name }} state=present
```

## 6.YAML语言

#### 介绍

**YAML**是一个可读性高的用来表达资料序列的格式。YAML参考了其他多种语言，包括：XML、C语言、Python、Perl以及电子邮件格式RFC2822等。**YAML Ain’t Markup Language**，即YAML不是XML。不过，在开发的这种语言时，YAML的意思其实是：”Yet Another Markup Language”（仍是一种标记语言）

官方网站：http://yaml.org/

#### 特性

- YAML的可读性好

- YAML和脚本语言的交互性好

- YAML使用实现语言的数据类型

- YAML有一个一致的信息模型

- YAML易于实现

- YAML可以基于流来处理

- YAML表达能力强，扩展性好

#### YAML语法格式

1. 在单一档案中，可用连续三个连字号“-”(——)区分多个档案。另外，还有选择性的连续三个点号“..”( … )用来表示档案结尾

2. 次行开始正常写Playbook的内容，一般建议写明该Playbook的功能

3. 使用#号注释代码

4. 缩进必须是统一的，不能空格和tab混用

5. 缩进的级别也必须是一致的，同样的缩进代表同样的级别，程序判别配置的级别是通过缩进结合换行来实现的

6. YAML文件内容和Linux系统大小写判断方式保持一致，是区别大小写的，k/v的值均需大小写敏感

7. k/v的值可同行写也可换行写。同行使用,分隔

8. v可是个字符串，也可是另一个列表

9. 一个完整的代码块功能需最少元素需包括 name和task

10. 一个name只能包括一个task

11. YAML文件扩展名通常为yml或yaml

##### List列表

列表由多个元素组成，且所有元素前军使用“-“打头

范例：

```ymal
# 列表
- Apple
- Orange
- Strawberry
- Mango
- {name: "curry", job: "basketball player"}
```

##### Dictionary字典

==由key和value构成==

范例

```yaml
name: curry
age: 33
gender: man
job: basketball player
honor:
  - 2014-2015 Champion
  - 2015-2016 MVP
```

#### 三种常见的数据格式

4.2.4三种常见的数据格式

- XML: Extenslble Markup Language，可扩展标记语言，可用于数据交换和配置

- JSON: JavaScrlp Object Notation. JavaScrip，对象表记法，主要用来数据交换或配置，不支持注释

- YAML: YAML Ain't Markup Language YAML，不是一种标记语言，主要用来配置， 大小写敏感，不支持tab

可以用工具相互转化:

http://json2yaml.com/

## 7.实例

### nginx

```shell
[root@localhost test]# tree
.
├── role_nginx.yml
└── roles
    └── nginx
        ├── files #files中存放文件、软件包、脚本等内容，可以被copy、unarchive、script等模块调用
        │   └── index.html
        ├── handlers #handlers中存放依赖任务，可以被notify关键字调用
        │   └── main.yml
        ├── tasks #tasks中存放主任务，ansible会首先进行调用
        │   ├── config.yml
        │   ├── index.yml
        │   ├── install.yml
        │   ├── main.yml
        │   └── service.yml
        ├── templates #templates中存放模板文件，模板中可以使用jinja模板调用defaults中定义的变量，被templates模块调用
        │   └── nginx.j2
        ├── vars
        │   └── main.yml          
        └── defaults  #defaults中存放默认的变量，可以通过jinja模板调用
            └── main.yml
```

```yaml
#role_nginx.yml
---
- hosts: vm
  remote_user: root

  roles:
      - nginx
```

```yaml
#tasks/main.yml
---
- include: install.yml
- include: config.yml
- include: index.yml
- include: service.yml
```

```yaml
#tasks/install.yml
---
- name: install nginx
  yum: name=nginx state=present
```

```yaml
#tasks/config.yml
---
- name: config file
  template: src=nginx.j2 dest=/etc/nginx/nginx.conf
  notify: restart nginx
```

```yaml
#templates/nginx.j2  此处只有修改部分！！！
user {{ uuser }};
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;         
```

```yaml
#vars/main.yml
---
uuser: xzc
```

```yaml
#handlers/main.yml
---
- name: restart nginx
  service: name=nginx state=restarted
```

```yaml
#tasks/index.yml
---
- name: index.html
  copy: src=index.html dest=/usr/share/nginx/html
```

```html
#files/index.html
<h1>hello welcome to nginx!</h1>
```

```yaml
#tasks/service.yml
---
- name: start service
  service: name=nginx state=started enabled=yes
```

**测试**

```shell
[root@localhost nginx]# ansible vm -m shell -a 'systemctl status nginx'
192.168.37.104 | CHANGED | rc=0 >>
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since 五 2021-07-30 13:40:41 CST; 32min ago
  Process: 71532 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
  Process: 71528 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
  Process: 71527 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
 Main PID: 71534 (nginx)
    Tasks: 3
   Memory: 2.0M
   CGroup: /system.slice/nginx.service
           ├─71534 nginx: master process /usr/sbin/ngin
           ├─71535 nginx: worker proces
           └─71536 nginx: worker proces

7月 30 13:40:41 node04 systemd[1]: Starting The nginx HTTP and reverse proxy server...
7月 30 13:40:41 node04 nginx[71528]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
7月 30 13:40:41 node04 nginx[71528]: nginx: configuration file /etc/nginx/nginx.conf test is successful
7月 30 13:40:41 node04 systemd[1]: Started The nginx HTTP and reverse proxy server.
#略。。

[root@localhost nginx]# ansible vm -m shell -a 'ss -ntl -p | grep nginx'
192.168.37.102 | CHANGED | rc=0 >>
LISTEN     0      128          *:80                       *:*                   users:(("nginx",pid=94129,fd=6),("nginx",pid=94128,fd=6),("nginx",pid=94127,fd=6))
LISTEN     0      128       [::]:80                    [::]:*                   users:(("nginx",pid=94129,fd=7),("nginx",pid=94128,fd=7),("nginx",pid=94127,fd=7))
#略。。

[root@localhost nginx]# ansible vm -m shell -a 'ps -aux | grep nginx'
192.168.37.104 | CHANGED | rc=0 >>
root      71534  0.0  0.0  39304   940 ?        Ss   13:40   0:00 nginx: master process /usr/sbin/nginx
xzc       71535  0.0  0.1  41776  1940 ?        S    13:40   0:00 nginx: worker process
xzc       71536  0.0  0.1  41776  1940 ?        S    13:40   0:00 nginx: worker process
root      80653  0.0  0.0 113280  1204 pts/1    S+   14:03   0:00 /bin/sh -c ps -aux | grep nginx
root      80655  0.0  0.0 112824   960 pts/1    S+   14:03   0:00 grep nginx
#略。。

[root@localhost nginx]# ansible vm -m uri -a 'url=http://localhost:80 return_content=yes'
192.168.37.104 | SUCCESS => {
    "accept_ranges": "bytes", 
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "connection": "close", 
    "content": "<h1>hello welcome to nginx!</h1>\n", 
    "content_length": "33", 
    "content_type": "text/html", 
    "cookies": {}, 
    "cookies_string": "", 
    "date": "Fri, 30 Jul 2021 06:12:33 GMT", 
    "elapsed": 0, 
    "etag": "\"61039711-21\"", 
    "last_modified": "Fri, 30 Jul 2021 06:07:13 GMT", 
    "msg": "OK (33 bytes)", 
    "redirected": false, 
    "server": "nginx/1.20.1", 
    "status": 200, 
    "url": "http://localhost:80"
}
#略。。
```

