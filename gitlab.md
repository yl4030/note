# gitlab

## gitlab安装

### 1.安装并配置必要的依赖

```shell
yum install -y curl policycoreutils-python openssh-server perl
# Enable OpenSSH server daemon if not enabled: systemctl status sshd
systemctl enable sshd
systemctl start sshd
# Check if opening the firewall is needed with: systemctl status firewalld
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
systemctl reload firewalld
```

### 2.添加gitlab包仓库并安装包

```shell
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.rpm.sh | sudo bash
EXTERNAL_URL="https://192.168.37.110:443" yum install -y gitlab-ee
```



```shell
#vim /etc/gitlab/gitlab.rb
external_url 'https://192.168.37.110:443'
#vim /opt/gitlab/embedded/service/gitlab-rails/config/gitlab.yml
host: 192.168.37.110
port: 443
https: ture

gitlab-ctl restart #重启
```

3.访问https://192.168.37.110:443

```shell
用户名：root
密码：cat /etc/gitlab/initial_root_password
#重置用户密码
[root@master ~]# gitlab-rake "gitlab:password:reset"
Enter username: root
Enter password: rootrootroot
Confirm password: rootrootroot
Password successfully updated for user with username root.
```

## gitlab-runner(了解)

### 1.下载安装

```shell
# Download the binary for your system
curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

# Give it permissions to execute
chmod +x /usr/local/bin/gitlab-runner

# Create a GitLab CI user
useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

# Install and run as service
gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
gitlab-runner start
```

### 2.注册runner

```
gitlab-runner register --url https://192.168.37.110/ --registration-token $REGISTRATION_TOKEN 
```

- For a [shared runner](https://docs.gitlab.com/ee/ci/runners/#shared-runners), have an administrator go to the GitLab Admin Area and click **Overview > Runners**

  <img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210810143753897.png" alt="image-20210810143753897" style="width:100%;" />

  

- For a [specific runner](https://docs.gitlab.com/ee/ci/runners/README.html#specific-runners), go to **Settings > CI/CD** and expand the **Runners** section

  ![image-20210810151935113](D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210810151935113.png)

# Git

## 1.git branch

```shell
git branch test
git branch #查看本地分支
git branch -a #查看所有分支
git branch -r #查看远程分支
git branch -f test C1 #移动分支
git branch -D test #删除本地2.git checkout
git branch -u o/main test #远程追踪（push test相当于push main）
git branch -m oldname newname #分支重命名
```

## 2.git checkout

```shell
git checkout test #进入分支
git checkout -b test  #创建并进入分支
git checkout -b test o/main #远程追踪（push test相当于push main）
```

## 3.git commit

```shell
git commit -m 'message' #提交
git commit -a -m 'message' #提交修改的commit
git commit --amend --message="modify message by daodaotest" --author="yl4030" # 修改最近提交的 commit 信息
```

## 4.git fetch

```shell
git fetch #下载远程的改动（不合并）
```

## 5.git merge 

```shell
git merge test #与test分支合并
```

## 6.git rebase

```shell
git rebase test #合并到test分支(创造更线性的提交历史,代码库的提交历史将会变得异常清晰。)
git rebase test1 test2 #合并test2到test1分支
```

## 7.git pull

```shell
git pull #下载远程分支并合并（相当于git fetch + git merge）
git pull --rebase #下载远程分支并合并（相当于git fetch + git rebase）
```

## 8.git push

```shell
git push #提交本地修改
git push origin --delete test #删除远程分支
```

## 9.git remote

```shell
###删除远程分支后###
git remote show origin #可以看到删除分支情况
git remote prune origin
```

## 10.git add

```shell
#添加文件到暂存区
git add . git add test
```

## 11.git rm

```shell
#删除文件
git rm test
```

## 12.git status

```shell
git status #查看在你上次提交之后是否有对文件进行再次修改
```

## 13.git clone

```shell
git clone git@gitcode.yealink.com:pipelines/observability/extra-monitoring-cd.git #克隆远程仓库
```

## 14.git init

```shell
git init #初始化仓库
```

## 15.git diff

```shell
git diff #比较文件的不同，即暂存区和工作区的差异
```

## 16.git log 

```shell
git log #按时间先后顺序列出所有的提交
```

## 16.git reset

```shell
git reset 8c267a58edf666d57bc43760fc86b9328b1b171e #回退版本（git log 查看）
```

## 17.git stash

```shell
#git分支更新主分支代码
git reset --soft HEAD^   #退回到前一次提交
git stash #把mybranch更新的内容stash
git checkout master  #checkout master分支
git pull
git branch -D mybranch #删除本地mybranch分支
git checkout -b mybranch
git stash pop  #stash pop后如果有冲突要解决冲突
git add .
git commit -m""
git push origin mybranch -f
```

# Gitlab-CI

## 1.基本概念

CI，为持续集成。即在代码构建过程中持续地进行代码的集成、构建、以及自动化测试等；有了 CI 工具，我们可以在代码提交的过程中通过单元测试等尽早地发现引入的错误；

GitLab CI/CD（后简称 GitLab CI）是一套基于 GitLab 的 CI/CD 系统，可以让开发人员通过 .gitlab-ci.yml 在项目中配置 CI/CD 流程，在提交后，系统可以自动/手动地执行任务，完成 CI/CD 操作。ci流程在每次团队成员**push/merge**后之后触发。每当你push/merge一次，gitlab-ci都会检查项目下有没有.gitlab-ci.yml文件，如果有，它会执行你在里面编写的脚本，并完整地走一遍从**intall =>** **eslint检查=>编译 =>部署服务器**的流程

```bash
#########################################  一个Pipleline有若干个stage,每个stage上有至少一个Job  ########################################
Job 
#Job 为任务，是 GitLab CI 系统中可以独立控制并运行的最小单位。 在提交代码后，开发者可以针对特定的 commit 完成一个或多个 job，从而进行 CI/CD 操作。

Pipeline 
#Pipeline 即流水线，可以像流水线一样执行多个 Job. 在代码提交或 MR 被合并时，GitLab 可以在最新生成的 commit 上建立一个 pipeline，在同一个 pipeline 上产生的多个任务中，所用到的代码版本是一致的。

Stage 
#一般的流水线通常会分为几段；在 pipeline中，可以将多个任务划分在多个阶段中，只有当前一阶段的所有任务都执行成功后，下一阶段的任务才可被执行。
```

## 2.gitlab-ci.yml

### 2.1. gitlab-ci.yml配置关键字

```bash
stages/stage #定义了任务所属的阶段
image #字段指定了执行任务时所需要的 docker 镜像
services #指定了执行任务时所需的依赖服务（如数据库、Docker 服务器等）
before_script #开始执行脚本前所需执行脚本
script #直接定义了任务所需执行的命令
after_script #每个任务的脚本执行完后所需执行脚本
tags #tags是当前Job的标记，这个tags关键字是很重要，因为gitlab的runner会通过tags去判断能否执行当前这个Job
variables #定义构建变量（变量将会被设置入任务环境并存储在git仓库里【应是非敏的项目配置】）
cache: #缓存（1.在不同pipeline之间重用资源 2.在同一pipeline的不同Job之间重用资源）
artifacts #当这个job执行成功后，其结果所保存的地方。将生成的资源作为pipeline运行成功的附件上传，并在gitlab交互界面上提供下载
only/except #后面跟的值是tag或者分支名的列表（only的作用是指定当前Job仅仅只在某些tag或者branch上触发，except的作用是当前Job不在某些tag或者branch上触发）
allow_failure #值为true/false, 表示当前Job是否允许允许失败。默认是false,如果当前Job因为报错而失败，则当前pipeline停止。true，则即使当前Job失败，pipeline也会继续运行下去）
retry #当前Job的失败重试次数的上限（最多重试两次）
timeout #配置超时时间，超过时间判定为失败
When
#表示当前Job在何种状态下运行，它可设置为3个值
#  on_success: 仅当先前pipeline中的所有Job都成功（或因为已标记，被视为成功allow_failure）时才执行当前Job 。这是默认值。
#  on_failure: 仅当至少一个先前阶段的Job失败时才执行当前Job。
#  always: 执行当前Job，而不管先前pipeline的Job状态如何。
needs #调整job执行顺序
#例：job1: stage:first | job2: stage:first | job3: stage:second needs:[job1]
#  则job1和job2并行。job1执行完成后立即执行job3，不会等job2完成任务
rules #设定一系列的规则，以此来判断是否能够创建/执行这个job，不能够与only / except共用
#  if：定义一个规则，类似于：only:variables
#  when：目前只支持always和never，如果没有设置，则默认为always
#  changes：类似于：only:changes
#  changes： if：tag == null 如果没有（打tag）并且发生改变 
#  exists
dependencies #定义这个job所依赖的job是哪一个。例：先build项目，再deploy项目。那么deploy就依赖于build，如果build失败了，那么deploy也不会执行
parallel #定义这个job会被多少个线程并行执行
pages #将job执行的结果，上传到执行的位置
```

### 2.2. YML的片段复用和模块化

- 使用 **&**符号可以定义一个片段的别名
- 使用 **<<**符号和 ***** 符号可以将别名对应的YML片段导入

```yml
.common-config: &commonConfig
  only: # 表示仅在develop/release分支上执行
    refs:
      - develop
      - release
install-job:
  # 其他配置 ....
  <<: *commonConfig
build-job:
  # 其他配置 ....
  <<: *commonConfig
#------------------------------------------------ 等价于extends（可读性更好一些）------------------------------------------------#
.common-config: 
  only: # 表示仅在develop/release分支上执行
    refs:
      - develop
      - release
install-job:
  # 其他配置 ....
  extends: .common-config

build-job:
  # 其他配置 ....
  extends: .common-config
```

- include合并yml

```yml
 #例如我们有如下的YML结构
 ├── .gitlab-ci.h5.yml'
 ├── .gitlab-ci.bd.yml'
 ├── .gitlab-ci.wx.yml
 └── .gitlab-ci.yml
 #那么在.gitlab-ci.yml中这么写，就可以对它们做合并
 include:
  - '/.gitlab-ci.wx.yml'
  - '/.gitlab-ci.bd.yml'
  - '/.gitlab-ci.h5.yml'
```

