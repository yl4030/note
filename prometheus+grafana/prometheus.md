# Prometheus

## go环境安装

由于Prometheus是由go语言开发的，所以在安装Prometheus之前需要先在监控主机上安装go环境。

### 1.下载解压

```shell
wget https://golang.org/dl/go1.16.6.linux-amd64.tar.gz # https://golang.org/dl/
tar -xvf go1.16.6.linux-amd64.tar.gz
```

### 2.配置环境变量

```shell
vim /etc/profile
# 在最后一行添加
export GOROOT=/home/software/go # 根据本地实际地址
export PATH=$PATH:$GOROOT/bin
# wq保存退出后source一下
source /etc/profile
# 验证
go version
```

## Prometheus安装

### 1.下载解压

```bash
wget https://prometheus.io/download/prometheus-*.tar.gz #下载最新版本
tar xvfz prometheus-*.tar.gz
mv prometheus-* prometheus
cd prometheus
./prometheus --version
```

### 2.修改配置文件，确定启动ip

```bash
vim prometheus.yml
```

```yaml
# my global config
global:
  scrape_interval:     15s # 指标采集间隔，默认为15s
  scrape_timeout: 10s       # 指标采集超时时间，默认为10s。注意scrape_timeout必须小于scrape_interval，所以scrape_timeout和scrape_interval一般情况成对出现
  evaluation_interval: 15s # 触发告警检测的时间（默认一分钟）
  metrics_path: /metrics    # 可选项；指标采集路径，默认为/metrics
  # scrape_timeout is set to the global default (10s).
 
# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # 配置连通alertmanager 
      - 192.168.37.101:9093
 
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
    - "/home/software/prometheus/rules.yml" #告警规则
 
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
 # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'
 
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
 
    static_configs:
    - targets: ['192.168.37.101:9090']
 
  - job_name: 'centos7-machine1'
    scrape_interval: 10s
    static_configs:
      - targets: ['192.168.37.101:9100']
        labels:
          instance: master

  - job_name: 'centos7-machine2'
    scrape_interval: 10s
    static_configs:
      - targets: ['192.168.37.102:9100']
        labels:
          instance: node02

  - job_name: 'centos7-machine3'
    scrape_interval: 10s
    static_configs:
      - targets: ['192.168.37.104:9100']
        labels:
          instance: node04
```

### 3.告警规则

语法检查规则

```shell
./promtool check rules /path/to/example.rules.yml
```

```shell
vim rules.yml
```

```yaml
groups:
- name: example 
  rules:
  ################### Alerting rules ###################
  - alert: test # 告警规则的名称。
    expr: rate(prometheus_http_requests_total[5m]) >= 0 # 基于PromQL表达式告警触发条件，用于计算是否有时间序列满足该条件。
    for: 1s # 评估等待时间，可选参数。用于表示只有当触发条件持续一段时间后才发送告警。在等待期间新产生告警的状态为pending。
    labels: #自定义标签，允许用户指定要附加到告警上的一组附加标签。
      severity: warning # 严重等级依次递增(warning、critical和emergency)
    annotations: # 用于指定一组附加信息，比如用于描述告警详细信息的文字等，annotations的内容在告警产生时会一同作为参数发送到Alertmanager。
      summary: this is a test!!!!!!!
  - alert: InstanceDown
    expr: up == 0
    for: 5s
    labels:
      severity: warning
    annotations:
      summary: "Instance {{$labels.instance}} down"
      description: "{{$labels.instance}} of job {{$labels.job}} has been down for more than 5 s."
      
  ################### Recording rules ###################
  #Prometheus 会在后台完成 expr 中定义的 PromQL 表达式计算，并且将计算结果保存到新的时间序列 record 中，同时还可以通过 labels 标签为这些样本添加额外的标签。
  - record: job:http_inprogress_requests:sum # record语句运行速度比expr快
    expr: sum by (job) (http_inprogress_requests) # 将以预定义的时间间隔进行评估，并存储为新的record
    # 添加或者覆盖的标签(可要可不要)
    labels:
      severity: warning
  - record: namespace:container_cpu_usage_seconds_total:sum_rate  
    expr: 
      sum(rate(container_cpu_usage_seconds_total{image!="", container!=""}[5m])) by (namespace)
```

### 4.配置服务配置文件 

```shell
vim /usr/lib/systemd/system/prometheus.service
```

```yaml
[Unit]
Description=Prometheus
Documentation=https://prometheus.io/
After=network.target


[Service]
# Type设置为notify时，服务会不断重启
Type=simple
User=root
# --storage.tsdb.path是可选项，默认数据目录在运行目录的./dada目录中
ExecStart=/home/software/prometheus/prometheus --config.file=/home/software/prometheus/prometheus.yml --storage.tsdb.path=/home/software/prometheus/software/prometheus-data #注意路径
Restart=on-failure

[Install]

WantedBy=multi-user.target

```

### 5.启动服务 

```bash
systemctl daemon-reload
systemctl enable prometheus
systemctl start prometheus
systemctl status prometheus
```

### 6.打开prometheus的web ui界面 

![image-20210808184235268](D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210808184235268.png)

## 部署node_exporter

### 1.下载解压

```bash
wget https://prometheus.io/download/node_exporter-*.tar.gz #下载最新版本
tar xvfz node_exporter-*.tar.gz
mv node_exporters-* node_exporter
cd node_exporter
```

### 2.配置系统启动文件

```bash
vim /usr/lib/systemd/system/node_exporter.service
```

```bash
[Unit]
Description=node_exporter
After=network.target

[Service]
Type=simple
User=root
ExecStart=/home/software/node_exporter/node_exporter #注意路径
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 3.启动服务

```
systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter
systemctl status node_exporter
```

## grafana安装

### 1.下载解压

```bash
wget https://dl.grafana.com/enterprise/release/grafana-enterprise-8.0.6-1.x86_64.rpm # https://grafana.com/grafana/download
yum -y install grafana-enterprise-8.0.6-1.x86_64.rpm
```

### 2.配置文件

```bash
# 配置文件位于/etc/grafana/grafana.ini，这里暂时保持默认配置
```

### 3.设置开机启动并启动服务

```
systemctl daemon-reload
systemctl start grafana-server
systemctl status grafana-server
systemctl enable grafana-server
```

### 4.查看端口是否启动

```shell
netstat -anptu |grep 3000
```

## Alertmanager

### Alertmanager安装

#### 1.下载解压

```shell
# https://grafana.com/grafana/download
wget https://github.com/prometheus/alertmanager/releases/download/v0.22.2/alertmanager-0.22.2.linux-amd64.tar.gz
tar -zxvf alertmanager-0.22.2.linux-amd64.tar.gz
mv alertmanager-0.22.2.linux-amd64 alertmanager
cd alertmanager
```

#### 2.配置文件

```shell
vim /usr/lib/systemd/system/alertmanager.service
```

```bash
[Unit]
Description=Alertmanager
After=network-online.target

[Service]
Restart=on-failure
ExecStart=/home/software/alertmanager/alertmanager --config.file=/home/software/alertmanager/alertmanager.yml # 注意路径

[Install]
WantedBy=multi-user.target
```

```shell
vim alertmanager.yml
```

```yaml
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.exmail.qq.com:465' # 邮箱smtp服务器代理
  smtp_from:  '123456@qq.com' # 发送邮箱名称
  smtp_auth_username: '123456@qq.com' # 邮箱名称
  smtp_auth_password:  '' # 邮箱密码或授权码
  smtp_require_tls: false

route:
  group_by: ['alertname'] # 报警分组依据
  group_wait: 30s # 最初即第一次等待多久时间发送一组警报的通知
  group_interval: 5m # 在发送新警报前的等待时间
  repeat_interval: 2h # 发送重复警报的周期 
  receiver: email 
  routes:   #路由分支（不同条件发给不同收件人）
  - receiver: node02
    match:
        altername: InstanceDown #条件
            
receivers:  
- name: 'email' # 对应route的receiver
  email_configs: # 邮箱配置
  - to: '123456@qq.com'  # 接收警报的email配置
    headers: { Subject: "[WARN] 报警邮件"} # 接收邮件的标题
- name: 'node02'
  email_configs: # 邮箱配置
  - to: 'xuzc@yealink.com'  # 接收警报的email配置
    headers: { Subject: "[WARN] 报警邮件"} # 接收邮件的标题

```

#### 3.启动服务

```shell
systemctl daemon-reload
systemctl start alertmanager
systemctl status alertmanager
systemctl enable alertmanager
netstat -nltup|grep 9093 # 验证
```

### Altermanager监控告警

#### 1.配置邮件服务（smtp暂不使用）

```shell
yum install sendmail # 安装邮件发送服务
```

```ini
vim /etc/grafana/grafana.ini # 添加邮件配置

#################################### Alerting ############################
[alerting]
# Disable alerting engine & UI features
enabled = true
# Makes it possible to turn off alert rule execution but alerting UI is visible
execute_alerts = true

# Default setting for new alert rules. Defaults to categorize error and timeouts as alerting. (alerting, keep_state)
error_or_timeout = alerting

# Default setting for how Grafana handles nodata or null values in alerting. (alerting, no_data, keep_state, ok)
nodata_or_nullvalues = no_data

# Alert notifications can include images, but rendering many images at the same time can overload the server
# This limit will protect the server from render overloading and make sure notifications are sent out quickly
concurrent_render_limit = 5

#################################### SMTP / Emailing ##########################
[smtp]
;enabled = false
;host = localhost:25
;user =
# If the password contains # or ; you have to wrap it with triple quotes. Ex """#password;"""
;password =
;cert_file =
;key_file =
;skip_verify = false
;from_address = admin@grafana.localhost
;from_name = Grafana
# EHLO identity in SMTP dialog (defaults to instance_name)
;ehlo_identity = dashboard.example.com
enabled = true
host = 192.168.37.101:465
user = root
password = root
skip_verify = true
from_address = admin@grafana.localhost
from_name = Grafana
```

#### 2.配置grafana邮件

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210805092926808.png" alt="image-20210805092926808" style="width:100%;" />

## AlertCenter

### 1.添加数据源<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210805143435254.png" alt="image-20210805143435254" style="width:100%;" />

### 2.添加告警订阅

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210805143611921.png" alt="image-20210805143611921" style="width:100%;" />

### 3..postman验证

```
http://alertcenter-out.yealinkops.com/api/v1/alerts
```

```json
[  
    {  
        "labels":{  
            "alertname":"test",
            "cluster":"yl4030",
            "appkey":"692b2d68-21ef-4dae-af62-a8483fe2aa38",  # 数据源中的App Key
            "severity": "3"
        },
        "annotations":{  
            "message":"this is a test!"
        }
    }
]
```

### 4.静默告警

<img src="D:\Users\yl4030\AppData\Roaming\Typora\typora-user-images\image-20210805143941941.png" alt="image-20210805143941941" style="width:100%;" />

## prometheus监控k8s

https://www.kancloud.cn/pshizhsysu/prometheus/1867120

