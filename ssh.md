# win10配置VScode remote-ssh(免密登录)
## 修订记录 
| 日期 | 修订版本 | 修改描述 | 作者| 审核|
| --- | --- |--- |--- |--- |
| 2021.07.07| V1.0| 初稿版本 | 许泽超|  |

## 配置步骤：
### 免密登录
*  1.生成SSH密钥和公钥
    * 在cmd下输入“ssh-keygen -t rsa -b 4096”，然后连敲三下Enter就完成了。密钥id_rsa和公钥id_rsa.pub文件保存在(D:\Users\yl4030\.ssh)文件夹下。
*  2.将公钥文件id_rsa.pub传到远程服务器的authorized_keys文件中
    *  在cmd下输入“SET REMOTEHOST=root@49.52.10.120”，其中“root”是服务器的用户名,“49.52.10.120”是远程服务器的ip。
    *  在cmd下输入“scp %USERPROFILE%\\.ssh\id_rsa.pub %REMOTEHOST%:~/tmp.pub”，把本地的公钥拷贝到当前目录下名为tmp.pub的临时文件。
    *  在cmd下输入“ssh %REMOTEHOST% "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat ~/tmp.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && rm -f ~/tmp.pub"”。
### VScode配置
* 1.下载插件Remote-SSH
* 2.Ctrl+Shift+p 选择Connect to Host
* 3.修改config文件
    * Host xzc --主机名
    * User root --用户名
    * HostName 49.52.10.120 --IP地址
* 保存，打开文件

# linux生成密钥GitLab下载文件

## 1.在本地生成密钥

命令：ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa

## 2.进入.ssh文件夹，创建保存密钥的文件

命令：touch authorized_keys

## 3.把秘钥复制到这个文件里

命令：cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys

## 4.把本地的公钥复制到指定机器上

### <font color=red>直接复制到gitlab的设置里的SSH密钥，然后进行git clone</font>

命令：scp id_dsa.pub root@node1:~/.ssh/authorized_keys
