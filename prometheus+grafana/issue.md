# Meeting 

## meeting大盘

```bash
#Meeting Port - 时延（P99、90）、平均时延
yl_ss_meeting_port_manager_http_response_duration_second_bucket #其中second应为seconds
```

## sfu-mc

```bash
#详情--topMC请求响应时间P90-99
只有P99
```

## sfu-mss

```bash
#会议数量
yl_sfu_conference #缺少
```

## meeting-controller

```bash
#客户端-客户端当前连接数
yl_ss_meeting_controller_client_connections_count
client_connections_current 客户端当前连接数统计 Gauge addr、name 参考业务metrics示例 #错误
```

## meeting-scheduler

```bash
#yrmq-yrmq响应数量和状态信息统计（速率）
sum(rate(yl_ss_meeting_scheduler_yrmq_response_duration_seconds_count{region=~"$region", namespace=~"$namespace", job=~"$job"}[2m])) by (code, method, path) #没有'code'label
```

## conference-manager

```
模块的业务metrics基本没有
```

## data-analyzer

```
模块的业务metrics基本没有
```

## ygateway

```
模块的业务metrics基本没有
```

# Mediation

## unigw-compat

```bash
#概览  
yl_unigw_h323_current_calls  #unigw-compat中没有，unigw中有
#详情-总量 - sip通话数量
yl_unigw_sip_current_calls_num
yl_unigw_sip_current_calls gauge 当前sip通话数量 数值 无 无 #错误
```

# YBSP

## sip-rediret

```bash
#缺少sip-rediret模块
```

## notification-manager

```bash
#业务自定义指标-模块
yl_be_nm_http_server_send_requests_seconds
yl_be_nm_http_server_send_requests 系统短信/邮件/微信消息发送接口的时延 数值 #错误
yl_be_nm_http_client_requests_seconds
yl_be_nm_http_client_requests 调用第三方服务的时延(HTTP) #错误
```

## developer-manager

```bash
#业务自定义指标-B - 是否开启XDEBUG模式
yl_be_xdebug
yl_be_region
yl_be_data_center_region #developer-manager没有，user-manager有
#业务自定义指标-B - 可用服务状态
yl_be_oss_status
yl_be_es_status 
yl_be_log_stash_status #developer-manager没有，user-manager有
#业务自定义指标-B - 调用其他服务接口的请求速率【调用其他服务接口的请求时延P99】
yl_be_feign_request_seconds #developer-manager没有，user-manager有（但是为yl_be_feign_request）
#业务自定义指标-B - 无明确数据归属的数据所属的数据中心区域信息
yl_be_data_center_region #developer-manager没有，user-manager有
#业务自定义指标-B - 回源操作调用次数信息
yl_be_trace_source_total #developer-manager没有，user-manager有
```

## user-manager

```bash
#业务自定义指标-模块 企业注册新增量统计
yl_be_enterprise_register_total
yl_be_enterprise_register_total 企业注册新增量统计 #应为企业注册总量统计
#业务自定义指标-B - 调用其他服务接口的请求速率【调用其他服务接口的请求时延P99】
yl_be_feign_request_seconds 
yl_be_feign_request 本服务调用其他服务接口的请求信息 #错误
yl_be_feign_request_seconds_max #缺少  
```

## phonebook-manager

```bash
#业务自定义指标-B - 是否开启XDEBUG模式
yl_be_xdebug
yl_be_region
yl_be_data_center_region #phonebook-manager没有，user-manager有
#业务自定义指标-B - 可用服务状态
yl_be_oss_status
yl_be_es_status 
yl_be_log_stash_status #phonebook-manager没有，user-manager有
#业务自定义指标-B - 调用其他服务接口的请求速率【调用其他服务接口的请求时延P99】
yl_be_feign_request_seconds 
yl_be_feign_request 本服务调用其他服务接口的请求信息 #错误
#业务自定义指标-B - 无明确数据归属的数据所属的数据中心区域信息
yl_be_data_center_region #phonebook-manager没有，user-manager有
#业务自定义指标-B - 回源操作调用次数信息
yl_be_trace_source_total #phonebook-manager没有，user-manager有
```

## service-ticket-manager

```bash
#业务自定义指标-B - 是否开启XDEBUG模式
yl_be_xdebug
yl_be_region
yl_be_data_center_region #service-ticket-manager没有，user-manager有
#业务自定义指标-B - 可用服务状态
yl_be_oss_status
yl_be_es_status 
yl_be_log_stash_status #service-ticket-manager没有，user-manager有
#业务自定义指标-B - 调用其他服务接口的请求速率【调用其他服务接口的请求时延P99】
yl_be_feign_request_seconds 
yl_be_feign_request 本服务调用其他服务接口的请求信息 #错误
#业务自定义指标-B - 无明确数据归属的数据所属的数据中心区域信息
yl_be_data_center_region #service-ticket-manager没有，user-manager有
#业务自定义指标-B - 回源操作调用次数信息
yl_be_trace_source_total #service-ticket-manager没有，user-manager有
```

## YGA

```bash
#转发各区域的最大耗时
yl_be_yga_http_region_delay_mills_max #缺少
#Http-基于转发区域的转发次数
yl_be_yga_http_region_forward_total
yl_be_yga_http_region_forward 基于区域的转发次数 #错误
#无token访问链接次数
yl_be_yga_http_no_token_url_access_total
yl_be_yga_http_no_token_url_access 基于url的无token访问 #错误
```

## pushbackend

```bash
#基础信息预览 - 推送消息耗时
yl_be_push_msg_delay_seconds_max #缺少
```

## pushfrontend

```bash
#基础信息预览 - 推送消息耗时
yl_be_push_msg_delay_seconds_max #缺少
```

# YBDP

## RocketMQ CloudV4X

```bash
#缺少RocketMQ CloudV4X模块
```

## rocketmq-proxy

```bash
#Overview - 概览
yl_ynn_rocketmq_proxy_consumer_total  #缺少（onsumer实例数）
yl_ynn_rocketmq_proxy_producer_total  #缺少（roducer实例数）
yl_ynn_rocketmq_proxy_consumer_instance 当前存活的 consumer 实例数 Gauge 
yl_ynn_rocketmq_proxy_producer_instance 当前存活的 producer 实例数 Gauge 
yl_ynn_rocketmq_proxy_push_count  #缺少
yl_ynn_rocketmq_proxy_pull_count  #缺少
```

## Cassandra

```bash
#缺少Cassandra模块
```

## TiDB Cluster Dashboard

```bash
#缺少TiDB Cluster Dashboard模块
```

## Redis Cluster Dashboard

```bash
#缺少Redis Cluster Dashboard模块
```

## Redis Instance Detail

```bash
#缺少Redis Instance Detail模块
```

## etcd

```bash
#缺少etcd模块
```

## kvpubsub

```bash
#错误（不知道是哪个）#Proxy - Subscribe
yl_ybsp_kvpubsub_rpc_sub_concurrent_total
yl_ybsp_kvpubsub_rpc_sub_concurrent Guage short 订阅命令并发数 #错误（不知道是哪个）
#Proxy - Bandwidth
yl_ybsp_kvpubsub_rpc_method_msg_recv_total
yl_ybsp_kvpubsub_rpc_method_msg_recv_bytes_total Counter byte 消息接收字节数
yl_ybsp_kvpubsub_rpc_method_msg_send_total
yl_ybsp_kvpubsub_rpc_method_msg_send_bytes_total Counter byte 消息发送字节数       #错误（不知道是哪个）
```

## dbhook

```bash
#整个服务的QPS
yl_dbhook_QPS #缺少
#TPS
yl_dbhook_TPS #缺少
```

## drainer

```bash
#详情 - Consumer Pull Binlog QPS
yl_ynn_drainer_consumer_binlog_total #缺少
#详情 - Consumer Pull Binlog Size
yl_ynn_drainer_consumer_binlog_bytes #缺少

```

## sync-manager

```bash
#业务指标 - http 接口响应延时分位数 P95-99
yl_ynn_sync_manager_http_response_duration_seconds #缺少
```

## yeureka

```bash
#缺少yeureka模块
```

