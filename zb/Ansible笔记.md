# Ansible笔记

## 1.Ansible简介

##### 1.1概念

​		Ansible 是一个简单的自动化运维管理工具，可以用来自动化部署应用、配置、编排 task(持续交付、无宕机更新等)，采用 paramiko 协议库，通过 SSH 或者 ZeroMQ 等连接主机，大概每 2 个月发布一个主版本。

##### 1.2工作机制

​		Ansible 在管理节点将 Ansible 模块通过 `SSH协议（或者 Kerberos、LDAP）`推送到被管理端执行，执行完之后自动删除，可以使用 SVN 等来管理自定义模块及编排

![image-20210720150348541](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210720150348541.png)

> 3.组成

| 组件          |                                                        |
| :------------ | ------------------------------------------------------ |
| **ansible**   | 核心                                                   |
| Modules       | 包括 Ansible 自带的核心模块及自定义模块                |
| Plugins       | 完成模块功能的补充，包括连接插件、邮件插件等           |
| **Playbooks** | 编排；定义 Ansible 多任务配置文件，有 Ansible 自动执行 |
| Inventory     | 定义 Ansible 管理主机的清单                            |

## 2.Ansible安装

#### 1.安装方法

![image-20210720151049391](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210720151049391.png)

#### 2.配置文件

- /etc/ansible/ansible.cfg    主配置文件
- /etc/ansible/hosts      主机（Inventory）清单
- /etc/ansible/roles       角色清单

## 3.Ansible工具

#### 1.ansible-doc

查看ansible模块列表和描述

```shell
ansible-doc [option] [module]
-l --list   		#列出所有模块清单
-s --snippet 		#显示指定模块的playbook片段
```



#### 2.ping（模块）

模块描述   

```shell
[root@Curry ~]# ansible-doc -s ping 
- name: Try to connect to host, verify a usable python and return `pong' on success
  ping:
      data:                  # Data to return for the `ping' return value. If this parameter is set to `crash', the module will cause an exception.
```

#### 3.ansible

> 格式

```bash
ansible <host-pattern> [-m module_name] [-a args]
```



> 选项说明：

```shell
--version		#显示版本
-m moudule		#指定模块，默认为command
-v				#详细过程 -vv -vvv更详细
--list-hosts	#显示主机列表，可写--list
-k, --ask-pass  #提示输入ssh连接密码，默认key验证
-C, --check 	#检查，并不执行
-T， --timeout=TIMEOUT	#执行命令超时时间，默认为10s
-u, --user=REMOTE_USER	 #执行远程执行的用户
-b, --become	#代替旧版的sudo求耳环
--become-user-USERNAME	#指定sudo的runas用户，默认为root
-K， --ask-become-pass  #提示输入sudo时的命令
```



> 命令写法

```shell
######通配符
ansible "*" -m ping
ansible 192.168.83.* -m ping 

[root@localhost ~]# ansible "*" -m ping
127.0.0.1 | SUCCESS => {					#local
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
192.168.83.101 | SUCCESS => {				#host
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
47.96.94.170 | SUCCESS => {					#server
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}


[root@localhost ~]# ansible 192.168.83.* -m ping
192.168.83.101 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
192.168.83.103 | UNREACHABLE! => {
    "changed": false, 
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 192.168.83.103 port 22: No route to host", 
    "unreachable": true
}


######或关系
ansible "web:host" -m ping
ansible "192.168.83.100:192.168.83.103" -m ping

[root@localhost ~]# ansible "web:host" -m ping
192.168.83.101 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
47.96.94.170 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}

######与关系
ansible "web:&host" -m ping

[root@localhost ~]# ansible "web:&host" -m ping        #47.96.94.170在web和host的分组下都有
47.96.94.170 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}

######逻辑非
ansible 'web:!host' -m ping				#单引号


[root@localhost ~]# ansible 'web:!host' -m ping			
[WARNING]: No hosts matched, nothing to do			 #47.96.94.170在web和host的分组下都有

[root@localhost ~]# ansible 'web:!host' -m ping		#47.96.94.170只在web下不在host下
47.96.94.170 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}


######正则表达式
[root@localhost ~]# ansible "~(db|app)server" -m ping
192.168.83.101 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
47.96.94.170 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}

```



> 执行过程

1.加载配置文件

2.加载对应的模块文件

3.通过ansible将模块或命令生成对应的临时py文件，并将该文件传输至远程服务器的对应执行用户 $HOME/.ansible/tep/ansible-tmp-num/XXX.py文件

4.给文件+x执行

5.执行并返回结果

6.删除==临时==py文件



```shell
####临时抓取到的，结束就删除
[root@localhost ~]# tree .ansible/
.ansible/
├── cp
└── tmp
    └── ansible-tmp-1626885807.87-5017-168485627628039

[root@localhost tmp]# grep "rm -f" ansible.log 
<192.168.83.101> SSH: EXEC ssh -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/root/.ansible/cp/7ed45f6d29 192.168.83.101 '/bin/sh -c '"'"'rm -f -r /root/.ansible/tmp/ansible-tmp-1626886365.82-5268-103643938047186/ > /dev/null 2>&1 && sleep 0'"'"''


```



#### 4.ansible-galaxy

此工具会链接https://galaxy.ansible.com,下载roles



#### 5.ansible-pull

推送ansible的命令到远程



#### 6.ansible-playbook

用于执行编好的playbook任务

> yaml文件



#### 7.ansible-vault

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



#### 8.ansible-console

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

```shell
[root@localhost ~]# ansible-console
Welcome to the ansible console.
Type help or ? to list commands.

root@all (5)[f:5]$ list
47.96.94.170
192.168.83.101
192.168.83.102
192.168.83.103
127.0.0.1
root@all (5)[f:5]$ cd host
root@host (4)[f:5]$ forks 10
root@host (4)[f:10]$ 

```



## 4.Ansible模块

#### 1.command模块

功能：在远程主机执行命令，此为默认模块，可忽略-m选项

注意：==此命令不支持$VARNAME、<>、|、;、&等，用shell模块执行（有局限性）==

说明：

```shell
[root@localhost ~]# ansible-doc -s command
- name: Execute commands on targets
  command:
      argv:                  # Passes the command as a list r ather than a string. Use `argv' to avoid quoting values that would otherwise be interpreted incorrectly (for example "user name"). Only the string or
                               the list form can be provided, not both.  One or the other must be provided.
      chdir:                 # Change into this directory before running the command.
      cmd:                   # The command to run.
      creates:               # A filename or (since 2.0) glob pattern. If it already exists, this step *won't* be run.
      free_form:             # The command module takes a free form command to run. There is no actual parameter named 'free form'.
      removes:               # A filename or (since 2.0) glob pattern. If it already exists, this step *will* be run.
      stdin:                 # Set the stdin of the command directly to the specified value.
      stdin_add_newline:     # If set to `yes', append a newline to stdin data.
      strip_empty_ends:      # Strip empty lines from the end of stdout/stderr in result.
      warn:                  # Enable or disable task warnings.
```

范例：

```shell
[root@localhost ~]# ansible test -m command -a 'cat /etc/centos-release'
192.168.83.101 | CHANGED | rc=0 >>
CentOS Linux release 7.9.2009 (Core)
47.96.94.170 | CHANGED | rc=0 >>
CentOS Linux release 7.9.2009 (Core)
#chdir 进入文件夹
[root@localhost ~]# ansible test -a 'chdir=/etc cat centos-release'
192.168.83.101 | CHANGED | rc=0 >>
CentOS Linux release 7.9.2009 (Core)
47.96.94.170 | CHANGED | rc=0 >>
CentOS Linux release 7.9.2009 (Core)

```



#### 2.Shell模块

功能：和command模块功能类似，但支持更多的命令和符号

```shell
[root@localhost czb]# ansible-doc -s shell
- name: Execute shell commands on targets
  shell:
      chdir:                 # 此参数的作用就是指定一个远程主机中的目录，在执行对应的脚本之前，会先进入到 chdir 参数指定的目录中。
      cmd:                   # 要运行的本地脚本的路径，后跟可选参数。
      creates:               # 使用此参数指定一个远程主机中的文件，当指定的文件存在时，就不执行对应脚本
      executable:            # Change the shell used to execute the command. This expects an absolute path to the executable.
      free_form:             # The shell module takes a free form command to run, as a string. There is no actual parameter named 'free form'. See the examples on how to use this module.
      removes:               #使用此参数指定一个远程主机中的文件，当指定的文件不存在时，就执行对应脚本
      stdin:                 # Set the stdin of the command directly to the specified value.
      stdin_add_newline:     # Whether to append a newline to stdin data.
      warn:                  # Whether to enable task warnings.

```



范例：

```shell
[root@localhost ~]# ansible test -m command -a 'echo $HOSTNAME'
192.168.83.101 | CHANGED | rc=0 >>
$HOSTNAME
47.96.94.170 | CHANGED | rc=0 >>
$HOSTNAME
[root@localhost ~]# ansible test -m shell -a 'echo $HOSTNAME'
47.96.94.170 | CHANGED | rc=0 >>
Curry
192.168.83.101 | CHANGED | rc=0 >>
localhost.localdomain
```

注意：在执行复杂命令时有时候shell也可能会失效，解决办法：写脚本时，copy到远程执行，再把结果拉回来。



#### 3.Script模块

功能：将主控端的脚本在远程机器上执行。

```shell
[root@localhost czb]# ansible-doc -s script
- name: Runs a local script on a remote node after transferring it
  script:
      chdir:                 # 此参数的作用就是指定一个远程主机中的目录，在执行对应的脚本之前，会先进入到 chdir 参数指定的目录中。
      cmd:                   # 要运行的本地脚本的路径，后跟可选参数。
      creates:               # 使用此参数指定一个远程主机中的文件，当指定的文件存在时，就不执行对应脚本，可参考 command 模块中的解释
      decrypt:               # 此选项使用 Vault 控制源文件的自动解密。
      executable:            # 用于调用脚本的可执行文件的名称或路径。
      free_form:             # 本地脚本文件的路径，后跟可选参数。
      removes:               # 使用此参数指定一个远程主机中的文件，当指定的文件不存在时，就不执行对应脚本，可参考 command 模块中的解释。
```



范例：

```shell
[root@localhost czb]# ansible test -m script -a './demo.sh'
192.168.83.101 | CHANGED => {
    "changed": true, 
    "rc": 0, 
    "stderr": "Shared connection to 192.168.83.101 closed.\r\n", 
    "stderr_lines": [
        "Shared connection to 192.168.83.101 closed."
    ], 
    "stdout": "My hostname is localhost.localdomain\r\n", 
    "stdout_lines": [
        "My hostname is localhost.localdomain"
    ]
}
47.96.94.170 | CHANGED => {
    "changed": true, 
    "rc": 0, 
    "stderr": "Shared connection to 47.96.94.170 closed.\r\n", 
    "stderr_lines": [
        "Shared connection to 47.96.94.170 closed."
    ], 
    "stdout": "My hostname is Curry\r\n", 
    "stdout_lines": [
        "My hostname is Curry"
    ]
}

#实际上就是ansible把脚本复制到远程执行后删了，如果在控制机上ctrl+c的话，远程不会删除？？？
[root@localhost ~]# cat .ansible/tmp/ansible-tmp-1626947103.86-4742-20430320822933/demo.sh 
echo My hostname is `hostname`
sleep 100

```



#### 4.Copy模块

功能：从主控端复制文件到远程主机

参数：（参数后面跟=）

```shell
src			#用于指定需要copy的文件或目录。
dest		#用于指定文件将被拷贝到远程主机的哪个目录中，dest为必须参数。
content		#当不使用src指定拷贝的文件时，可以使用content直接指定文件内容，src与content两个参数必有其一，否则会报错。
force		#当远程主机的目标路径中已经存在同名文件，并且与ansible主机中的文件内容不同时，是否强制覆盖，可选值有yes和no，默认值为yes，表示覆盖，如果设置为no，则不会执行覆盖拷贝操作，远程主机中的文件保持不变。
backup		#当远程主机的目标路径中已经存在同名文件，并且与ansible主机中的文件内容不同时，是否对远程主机的文件进行备份，可选值有yes和no，当设置为yes时，会先备份远程主机中的文件，然后再将ansible主机中的文件拷贝到远程主机。
owner		#指定文件拷贝到远程主机后的属主，但是远程主机上必须有对应的用户，否则会报错。
group		#指定文件拷贝到远程主机后的属组，但是远程主机上必须有对应的组，否则会报错。
mode		#指定文件拷贝到远程主机后的权限，如果你想将权限设置为”rw-r--r--“，则可以使用mode=0644表示，如果你想要在user对应的权限位上添加执行权限，则可以使用mode=u+x表示。
```

范例：

```shell
#把主控端文件复制到远程主机并设置路径、权限、属主等。
[root@localhost czb]# ansible test -m copy -a "src=/home/czb/demo.sh dest=/home/czb/os.sh owner=root mode=600"
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "checksum": "7ffac767d77b3267fe802d1bcbe1c115703e4d6a", 
    "dest": "/home/czb/os.sh", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "91f405a712ca594ef9d415030bb54097", 
    "mode": "0600", 
    "owner": "root", 
    "secontext": "unconfined_u:object_r:user_home_t:s0", 
    "size": 41, 
    "src": "/root/.ansible/tmp/ansible-tmp-1626948592.4-5447-223541477012720/source", 
    "state": "file", 
    "uid": 0
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "checksum": "7ffac767d77b3267fe802d1bcbe1c115703e4d6a", 
    "dest": "/home/czb/os.sh", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "91f405a712ca594ef9d415030bb54097", 
    "mode": "0600", 
    "owner": "root", 
    "size": 41, 
    "src": "/root/.ansible/tmp/ansible-tmp-1626948592.46-5445-234330043625150/source", 
    "state": "file", 
    "uid": 0
}
[root@localhost czb]# ansible test -m shell -a 'cat /home/czb/os.sh'
192.168.83.101 | CHANGED | rc=0 >>
echo My hostname is `hostname`
sleep 100
47.96.94.170 | CHANGED | rc=0 >>
echo My hostname is `hostname`
sleep 100


#指定内容，直接生成文件
[root@localhost ~]# ansible test -m copy -a "content='test line1\ntest line2' dest=/home/test.txt"
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "checksum": "43791ccbbcf72774b2bbbe6fe8d7ab488359b922", 
    "dest": "/home/test.txt", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "f0e596e1a1a3ef7d278f2dda4d4e6ec8", 
    "mode": "0644", 
    "owner": "root", 
    "secontext": "unconfined_u:object_r:user_home_dir_t:s0", 
    "size": 21, 
    "src": "/root/.ansible/tmp/ansible-tmp-1626948117.12-5161-216841157566970/source", 
    "state": "file", 
    "uid": 0
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "checksum": "43791ccbbcf72774b2bbbe6fe8d7ab488359b922", 
    "dest": "/home/test.txt", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "f0e596e1a1a3ef7d278f2dda4d4e6ec8", 
    "mode": "0644", 
    "owner": "root", 
    "size": 21, 
    "src": "/root/.ansible/tmp/ansible-tmp-1626948117.13-5159-86372660358484/source", 
    "state": "file", 
    "uid": 0
}
[root@localhost ~]# ansible test -m shell -a 'cat /home/test.txt'
192.168.83.101 | CHANGED | rc=0 >>
test line1
test line2
47.96.94.170 | CHANGED | rc=0 >>
test line1
test line2

```



#### 5.Fetch模块

功能：从远程主机文件提取至ansible的主控端，不支持目录

```shell
[root@localhost ~]# ansible-doc -s fetch
- name: Fetch files from remote nodes
  fetch:
      dest:                  # (required) A directory to save the file into. For example, if the `dest' directory is `/backup' a `src' file named `/etc/profile' on host `host.example.com', would be saved into
                               `/backup/host.example.com/etc/profile'. The host name is based on the inventory name.
      fail_on_missing:       # When set to `yes', the task will fail if the remote file cannot be read for any reason. Prior to Ansible 2.5, setting this would only fail if the source file was missing. The
                               default was changed to `yes' in Ansible 2.5.
      flat:                  # Allows you to override the default behavior of appending hostname/path/to/file to the destination. If `dest' ends with '/', it will use the basename of the source file, similar to
                               the copy module. This can be useful if working with a single host, or if retrieving files that are uniquely named per host. If using multiple hosts
                               with the same filename, the file will be overwritten for each host.
      src:                   # (required) The file on the remote system to fetch. This `must' be a file, not a directory. Recursive fetching may be supported in a later release.
      validate_checksum:     # Verify that the source and destination checksums match after the files are fetched.
```

范例：

```shell
[root@localhost ~]# ansible test -m fetch -a 'src=/etc/redhat-release dest=/home/czb/os'
192.168.83.101 | CHANGED => {
    "changed": true, 
    "checksum": "0d3186157c40752f89db0e618a5866935b523e7b", 
    "dest": "/home/czb/os/192.168.83.101/etc/redhat-release", 
    "md5sum": "902962816d0ec4fbb532949f70a41ae7", 
    "remote_checksum": "0d3186157c40752f89db0e618a5866935b523e7b", 
    "remote_md5sum": null
}
47.96.94.170 | CHANGED => {
    "changed": true, 
    "checksum": "0d3186157c40752f89db0e618a5866935b523e7b", 
    "dest": "/home/czb/os/47.96.94.170/etc/redhat-release", 
    "md5sum": "902962816d0ec4fbb532949f70a41ae7", 
    "remote_checksum": "0d3186157c40752f89db0e618a5866935b523e7b", 
    "remote_md5sum": null
}
[root@localhost ~]# tree /home/czb/os/
/home/czb/os/
├── 192.168.83.101
│   └── etc
│       └── redhat-release
└── 47.96.94.170
    └── etc
        └── redhat-release

4 directories, 2 files
```



#### 6.File模块

功能：设置文件属性

```shell
path		#必须参数，用于指定要操作的文件或目录，在之前版本的ansible中，使用dest参数或者name参数指定要操作的文件或目录，为了兼容之前的版本，使用dest或name也可以。
state：
-directory	#如果目录不存在，创建目录
-file 		#文件不存在，则不会被创建，存在则返回文件的信息 （常用于检查文件是否存在）
-link 		#创建软链接
-hard 		#创建硬链接
-touch 		#如果文件不存在，则会创建一个新的文件，如果文件或目录（已存在，则更新其最后修改时间）
-absent 	#删除目录、文件或者取消链接文件
src		#当state设置为link或者hard时，表示我们想要创建一个软链或者硬链，所以，我们必须指明软链或硬链链接的哪个文件，通过src参数即可指定链接源。
force  #当state=link的时候，可配合此参数强制创建链接文件，当force=yes时，表示强制创建链接文件。不过强制创建链接文件分为三种情况。情况一：当要创建的链接文件指向的源文件并不存在时，使用此参数，可以先强制创建出链接文件。情况二：当要创建链接文件的目录中已经存在与链接文件同名的文件时，将force设置为yes，会将同名文件覆盖为链接文件，相当于删除同名文件，创建链接文件。情况三：当要创建链接文件的目录中已经存在与链接文件同名的文件，并且链接文件指向的源文件也不存在，这时会强制替换同名文件为链接文件。
owner		#用于指定被操作文件的属主，属主对应的用户必须在远程主机中存在，否则会报错。
group		#用于指定被操作文件的属组，属组对应的组必须在远程主机中存在，否则会报错。
mode		#用于指定被操作文件的权限，比如，如果想要将文件权限设置为"rw-r-x---"，则可以使用mode=650进行设置，或者使用mode=0650，效果也是相同的。如果想要设置特殊权限，比如为二进制文件设置suid，则可以使用mode=4700。
recurse		#当要操作的文件为目录，将recurse设置为yes，可以递归的修改目录中文件的属性。
```

范例：

```shell
[root@localhost ~]# ansible test -m file -a 'path=/home/czb/sgyt state=directory'		#创建文件夹
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "gid": 0, 
    "group": "root", 
    "mode": "0755", 
    "owner": "root", 
    "path": "/home/czb/sgyt", 
    "secontext": "unconfined_u:object_r:home_root_t:s0", 
    "size": 6, 
    "state": "directory", 
    "uid": 0
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "gid": 0, 
    "group": "root", 
    "mode": "0755", 
    "owner": "root", 
    "path": "/home/czb/sgyt", 
    "size": 4096, 
    "state": "directory", 
    "uid": 0
}
[root@localhost ~]# ansible test -m shell -a 'tree /home/czb'
192.168.83.101 | CHANGED | rc=0 >>
/home/czb
├── hello.log
├── os.sh
├── sgyt
└── test.txt

1 directory, 3 files
47.96.94.170 | CHANGED | rc=0 >>
/home/czb
├── hello.log
├── os.sh
├── sgyt
└── test.sh

1 directory, 3 files

[root@localhost ~]# ansible test -m file -a 'path=/home/czb/sgyt/text.txt state=file'		#查看文件是否存在
192.168.83.101 | FAILED! => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "msg": "file (/home/czb/sgyt/text.txt) is absent, cannot continue", 
    "path": "/home/czb/sgyt/text.txt", 
    "state": "absent"				#文件不存在
}
47.96.94.170 | FAILED! => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "msg": "file (/home/czb/sgyt/text.txt) is absent, cannot continue", 
    "path": "/home/czb/sgyt/text.txt", 
    "state": "absent"				#文件不存在
}
[root@localhost ~]# ansible test -m file -a 'path=/home/czb/sgyt/text.txt state=touch'		#创建文件
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "dest": "/home/czb/sgyt/text.txt", 
    "gid": 0, 
    "group": "root", 
    "mode": "0644", 
    "owner": "root", 
    "secontext": "unconfined_u:object_r:home_root_t:s0", 
    "size": 0, 
    "state": "file", 
    "uid": 0
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "dest": "/home/czb/sgyt/text.txt", 
    "gid": 0, 
    "group": "root", 
    "mode": "0644", 
    "owner": "root", 
    "size": 0, 
    "state": "file", 
    "uid": 0
}
[root@localhost ~]# ansible test -m shell -a 'ls /home/czb/sgyt'
192.168.83.101 | CHANGED | rc=0 >>
text.txt
47.96.94.170 | CHANGED | rc=0 >>
text.txt
[root@localhost ~]# ansible test -m file -a 'path=/home/czb/sgyt/text.txt state=absent'		#删除文件
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "path": "/home/czb/sgyt/text.txt", 
    "state": "absent"
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "path": "/home/czb/sgyt/text.txt", 
    "state": "absent"
}
[root@localhost ~]# ansible test -m shell -a 'ls /home/czb/sgyt'
192.168.83.101 | CHANGED | rc=0 >>

47.96.94.170 | CHANGED | rc=0 >>

[root@localhost ~]# ansible test -m file -a 'path=/home/czb/sgyt/text.txt owner=sgyt mode=600'	#更改属主和权限
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "gid": 0, 
    "group": "root", 
    "mode": "0600", 
    "owner": "sgyt", 
    "path": "/home/czb/sgyt/text.txt", 
    "secontext": "unconfined_u:object_r:home_root_t:s0", 
    "size": 0, 
    "state": "file", 
    "uid": 1001
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "gid": 0, 
    "group": "root", 
    "mode": "0600", 
    "owner": "sgyt", 
    "path": "/home/czb/sgyt/text.txt", 
    "size": 0, 
    "state": "file", 
    "uid": 1001
}
[root@localhost ~]# ansible test -m shell -a 'ls -l /home/czb/sgyt'
192.168.83.101 | CHANGED | rc=0 >>
total 0
-rw-------. 1 sgyt root 0 Jul 22 20:26 text.txt
47.96.94.170 | CHANGED | rc=0 >>
total 0
-rw------- 1 sgyt root 0 Jul 22 14:07 text.txt

```



#### 7.unarchive模块

功能：解包解压缩

实现有两种做法：

- 将ansible主机 上的压缩包传到远程主机后解压缩至特定目录，设置copy=yes

- 将远程主机上的某个压缩包解压缩到指定路径下，设置copy=no

```shell
copy: 			#默认为yes,当copy=yes, 拷贝的文件是从ansible主机复制到远程主机上，如果设置为copy=no,会在远程主机上寻找src源文件
remote_src		#和copy功能-样且互斥，yes表示在远程主机,不在ansible主机，no表示文件在ansible主机上
src 			#源路径，可以是ansible主机上的路径,也可以是远程主机上的路径,如果是远程主机上的路径,则需要设置copy=no
dest 			#远程主机上的目标路径
mode			#设置解压缩后的文件权限
```

范例：

```shell
[root@localhost home]# ansible test -m unarchive -a 'src=/home/test.tar.gz dest=/home/sgyt owner=sgyt'  #压缩包在主控端
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "dest": "/home/sgyt", 
    "extract_results": {
        "cmd": [
            "/usr/bin/gtar", 
            "--extract", 
            "-C", 
            "/home/sgyt", 
            "-z", 
            "--owner=sgyt", 
            "-f", 
            "/root/.ansible/tmp/ansible-tmp-1626959110.85-8994-1942955362360/source"
        ], 
        "err": "", 
        "out": "", 
        "rc": 0
    }, 
    "gid": 1001, 
    "group": "sgyt", 
    "handler": "TgzArchive", 
    "mode": "0700", 
    "owner": "sgyt", 
    "secontext": "unconfined_u:object_r:user_home_dir_t:s0", 
    "size": 89, 
    "src": "/root/.ansible/tmp/ansible-tmp-1626959110.85-8994-1942955362360/source", 
    "state": "directory", 
    "uid": 1001
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "dest": "/home/sgyt", 
    "extract_results": {
        "cmd": [
            "/usr/bin/gtar", 
            "--extract", 
            "-C", 
            "/home/sgyt", 
            "-z", 
            "--owner=sgyt", 
            "-f", 
            "/root/.ansible/tmp/ansible-tmp-1626959110.9-8992-63262994575419/source"
        ], 
        "err": "", 
        "out": "", 
        "rc": 0
    }, 
    "gid": 1001, 
    "group": "sgyt", 
    "handler": "TgzArchive", 
    "mode": "0700", 
    "owner": "sgyt", 
    "size": 4096, 
    "src": "/root/.ansible/tmp/ansible-tmp-1626959110.9-8992-63262994575419/source", 
    "state": "directory", 
    "uid": 1001
}
[root@localhost home]# ansible test -m shell -a 'tree /home/sgyt'
192.168.83.101 | CHANGED | rc=0 >>
/home/sgyt
└── czb
    ├── demo.sh
    └── os
        ├── 192.168.83.101
        │   └── etc
        │       └── redhat-release
        └── 47.96.94.170
            └── etc
                └── redhat-release

6 directories, 3 files
47.96.94.170 | CHANGED | rc=0 >>
/home/sgyt
└── czb
    ├── demo.sh
    └── os
        ├── 192.168.83.101
        │   └── etc
        │       └── redhat-release
        └── 47.96.94.170
            └── etc
                └── redhat-release

6 directories, 3 files

[root@localhost home]# ansible test -a 'ls /home/sgyt'
192.168.83.101 | CHANGED | rc=0 >>
test.tar.gz
47.96.94.170 | CHANGED | rc=0 >>
test.tar.gz
[root@localhost home]# ansible test -m unarchive -a 'src=/home/sgyt/test.tar.gz dest=/home/sgyt copy=no'
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "dest": "/home/sgyt", 
    "extract_results": {
        "cmd": [
            "/usr/bin/gtar", 
            "--extract", 
            "-C", 
            "/home/sgyt", 
            "-z", 
            "-f", 
            "/home/sgyt/test.tar.gz"
        ], 
        "err": "", 
        "out": "", 
        "rc": 0
    }, 
    "gid": 1001, 
    "group": "sgyt", 
    "handler": "TgzArchive", 
    "mode": "0700", 
    "owner": "sgyt", 
    "secontext": "unconfined_u:object_r:user_home_dir_t:s0", 
    "size": 108, 
    "src": "/home/sgyt/test.tar.gz", 
    "state": "directory", 
    "uid": 1001
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "dest": "/home/sgyt", 
    "extract_results": {
        "cmd": [
            "/usr/bin/gtar", 
            "--extract", 
            "-C", 
            "/home/sgyt", 
            "-z", 
            "-f", 
            "/home/sgyt/test.tar.gz"
        ], 
        "err": "", 
        "out": "", 
        "rc": 0
    }, 
    "gid": 1001, 
    "group": "sgyt", 
    "handler": "TgzArchive", 
    "mode": "0700", 
    "owner": "sgyt", 
    "size": 4096, 
    "src": "/home/sgyt/test.tar.gz", 
    "state": "directory", 
    "uid": 1001
}
[root@localhost home]# ansible test -a 'ls /home/sgyt'
192.168.83.101 | CHANGED | rc=0 >>
czb
test.tar.gz
47.96.94.170 | CHANGED | rc=0 >>
czb
test.tar.gz
```



#### 8.Archive模块

功能：打包压缩

范例

```shell
[root@localhost home]# ansible test -m archive -a 'path=/var/log/ dest=/home/sgyt/log.tar.gz format=bz2'
192.168.83.101 | CHANGED => {
    
}
47.96.94.170 | CHANGED => {
  
}
[root@localhost home]# ansible test -a 'ls -l /home/sgyt'
192.168.83.101 | CHANGED | rc=0 >>
total 552
drwxr-xr-x. 3 root root     31 Jul 22 20:54 czb
-rw-r--r--. 1 root root 558731 Jul 22 21:15 log.tar.gz
-rw-r--r--. 1 root root    367 Jul 22 21:08 test.tar.gz
47.96.94.170 | CHANGED | rc=0 >>
total 5256
drwxr-xr-x 3 root root    4096 Jul 22  2021 czb
-rw-r--r-- 1 root root 5373867 Jul 22 14:56 log.tar.gz
-rw-r--r-- 1 root root     367 Jul 22 14:48 test.tar.gz

```

#### 9.hostname模块

功能：改主机名

范例：

```shell
[root@localhost home]# ansible appserver -m hostname -a 'name=sgyt'
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "ansible_domain": "", 
        "ansible_fqdn": "sgyt", 
        "ansible_hostname": "sgyt", 
        "ansible_nodename": "sgyt", 
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "name": "sgyt"
}
[root@localhost home]# ansible test -a 'hostname'
192.168.83.101 | CHANGED | rc=0 >>
sgyt
47.96.94.170 | CHANGED | rc=0 >>
Curry
```



#### 10.Cron模块

功能：计划任务模块

支持时间：minute、hour、day、month、weekday

```shell
[root@localhost home]# ansible-doc -s hostname
- name: Manage hostname
  hostname:
      name:                  # (required) Name of the host
      use:                   # Which strategy to use to update the hostname. If not set we try to autodetect, but this can be problematic, specially with containers as they can present misleading information.
[root@localhost home]# ansible-doc -s cron
- name: Manage cron.d and crontab entries
  cron:
      backup:                # If set, create a backup of the crontab before it is modified. The location of the backup is returned in the `backup_file' variable by this module.
      cron_file:             # If specified, uses this file instead of an individual user's crontab. If this is a relative path, it is interpreted with respect to `/etc/cron.d'. If it is absolute, it will
                               typically be `/etc/crontab'. Many linux distros expect (and some require) the filename portion to consist solely of upper- and lower-case letters,
                               digits, underscores, and hyphens. To use the `cron_file' parameter you must specify the `user' as well.
      day:                   # Day of the month the job should run ( 1-31, *, */2, etc )
      disabled:              # If the job should be disabled (commented out) in the crontab. Only has effect if `state=present'.
      env:                   # If set, manages a crontab's environment variable. New variables are added on top of crontab. `name' and `value' parameters are the name and the value of environment variable.
      hour:                  # Hour when the job should run ( 0-23, *, */2, etc )
      insertafter:           # Used with `state=present' and `env'. If specified, the environment variable will be inserted after the declaration of specified environment variable.
      insertbefore:          # Used with `state=present' and `env'. If specified, the environment variable will be inserted before the declaration of specified environment variable.
      job:                   # The command to execute or, if env is set, the value of environment variable. The command should not contain line breaks. Required if `state=present'.
      minute:                # Minute when the job should run ( 0-59, *, */2, etc )
      month:                 # Month of the year the job should run ( 1-12, *, */2, etc )
      name:                  # Description of a crontab entry or, if env is set, the name of environment variable. Required if `state=absent'. Note that if name is not set and `state=present', then a new
                               crontab entry will always be created, regardless of existing ones. This parameter will always be required in future releases.
      reboot:                # If the job should be run at reboot. This option is deprecated. Users should use special_time.
      special_time:          # Special time specification nickname.
      state:                 # Whether to ensure the job or environment variable is present or absent.
      user:                  # The specific user whose crontab should be modified. When unset, this parameter defaults to using `root'.
      weekday:               # Day of the week that the job should run ( 0-6 for Sunday-Saturday, *, etc )
```

范例：

```shell
[root@localhost home]# ansible test -m cron -a 'hour=2 minute=30 name="get hostname" job=/home/czb/os.sh'
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "envs": [], 
    "jobs": [
        "get hostname"
    ]
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "envs": [], 
    "jobs": [
        "get hostname"
    ]
}
[root@localhost home]# ansible test -a 'crontab -l'
192.168.83.101 | CHANGED | rc=0 >>
#Ansible: get hostname
30 2 * * * /home/czb/os.sh
47.96.94.170 | CHANGED | rc=0 >>
#Ansible: get hostname
30 2 * * * /home/czb/os.sh
[root@localhost home]# ansible test -a 'cat /var/spool/cron/root'
192.168.83.101 | CHANGED | rc=0 >>
#Ansible: get hostname
30 2 * * * /home/czb/os.sh
47.96.94.170 | CHANGED | rc=0 >>
#Ansible: get hostname
30 2 * * * /home/czb/os.sh
[root@localhost home]# ansible test -m cron -a 'hour=2 minute=30 name="get hostname" job=/home/czb/os.sh disabled=yes'
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "envs": [], 
    "jobs": [
        "get hostname"
    ]
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "envs": [], 
    "jobs": [
        "get hostname"
    ]
}
[root@localhost home]# ansible test -a 'cat /var/spool/cron/root'		#禁用后被注释掉了
192.168.83.101 | CHANGED | rc=0 >>
#Ansible: get hostname
#30 2 * * * /home/czb/os.sh
47.96.94.170 | CHANGED | rc=0 >>
#Ansible: get hostname
#30 2 * * * /home/czb/os.sh
[root@localhost home]# ansible test -m cron -a 'name="get hostname" state=absent'		#删除计划任务
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "envs": [], 
    "jobs": []
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "envs": [], 
    "jobs": []
}
[root@localhost home]# ansible test -a 'cat /var/spool/cron/root'
192.168.83.101 | CHANGED | rc=0 >>

47.96.94.170 | CHANGED | rc=0 >>
```



#### 11.yum模块

功能：管理软件包，只支持RHEL, Centos，fedora

```shell
[root@localhost home]# ansible-doc -s yum
- name: Manages packages with the `yum' package manager
  yum:
      allow_downgrade:       # Specify if the named package and version is allowed to downgrade a maybe already installed higher version of that package. Note that setting allow_downgrade=True can make this
                               module behave in a non-idempotent way. The task could end up with a set of packages that does not match the complete list of specified packages to
                               install (because dependencies between the downgraded package and others can cause changes to the packages which were in the earlier transaction).
      autoremove:            # If `yes', removes all "leaf" packages from the system that were originally installed as dependencies of user-installed packages but which are no longer required by any such
                               package. Should be used alone or when state is `absent' NOTE: This feature requires yum >= 3.4.3 (RHEL/CentOS 7+)
      bugfix:                # If set to `yes', and `state=latest' then only installs updates that have been marked bugfix related.
      conf_file:             # The remote yum configuration file to use for the transaction.
      disable_excludes:      # Disable the excludes defined in YUM config files. If set to `all', disables all excludes. If set to `main', disable excludes defined in [main] in yum.conf. If set to `repoid',
                               disable excludes defined for given repo id.
      disable_gpg_check:     # Whether to disable the GPG checking of signatures of packages being installed. Has an effect only if state is `present' or `latest'.
      disable_plugin:        # `Plugin' name to disable for the install/update operation. The disabled plugins will not persist beyond the transaction.
      disablerepo:           # `Repoid' of repositories to disable for the install/update operation. These repos will not persist beyond the transaction. When specifying multiple repos, separate them with a `","'. As of Ansible 2.7, this can alternatively be a list instead of `","' separated string
      download_dir:          # Specifies an alternate directory to store packages. Has an effect only if `download_only' is specified.
      download_only:         # Only download the packages, do not install them.
      enable_plugin:         # `Plugin' name to enable for the install/update operation. The enabled plugin will not persist beyond the transaction.
      enablerepo:            # `Repoid' of repositories to enable for the install/update operation. These repos will not persist beyond the transaction. When specifying multiple repos, separate them with a `","'. As of Ansible 2.7, this can alternatively be a list instead of `","' separated string
      exclude:               # Package name(s) to exclude when state=present, or latest
      install_weak_deps:     # Will also install all packages linked by a weak dependency relation. NOTE: This feature requires yum >= 4 (RHEL/CentOS 8+)
      installroot:           # Specifies an alternative installroot, relative to which all packages will be installed.
      list:                  # Package name to run the equivalent of yum list --show-duplicates <package> against. In addition to listing packages, use can also list the following: `installed', `updates',
                               `available' and `repos'. This parameter is mutually exclusive with `name'.
      lock_timeout:          # Amount of time to wait for the yum lockfile to be freed.
      name:                  # A package name or package specifier with version, like `name-1.0'. If a previous version is specified, the task also needs to turn `allow_downgrade' on. See the `allow_downgrade'documentation for caveats with downgrading packages. When using state=latest, this can be `'*'' which means run `yum -y update'. You can also pass aurl or a local path to a rpm file (using state=present). To operate on several packages this can accept a comma separated string of packages or (asof 2.0) a list of packages.
      releasever:            # Specifies an alternative release from which all packages will be installed.
      security:              # If set to `yes', and `state=latest' then only installs updates that have been marked security related.
      skip_broken:           # Skip packages with broken dependencies(devsolve) and are causing problems.
      state:                 # Whether to install (`present' or `installed', `latest'), or remove (`absent' or `removed') a package. `present' and `installed' will simply ensure that a desired package is installed. `latest' will update the specified package if it's not of the latest available version. `absent' and `removed' will remove the specified package. Default is `None', however in effect the default action is `present' unless the `autoremove' option is enabled for this module, then `absent' is inferred.
      update_cache:          # Force yum to check if cache is out of date and redownload if needed. Has an effect only if state is `present' or `latest'.
      update_only:           # When using latest, only update installed packages. Do not install packages. Has an effect only if state is `latest'
      use_backend:           # This module supports `yum' (as it always has), this is known as `yum3'/`YUM3'/`yum-deprecated' by upstream yum developers. As of Ansible 2.7+, this module also supports `YUM4',
which is the "new yum" and it has an `dnf' backend. By default, this module will select the backend based on the `ansible_pkg_mgr' fact.
      validate_certs:        # This only applies if using a https url as the source of the rpm. e.g. for localinstall. If set to `no', the SSL certificates will not be validated. This should only set to `no' used on personally controlled sites using self-signed certificates as it avoids verifying the source site. Prior to 2.1 the code worked as if this was set to `yes'.
```

范例：

```shell
[root@localhost home]# ansible test -m yum -a 'name=tree'
192.168.83.101 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "msg": "", 
    "rc": 0, 
    "results": [
        "tree-1.6.0-10.el7.x86_64 providing tree is already installed"
    ]
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "changes": {
        "installed": [
            "tree"
        ]
    }, 
    "msg": "", 
    "rc": 0, 
    "results": [
        "Loaded plugins: fastestmirror\nLoading mirror speeds from cached hostfile\nResolving Dependencies\n--> Running transaction check\n---> Package tree.x86_64 0:1.6.0-10.el7 will be installed\n--> Finished Dependency Resolution\n\nDependencies Resolved\n\n================================================================================\n Package        Arch             Version                   Repository      Size\n================================================================================\nInstalling:\n tree           x86_64           1.6.0-10.el7              base            46 k\n\nTransaction Summary\n================================================================================\nInstall  1 Package\n\nTotal download size: 46 k\nInstalled size: 87 k\nDownloading packages:\nRunning transaction check\nRunning transaction test\nTransaction test succeeded\nRunning transaction\n  Installing : tree-1.6.0-10.el7.x86_64                                     1/1 \n  Verifying  : tree-1.6.0-10.el7.x86_64                                     1/1 \n\nInstalled:\n  tree.x86_64 0:1.6.0-10.el7                                                    \n\nComplete!\n"
    ]
}
[root@localhost home]# ansible test -a "rpm -qi tree"
[WARNING]: Consider using the yum, dnf or zypper module rather than running 'rpm'.  If you need to use command because yum, dnf or zypper is insufficient you can add 'warn: false' to this command task or set
'command_warnings=False' in ansible.cfg to get rid of this message.
192.168.83.101 | CHANGED | rc=0 >>
Name        : tree
Version     : 1.6.0
Release     : 10.el7
Architecture: x86_64
Install Date: Thu 22 Jul 2021 12:42:32 AM CST
Group       : Applications/File
Size        : 89505
License     : GPLv2+
Signature   : RSA/SHA256, Fri 04 Jul 2014 01:36:46 PM CST, Key ID 24c6a8a7f4a80eb5
Source RPM  : tree-1.6.0-10.el7.src.rpm
Build Date  : Tue 10 Jun 2014 03:28:53 AM CST
Build Host  : worker1.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://mama.indstate.edu/users/ice/tree/
Summary     : File system tree viewer
Description :
The tree utility recursively displays the contents of directories in a
tree-like format.  Tree is basically a UNIX port of the DOS tree
utility.
47.96.94.170 | CHANGED | rc=0 >>
Name        : tree
Version     : 1.6.0
Release     : 10.el7
Architecture: x86_64
Install Date: Thu 22 Jul 2021 03:28:24 PM CST
Group       : Applications/File
Size        : 89505
License     : GPLv2+
Signature   : RSA/SHA256, Fri 04 Jul 2014 01:36:46 PM CST, Key ID 24c6a8a7f4a80eb5
Source RPM  : tree-1.6.0-10.el7.src.rpm
Build Date  : Tue 10 Jun 2014 03:28:53 AM CST
Build Host  : worker1.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://mama.indstate.edu/users/ice/tree/
Summary     : File system tree viewer
Description :
The tree utility recursively displays the contents of directories in a
tree-like format.  Tree is basically a UNIX port of the DOS tree
utility.

```

#### 12.Service模块

功能：启动服务

```shell
[root@localhost home]# ansible-doc service
> SERVICE    (/usr/lib/python2.7/site-packages/ansible/modules/system/service.py)
        Controls services on remote hosts. Supported init systems include BSD init, OpenRC, SysV, Solaris SMF, systemd, upstart. For Windows targets, use the
        [win_service] module instead.

  * This module is maintained by The Ansible Core Team
  * note: This module has a corresponding action plugin.
OPTIONS (= is mandatory):

- arguments
        Additional arguments provided on the command line.
        (Aliases: args)[Default: (null)]
        type: str
- enabled		#是否开机启动
        Whether the service should start on boot.
        *At least one of state and enabled are required.*
        [Default: (null)]
        type: bool
= name		#服务名字
        Name of the service.
        type: str
- pattern
        If the service does not respond to the status command, name a substring to look for as would be found in the output of the `ps' command as a stand-in for a
        status result.
        If the string is found, the service will be assumed to be started.
        [Default: (null)]
        type: str
        version_added: 0.7
- runlevel
        For OpenRC init scripts (e.g. Gentoo) only.
        The runlevel that this service belongs to.
        [Default: default]
        type: st
- sleep
        If the service is being `restarted' then sleep this many seconds between the stop and start command.
        This helps to work around badly-behaving init scripts that exit immediately after signaling a process to - stop.
        Not all service managers support sleep, i.e when using systemd this setting will be ignored.
        [Default: (null)]
        type: int
        version_added: 1.3
- state			#状态
        `started'/`stopped' are idempotent actions that will not run commands unless necessary.
        `restarted' will always bounce the service.
        `reloaded' will always reload.
        *At least one of state and enabled are required.*
        Note that reloaded will start the service if it is not already started, even if your chosen init system wouldn't normally.
        (Choices: reloaded, restarted, started, stopped)[Default: (null)]
        type: str

- use
        The service module actually uses system specific modules, normally through auto detection, this setting can force a specific module.
        Normally it uses the value of the 'ansible_service_mgr' fact and falls back to the old 'service' module when none matching is found.
        [Default: auto]
        type: str
        version_added: 2.2
- enable 		#设置是否开机启动
```

范例：

```shell
[root@localhost home]# ansible appserver -m service -a "name=httpd state=started"	#打开http服务
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "name": "httpd", 
    "state": "started", 
    "status": {
        ······
    }
}
[root@localhost home]# ansible appserver -a 'ss -ntl'		#打开http服务后就打开了80端口
192.168.83.101 | CHANGED | rc=0 >>
State      Recv-Q Send-Q Local Address:Port               Peer Address:Port                          
LISTEN     0      128       [::]:80                    [::]:*   
[root@localhost home]# ansible appserver -m service -a "name=httpd state=stopped"	#停止http服务
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "name": "httpd", 
    "state": "stopped", 
    "status": {
        ······
    }
}
[root@localhost home]# ansible appserver -a 'ss -ntl'		#80端口关闭
192.168.83.101 | CHANGED | rc=0 >>
State      Recv-Q Send-Q Local Address:Port               Peer Address:Port              
LISTEN     0      128          *:22                       *:*                  
LISTEN     0      128    127.0.0.1:631                      *:*                  
LISTEN     0      100    127.0.0.1:25                       *:*                  
LISTEN     0      128    127.0.0.1:6011                     *:*                  
LISTEN     0      128          *:111                      *:*                  
LISTEN     0      128       [::]:22                    [::]:*                  
LISTEN     0      128      [::1]:631                   [::]:*                  
LISTEN     0      100      [::1]:25                    [::]:*                  
LISTEN     0      128      [::1]:6011                  [::]:*                  
LISTEN     0      128       [::]:111                   [::]:*  

#查看监听端口，默认为80
[root@localhost home]# ansible appserver -a 'grep ^Listen /etc/httpd/conf/httpd.conf'		
192.168.83.101 | CHANGED | rc=0 >>
Listen 80
#更改监听端口为8080
[root@localhost home]# ansible appserver -a "sed -i 's/^Listen 80/Listen 8080/' /etc/httpd/conf/httpd.conf"		
192.168.83.101 | CHANGED | rc=0 >>
#重启服务
[root@localhost home]# ansible appserver -m service -a "name=httpd state=restarted"
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "name": "httpd", 
    "state": "started", 
    "status": {
        ······
    }
}
#查看监听端口
[root@localhost home]# ansible appserver -a 'ss -ntl'
192.168.83.101 | CHANGED | rc=0 >>              
LISTEN     0      128       [::]:8080                  [::]:* 
```

#### 13.User模块

功能：管理用户

```shell
-name		#必须参数，用于指定要操作的用户名称，可以使用别名 user。
-group		#此参数用于指定用户所在的基本组。
-gourps		#此参数用于指定用户所在的附加组。注意，如果说用户已经存在并且已经拥有多个附加组，那么如果想要继续添加新的附加组，需要结合 append 参数使用，否则在默认情况下，当再次使用 groups 参数设置附加组时，用户原来的附加组会被覆盖。
-append		#如果用户原本就存在多个附加组，那么当使用 groups 参数设置附加组时，当前设置会覆盖原来的附加组设置，如果不想覆盖原来的附加组设置，需要结合 append 参数，将 append 设置为 yes，表示追加附加组到现有的附加组设置，append 默认值为 no。
-shell		#此参数用于指定用户的默认 shell。
-uid		#此参数用于指定用户的 uid 号。
-expires		#此参数用于指定用户的过期时间，相当于设置 /etc/shadow 文件中的的第8列，比如，你想要设置用户的过期日期为2018年12月31日，那么你首先要获取到2018年12月31日的 unix 时间戳，使用命令 “date -d 2018-12-31 +%s” 获取到的时间戳为1546185600，所以，当设置 expires=1546185600 时，表示用户的过期时间为2018年12月31日0点0分，设置成功后，查看远程主机的 /etc/shadow 文件，对应用户的第8八列的值将变成17895（表示1970年1月1日到2018年12月31日的天数，unix 时间戳的值会自动转换为天数，我们不用手动的进行换算），目前此参数只支持在 Linux 和 FreeBSD 系统中使用。
-comment		#此参数用于指定用户的注释信息。
-state		#此参数用于指定用户是否存在于远程主机中，可选值有 present、absent，默认值为 present，表示用户需要存在，当设置为 absent 时表示删除用户。
-remove		#当 state 的值设置为 absent 时，表示要删除远程主机中的用户。但是在删除用户时，不会删除用户的家目录等信息，这是因为 remove 参数的默认值为 no，如果设置为yes，在删除用户的同时，会删除用户的家目录。当 state=absent 并且 remove=yes 时，相当于执行 “userdel --remove” 命令。
-password		#此参数用于指定用户的密码。但是这个密码不能是明文的密码，而是一个对明文密码”加密后”的字符串，相当于 /etc/shadow 文件中的密码字段，是一个对明文密码进行哈希后的字符串，你可以在 python 的命令提示符下输入如下命令，生成明文密码对应的加密字符串。
									import crypt; crypt.crypt('666666')
输入上述命令后，即可得到明文密码666666对应的加密字符串。
-update_password		#此参数有两个值可选，always 和 on_create，当此参数的值设置为always 时表示，如果 password 参数设置的值与用户当前的加密过的密码字符串不一致，则直接更新用户的密码，默认值即为 always，但是当此参数设置为 on_create 时，如果 password参数设置的值与用户当前的加密过的密码字符串不一致，则不会更新用户的密码字符串，保持之前的密码设定。如果是新创建的用户，即使此参数设置为 on_create，也会将用户的密码设置为 password 参数对应的值。
-generate_ssh_key		#此参数默认值为 no，如果设置为 yes，表示为对应的用户生成 ssh 密钥对，默认在用户家目录的 ./ssh 目录中生成名为 id_rsa 的私钥和名为 id_rsa.pub 的公钥，如果同名的密钥已经存在与对应的目录中，原同名密钥并不会被覆盖(不做任何操作)。
-ssh_key_file		#当 generate_ssh_key 参数的值为 yes 时，使用此参数自定义生成 ssh 私钥的路径和名称，对应公钥会在同路径下生成，公钥名以私钥名开头，以”.pub”结尾。
-ssh_key_comment		#当 generate_ssh_key 参数的值为 yes 时，在创建证书时，使用此参数设置公钥中的注释信息。但是如果同名的密钥对已经存在，则并不会修改原来的注释信息，即不做任何操作。当不指定此参数时，默认的注释信息为”ansible-generated on 远程主机的主机名”。
-ssh_key_passphrase		#当 generate_ssh_key 参数的值为 yes 时，在创建证书时，使用此参数设置私钥的密码。但是如果同名的密钥对已经存在，则并不会修改原来的密码，即不做任何操作。
-ssh_key_type		#当 generate_ssh_key 参数的值为 yes 时，在创建证书时，使用此参数设置密钥对的类型。默认密钥类型为 rsa，但是如果同名的密钥对已经存在，并不会对同名密钥做任何操作。
```

范例：

```shell
#创建用户
[root@localhost home]# ansible appserver -m user -a 'name=user1 comment="test user" uid=1234 home=/home/user1 group=root'
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "comment": "test user", 
    "create_home": true, 
    "group": 0, 
    "home": "/home/user1", 
    "name": "user1", 
    "shell": "/bin/bash", 
    "state": "present", 
    "system": false, 
    "uid": 1234
}
[root@localhost home]# ansible appserver -a 'grep -r "user1" /etc/passwd'
192.168.83.101 | CHANGED | rc=0 >>
user1:x:1234:0:test user:/home/user1:/bin/bash
#删除用户
[root@localhost home]# ansible appserver -m user -a 'name=user1 state=absent remove=yes'
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "force": false, 
    "name": "user1", 
    "remove": true, 
    "state": "absent"
}
[root@localhost home]# ansible appserver -a 'grep -r "user1" /etc/passwd'
192.168.83.101 | FAILED | rc=1 >>
non-zero return code


```

#### 14.Group模块

功能：创建管理组

范例：

#### 15. Lineinfile模块

功能：相当于sed，可以修改文件内容

```shell
path			#必须参数，指定要操作的文件。
line			# 使用此参数指定文本内容。
regexp			#使用正则表达式匹配对应的行，当替换文本时，如果有多行文本都能被匹配，则只有最后面被匹配到的那行文本才会被替换，当删除文本时，如果有多行文本都能被匹配，这么这些行都会被删除。
state			#当想要删除对应的文本时，需要将state参数的值设置为absent，absent为缺席之意，表示删除，state的默认值为present。
backrefs		#默认情况下，当根据正则替换文本时，即使regexp参数中的正则存在分组，在line参数中也不能对正则中的分组进行引用，除非将backrefs参数的值设置为yes。backrefs=yes表示开启后向引用，这样，line参数中就能对regexp参数中的分组进行后向引用了，这样说不太容易明白，可以参考后面的示例命令理解。backrefs=yes除了能够开启后向引用功能，还有另一个作用，默认情况下，当使用正则表达式替换对应行时，如果正则没有匹配到任何的行，那么line对应的内容会被插入到文本的末尾，不过，如果使用了backrefs=yes，情况就不一样了，当使用正则表达式替换对应行时，同时设置了backrefs=yes，那么当正则没有匹配到任何的行时，则不会对文件进行任何操作，相当于保持原文件不变。
insertafter		#借助insertafter参数可以将文本插入到“指定的行”之后，insertafter参数的值可以设置为EOF或者正则表达式，EOF为End Of File之意，表示插入到文档的末尾，默认情况下insertafter的值为EOF，如果将insertafter的值设置为正则表达式，表示将文本插入到匹配到正则的行之后，如果正则没有匹配到任何行，则插入到文件末尾，当使用backrefs参数时，此参数会被忽略。
insertbefore	#借助insertbefore参数可以将文本插入到“指定的行”之前，insertbefore参数的值可以设置为BOF或者正则表达式，BOF为Begin Of File之意，表示插入到文档的开头，如果将insertbefore的值设置为正则表达式，表示将文本插入到匹配到正则的行之前，如果正则没有匹配到任何行，则插入到文件末尾，当使用backrefs参数时，此参数会被忽略。
backup			#是否在修改文件之前对文件进行备份。
create			#当要操作的文件并不存在时，是否创建对应的文件。
```

范例：

```shell
[root@localhost home]# ansible test -a 'cat /home/czb/test.txt'
192.168.83.101 | CHANGED | rc=0 >>
Who=czb
47.96.94.170 | CHANGED | rc=0 >>
Who=czb
[root@localhost home]# ansible test -m lineinfile -a "path=/home/czb/test.txt regexp='^Who=' line='Who=curry'"
192.168.83.101 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "backup": "", 
    "changed": true, 
    "msg": "line replaced"
}
47.96.94.170 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "backup": "", 
    "changed": true, 
    "msg": "line replaced"
}
[root@localhost home]# ansible test -a 'cat /home/czb/test.txt'
192.168.83.101 | CHANGED | rc=0 >>
Who=curry
47.96.94.170 | CHANGED | rc=0 >>
Who=curry
```

#### 16.Replace模块

功能：类似于sed命令，也是基于正则表达式进行匹配和替换

#### 17.setup模块

功能：收集主机的系统信息，这些facts信息可以直接以变量的形式使用，如果主机较多，会影响速度，可以使用==gather_facts=no==来禁止Ansible收集facts信息。

```shell
[root@localhost home]# ansible-doc -s setup
- name: Gathers facts about remote hosts
  setup:
      fact_path:             # Path used for local ansible facts (`*.fact') - files in this dir will be run (if executable) and their results be added to `ansible_local' facts if a file is not executable it is read. Check notes for Windows options. (from 2.1 on) File/results format can be JSON or INI-format. The default `fact_path' can be specified in `ansible.cfg' for when setup is automatically called as part of `gather_facts'.
      filter:                # If supplied, only return facts that match this shell-style (fnmatch) wildcard.
      gather_subset:         # If supplied, restrict the additional facts collected to the given subset. Possible values: `all', `min', `hardware', `network', `virtual', `ohai', and `facter'. Can specify a list of values to specify a larger subset. Values can also be used with an initial `!' to specify that that specific subset should not be collected.  For instance: `!hardware,!network,!virtual,!ohai,!facter'. If `!all' is specified then only the min subset is collected. To avoid collecting even the min subset, specify `!all,!min'. To collect only specific facts, use `!all,!min', and specify the particular fact subsets. Use the filter parameter if you do not want to display some collected facts.
      gather_timeout:        # Set the default timeout in seconds for individual fact gathering.
```

范例：

```shell
[root@localhost home]# ansible appserver -m setup
192.168.83.101 | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.83.101"
        ], 
        "ansible_all_ipv6_addresses": [
            "fe80::9d0:20b8:5675:c0a8", 
            "fe80::3039:f8c5:97f7:1d68"
        ], 
        "ansible_distribution": "CentOS", 
        "ansible_distribution_file_parsed": true, 
        "ansible_distribution_file_path": "/etc/redhat-release", 
        "ansible_distribution_file_variety": "RedHat", 
        "ansible_distribution_major_version": "7", 
        "ansible_distribution_release": "Core", 
        "ansible_distribution_version": "7.9", 
        "ansible_virtualization_role": "guest", 
        "ansible_virtualization_type": "VMware", 
        "discovered_interpreter_python": "/usr/bin/python"
        ····
[root@localhost home]# ansible test -m setup -a 'filter=discovered_distribution_python'		#增加过滤信息
192.168.83.101 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false
}
47.96.94.170 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false
}
```

#### 18.blockinfile模块

功能：对目标文件进行多行的添加/更新/删除操作

```shell
-path		#必须参数，指定要操作的文件。
-block		#此参数用于指定我们想要操作的那”一段文本”，此参数有一个别名叫”content”，使用content或block的作用是相同的。
-marker		#假如我们想要在指定文件中插入一段文本，ansible会自动为这段文本添加两个标记，一个开始标记，一个结束标记，默认情况下，开始标记为# BEGIN ANSIBLE MANAGED BLOCK，结束标记为# END ANSIBLE MANAGED BLOCK，我们可以使用marker参数自定义”标记”。比如，marker=#{mark}test ，这样设置以后，开始标记变成了# BEGIN test，结束标记变成了# END test，没错，{mark}会自动被替换成开始标记和结束标记中的BEGIN和END，我们也可以插入很多段文本，为不同的段落添加不同的标记，下次通过对应的标记即可找到对应的段落。
-state		#tate参数有两个可选值，present与absent，默认情况下，我们会将指定的一段文本”插入”到文件中，如果对应的文件中已经存在对应标记的文本，默认会更新对应段落，在执行插入操作或更新操作时，state的值为present，默认值就是present，如果对应的文件中已经存在对应标记的文本并且将state的值设置为absent，则表示从文件中删除对应标记的段落。
-insertafter		#在插入一段文本时，默认会在文件的末尾插入文本，如果你想要将文本插入在某一行的后面，可以使用此参数指定对应的行，也可以使用正则表达式(python正则)，表示将文本插入在符合正则表达式的行的后面。如果有多行文本都能够匹配对应的正则表达式，则以最后一个满足正则的行为准，此参数的值还可以设置为EOF，表示将文本插入到文档末尾。
-insertbefore		#在插入一段文本时，默认会在文件的末尾插入文本，如果你想要将文本插入在某一行的前面，可以使用此参数指定对应的行，也可以使用正则表达式(python正则)，表示将文本插入在符合正则表达式的行的前面。如果有多行文本都能够匹配对应的正则表达式，则以最后一个满足正则的行为准，此参数的值还可以设置为BOF，表示将文本插入到文档开头。
-backup		#是否在修改文件之前对文件进行备份。
-create		#当要操作的文件并不存在时，是否创建对应的文件。
```

范例：



## 5.Playbook

#### 1.介绍

![img](http://www.178linux.com/wp-content/uploads/2018/05/playbook.png)

Playbook剧本是由一个或多个play组成的列表。

play的主要功能在于将预定义的一组主机，装扮成事先通过ansible中的task定义好的角色。Task实际是调用ansible的一个module，将多个play组织在一个playbook中，既可以让他们联合起来，按事先编排的机制执行预定义的动作。

#### 2.Playbook核心元素

- **Hosts**：执行的远程主机列表

- **Tasks**：任务列表

- **Varniables**：内置变量或自定义变量在playbook中调用

- **Templates**：模板，可替换模板文件中的变量并实现一些简单逻辑的文件

- **Handlers**：和notify结合使用，由特定条件触发的操作，满足条件方才执行，否则不执行

- **tags**：标签，指定某条任务执行，用于选择运行playbook中的部分代码。ansible具有幂等性。因此会自动跳过没有变化的部分。此时，如果确信其没有变化，就可以通过tags跳过此些代码片段

##### 1.host组件

**作用：**playbook中的每一个play的目的都是为了让某个或某些主机以某个指定的用户

身份执行任务。hosts用于指定要执行指定任务的主机，须事先定义在主机清单中

可以是如下形式：

```yaml
one.example.com
one.example.com:two.example.com
192.168.1.50
192.168.1.*
websrvs:dbsrvs        	#两个组的并集
websrvs:&dbsrvs			#两个组的交集
webservers:!dbsrvs		#在websrvs组，但不在dbsrvs组
```

**示例:**

 ```yaml
 – hosts: websrvs：dbsrvs
 ```

##### 2.remote_user组件

**作用：**可用于Host和task中。也可以通过指定其通过sudo的方式在远程主机上执行任务，其可用于play全局或某任务；此外，甚至可以在sudo时使用sudo_user指定sudo时切换的用户

```yaml
– hosts: websrvs
 remote_user: root
 
 tasks:
  – name: test connection
    ping:
    remote_user: magedu
    sudo: yes 				#默认sudo为root
    sudo_user: czb 			#sudo为czb
```

##### 3.task列表和action组件

play的主体部分是task list, task list中有一个或多个task，各个task 按次序逐个在hosts中指定的所有主机上执行，即在所有主机上完成第一个task后，再开始第二个task

task的目的是使用指定的参数执行模块，而在模块参数中可以使用变量。模块执行是幂等的，这意味着多次执行是安全的，因为其结果均一致。

每个task都应该有其name,用于playbok的执行结果输出，建议其内容能清晰地描述任务执行步骤。如果未提供name,则action的结果将用于输出

==task的两种格式==

1. action：module arguments
2. module：arguments               #建议使用

注意：shell和command模块后面跟命令，而非key=value。

范例：

```yaml
---
- hosts: test
  remote_user: root
  tasks:
    - name: install httpd
      yum: name=httpd
    - name: start httpd
      service: name=httpd state=started enabled=yes
```

##### 4.其他组件

#### 3.ShellScripts VS Playbook

范例：安装http服务，并开启服务，设置为自启动

```shell
#Shell脚本实现
#！/bin/bash
#安装Apache
yum install --quiet -y httpd
#复制配置文件
cp /tmp/httpd.conf /etc/httpd/conf/httpd.conf
cp /tmp/vhosts.conf /etc/httpd/conf.d/
#启动Apache，并设置开机自启动
systemctl enable --now httpd
```

```yaml
#Playbook实现
---
- hosts: appserver
  remote_user: root
  tasks:
    - name: "安装apache"
      yum: name=httpd
    - name: "复制配置文件"
      copy: sec=/tmp/httpd.conf dest=/etc/httpd/conf/httpd.conf
    - name: "复制配置文件"
      copy: sec=/tmp/vhosts.conf dest=/etc/httpd/conf.d/
    - name: "启动Apache，并设置开机自启动"
      service: name=httpd state=started enabled=yes
```

#### 4.playbook 初步

格式：

```shell
ansible-playbook <filename.yml> ... [option]

options：
-check                 		#只检测可能会发生的改变，但不真正的操作
-list-hosts            		#列出运行任务的主机
-limit 主机列表     		 #只针对主机列表中的主机执行
-v -vv -vvv            		#显示详细过程
```

范例

```yaml
ansible-playbook file.yml --check
ansible-playbook file.yml 
ansible-playbook file.ym -limit test
```

##### 4.1 mysql

```yaml
#创建mysql用户和组
---
- hosts: dbserver
  romote_name: root
  gather_facts: no
  
  tasks:
    - name: install packages
      yum: name=libaio,perl-Data-Dumper,perl-Getopt-Long
    - name: create group
      group: name=mysql gid=306
    - name: creat user
      user: name=mysql uid=306 group=mysql shell=/sbin/nologin system=yes home=/data/mysql create_home=no 

```

结果：

```shell
[root@localhost playbook]# ansible-playbook mysql_user.yml 

PLAY [dbserver] ****************************************************************************************************************

TASK [Gathering Facts] ****************************************************************************************************************
ok: [192.168.83.102]

TASK [创建组] ****************************************************************************************************************
changed: [192.168.83.102]

TASK [创建用户] ****************************************************************************************************************
changed: [192.168.83.102]

PLAY RECAP ****************************************************************************************************************
192.168.83.102           : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[root@localhost playbook]# ansible dbserver -a 'getent passwd mysql'
192.168.83.102 | CHANGED | rc=0 >>
mysql:x:306:306::/data/mysql:/sbin/nologin
[root@localhost playbook]# ansible dbserver -a 'id mysql'
192.168.83.102 | CHANGED | rc=0 >>
uid=306(mysql) gid=306(mysql) groups=306(mysql)
```

部署mysql

```yaml
#部署mysql
---
- hosts: dbserver
  romote_user: root
  gather_facts: no
  
  tasks:
    - name: "创建组"
      group: name=mysql system=yes gid=306
    - name: "创建用户"
      user: name=mysql shell=/sbin/nologin system=yes group=mysql uid=306 home=/data/mysql create_home=no
    - name: copy tar to remote host and file mode
      unarchive: src=/home/playbook/test_mysql/mysql-8.0.26-linux-glibc2.12-x86_64.tar.xz dest=/usr/local/ owner=root group=root
    - name: creat linkfile /usr/local/muysql
      file: src=/home/playbook/mysql-8.0.26-linux-glibc2.12-x86_64 dest=/usr/local/muysql state=link
    - name: data dir
      shell: chdir=/usr/local/mysql ./scripts/mysql_install_db --datadir=/data/mysql --user=mysql
      tags: data
    - name: config my.cnf
      copy: src=/home/playbook/test_mysql/my.cnf dest=/etc/my.cnf
    - name: service script
      shell: /bin/cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysqld
    - name: enable service
      shell: /etc/init.d/mysqld start;chkconfig --add mysql;chkconfig mysqld on
      tags: service
    - name: PATH variable
      copy: content='PATH=/usr/local/mysql/bin:$PATH' dest=/etc/profile.d/mysql.sh
    - name: secure script
      script: /home/playbook/test_mysql/secure_mysql.sh
      tags: script 
```



##### 4.2 安装nginx

```yaml
---
- hosts: webserver
  remote_user: root
  gather_facts: no
  
  tasks:
    - name: crete group nginx
      group: name=nginx state=present
    - name: add user nginx
      user: name=nginx state=present group=nginx
    - name: install nginx
      yum: name=nginx state=installed
    - name: html page
      copy: src=/home/czb/index.html dest=/usr/share/nginx/html/index.html
    - name: start service 
      service: name=nginx state=started enabled=yes
```

测试：

```bash
[root@localhost playbook]# ansible-playbook nginx_test.yml 

PLAY [webserver] ****************************************************************************************************************

TASK [crete group nginx] ****************************************************************************************************************
changed: [192.168.83.103]

TASK [add user nginx] ****************************************************************************************************************
changed: [192.168.83.103]

TASK [install nginx] ****************************************************************************************************************
changed: [192.168.83.103]

TASK [start service] ****************************************************************************************************************
changed: [192.168.83.103]

PLAY RECAP ****************************************************************************************************************
192.168.83.103             : ok=4    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[root@localhost ~]# ps -ef | grep nginx			#查看nginx服务
root       3232      1  0 17:23 ?        00:00:00 nginx: master process /usr/sbin/nginx
nginx      3233   3232  0 17:23 ?        00:00:00 nginx: worker process
nginx      3234   3232  0 17:23 ?        00:00:00 nginx: worker process
nginx      3235   3232  0 17:23 ?        00:00:00 nginx: worker process
nginx      3236   3232  0 17:23 ?        00:00:00 nginx: worker process
root       3383   1860  0 17:33 pts/0    00:00:00 grep --color=auto nginx
[root@localhost ~]# ss -ntl						#80端口也已经开启
State      Recv-Q Send-Q                           Local Address:Port                         Peer Address:Port 
LISTEN     0      128                                  *:80                                               *:*   
[root@localhost ~]# rpm -qa |grep nginx 		#查看安装nginx版本
nginx-1.20.1-2.el7.x86_64
nginx-filesystem-1.20.1-2.el7.noarch
[root@localhost ~]# cat /etc/passwd				#查看账户和组
nginx:x:1001:1001::/home/nginx:/bin/bash
[root@localhost home]# service nginx status
Redirecting to /bin/systemctl status nginx.service
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2021-07-23 18:11:09 CST; 37min ago
  Process: 4661 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
  Process: 4659 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
  Process: 4655 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
 Main PID: 4663 (nginx)
    Tasks: 5
   CGroup: /system.slice/nginx.service
           ├─4663 nginx: master process /usr/sbin/nginx
           ├─4664 nginx: worker process
           ├─4665 nginx: worker process
           ├─4666 nginx: worker process
           └─4667 nginx: worker process

Jul 23 18:11:09 localhost.localdomain systemd[1]: Starting The nginx HTTP and reverse proxy server...
Jul 23 18:11:09 localhost.localdomain nginx[4659]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
Jul 23 18:11:09 localhost.localdomain nginx[4659]: nginx: configuration file /etc/nginx/nginx.conf test is successful
Jul 23 18:11:09 localhost.localdomain systemd[1]: Started The nginx HTTP and reverse proxy server.
```

##### 4.3 部署httpd

```yaml
---
- hosts: webserver
  remote_user: root
  gather_facts: no

  tasks:
    - name: install httpd
      yum: name=httpd state=installed
    - name: install configure file
      copy: src=files/httpd.conf dest=/etc/httpd/conf/		#修改配置文件，将端口设为8080
    - name: web html
      copy: src=files/index.html dest=/var/www/html/
    - name: start service
      service: name=httpd state=started enabled=yes
```

结果：

```shell
[root@localhost home]# service httpd status				#查看服务状态
Redirecting to /bin/systemctl status httpd.service
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2021-07-23 19:24:36 CST; 16s ago
     Docs: man:httpd(8)
           man:apachectl(8)
 Main PID: 11980 (httpd)
   Status: "Total requests: 0; Current requests/sec: 0; Current traffic:   0 B/sec"
    Tasks: 6
   CGroup: /system.slice/httpd.service
           ├─11980 /usr/sbin/httpd -DFOREGROUND
           ├─11984 /usr/sbin/httpd -DFOREGROUND
           ├─11985 /usr/sbin/httpd -DFOREGROUND
           ├─11986 /usr/sbin/httpd -DFOREGROUND
           ├─11987 /usr/sbin/httpd -DFOREGROUND
           └─11988 /usr/sbin/httpd -DFOREGROUND

Jul 23 19:24:36 localhost.localdomain systemd[1]: Starting The Apache HTTP Server...
Jul 23 19:24:36 localhost.localdomain httpd[11980]: AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using localhost.localdomain. Set the 'ServerName' direc... this message
Jul 23 19:24:36 localhost.localdomain systemd[1]: Started The Apache HTTP Server.
Hint: Some lines were ellipsized, use -l to show in full.
[root@localhost home]# ps -ef | grep httpd			#查看服务进程
root      11980      1  0 19:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache    11984  11980  0 19:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache    11985  11980  0 19:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache    11986  11980  0 19:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache    11987  11980  0 19:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache    11988  11980  0 19:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache    12056  11980  0 19:25 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
root      12087   1860  0 19:26 pts/0    00:00:00 grep --color=auto httpd
[root@localhost home]# ss -ntl      				#查看8080端口是否打开
State      Recv-Q Send-Q           Local Address:Port            Peer Address:Port              
LISTEN     0      128                       [::]:8080                    [::]:*  
```



#### 5.playbook中使用handlers和notify

Handlers本质是task list，类似于MySQL中的触发器触发的行为，其中的task 与前述的task并没有本质上的不同，主要用于当关注的资源发生变化时，才会采取一定的操作。 而Notify对应的action可用于在每个play的最后被触发，这样可避免多次有改变发生时每次都执行指定的操作，仅在所有的变化发生完成后一次性地执行指定操作。在notify中列出的操作称为handler,也即notify中调用handler中定义的操作

范例：

```yaml
#配置notify，当修改服务时，重启http服务

---
- hosts: webserver
  remote_user: root
  gather_facts: no

  tasks:
    - name: install httpd
      yum: name=httpd state=installed
    - name: install configure file
      copy: src=files/httpd.conf dest=/etc/httpd/conf/
      notify: restart httpd
    - name: web html
      copy: src=files/index.html dest=/var/www/html/
    - name: start service
      service: name=httpd state=started enabled=yes

  handlers:
    - name: restart httpd
      service: name=httpd state=restarted
```

```shell
[root@localhost playbook]# ansible-playbook http_install.yml 

PLAY [webserver] ***************************************************************************************************************

TASK [install httpd] ***************************************************************************************************************
ok: [192.168.83.103]

TASK [install configure file] ***************************************************************************************************************
changed: [192.168.83.103]

TASK [web html] ***************************************************************************************************************
ok: [192.168.83.103]

TASK [start service] ***************************************************************************************************************
ok: [192.168.83.103]

RUNNING HANDLER [restart httpd]     #运行handler    ***************************************************************************************************************
changed: [192.168.83.103]

PLAY RECAP ***************************************************************************************************************
192.168.83.103             : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```



#### 6.Tags组件

在Playbook中，可以同tags组件为特定的task指定标签，当在执行playbook时可以只执行特定的tags的task，而非整个文件。

范例：

```yaml
#配置tags,指定模块执行

---
- hosts: webserver
  remote_user: root
  gather_facts: no

  tasks:
    - name: install httpd
      yum: name=httpd state=installed
    - name: install configure file
      copy: src=files/httpd.conf dest=/etc/httpd/conf/          
      tags: conf
    - name: web html
      copy: src=files/index.html dest=/var/www/html/
    - name: start service
      service: name=httpd state=started enabled=yes
      tags: service
```



结果：

```shell
[root@localhost playbook]# ansible-playbook -t conf http_tags.yml 

PLAY [webserver] *************************************************************************************************************************************************************************************************

TASK [install configure file] ************************************************************************************************************************************************************************************
changed: [192.168.83.103]

PLAY RECAP *******************************************************************************************************************************************************************************************************
192.168.83.103             : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```



#### 7.变量

变量名：仅能由字母、数字和下划线组成，且只能字母开头

**变量定义：**

```shell
variable=value
```

**变量调用**：

通过{{ variable_name }}调用变量，且变量名前后建议加空格，有时需要“{{variable_name}}”才生效

**变量来源：**

1.ansible的setup facts远程主机的所用变量都是可以直接调用

2.通过命令行指定变量，优先级最高

```shell
ansible-playbook -e varname=value
```

3.在playbook中定义

4.变量文件

5.主机清单文件中配置变量

范例：

##### 1.调用setup中的变量

```yaml
---
- hosts: appserver
  remote_user: root
  
  tasks:
    - name: creat log file
      file: name=/home/ansible/{{ ansible_fqdn }}.log state=touch
```

结果：

```shell
[root@localhost playbook]# ansible-playbook var.yml 
PLAY [dbserver] ***************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************
ok: [192.168.83.102]

TASK [creat log file] ***************************************************************************************************************
changed: [192.168.83.102]

PLAY RECAP ***************************************************************************************************************
192.168.83.102             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[root@localhost playbook]# ansible dbserver -a 'tree /home'
192.168.83.102 | CHANGED | rc=0 >>
/home
├── ansible
│   └── localhost.localdomain.log
├── czb
└── roo
```

##### 2.命令行 ansible-playbook -e选项

```yaml
---
- hosts: dbserver
  remote_user: root
  
  tasks:
    - name: install package
      yum: name={{ pkname }} state=present
```

结果：

```shell
[root@localhost playbook]# ansible-playbook -e pkname=memcached var2.yml 

PLAY [dbserver] ***************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************
ok: [192.168.83.102]

TASK [install package] ***************************************************************************************************************
changed: [192.168.83.102]

PLAY RECAP ***************************************************************************************************************
192.168.83.102             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[root@localhost home]# rpm -qi memcached
Name        : memcached
Epoch       : 0
Version     : 1.4.15
Release     : 10.el7_3.1
Architecture: x86_64
Install Date: Mon 26 Jul 2021 02:05:01 PM CST
Group       : System Environment/Daemons
Size        : 180237
License     : BSD
Signature   : RSA/SHA256, Sat 26 Nov 2016 12:03:28 AM CST, Key ID 24c6a8a7f4a80eb5
Source RPM  : memcached-1.4.15-10.el7_3.1.src.rpm
Build Date  : Fri 25 Nov 2016 11:36:56 PM CST
Build Host  : c1bm.rdu2.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://www.memcached.org/
Summary     : High Performance, Distributed Memory Object Cache
Description :
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.
```

##### 3.在playbook中定义变量

```yaml
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

结果：

```shell
[root@localhost playbook]# ansible-playbook var3.yml 

PLAY [dbserver] ***************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************
ok: [192.168.83.102]

TASK [creat group] ***************************************************************************************************************
changed: [192.168.83.102]

TASK [creat user] ***************************************************************************************************************
changed: [192.168.83.102]

PLAY RECAP ***************************************************************************************************************
192.168.83.102             : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
[root@localhost home]# id user1
uid=1002(user1) gid=1002(group1) groups=1002(group1)
[root@localhost home]# getent passwd
user1:x:1002:1002::/home/user1:/bin/bash
```

##### 4.使用变量文件。

范例：

```yaml
vars.yml
---
#variables file
package_name: vsftpd
service_name: vsftpd

var4.yml
---
- hosts: dbserver
  remote_user: root
  vars_files:
    - vars.yml
  
  tasks:
    - name: install package
      yum: name={{ package_name }} state=present
      tags: install
    - name: start service
      service: name={{ service_name }} state=started enable=yes
```

结果：

```shell
[root@localhost playbook]# ansible-playbook var4.yml 

PLAY [dbserver] ***************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************
ok: [192.168.83.102]

TASK [install package] ***************************************************************************************************************
changed: [192.168.83.102]

TASK [start service] ***************************************************************************************************************
changed: [192.168.83.102]

PLAY RECAP ***************************************************************************************************************
192.168.83.102             : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[root@localhost home]# rpm -qi vsftpd
Name        : vsftpd
Version     : 3.0.2
Release     : 29.el7_9
Architecture: x86_64
Install Date: Mon 26 Jul 2021 02:27:33 PM CST
Group       : System Environment/Daemons
Size        : 361349
License     : GPLv2 with exceptions
Signature   : RSA/SHA256, Fri 11 Jun 2021 11:06:15 PM CST, Key ID 24c6a8a7f4a80eb5
Source RPM  : vsftpd-3.0.2-29.el7_9.src.rpm
Build Date  : Thu 10 Jun 2021 12:15:50 AM CST
Build Host  : x86-02.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : https://security.appspot.com/vsftpd.html
Summary     : Very Secure Ftp Daemon
Description :
vsftpd is a Very Secure FTP daemon. It was written completely from
scratch.
[root@localhost home]# service vsftpd status
Redirecting to /bin/systemctl status vsftpd.service
● vsftpd.service - Vsftpd ftp daemon
   Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2021-07-26 14:27:34 CST; 1min 9s ago
  Process: 26827 ExecStart=/usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf (code=exited, status=0/SUCCESS)
 Main PID: 26831 (vsftpd)
    Tasks: 1
   CGroup: /system.slice/vsftpd.service
           └─26831 /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf

Jul 26 14:27:34 localhost.localdomain systemd[1]: Starting Vsftpd ftp daemon...
Jul 26 14:27:34 localhost.localdomain systemd[1]: Started Vsftpd ftp daemon.
```

##### 5.主机清单文件中配置变量

1.主机变量

```yaml
[webserver]
192.168.83.02 http_port=80
192.168.83.03 http_port=8080
```

2.组变量

```yaml
[webserver]
192.168.83.02 
192.168.83.03
[webserver:vars]
http_port=80
```

主机变量的优先级更高

范例：

```yaml
#host文件
[webserver]
192.168.83.02 http_port=80 hostname=node1
192.168.83.03 http_port=8080 hostname=node2 

[webserver:vars]
domain=chen.com
```

结果：

```shell
[root@localhost playbook]# ansible webserver -m hostname -a 'name={{ hostname }}.{{ domain }}'
192.168.83.102 | CHANGED => {
    "ansible_facts": {
        "ansible_domain": "chen.com", 
        "ansible_fqdn": "node1.chen.com", 
        "ansible_hostname": "node1", 
        "ansible_nodename": "node1.chen.com", 
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "name": "node1.chen.com"
}
192.168.83.103 | CHANGED => {
    "ansible_facts": {
        "ansible_domain": "chen.com", 
        "ansible_fqdn": "node2.chen.com", 
        "ansible_hostname": "node2", 
        "ansible_nodename": "node2.chen.com", 
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "name": "node2.chen.com"
}

[root@localhost playbook]# ansible webserver -a 'hostname'
192.168.83.103 | CHANGED | rc=0 >>
node2.chen.com
192.168.83.102 | CHANGED | rc=0 >>
node1.chen.com
```



#### 8.template模板

模板是一个文本文件，可以作为生成文件的模板，并且模板文件中还可以嵌套jinja语法

##### 1.jinja2语言

jinja2语言使用字面量，有下面形式：

字符串：使用单引号或者双引号

数字:整数,浮点数

列表: [item1, item2, ..]

元组: (item1, item2, ..）

字典: {key1:value1, key2:value2..} 

布尔型: true/false

算术运算: +，-，*，/，/，%，**

比较操作: ==，！=，>，>=，<， <=

逻辑运算: and, or, not

流表达式: For, If, When

Jinja2相关

字面量:

表达式最简单的形式就是字面量.字面量表示诸如字符串和数值的Python对象。如"Hello World"

双引号或单引号中间的一-切都是字符串。无论何时你需要在模板中使用一一个字符串(比如函数调用、过滤器或只是包含或继承-个模板的参数)， 如42, 42.23

数值可以为整数和浮点数。如果有小数点，则为浮点数，否则为整数。在Python里，42 和42.0是不一样的

算术：

| 符号 | 说明                                                         |
| ---- | ------------------------------------------------------------ |
| +    | 把两个对象加到一起。通常对象是素质，但是如果两者是字符串或列表，你可以用这 种方式来衔接它们。无论如何这不是首选的连接字符串的方式！连接字符串见 ~ 运算符。 {{ 1 + 1 }} 等于 2 。 |
| -    | 用第一个数减去第二个数。 {{ 3 - 2 }} 等于 1 。               |
| /    | 对两个数做除法。返回值会是一个浮点数。 {{ 1 / 2 }} 等于 {{ 0.5 }} |
| //   | 对两个数做除法，返回整数商。 {{ 20 // 7 }} 等于 2            |
| %    | 计算整数除法的余数。 {{ 11 % 7 }} 等于 4                     |
| *    | 用右边的数乘左边的操作数。 {{ 2 * 2 }} 会返回 4 。也可以用于重 复一个字符串多次。{{ ‘=’ * 80 }} 会打印 80 个等号的横条 |
| **   | 取左操作数的右操作数次幂。 {{ 2**3 }} 会返回 8               |

比较操作符：

| 符号 | 说明                               |
| ---- | ---------------------------------- |
| ==   | 比较两个对象是否相等               |
| !=   | 比较两个对象是否不等               |
| >    | 如果左边大于右边，返回 true        |
| >=   | 如果左边大于等于右边，返回 true    |
| <    | 如果左边小于右边，返回 true        |
| <=   | 如果左边小于等于右边，返回 true 。 |

逻辑运算符：

| 符号   | 说明                                        |
| ------ | ------------------------------------------- |
| and    | 如果左操作数和右操作数同为真，返回 true     |
| or     | 如果左操作数和右操作数有一个为真，返回 true |
| not    | 对一个表达式取反（见下）                    |
| (expr) | 表达式组                                    |

其他：

| 符号 | 说明                                                         |
| ---- | ------------------------------------------------------------ |
| in   | 运行序列/映射包含检查。如果左操作数包含于右操作数，返回 true 。比如 {{ 1 in[1,2,3] }} 会返回 true |
| is   | 运行一个测试                                                 |
| \|   | 应用一个过滤器                                               |
| ~    | 把所有的操作数转换为字符串，并且连接它们。 {{ "Hello " ~ name ~ "!" }} 会返回（假设 name 值为 ''John' ） Hello John! |
| ()   | 调用一个可调用量:{{ post.render() }} 。在圆括号中，你可以像在 python 中一样使用位置参数和关键字参数：{{ post.render(user, full=true) }} 。 |
| ./[] | 获取一个对象的属性。                                         |

##### 2.template

说明：由于template模块还负责将最终生成的文件拷贝到远程主机上，所以还有一些常用的参数，可以用于设置配置文件的权限

```shell
src 			#指定控制端文件路径
dest 			#被控端文件路径
owner  			#指定最终生成的文件拷贝到远程主机后的属主。
group  			#指定最终生成的文件拷贝到远程主机后的属组。
mode			#指定最终生成的文件拷贝到远程主机后的权限，如果你想将权限设置为"rw-r–r--"，则可以使用mode=0644表示，如果你想要在user对应的权限位上添加执行权限，则可以使用mode=u+x表示。
force			#当远程主机的目标路径中已经存在同名文件，并且与最终生成的文件内容不同时，是否强制覆盖，可选值有yes和no，默认值为yes，表示覆盖，如果设置为no，则不会执行覆盖拷贝操作，远程主机中的文件保持不变。
backup			#当远程主机的目标路径中已经存在同名文件，并且与最终生成的文件内容不同时，是否对远程主机的文件进行备份，可选值有yes和no，当设置为yes时，会先备份远程主机中的文件，然后再将最终生成的文件拷贝到远程主机。
```

template功能：可以根据和参考模块文件，动态生成相类似的配置文件

template文件必须存放在templates目录下，且命名为.j2结尾

yaml/yml文件需和templates目录平级，目录结构如下

```shell
├── temp.yml
└── templates
    └── temp_template.j2
```

范例：

```yaml
#templnginx.yml
---
- hosts: webserver
  remote_user: root

  tasks:
    - name: install nginx
      yum: name=nginx state=installed
    - name: template config to remote hosts
      template: src=nginx.conf.j2 dest=/etc/nginx.conf
    - name: start service
      service: name=nginx state=started  enabled=yes
     
#nginx.conf.j2
[root@localhost temp]# cat templates/nginx.conf.j2
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes 6;
```

```shell
[root@localhost temp]# ansible-playbook templnginx.yml 
PLAY [webserver] ***************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************
ok: [192.168.83.103]
ok: [192.168.83.102]

TASK [install nginx] ***************************************************************************************************************
ok: [192.168.83.103]
changed: [192.168.83.102]

TASK [template config to remote hosts] ***************************************************************************************************************
changed: [192.168.83.103]
changed: [192.168.83.102]

TASK [start service] ***************************************************************************************************************
ok: [192.168.83.103]
changed: [192.168.83.102]

PLAY RECAP ***************************************************************************************************************
192.168.83.102: ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.83.103: ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[root@localhost temp]# ansible webserver -a 'service nginx status'
192.168.83.103 | CHANGED | rc=0 >>
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2021-07-26 16:37:12 CST; 6h ago
192.168.83.102 | CHANGED | rc=0 >>
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2021-07-26 16:17:20 CST; 1min 15s ago
```

##### 3.使用for 和 if

=={% %}== ：用来装载控制语句，比如 if 控制结构，for循环控制结构。

范例：

```yaml
----------------------------------------------变量单一值
#nginx.conf.j2   
{% for vhost in nginx_vhosts %}
server{
  listen {{ vhost }};
}
{% endfor %}

#tempnginx.yml
---
- hosts: webserver
  remote_user: root
  vars:
  	nginx_vhosts:
  	  - 81
  	  - 82
  	  - 83
  tasks:
    - name: template config to remote hosts
      template: src=nginx.conf.j2 dest=/etc/nginx.conf
      
----------------------------------------------变量是字典
#nginx.conf2.j2
{% for vhost in nginx_vhosts %}
server{
  listen {{ vhost.listen }};
}
{% endfor %}
#tempnginx2.yml
---
- hosts: webserver
  remote_user: root
  vars:
        nginx_vhosts:
          - listen: 8080

  tasks:
    - name: template config to remote hosts
      template: src=nginx.conf2.j2 dest=/home/ansible/nginx2.conf
      
----------------------------------------------变量是字典，用多个键值
#nginx.conf3.j2
{% for vhost in nginx_vhosts %}
server{
  listen {{ vhost.listen }};
  server_name {{ vhost.server_name }};
  root {{ vhost.root }}
}
{% endfor %}
#tempnginx3.yml
---
- hosts: webserver
  remote_user: root
  vars:
        nginx_vhosts:
          - listen: 8080
            server_name: "curry.com"
            root: "/var/www/nginx/web1"
          - listen: 8081
            server_name: "chenzb.com"
            root: "/var/www/nginx/web2"            
  tasks:
    - name: template config to remote hosts
      template: src=nginx.conf3.j2 dest=/home/ansible/nginx3.conf
```

结果：

```shell
[root@localhost test_for]# ansible webserver -a 'cat /home/ansible/nginx.conf'
192.168.83.103 | CHANGED | rc=0 >>
server{
  listen 81;
}
server{
  listen 82;
}
server{
  listen 83;
}
192.168.83.102 | CHANGED | rc=0 >>
server{
  listen 81;
}
server{
  listen 82;
}
server{
  listen 83;
}


[root@localhost test_for]# ansible webserver -a 'cat /home/ansible/nginx2.conf'
192.168.83.103 | CHANGED | rc=0 >>
server{
  listen 8080;
}
192.168.83.102 | CHANGED | rc=0 >>
server{
  listen 8080;
}

[root@localhost test_for]# ansible webserver -a 'cat /home/ansible/nginx3.conf'
192.168.83.103 | CHANGED | rc=0 >>
server{
  listen 8080;
  server_name curry.com;
  root /var/www/nginx/web1
}
server{
  listen 8081;
  server_name chenzb.com;
  root /var/www/nginx/web2
}
```



if语句

范例：

```yaml
#nginx.conf4.j2
{% for vhost in nginx_vhosts %}
server{
  listen {{ vhost.listen }};
  {{% if vhost.server_name is defined %}}
  	server_name {{ vhost.server_name }};
  {% endif %}
  root {{ vhost.root }}
}
{% endfor %}
#tempnginx4.yml
---
- hosts: webserver
  remote_user: root
  vars:
        nginx_vhosts:
          - listen: 8080
            root: "/var/www/nginx/web1"
          - listen: 8081
            server_name: "chenzb.com"
            root: "/var/www/nginx/web2"            
  tasks:
    - name: template config to remote hosts
      template: src=nginx.conf4.j2 dest=/home/ansible/nginx4.conf
```

结果：

```shell
[root@localhost test_for]# ansible webserver -a 'cat /home/ansible/nginx4.conf'
192.168.83.103 | CHANGED | rc=0 >>
server{
  listen 8080;
    root /var/www/nginx/web2
}
server{
  listen 8081;
      server_name chenzb.com;
    root /var/www/nginx/web2
}
```

#### 4.playbook的when语句

when语句可以实现条件测试，如果需要根据变量、facts或此前任务的执行结果来为某task执行与否的前提时，要用到条件测试通过在task后添加when子句既可以使用条件测试，jinja2的语法格式

范例：

```yaml
---
- hosts: webserver
  remote_user: root
  
  tasks:
    - name: "shutdown redhat system"
      command: /sbin/shutdown -h now
      when: ansible_os_family == "RedHat"
    - name: install conf file to centos7
      template: src=nginx.conf.c7.j2 dest=/etc/nginx/nginx.conf
      when: ansible_distribution_major_version == "7"
    - name: install conf file to centos7
      template: src=nginx.conf.c6.j2 dest=/etc/nginx/nginx.conf
      when: ansible_distribution_major_version == "6"
```

#### 5.playbook的with_items语句

当有需要重复执行的任务时，可以使用迭代机制

对迭代项的引用，固定变量名为“item”

要在task中使用with_items给定要迭代的元素列表

==列表元素==

- 字符串
- 字典

范例：

```yaml
---
- hosts: webserver
  remote_user: root
  
  tasks:
    - name: "add users"
      user: name={{ item }} state=present groups=wheel
      with_items:
        - testuser1
        - testuser2
        
=====================上下等价===========================        
        
    - name: add user1
      user: name=testuser1 state=present groups=wheel
    - name: add user2
      user: name=testuser2 state=present groups=wheel
      
      
------------------------------------------------
#迭代中嵌套子变量，关联多个变量在一起使用
---
- hosts: webserver
  remote_user: root
  
  tasks:
    - name: "add group"
      group: name={{ item }} state=present groups=wheel
      with_items:
        - nginx
        - mysql
        - apache
    - name: "add users"
      group: name={{ item.name }} group={{ item.group }} state=present 
      with_items:
        - { name:'nginx', group='nginx'}
        - { name:'mysql', group='mysql'}
        - { name:'apache', group='apache'}
```

结果：

```shell
[root@localhost test_when]# ansible webserver -a 'id testuser1'
192.168.83.103 | CHANGED | rc=0 >>
uid=1002(testuser1) gid=1002(testuser1) groups=1002(testuser1),10(wheel)
192.168.83.102 | CHANGED | rc=0 >>
uid=1003(testuser1) gid=1003(testuser1) groups=1003(testuser1),10(wheel)
[root@localhost test_when]# ansible webserver -a 'id testuser2'
192.168.83.103 | CHANGED | rc=0 >>
uid=1003(testuser2) gid=1003(testuser2) groups=1003(testuser2),10(wheel)
192.168.83.102 | CHANGED | rc=0 >>
uid=1004(testuser2) gid=1004(testuser2) groups=1004(testuser2),10(wheel)



---------------------------------迭代嵌套
[root@localhost test_when]# ansible webserver -a 'cat /etc/passwd'
192.168.83.103 | CHANGED | rc=0 >>
nginx:x:1001:1001::/home/nginx:/bin/bash
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
mysql:x:1004:1004::/home/mysql:/bin/bash
192.168.83.102 | CHANGED | rc=0 >>
mysql:x:306:306::/data/mysql:/sbin/nologin
nginx:x:304:304:Nginx web server:/var/lib/nginx:/sbin/nologin
apache:x:1005:1005::/home/apache:/bin/bash
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



## 7.roles角色

角色是ansible自1.2版本引入的新特性，用于层次性、结构化地组织playbook。roles能够根据层次型结构自动装载变量文件、tasks以及handlers等。 要使用roles只需要在playbook中使用include指令即可。 简单来讲，roles就是通过分别将变量、文件、任务、模板及处理器放置于单独的目录中，并可以便捷地include它们的一种机制。角色一般用于基于主机构建服务的场景中，但也可以是用于构建守护进程等场景中

运维复杂的场景:建议使用roles, 代码复用度高

roles:多个角色的集合，可以将多 个的role,分别放至roles目录下的独立子目录中

```bash
roles/
	mysql/
	httpd/
	nginx/
	redis/
	
```

结构示例：

![image-20210726195743901](D:\Users\yl4032\AppData\Roaming\Typora\typora-user-images\image-20210726195743901.png)

#### 1.roles目录

roles/project/ :项目名称有以下子目录

- files/: 存放由copy或script模块等调用的文件

- templates/: template模块查找所需要模板文件的目录

- tasks/: 定义task.role的基本元素， 至少应该包含一个名为main,ym的文件;其它的文件需要在此文件中通过include进行包含

- handlers/: 至少应该包含一一个名为main.yml的文件; 其它的文件需要在此文件中通过include进行包含

- vars/: 定义变量，至少应该包含一一个名为main.yml的文件;其它的文件需要在此文件中通过include进行包含
- meta/: 定义当前角色的特殊设定及其依赖关系,至少应该包含一个名为main.ym的文件，其它文件需在此文件中通过include进行包含

- default/: 设定默认变量时使用此目录中的main.yml文件，比vars的优先级低

#### 2.创建role

创建role的步骤

1. 创建以roles命名的目录
2. 在roles目录中分别创建以各角色名称命名的目录，如webservers等
3. 在每个角色命名的目录中分别创建files. handlers. meta. tasks. templates和vars目录; 用不到的目录可以创建为空目录，也可以不创建
4.  在playbook文件中，调用各角色

针对大型项目使用Roles进行编排

范例: roles的目录结构

#### 3.调用roles

方法1：

```yaml
--- 
- hosts: webserver
  remote_user: root
  
  roles:
    - mysql
    - memcached
    - nginx
```

方法2：

```yaml
--- 
- hosts: webserver
  remote_user: root
  
  roles:
    - mysql
    - memcached
    - { role: nginx, username: nginx }
```

方法3：

```yaml
--- 
- hosts: webserver
  remote_user: root
  
  roles:
    - mysql
    - memcached
    - { role: nginx, username: nginx, when: ansible_distribution_version="7" }
```

#### 4.roles中tags的应用

```yaml
--- 
- hosts: webserver
  remote_user: root
  
  roles:
    - { roles: mysql ,tags: [ 'mysql','db' ] }
    - { roles: memcached ,tags: [ 'memcached','db' ] }
    - { role: nginx, username: nginx, ,tags: [ 'nginx','web' ] ,when: ansible_distribution_version="7" }
    - { role: httpd, username: httpd, ,tags: [ 'httpd','web' ] ,when: ansible_distribution_version="7" }
    
ansible-playbook --tags="nginx,httpd,mysql"
```

## 8.实例

#### 1.httpd角色

```bash
#文件目录
.
├── role_httpd.yml
└── roles
    └── httpd
        ├── files
        │   ├── httpd.conf
        │   └── index.html
        ├── handlers
        │   └── main.yml
        └── tasks
            ├── config.yml
            ├── index.yml
            ├── install.yml
            ├── main.yml
            └── service.yml
```

```yaml
#main.yml
- include: install.yml
- include: config.yml
- include: index.yml
- include: service.yml
  
#install.yml
- name: install httpd
  yum: name=httpd
 
#config.yml
- name: config file
  copy: src=httpd.conf dest=/etc/httpd/conf/ backup=yes
  notify: restart

#index.yml
- name: index.html
  copy: src=index.html dest=/var/www/html
  
#service.yml
- name: start service
  service: name=httpd state=started enabled=yes

```

#### 2.nginx角色

```bash
.
├── files
│   └── nginx.conf
├── handlers
│   └── main.yml
├── tasks
│   ├── config.yml
│   ├── index.yml
│   ├── install.yml
│   ├── main.yml
│   └── service.yml
├── template
│   ├── nginx.conf7.j2
│   └── nginx.conf8.j2
└── vars
    └── main.yml
```

```yaml
#main.yml
- include: install.yml
- include: config.yml
- include: index.yml
- include: service.yml

#install.yml
- name: install nginx
  yum: name=nginx state=installed
 
#config.yml
- name: config file for centos7
  copy: src=nginx7.conf.j2 dest=/etc/nginx/nginx.conf
  when: ansible_distribution_major_version=="7"
  notify: restart
- name: config file for centos8
  copy: src=nginx8.conf.j2 dest=/etc/nginx/nginx.conf
  when: ansible_distribution_major_version=="8"
  notify: restart

#index.yml       
- name: index.html
  copy: src=roles/httpd/files/index.html dest=/usr/share/nginx/html/            #跨角色调用路径要从roles开始写
  
#service.yml
- name: start service
  service: name=nginx state=started enabled=yes

#nginx7.conf.j2
user {{ user_103 }};
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

#nginx8.conf.j2
user {{ user_102 }};
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

#vars/main.yml 
user_103: daemon
user_102: czb
```

```bash
[root@localhost test]# ansible webserver -a 'service nginx status'
192.168.83.103 | CHANGED | rc=0 >>
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-07-27 11:25:27 CST; 1min 34s ago

192.168.83.102 | CHANGED | rc=0 >>
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-07-27 11:25:23 CST; 1min 34s ago
[root@localhost test]# ansible webserver -a 'ss -ntl -p'
192.168.83.103 | CHANGED | rc=0 >>
State      Recv-Q Send-Q    Local Address:Port         Peer Address:Port              
LISTEN     0      128       [::]:80                    [::]:*                   
users:(("nginx",pid=33801,fd=7),("nginx",pid=33800,fd=7),("nginx",pid=33799,fd=7),("nginx",pid=33798,fd=7),("nginx",pid=33797,fd=7))
192.168.83.102 | CHANGED | rc=0 >>
State      Recv-Q Send-Q    Local Address:Port         Peer Address:Port              
LISTEN     0      128       [::]:80                    [::]:*                   
users:(("nginx",pid=48516,fd=7),("nginx",pid=48515,fd=7),("nginx",pid=48514,fd=7),("nginx",pid=48513,fd=7),("nginx",pid=48512,fd=7))

#ps aux 查看102的进程，nginx的账户是czb。
root      59957  0.0  0.0  39304  1044 ?        Ss   14:00   0:00 nginx: master process /usr/sbin/nginx
czb       59958  0.0  0.0  41776  1932 ?        S    14:00   0:00 nginx: worker process
czb       59959  0.0  0.0  41776  1932 ?        S    14:00   0:00 nginx: worker process
czb       59960  0.0  0.0  41776  1932 ?        S    14:00   0:00 nginx: worker process
czb       59961  0.0  0.0  41776  1932 ?        S    14:00   0:00 nginx: worker process
#ps aux 查看103的进程，nginx的账户是daemon。
root      33797  0.0  0.0  39304  1052 ?        Ss   11:25   0:00 nginx: master process /usr/sbin/nginx
daemon    33798  0.0  0.0  41776  1940 ?        S    11:25   0:00 nginx: worker process
daemon    33799  0.0  0.0  41776  1940 ?        S    11:25   0:00 nginx: worker process
daemon    33800  0.0  0.0  41776  1940 ?        S    11:25   0:00 nginx: worker process
daemon    33801  0.0  0.0  41776  1940 ?        S    11:25   0:00 nginx: worker process
```

#### 3.memcached角色

文件列表：

```bash
roles/memcached/
├── files
├── handlers
├── tasks
│   ├── config.yml
│   ├── install.yml
│   ├── main.yml
│   └── service.yml
├── templates
│   └── memcached.j2
└── vars
```

文件清单：

```yaml
#main.yml
---
- include: install.yml
- include: config.yml
- include: service.yml

#install.yml
---
- name: install memcached
  yum: name=memcached state=installed
 
#config.yml
---
- name: config files
  template: src=memcached.j2 dest=/etc/sysconfig/memcached

#service.yml
---
- name: start service
  service: name=memcached state=started

#memcached.j2 
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE=" {{ ansible_memtotal_mb//4 }} "
OPTIONS=""


```

结果：

```bash
[root@localhost test]# ansible webserver -a 'cat /etc/sysconfig/memcached'
192.168.83.103 | CHANGED | rc=0 >>
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE=" 942 "
OPTIONS=""
192.168.83.102 | CHANGED | rc=0 >>
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE=" 942 "
OPTIONS=""

#memcached默认端口为11211
[root@localhost test]# ansible webserver -a 'ss -ntl'
192.168.83.103 | CHANGED | rc=0 >>
State      Recv-Q Send-Q   Local Address:Port               Peer Address:Port                            
LISTEN     0      128                  *:11211                         *:*                             
192.168.83.102 | CHANGED | rc=0 >>
State      Recv-Q Send-Q   Local Address:Port               Peer Address:Port                           
LISTEN     0      128               [::]:11211                      [::]:*       

[root@localhost test]# ansible webserver -a 'service memcached status'
[WARNING]: Consider using the service module rather than running 'service'.  If you need to use command because service is insufficient you can add 'warn: false' to this command task or set
'command_warnings=False' in ansible.cfg to get rid of this message.
192.168.83.103 | CHANGED | rc=0 >>
● memcached.service - Memcached
   Loaded: loaded (/usr/lib/systemd/system/memcached.service; disabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-07-27 14:33:31 CST; 7min ago
 Main PID: 46476 (memcached)
    Tasks: 6
   CGroup: /system.slice/memcached.service
           └─46476 /usr/bin/memcached -u memcached -p 11211 -m 942 -c 1024
192.168.83.102 | CHANGED | rc=0 >>
● memcached.service - Memcached
   Loaded: loaded (/usr/lib/systemd/system/memcached.service; disabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-07-27 14:33:27 CST; 7min ago
 Main PID: 62088 (memcached)
    Tasks: 6
   CGroup: /system.slice/memcached.service
           └─62088 /usr/bin/memcached -u memcached -p 11211 -m 942 -c 1024  
```

#### 4.mysql角色

```bash
#cnf
[mysqld]
socket=/tmp/mysql.sock
user=mysql
symbolic-link=0
datadir=/data/mysql
innodb_file_per_table=1
log-bin
pid-file=/data/mysql/mysql.pid

[client]
port=3306
socket=/tmp/mysql.sock

[mysqld_safe]
log-error=/var/mysqld.log


yml
---
- hosts: dbserver
  remote_user: root
  gather_facts: no

  tasks:
    - name: "创建组"
      group: name=mysql system=yes gid=306
    - name: "创建用户"
      user: name=mysql shell=/sbin/nologin system=yes group=mysql uid=306 home=/data/mysql create_home=no
    - name: copy tar to remote host and file mode
      unarchive: src=/home/playbook/test_mysql/mysql-8.0.26-linux-glibc2.12-x86_64.tar.xz dest=/usr/local/ owner=root group=root
    - name: creat linkfile /usr/local/mysql
      file: path=/usr/local/mysql src=/usr/local/mysql-8.0.26-linux-glibc2.12-x86_64 state=link
    - name: data dir
      shell: chdir=/usr/local/mysql/bin ./mysqld --defaults-file=/etc/my.cnf --basedir=/usr/local/mysql --datadir=/data/mysql --user=mysql --initialize
      tags: data
    - name: config my.cnf
      copy: src=/home/playbook/test_mysql/my.cnf dest=/etc/my.cnf
    - name: service script
      shell: /bin/cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysqld
    - name: enable service
      shell: /etc/init.d/mysqld start;chkconfig --add mysql;chkconfig mysqld on
      tags: service
    - name: PATH variable
      copy: content='PATH=/usr/local/mysql/bin:$PATH' dest=/etc/profile.d/mysql.sh
    - name: secure script
      script: /home/playbook/test_mysql/secure_mysql.sh
      tags: script

```

