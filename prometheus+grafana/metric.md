# PromQL 

https://www.prometheus.wang/quickstart/

## 1.常用的函数

https://hulining.gitbook.io/prometheus/prometheus/querying/functions

```
irate：在指定时间范围内的最近两个数据点来算速率  
rate：取指定时间范围内所有数据点，算出一组速率，然后取平均值作为结果  
delta：计算一个区间向量v 的第一个元素和最后一个元素之间的差值  
```



- rate(): 一般用于计算Counter类型的指标，计算每秒的速率

  ```shell
  #消息发送错误率大于0% 触发告警
  rate(prometheus_notifications_errors_total{}[5m]) / rate(prometheus_notifications_sent_total{}[5m]) > 0
  ```

- irate()

  `irate(v range-vector)`计算范围矢量中时间序列的每秒瞬时增加率。这基于最后两个数据点。单调性中断(例如由于目标重新启动而导致的计数器重置)会自动进行调整。仅在绘制易变、快速变化的计数器时才使用`irate`函数。告警和缓慢移动计数器使用`rate`函数，因为速率的细微改变会在 For 子句中重置，且完全没有峰值的图形很难读取。

  ```shell
  #区间向量中每个时间序列过去 5 分钟内最后两个样本数据的 HTTP 请求数的增长率
  irate(http_requests_total{job="api-server"}[5m]) 
  ```

- delta() 

  ```
  delta的参数是一个区间向量, 返回一个瞬时向量。它计算最新的 2 个样本值之间的差值。这个函数一般只用在 Gauge 类型的时间序列上。
  ```

- sum(): 将所有满足的指标值分类相加

  ```shell
  #所有pod的mcu使用率按照service_name和namespace标签进行分类，计算出mcu各模块的使用率，得出的值大于80%则告警
  (sum(ylmcu_usage)  by (service_name, namespace))/(sum(ylmcu_capcity)  by (service_name,namespace)) > 0.8
  ```

- `topk` 和 `bottomk`用于对样本值进行排序，返回当前样本值前 n 位，或者后 n 位的时间序列。

  ```bash
  #按照应用和进程类型来获取 CPU 利用率最高的 3 个样本数据：
  topk(3, sum(rate(instance_cpu_time_ns[5m])) by (app, proc))
  #获取 HTTP 请求数后 5 位的时序样本数据
  bottomk(5, http_requests_total)
  ```


- quantile():用于计算当前样本数据值的分布情况 quantile(φ, express) ，其中 `0 ≤ φ ≤ 1`

  ```bash
  #当 φ 为 0.5 时，即表示找到当前样本数据中的中位数：
  quantile(0.5, http_requests_total)
  #返回结果：
  {}   656
  ```

- histogram_quantile()

  `histogram_quantile(φ float, b instant-vector)`从**直方图()**的`b`区间向量计算 φ-quantile(0 ≤ φ ≤ 1)分位数。`b`中的样本是每个区间中观察值的计数。每个样本必须具有标签`le`，其中标签值表示区间上限(没有此类标签的样本将被忽略)。**直方图数据指标类型**()会自动提供带有`_bucket`后缀和适当标签的时间序列。

  使用`rate()`函数指定分位数计算的时间窗口。

  ```bash
  #一个直方图指标名称为 http_request_duration_seconds 计算最近 10m 的请求持续时间的 90%
  histogram_quantile(0.9, rate(http_request_duration_seconds_bucket[10m]))
  ```

  对于`http_request_duration_seconds`中的每个标签组合计算分位数。要进行汇总，请在`rate()`函数外使用`sum()`。由于`histogram_quantile()`要求使用`le`标签，因此必须将其包含在`by`子句中。

  ```bash
  #按job汇总 90%
  histogram_quantile(0.9, sum by (job, le) (rate(http_request_duration_seconds_bucket[10m])))
  #汇总所有内容，仅指定le标签：
  histogram_quantile(0.9, sum by (le) (rate(http_request_duration_seconds_bucket[10m])))
  ```

  `histogram_quantile()`函数通过假设区间内的线性分布来对分位数进行插值。存储桶的最高上限必须为`+Inf`(否则返回`NaN`)。如果分位数位于最高的区间中，则返回第二高的区间的上限。如果该区间的上限大于0，则将最低区间的下限假定为0。在这种情况下，通常在该区间中应用线性插值。否则，将为位于最低区间中的分位数返回最低区间的上限。

  如果 `b` 的观测值为0，则返回 `NaN`。如果`b`包含少于两个区间，则返回`NaN`。如果`φ<0`，则返回`-Inf`。 对于`φ> 1`，返回`+Inf`。

- increase()

  `increase`计算范围向量中时间序列的增长。单调性中断(例如由于目标重新启动而导致的计数器重置)会自动进行调整。根据范围向量选择器中的指定，可以推断出覆盖整个时间范围的增长。因此，即使计数器仅以整数增量增加，也可能会获得非整数结果。

  ```bash
  #范围向量中每个时间序列在最近 5 分钟内测得的 HTTP 请求数
  increase(http_requests_total{job="api-server"}[5m])
  ```

  `increase()`只能与 counter 一起使用。它是`rate(v)`乘以指定时间范围窗口内的秒数的语法糖，主要用于可读性。在记录规则中使用`rate`函数，以便在每秒的基础上持续跟踪增长情况。

- time()

  `time()`返回自 UTC 1970-01-01 以来的秒数。请注意，这实际上并不返回当前时间，而是返回要计算的表达式的时间。

- ceil()

  `ceil(v instant-vector)`将`v`中所有元素的样本值增加到最接近的整数。

- label_replace()

  对于`v`中的每个时间序列，`label_replace(v instant-vector, dst_label string, replacement string, src_label string, regex string)`将正则表达式`regex`与标签`src_label`匹配。如果匹配，则返回时间序列，其中标签`dst_label`被替换为`replacement`。 `$1`表示被第一个匹配的子组替换，`$2`表示被第二个匹配的子组替换，依次类推。如果正则表达式不匹配，则时间序列将保持不变。

  该示例将返回每个时间序列都带有一个值为`a`的`foo`标签的新向量：

  ```
  label_replace(up{job="api-server",service="a:c"}, "foo", "$1", "service", "(.*):.*")
  ```

## 2.通用指标

| metric（<font color='red'>网络cpu相关</font>） | 单位        | 说明                         |
| ---------------------------------------------- | ----------- | ---------------------------- |
| container_cpu_usage_seconds_total              | 秒          | 每个 cpu 消耗的累积 cpu 时间 |
| container_cpu_system_seconds_total             | 秒          | 累计消耗的系统cpu时间        |
| process_cpu_seconds_total                      | 秒          | 用户和系统 CPU 花费的总时间  |
| container_network_transmit_bytes_total         | 字节数bytes | 容器通过网络传输的字节数     |
| container_network_receive_bytes_total          | 字节数bytes | 容器通过网络接收的字节数     |

| metric（<font color='red'>容器监控内存相关指标</font>） | 类型    | 单位        | 说明                                                         |
| ------------------------------------------------------- | ------- | ----------- | ------------------------------------------------------------ |
| container_memory_rss                                    | gauge   | 字节数bytes | RSS内存，即常驻内存集（Resident Set Size），是分配给进程使用实际物理内存，而不是磁盘上缓存的虚拟内存。RSS内存包括所有分配的栈内存和堆内存，以及加载到物理内存中的共享库占用的内存空间，但不包括进入交换分区的内存。 |
| container_memory_usage_bytes                            | gauge   | 字节数bytes | 当前使用的内存量，包括所有使用的内存，不管有没有被访问。     |
| container_memory_max_usage_bytes                        | gauge   | 字节数bytes | 最大内存使用量的记录。                                       |
| container_memory_cache                                  | gauge   | 字节数bytes | 高速缓存（cache）的使用量。cache是位于CPU与主内存间的一种容量较小但速度很高的存储器，是为了提高cpu和内存之间的数据交换速度而设计的。 |
| container_memory_swap                                   | gauge   | 字节数bytes | 虚拟内存使用量。虚拟内存（swap）指的是用磁盘来模拟内存使用。当物理内存快要使用完或者达到一定比例，就可以把部分不用的内存数据交换到硬盘保存，需要使用时再调入物理内存 |
| container_memory_working_set_bytes                      | gauge   | 字节数bytes | 当前内存工作集（working set）使用量。                        |
| container_memory_failcnt                                | counter | 次          | 申请内存失败次数计数                                         |
| container_memory_failures_total                         | counter | 次          | 累计的内存申请错误次数                                       |

| metric（<font color='red'>springboot</font>） | metric说明(用途)                 | 值      | 必选label | 可选label      | 备注                                                         |
| --------------------------------------------- | -------------------------------- | ------- | --------- | -------------- | ------------------------------------------------------------ |
| http_server_requests_seconds                  | spring自身框架上报的http请求信息 | 数值    | -         | exception，uri | exception的值有 MethodArgumentNotValidException、MissingServletRequestParameterException、BadRequestException、ForbiddenException、ForbiddenException、NotAcceptableException、PreconditionFailedException、ProtocolNotMatchException、RemoteServiceUnavailableException、ResourceConflictException、ResourceNotFoundException、UnauthorizedException.uri为具体请求的uri. |
| jvm_buffer_pool_capacity_bytes                | 给定jvm的估算缓冲区大小          | Counter |           |                |                                                              |
| jvm_buffer_pool_used_buffers                  | 给定jvm的已使用缓冲区大小        | Counter |           |                |                                                              |
| jvm_classes_loaded                            | 当前jvm已加载类数量              | Counter |           |                |                                                              |
| jvm_classes_loaded_total                      | 从jvm运行开始加载的类的数量      | Counter |           |                |                                                              |
| jvm_classes_unloaded_total                    | jvm运行后卸载的类数量            | Counter |           |                |                                                              |
| jvm_gc_collection_seconds                     | 对指标数据进行采样               | Summary |           |                |                                                              |
| jvm_memory_bytes_used                         | jvm已用内存区域                  |         |           |                |                                                              |
| jvm_memory_bytes_committed                    | JVM 内存区域当前可使用的内存大小 |         |           |                |                                                              |
| jvm_memory_bytes_max                          | jvm内存区域的最大字节数          |         |           |                |                                                              |
| jvm_memory_bytes_init                         | jvm内存区域的初始化字节数        |         |           |                |                                                              |
| jvm_memory_pool_bytes_used                    | jvm内存池使用情况                |         |           |                |                                                              |
| jvm_memory_pool_bytes_committed               | jvm内存池当前可使用的内存大小    |         |           |                |                                                              |
| jvm_threads_live                              | JVM当前活跃线程数                | 数值    |           |                |                                                              |
| jvm_threads_peak                              | JVM峰值线程数                    | 数值    |           |                |                                                              |
| jvm_threads_daemon                            | JVM守护线程数                    | 数值    |           |                |                                                              |
| tomcat_threads_config_max                     | tomcat配置的线程最大数           | 数值    |           |                |                                                              |
| tomcat_threads_busy                           | tomcat繁忙线程                   | 数值    |           |                |                                                              |
| tomcat_threads_current                        | tomcat当前线程数（包括守护线程） | 数值    |           |                |                                                              |

| **metric（<font color='red'>http</font>）** | metric说明(用途)  | 值        | 必选label           | 可选label | 备注 |
| ------------------------------------------- | ----------------- | --------- | ------------------- | --------- | ---- |
| http_server_response_duration_seconds       | http 接口响应延迟 | Histogram | method, status, url |           |      |

| **metric（<font color='red'>grpc</font>）** | metric说明(用途)                             | 值      | 必选label                            | 可选label | 备注 |
| ------------------------------------------- | -------------------------------------------- | ------- | ------------------------------------ | --------- | ---- |
| grpc_server_handled_total                   | 已经处理完的调用次数计数                     | Counter | grpc_service, grpc_method, grpc_type | grpc_code |      |
| grpc_server_msg_received_total              | 消息接收次数计数                             | Counter | grpc_service, grpc_method, grpc_type | grpc_code |      |
| grpc_server_msg_sent_total                  | 消息发送次数计数                             | Counter | grpc_service, grpc_method, grpc_type | grpc_code |      |
| grpc_server_started_total                   | 接受到的调用次数计数，包括已经处理完或断开的 | Counter | grpc_service, grpc_method, grpc_type | grpc_code |      |

# baker metrics

## a. Meeting

### 1.基础metrics

| metric     | metric说明(用途) | 值            | 必选label    | 可选label |
| ---------- | ---------------- | ------------- | ------------ | --------- |
| health     | 服务健康检查     | 0/正常;1/异常 | service_name |           |
| start_time | 服务启动时间     | 时间戳        | service_name |           |

### 2.业务metrics

| metric（<font color='red'>meeting-controller</font>） | metric说明(用途)           | 值        | 必选label          | 可选label |
| ----------------------------------------------------- | -------------------------- | --------- | ------------------ | --------- |
| http_request_duration_seconds                         | http请求延时               | Histogram | method、path       |           |
| http_request_total                                    | http请求数和请求状态统计   | counter   | method、path、code |           |
| memory_cache_hits_total                               | 内存的缓存命中数统计       | counter   | name               |           |
| memory_cache_misses_total                             | 内存的缓存命中未数统计     | counter   | name               |           |
| http_response_duration_seconds                        | http响应延时统计           | Histogram | method、path       |           |
| http_response_code_total                              | http响应数量和状态信息统计 | counter   | method、path、code |           |
| http_response_bbr_total                               | http响应的限流次数统计     | counter   | method、path       |           |
| http_response_handle_panic_total                      | http请求的panic次数统计    | counter   | method、path       |           |
| client_connections_total                              | 客户端连接数统计           | counter   | addr、name         |           |
| client_connections_current                            | 客户端当前连接数统计       | Gauge     | addr、name         |           |
| ypush_request_duration_s                              | ypush的请求延时            | Histogram | method             |           |
| ypush_request_code_total                              | ypush的请求统计            | Counter   | method、code       |           |
| meeting_count                                         | 当前会议数量统计           | Gauge     | createType         |           |
| user_count                                            | 服务user数量统计           | Gauge     |                    |           |
| meeting_user_count                                    | 每个会议中的人数信息       | Gauge     | meetingNum         |           |
| go_memstats_alloc_bytes                               | 当前服务使用的内存量       | gauge     |                    |           |
| go_gc_duration_seconds                                | go内存gc耗时统计           | summary   |                    |           |
| go_goroutines                                         | go routines的数量统计      | gauge     |                    |           |

| metric（<font color='red'>meeting-port-manager</font>） | metric说明(用途)           | 值        | 必选label          | 可选label |
| ------------------------------------------------------- | -------------------------- | --------- | ------------------ | --------- |
| memory_cache_hits_total                                 | 内存的缓存命中数统计       | counter   | name               |           |
| memory_cache_misses_total                               | 内存的缓存命中未数统计     | counter   | name               |           |
| http_response_duration_seconds                          | http响应延时统计           | Histogram | method、path       |           |
| http_response_code_total                                | http响应数量和状态信息统计 | counter   | method、path、code |           |
| go_memstats_alloc_bytes                                 | 当前服务使用的内存量       | gauge     |                    |           |
| go_gc_duration_seconds                                  | go内存gc耗时统计           | summary   |                    |           |
| go_goroutines                                           | go routines的数量统计      | gauge     |                    |           |

| metric（<font color='red'>meeting-scheduler</font>） | metric说明(用途)           | 值        | 必选label          | 可选label |
| ---------------------------------------------------- | -------------------------- | --------- | ------------------ | --------- |
| http_request_duration_seconds                        | http请求延时               | Histogram | method、path       |           |
| http_request_total                                   | http请求数和请求状态统计   | counter   | method、path、code |           |
| memory_cache_hits_total                              | 内存的缓存命中数统计       | counter   | name               |           |
| memory_cache_misses_total                            | 内存的缓存命中未数统计     | counter   | name               |           |
| yrmq_response_duration_seconds                       | yrmq响应延时统计           | Histogram | method、path       |           |
| yrmq_response_code_total                             | yrmq响应数量和状态信息统计 | counter   | method、path、code |           |
| yrmq_response_bbr_total                              | yrmq响应的限流次数统计     | counter   | method、path       |           |
| yrmq_response_handle_panic_total                     | yrmq请求的panic次数统计    | counter   | method、path       |           |
| client_connections_total                             | 客户端连接数统计           | counter   | addr、name         |           |
| client_connections_current                           | 客户端当前连接数统计       | Gauge     | addr、name         |           |
| counter_total                                        | 相关数量的统计             | counter   | name               |           |
| go_memstats_alloc_bytes                              | 当前服务使用的内存量       | gauge     |                    |           |
| go_gc_duration_seconds                               | go内存gc耗时统计           | summary   |                    |           |
| go_goroutines                                        | go routines的数量统计      | gauge     |                    |           |

| metric（<font color='red'>sfu-mc</font>）            | metric说明(用途)          | 值        | 必选label | 可选label |
| ---------------------------------------------------- | ------------------------- | --------- | --------- | --------- |
| yl_sfu_mc_sdk_requests_total                         | 终端请求总量              | counter   |           |           |
| yl_sfu_mc_mss_local_route_requests_total             | 本地集群路由查询次数      | counter   |           |           |
| yl_sfu_mc_mss_cross_route_requests_total             | 跨区路由查询次数          | counter   |           |           |
| yl_sfu_mc_topmc_request_duration_seconds             | topMc请求响应时间         | histogram |           |           |
| yl_sfu_mc_mss_participant_change_request_total       | 入会/退会变更请求总量     | counter   |           |           |
| yl_sfu_mc_mss_cross_participant_change_request_total | 跨区入会/退会变更请求总量 | counter   |           |           |

| metric（<font color='red'>sfu-mss</font>） | metric说明(用途)       | 值       | 必选label     | 可选label | 备注              |
| ------------------------------------------ | ---------------------- | -------- | ------------- | --------- | ----------------- |
| yl_sfu_media_capcity                       | mss最大接入终端路数    | 终端数   | service_name  |           |                   |
| yl_sfu_media_used                          | mss当前接入终端路数    | 终端数   | service_name  |           | 包含mss之间的消耗 |
| yl_sfu_conference_user                     | 当前每个会议的参会人数 | 会议人数 | conference_id |           |                   |

| metric（<font color='red'>conference-manager</font>） | metric说明(用途)                             | 值            | 必选label    | 可选label |
| ----------------------------------------------------- | -------------------------------------------- | ------------- | ------------ | --------- |
| service_request_rate_per_second                       | 请求速率(每秒请求数)                         | 数值          | service_name | item      |
| yl_be_materialized_view_health                        | 会议服务从用户中心同步的物化视图数据是否正常 | 0/正常;1/异常 | service_name |           |

| metric（<font color='red'>data-analyzer、ygateway</font>） | metric说明(用途)     | 值   | 必选label    | 可选label | 备注 |
| ---------------------------------------------------------- | -------------------- | ---- | ------------ | --------- | ---- |
| service_request_rate_per_second                            | 请求速率(每秒请求数) | 数值 | service_name | item      | 无   |

| metric（<font color='red'>recording-manager2</font>） | 类型    | 单位  | 说明（用途）         | label名称    | 备注 |
| ----------------------------------------------------- | ------- | ----- | -------------------- | ------------ | ---- |
| yl_be_recording_file_transcodeing_failed_total        | Counter | short | 录制文件转码失败数量 | service_name | 无   |
| yl_be_recording_file_transcodeing_error_total         | Counter | short | 录制文件异常状态数量 | service_name | 无   |



## b. Mediation

### 1.基础metrics

| metric        | metric说明(用途)         | 值                         | label |
| ------------- | ------------------------ | -------------------------- | ----- |
| yl_health     | 服务健康状态检测         | 正常为0，异常为1           | 无    |
| yl_start_time | 用于判断程序是否异常重启 | 程序启动时间戳（单位：秒） | 无    |

### 2.业务metrics

| metric（<font color='red'>unigs-compat</font>） | type    | metric说明(用途)                       | 值   | 必选label   | 可选label | 备注                                                        |
| ----------------------------------------------- | ------- | -------------------------------------- | ---- | ----------- | --------- | ----------------------------------------------------------- |
| yl_unigs_gwmgr_current_gws                      | gauge   | gs当前连接的gw总个数                   | 数值 | 无          | 无        |                                                             |
| yl_unigs_sip_current_thirdreg                   | gauge   | 当前sip注册数量                        | 数值 | client_type | 无        | client_type：hard是硬端；soft是软端；test是压测端           |
| yl_unigs_dsd_top_register_ua                    | gauge   | 当前注册量前十的user-agent             | 数值 | name        | 无        | unigs内部有进行排序，每次只上报指标值大小在前十的10个维度； |
| yl_unigs_dsd_ddos_request_ua_total              | counter | 最近频繁发起请求的UA（user-agent）     | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_request_ip_total              | counter | 最近频繁发起请求的IP                   | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_request_uri_total             | counter | 最近频繁发起请求的URI                  | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_register_uri_total            | counter | 最近频繁发注册请求的URI                | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_subscribe_uri_total           | counter | 最近频繁发订阅请求的URI                | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_invite_uri_total              | counter | 最近频繁发呼叫请求的URI                | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_unauth_ua_total               | counter | 最近频繁鉴权认证失败的UA（user-agent） | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_unauth_ip_total               | counter | 最近频繁鉴权认证失败的IP               | 数值 | name        | 无        |                                                             |
| yl_unigs_dsd_ddos_unauth_uri_total              | counter | 最近频繁鉴权认证失败的URI              | 数值 | name        | 无        |                                                             |
| yl_unigs_sip_request_receive_total              | counter | 收到的sip请求报文总数                  | 数值 | method      | 无        |                                                             |
| yl_unigs_sip_response_receive_total             | counter | 收到的sip响应报文总数                  | 数值 | code        | 无        |                                                             |
| yl_unigs_sip_request_send_total                 | counter | 发送的sip请求报文总数                  | 数值 | method      | 无        |                                                             |
| yl_unigs_sip_response_send_total                | counter | 发送的sip响应报文总数                  | 数值 | code        | 无        |                                                             |
| yl_unigs_sip_current_transports_num             | gauge   | 当前sip的连接数                        | 数值 | 无          | 无        |                                                             |
| yl_unigs_h323_gk_current_thirdreg               | gauge   | 当前H.323 GK注册数量                   | 数值 | 无          | 无        | 该指标在REG身份的unigs服务才存在                            |
| yl_unigs_h323_current_calls                     | gauge   | 当前H.323通话数量                      | 数值 | 无          | 无        |                                                             |

| metric（<font color='red'>unigs-coop、unigs-wechat</font>） | type  | metric说明(用途)     | 值   | 必选label | 可选label | 备注 |
| ----------------------------------------------------------- | ----- | -------------------- | ---- | --------- | --------- | ---- |
| yl_unigs_gwmgr_current_gws                                  | gauge | gs当前连接的gw总个数 | 数值 | 无        | 无        |      |

| metric（<font color='red'>unigs</font>） | type    | metric说明(用途)           | 值   | 必选label | 可选label | 备注                                                         |
| ---------------------------------------- | ------- | -------------------------- | ---- | --------- | --------- | ------------------------------------------------------------ |
| yl_unigs_gwmgr_current_gws               | gauge   | gs当前连接的gw总个数       | 数值 | 无        | 无        |                                                              |
| yl_unigs_sip_current_thirdreg            | gauge   | 当前sip注册数量            | 数值 | 无        | 无        | 该指标在REG身份的unigs服务才存在                             |
| yl_unigs_sip_current_calls               | gauge   | 当前sip通话数量            | 数值 | 无        | 无        |                                                              |
| yl_unigs_h323_gk_current_thirdreg        | gauge   | 当前H.323 GK注册数量       | 数值 | 无        | 无        | 该指标在REG身份的unigs服务才存在                             |
| yl_unigs_h323_current_calls              | gauge   | 当前H.323通话数量          | 数值 | 无        | 无        |                                                              |
| yl_unigs_dsd_top_register_ua             | gauge   | 当前注册量前十的user-agent | 数值 | name      | 无        | unigs内部有进行排序，每次只上报指标值大小在前十的10个维度；该指标在REG身份的unigs服务才存在 |
| yl_unigs_dsd_ddos_request_ua_total       | counter | 最近频繁发起请求的UA       | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_request_ip_total       | counter | 最近频繁发起请求的IP       | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_request_uri_total      | counter | 最近频繁发起请求的URI      | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_register_uri_total     | counter | 最近频繁发注册请求的URI    | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_subscribe_uri_total    | counter | 最近频繁发订阅请求的URI    | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_invite_uri_total       | counter | 最近频繁发呼叫请求的URI    | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_unauth_ua_total        | counter | 最近频繁鉴权认证失败的UA   | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_unauth_ip_total        | counter | 最近频繁鉴权认证失败的IP   | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_unauth_uri_total       | counter | 最近频繁鉴权认证失败的URI  | 数值 | name      | 无        |                                                              |
| yl_unigs_dsd_ddos_request_phone_total    | counter | 用户号码呼入次数           | 数值 | name      | 无        | 用于统计用户的呼入频率                                       |
| yl_unigs_sip_request_receive_total       | counter | 收到的sip请求报文总数      | 数值 | method    | 无        |                                                              |
| yl_unigs_sip_response_receive_total      | counter | 收到的sip响应报文总数      | 数值 | code      | 无        |                                                              |
| yl_unigs_sip_request_send_total          | counter | 发送的sip请求报文总数      | 数值 | method    | 无        |                                                              |
| yl_unigs_sip_response_send_total         | counter | 发送的sip响应报文总数      | 数值 | code      | 无        |                                                              |
| yl_unigs_sip_current_transports_num      | gauge   | 当前sip的连接数            | 数值 |           | 无        |                                                              |

| metric（<font color='red'>unigw-compat</font>） | type      | metric说明(用途)                       | 值               | 必选label                 | 可选label | 备注                                                         |
| ----------------------------------------------- | --------- | -------------------------------------- | ---------------- | ------------------------- | --------- | ------------------------------------------------------------ |
| yl_unigw_ivvr_current_users                     | gauge     | 用户ivvr状态类型分布                   | 数值             | ivvr_menu、ivvr_type      | 无        |                                                              |
| yl_unigw_meeting_current_calls                  | gauge     | meeting模块的call_session个数          | 数值             | 无                        | 无        |                                                              |
| yl_unigw_meeting_http_request_total             | counter   | 中介请求会控的http请求次数             | 数值             | uri、method               | 无        |                                                              |
| yl_unigw_meeting_http_request_duration_seconds  | histogram | 中介请求会控的http请求延时时间         | 数值（单位：秒） | uri、method、code         | 无        |                                                              |
| yl_unigw_meeting_http_request_error_total       | counter   | 中介请求会控的http请求返回错误次数     | 数值             | uri、method、code、reason | 无        |                                                              |
| yl_unigw_sfu_current_instances                  | gauge     | sfu模块当前instance的数量              | 数值             | 无                        | 无        |                                                              |
| yl_unigw_sip_current_calls                      | gauge     | 当前sip通话数量                        | 数值             | 无                        | 无        |                                                              |
| yl_unigw_sip_request_receive_total              | counter   | 收到的sip请求报文总数                  | 数值             | method                    | 无        |                                                              |
| yl_unigw_sip_response_receive_total             | counter   | 收到的sip响应报文总数                  | 数值             | code                      | 无        |                                                              |
| yl_unigw_sip_request_send_total                 | counter   | 发送的sip请求报文总数                  | 数值             | method                    | 无        |                                                              |
| yl_unigw_sip_response_send_total                | counter   | 发送的sip响应报文总数                  | 数值             | code                      | 无        |                                                              |
| yl_unigw_media_resource_usage                   | gauge     | gw当前的媒体资源使用情况               | 数值             | 无                        | 无        |                                                              |
| yl_unigw_media_resource_capacity                | gauge     | gw的媒体资源总容量                     | 数值             | 无                        | 无        |                                                              |
| yl_unigw_sip_current_transports_num             | gauge     | 当前sip的连接数                        | 数值             | 无                        | 无        |                                                              |
| yl_unigw_current_conf_num                       | gauge     | 当前进行的会议数                       | 数值             | 无                        | 无        |                                                              |
| yl_unigw_current_calls_num                      | gauge     | 当前通话总数                           | 数值             | 无                        | 无        |                                                              |
| yl_unigw_current_mode                           | gauge     | 当前unigw状态                          | 数值             | 无                        | 无        | 0=正常模式；1=下线模式；2=维护模式；3=缩容模式               |
| yl_unigw_current_appshare_num                   | gauge     | 当前开启的辅流个数                     | 数值             | 无                        | 无        |                                                              |
| yl_unigw_join_respond_duration_seconds          | histogram | unigw-compat响应终端入会请求结果的时间 | 数值（单位：秒） | join_result               | 无        | 标签join_result的含义：首次入会请求的结果：joined/ivvrPut/hangup，即入会成功/进入到ivvr/被挂断 |
| yl_unigw_report_request_all_bytes               | gauge     | 当前中介服务每次上报的数据量的总大小   | 数值             | 无                        | 无        |                                                              |
| yl_unigw_report_request_error_total             | counter   | 上报结果错误统计                       | 数值             | httpcode、reqtype         | 无        |                                                              |

| metric（<font color='red'>unigw-coop、unigw-wechat</font>） | type      | metric说明(用途)                   | 值               | 必选label                 | 可选label | 备注                                           |
| ----------------------------------------------------------- | --------- | ---------------------------------- | ---------------- | ------------------------- | --------- | ---------------------------------------------- |
| yl_unigw_meeting_current_calls                              | gauge     | meeting模块的call_session个数      | 数值             | 无                        | 无        |                                                |
| yl_unigw_meeting_http_request_total                         | counter   | 中介请求会控的http请求次数         | 数值             | uri、method               | 无        |                                                |
| yl_unigw_meeting_http_request_duration_seconds              | histogram | 中介请求会控的http请求延时时间     | 数值（单位：秒） | uri、method、code         | 无        |                                                |
| yl_unigw_meeting_http_request_error_total                   | counter   | 中介请求会控的http请求返回错误次数 | 数值             | uri、method、code、reason | 无        |                                                |
| yl_unigw_sfu_current_instances                              | gauge     | sfu模块当前instance的数量          | 数值             | 无                        | 无        |                                                |
| yl_unigw_media_resource_usage                               | gauge     | gw当前的媒体资源使用情况           | 数值             | 无                        | 无        |                                                |
| yl_unigw_media_resource_capacity                            | gauge     | gw的媒体资源总容量                 | 数值             | 无                        | 无        |                                                |
| yl_unigw_current_conf_num                                   | gauge     | 当前进行的会议数                   | 数值             | 无                        | 无        |                                                |
| yl_unigw_current_calls_num                                  | gauge     | 当前通话总数                       | 数值             | 无                        | 无        |                                                |
| yl_unigw_current_mode                                       | gauge     | 当前unigw状态                      | 数值             | 无                        | 无        | 0=正常模式；1=下线模式；2=维护模式；3=缩容模式 |
| yl_unigw_current_appshare_num                               | gauge     | 当前开启的辅流个数                 | 数值             | 无                        | 无        |                                                |

| metric（<font color='red'>unigw</font>）       | type      | metric说明(用途)                     | 值               | 必选label                 | 可选label | 备注                                           |
| ---------------------------------------------- | --------- | ------------------------------------ | ---------------- | ------------------------- | --------- | ---------------------------------------------- |
| yl_unigw_ivvr_current_users                    | gauge     | 用户ivvr状态类型分布                 | 数值             | ivvr_menu、ivvr_type      | 无        |                                                |
| yl_unigw_meeting_current_calls                 | gauge     | meeting模块的call_session个数        | 数值             | 无                        | 无        |                                                |
| yl_unigw_meeting_http_request_total            | counter   | 中介请求会控的http请求次数           | 数值             | uri、method               | 无        |                                                |
| yl_unigw_meeting_http_request_duration_seconds | histogram | 中介请求会控的http请求延时时间       | 数值（单位：秒） | uri、method、code         | 无        |                                                |
| yl_unigw_meeting_http_request_error_total      | counter   | 中介请求会控的http请求返回错误次数   | 数值             | uri、method、code、reason | 无        |                                                |
| yl_unigw_sfu_current_instances                 | gauge     | sfu模块当前instance的数量            | 数值             | 无                        | 无        |                                                |
| yl_unigw_h323_current_calls                    | gauge     | 当前H.323通话数量                    | 数值             | 无                        | 无        |                                                |
| yl_unigw_sip_current_calls                     | gauge     | 当前sip通话数量                      | 数值             | 无                        | 无        |                                                |
| yl_unigw_sip_request_receive_total             | counter   | 收到的sip请求报文总数                | 数值             | method                    | 无        |                                                |
| yl_unigw_sip_response_receive_total            | counter   | 收到的sip响应报文总数                | 数值             | code                      | 无        |                                                |
| yl_unigw_sip_request_send_total                | counter   | 发送的sip请求报文总数                | 数值             | method                    | 无        |                                                |
| yl_unigw_sip_response_send_total               | counter   | 发送的sip响应报文总数                | 数值             | code                      | 无        |                                                |
| yl_unigw_pstn_callee_number                    | gauge     | 购买的号码的被叫实时并发数           | 数值             | number                    | 无        |                                                |
| yl_unigw_pstn_caller_number                    | gauge     | 购买的号码的呼出实时并发数           | 数值             | number                    | 无        |                                                |
| yl_unigw_rtmp_open_channel_error_total         | counter   | 阿里云RTMP连接失败异常统计           | 数值             | event_type                | 无        |                                                |
| yl_unigw_rtmp_current_player_number            | gauge     | 当前rtmp录播录播的数量               | 数值             | gw_type                   | 无        |                                                |
| yl_unigw_rtmp_current_stream_number            | gauge     | 当前unigw-rtmp流的连接数量           | 数值             | 无                        | 无        |                                                |
| yl_unigw_media_resource_usage                  | gauge     | gw当前的媒体资源使用情况             | 数值             | 无                        | 无        |                                                |
| yl_unigw_media_resource_capacity               | gauge     | gw的媒体资源总容量                   | 数值             | 无                        | 无        |                                                |
| yl_unigw_sip_current_transports_num            | gauge     | 当前sip的连接数                      | 数值             | 无                        | 无        |                                                |
| yl_unigw_current_conf_num                      | gauge     | 当前进行的会议数                     | 数值             | 无                        | 无        |                                                |
| yl_unigw_current_calls_num                     | gauge     | 当前通话总数                         | 数值             | 无                        | 无        |                                                |
| yl_unigw_current_mode                          | gauge     | 当前unigw状态                        | 数值             | 无                        | 无        | 0=正常模式；1=下线模式；2=维护模式；3=缩容模式 |
| yl_unigw_current_appshare_num                  | gauge     | 当前开启的辅流个数                   | 数值             | 无                        | 无        |                                                |
| yl_unigw_report_request_all_bytes              | gauge     | 当前中介服务每次上报的数据量的总大小 | 数值             | 无                        | 无        |                                                |
| yl_unigw_report_request_error_total            | counter   | 上报结果错误统计                     | 数值             | httpcode、reqtype         | 无        |                                                |

## c. YBSP

### 1.基础metrics

| metric                           | metric说明(用途) | 值            | 必选label    | 可选label |
| -------------------------------- | ---------------- | ------------- | ------------ | --------- |
| yl_health                        | 服务健康检查     | 0/正常;1/异常 | service_name |           |
| yl_start_time                    | 服务启动时间     | 时间戳        | service_name |           |
| yl_be_thread_pool_largest_thread | 线程池最大线程数 | 数值          | thread_name  |           |

### 2.业务metrics


| metric（<font color='red'>unified-storage-service</font>） | metric说明(用途)     | 值   | 必选label    | 可选label |
| ---------------------------------------------------------- | -------------------- | ---- | ------------ | --------- |
| yl_be_recording                                            | 当前录制中数         | 数值 | service_name | -         |
| yl_be_transcoding                                          | 当前转码中作业数     | 数值 | service_name | -         |
| yl_be_transcode_error                                      | 转码错误类型数       | 数值 | service_name | type      |
| yl_be_transcode_all_total                                  | 转码总数             | 数值 | service_name | -         |
| yl_be_transcode_success_total                              | 转码成功数           | 数值 | service_name | -         |
| yl_be_record_seconds                                       | 录制时长             | 数值 | service_name | -         |
| yl_be_transcode_seconds                                    | 转码时长             | 数值 | service_name | -         |
| yl_be_file_duplicate_uploaded_total                        | 文件重复上传数量     | 数值 | service_name | -         |
| yl_be_file_uploaded_total                                  | 文件上传总数         | 数值 | service_name | -         |
| yl_be_s3_resize_image_fail_total                           | S3缩略图处理失败总数 | 数值 | service_name | -         |
| yl_be_s3_resize_request_total                              | S3缩略图处理请求总数 | 数值 | service_name | -         |
| yl_be_pre_signed_not_upload                                | 预签但没有上传数量   | 数值 | service_name | -         |
| yl_be_pre_signed_to_upload_total                           | 预签上传请求总数     | 数值 | service_name | -         |
| yl_be_scan_blocked_result_total                            | 内容检测违规结果数目 | 数值 | service_name | -         |
| yl_be_scan_request_fail_total                              | 内容检测请求失败总数 | 数值 | service_name | -         |

| metric（<font color='red'>notification-manager</font>） | metric说明(用途)                           | 值   | 必选label                                                    | 可选label                      | 备注                        |
| ------------------------------------------------------- | ------------------------------------------ | ---- | ------------------------------------------------------------ | ------------------------------ | --------------------------- |
| service_request_rate_per_second                         | 请求速率(每秒请求数)                       | 数值 | service_name                                                 | item                           | 示例                        |
| yl_be_nm_http_server_send_requests                      | 系统短信/邮件/微信消息发送接口的时延       | 数值 | **msg_type**: 消息类型，值为：sms、mail、wx **api**：请求的api，值为/v1/sms、/v1/mails、/v1/plain-mails、/v1/wechat-messages **status**：可枚举的状态码 **action**：发送方式，值为：single_sync、single_async、batch_async **priority**：优先级，值为：low、medium、high **tenant**：可枚举的租户id | **error_code**：可枚举的错误码 | 上报的类型为Histogram       |
| yl_be_nm_http_client_requests                           | 调用第三方服务的时延(HTTP)                 | 数值 | **provider**：服务商，值为：aliyun、tencent、aws、twilio **product**：云产品，值为：ali-sms、tencent-sms、tencent-wxmp、aws-sns、twilio-sms **code**：可枚举的状态码 |                                | 上报的类型为Histogram       |
| yl_be_nm_smtp_client_requests                           | 调用第三方服务的时延(SMTP)                 | 数值 | **provider**：服务商，值为：aliyun、aws **product**：云产品，值为ali-directMail、aws-ses **code**：状态码，值为：success、fail |                                | 上报的类型为Histogram       |
| yl_be_nm_msg_send_total                                 | 调用第三方服务发送短信/邮件/微信消息的条数 | 数值 | **provider**：服务商，值为：aliyun、tencent、aws、twilio **product**：云产品，值为：ali-sms、tencent-sms、tencent-wxmp、aws-sns、twilio-sms、ali-directMail、aws-ses |                                | 上报的类型为Counter         |
| yl_be_nm_msg_send_queue_size                            | 消息发送队列的大小                         | 数值 | **msg_type**: 消息类型，值为：sms、mail、wx **priority**：优先级，值为：low、medium、high |                                | 上报的类型为Gauge           |
| yl_be_nm_service_config_info                            | 当前服务配置信息                           | NaN  | **wechat_enable**：是否开启微信服务 **ali_sms_host**：阿里云短信服务host **tencent_sms_host**：腾讯云短信服务host **aws_sms_region**：AWS短信服务区域 **sms_send_strategy**：短信发送策略 **mail_send_strategy**：邮件发送策略 **wechat_send_strategy**：微信发送策略 **mfa_enable**: 是否开启多因子校验 **channel_ticket_generate_rate**：产生令牌的速度，及从请求队列中获取请求的速度 |                                | 配置信息，上报的类型为Gauge |
| yl_be_nm_sms_provider_config_info                       | 当前短信服务商配置信息                     | NaN  | **id**：服务商id **enable**：是否启用 **provider**：服务商类型，值为：aliyun、tencent、aws、twilio **access_key**：AccessKeyId **is_master**：是否为主账号 |                                | 配置信息，上报的类型为Gauge |
| yl_be_nm_mail_provider_config_info                      | 当前邮件服务商配置信息                     | NaN  | **id**：服务商id **enable**：是否启用 **provider**：服务商类型，值为：aliyun、tencent、aws、twilio **access_key**：AccessKeyId **host**：smtp服务器地址 **is_master**：是否为主账号 |                                | 配置信息，上报的类型为Gauge |
| yl_be_nm_wechat_provider_config_info                    | 当前微信服务商配置信息                     | NaN  | **id**：服务商id **enable**：是否启用 **provider**：服务商类型，值为：aliyun、tencent、aws、twilio **access_key**：AccessKeyId **is_master**：是否为主账号 |                                | 配置信息，上报的类型为Gauge |
| yl_be_nm_weixin_mp_config_info                          | 当前微信公众号配置信息                     | NaN  | **wechat_links_mobile_register**：手机注册链接 **wechat_links_mobile_binding_wechat**：手机绑定微信链接 **wechat_links_mobile_help_center**：手机帮助中心链接 **wechat_links_mobile_portal**：手机门户链接 **wechat_links_mobile_mall_software_download**：手机、邮件下载链接 **wechat_meeting_url**：会议链接 |                                | 配置信息，上报的类型为Gauge |

| metric（<font color='red'>http-scheduler</font>） | metric说明(用途)     | 值   | 必选label    | 可选label | 备注 |
| ------------------------------------------------- | -------------------- | ---- | ------------ | --------- | ---- |
| service_request_rate_per_second                   | 请求速率(每秒请求数) | 数值 | service_name | item      | 示例 |

| metric（<font color='red'>developer-manager</font>） | metric说明(用途)                | 值                                                           | 必选label           | 可选label | 备注                   |
| ---------------------------------------------------- | ------------------------------- | ------------------------------------------------------------ | ------------------- | --------- | ---------------------- |
| yl_developer_manager_authenticate_total              | 获取访问token请求数量           | 数值                                                         | method、module、uri |           |                        |
| yl_developer_manager_authenticate_failed_total       | 获取访问token错误数量           | 数值                                                         | method、module、uri |           |                        |
| yl_developer_manager_check_total                     | 验证访问token请求数量           | 数值                                                         | method、module、uri |           |                        |
| yl_developer_manager_check_failed_total              | 验证访问token错误数量           | 数值                                                         | method、module、uri |           |                        |
| yl_be_schedule_exec_time                             | 各定时任务执行时间点上报        | 数值                                                         | service_name        | task_name | task_name为任务的名称  |
| yl_be_schedule_exec_status                           | 各定时任务执行状态上报          | 数值                                                         | service_name        | task_name | task_name为任务的名称  |
| yl_be_schedule_cost_time_seconds                     | 各定时任务执行耗时上报          | 数值                                                         | service_name        | task_name | task_name为任务的名称  |
| yl_be_com_yealink_logger_level                       | 当前com.yealink服务日志级别上报 | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name        |           |                        |
| yl_be_root_logger_level                              | 当前ROOT服务日志级别上报        | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name        |           |                        |
| yl_be_thread_pool_active_thread                      | 线程池活动线程数量              | 数值                                                         | thread_name         |           | thread_name ：线程名称 |
| yl_be_thread_pool_queue                              | 线程池任务队列中任务数量        | 数值                                                         | thread_name         |           | thread_name ：线程名称 |
| yl_be_thread_pool_task                               | 线程池执行的任务数量            | 数值                                                         | thread_name         |           | thread_name ：线程名称 |
| yl_be_thread_pool_largest_thread                     | 线程池曾经达到的最大峰值数量    | 数值                                                         | thread_name         |           | thread_name ：线程名称 |

| metric（<font color='red'>user-manager</font>） | metric说明(用途)                                 | 值                                                           | 必选label                 | 可选label                                                    | 备注                                                         |
| ----------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------ | ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| yl_be_individual_register_total                 | 个人注册新增量统计                               | 数值                                                         | service_name              | -                                                            |                                                              |
| yl_be_enterprise_register_total                 | 企业注册新增量统计                               | 数值                                                         | service_name              | -                                                            |                                                              |
| yl_be_party_register_amount                     | 当前平台注册的企业数量                           | 数值                                                         | service_name，region_name | -                                                            | region_name为区域的文本信息，值范围为运维划分的区域          |
| yl_be_individual_register_amount                | 当前平台注册的用户数量                           | 数值                                                         | service_name，region_name | -                                                            | region_name为区域的文本信息，值范围为运维划分的区域          |
| yl_be_xdebug                                    | 是否开启XDEBUG模式                               | 0 开启，1 关闭                                               | service_name              | -                                                            |                                                              |
| yl_be_data_center_region                        | 无明确数据归属的数据所属的数据中心区域信息       | label中的 region上报                                         | service_name              | region_name                                                  | region_name为区域的文本信息，值范围为运维划分的区域          |
| yl_be_region                                    | 运维配置的region信息上报                         | label中的 region上报                                         | service_name              | region_name                                                  | region_name为区域的文本信息，值范围为运维划分的区域          |
| yl_be_machine_verify_health                     | 人机校验可达性上报                               | 0/正常;1/异常                                                | service_name              | -                                                            |                                                              |
| yl_be_feign_request                             | 本服务调用其他服务接口的请求信息                 | 数值                                                         | service_name              | request_url                                                  | request_url所请求的url                                       |
| yl_be_trace_source_total                        | 回源操作调用次数信息，源uri与调用uri维度维度上报 | 数值                                                         | service_name              | source_request，source_region，target_request，target_region | source_request：来源请求，source_region：来源请求所属region，target_request：转换后的目标请求，target_region：转换后的目标区域 |
| yl_be_schedule_exec_time                        | 各定时任务执行时间点上报                         | 数值                                                         | service_name              | task_name                                                    | task_name为任务的名称                                        |
| yl_be_schedule_exec_status                      | 各定时任务执行状态上报                           | 数值                                                         | service_name              | task_name                                                    | task_name为任务的名称                                        |
| yl_be_schedule_cost_time_seconds                | 各定时任务执行耗时上报                           | 数值                                                         | service_name              | task_name                                                    | task_name为任务的名称                                        |
| yl_be_com_yealink_logger_level                  | 当前com.yealink服务日志级别上报                  | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name              |                                                              |                                                              |
| yl_be_root_logger_level                         | 当前ROOT服务日志级别上报                         | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name              |                                                              |                                                              |
| yl_be_oss_status                                | oss可用服务状态                                  | 0/正常;1/异常                                                | service_name              |                                                              |                                                              |
| yl_be_es_status                                 | es可用服务状态                                   | 0/正常;1/异常                                                | service_name              |                                                              |                                                              |
| yl_be_log_stash_status                          | log stash可用服务状态                            | 0/正常;1/异常                                                | service_name              |                                                              |                                                              |
| yl_be_thread_pool_active_thread                 | 线程池活动线程数量                               | 数值                                                         | thread_name               |                                                              | thread_name ：线程名称                                       |
| yl_be_thread_pool_queue                         | 线程池任务队列中任务数量                         | 数值                                                         | thread_name               |                                                              | thread_name ：线程名称                                       |
| yl_be_thread_pool_task                          | 线程池执行的任务数量                             | 数值                                                         | thread_name               |                                                              | thread_name ：线程名称                                       |
| yl_be_thread_pool_largest_thread                | 线程池曾经达到的最大峰值数量                     | 数值                                                         | thread_name               |                                                              | thread_name ：线程名称                                       |

| metric（<font color='red'>phonebook-manager</font>） | metric说明(用途)                    | 值                                                           | 必选label    | 可选label   | 备注                                           |
| ---------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------ | ------------ | ----------- | ---------------------------------------------- |
| yl_be_phonebook_version                              | 地址簿协商时下发的 地址簿版本号信息 | label中的 version上报                                        | service_name | version     | -                                              |
| yl_be_region                                         | 运维配置的region信息上报            | label中的 region上报                                         | service_name | region_name | region为区域的文本信息，值范围为运维划分的区域 |
| yl_be_you_tu_be_status                               | youtube 直播认证的接口耗时上报      | 0/正常;1/异常                                                | service_name | -           |                                                |
| yl_be_feign_request                                  | 本服务调用其他服务接口的请求信息    | 数值                                                         | service_name | request_url | request_url所请求的url                         |
| yl_be_schedule_exec_time                             | 各定时任务执行时间点上报            | 数值                                                         | service_name | task_name   | task_name为任务的名称                          |
| yl_be_schedule_exec_status                           | 各定时任务执行状态上报              | 数值                                                         | service_name | task_name   | task_name为任务的名称                          |
| yl_be_schedule_cost_time_seconds                     | 各定时任务执行耗时上报              | 数值                                                         | service_name | task_name   | task_name为任务的名称                          |
| yl_be_com_yealink_logger_level                       | 当前com.yealink服务日志级别上报     | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name |             |                                                |
| yl_be_root_logger_level                              | 当前ROOT服务日志级别上报            | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name |             |                                                |
| yl_be_thread_pool_active_thread                      | 线程池活动线程数量                  | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |
| yl_be_thread_pool_queue                              | 线程池任务队列中任务数量            | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |
| yl_be_thread_pool_task                               | 线程池执行的任务数量                | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |
| yl_be_thread_pool_largest_thread                     | 线程池曾经达到的最大峰值数量        | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |

| metric（<font color='red'>service-ticket-manager</font>） | metric说明(用途)                 | 值                                                           | 必选label    | 可选label   | 备注                                           |
| --------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------ | ------------ | ----------- | ---------------------------------------------- |
| yl_be_region                                              | 运维配置的region信息上报         | label中的 region上报                                         | service_name | region_name | region为区域的文本信息，值范围为运维划分的区域 |
| yl_be_feign_request                                       | 本服务调用其他服务接口的请求信息 | 数值                                                         | service_name | request_url | request_url所请求的url                         |
| yl_be_schedule_exec_time                                  | 各定时任务执行时间点上报         | 数值                                                         | service_name | task_name   | task_name为任务的名称                          |
| yl_be_schedule_exec_status                                | 各定时任务执行状态上报           | 数值                                                         | service_name | task_name   | task_name为任务的名称                          |
| yl_be_schedule_cost_time_seconds                          | 各定时任务执行耗时上报           | 数值                                                         | service_name | task_name   | task_name为任务的名称                          |
| yl_be_com_yealink_logger_level                            | 当前com.yealink服务日志级别上报  | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name |             |                                                |
| yl_be_root_logger_level                                   | 当前ROOT服务日志级别上报         | 0 UNKNOWN,1 TRACE,2 DEBUG,3 INFO,4 WARN,5 ERROR,6 FATAL,7 OFF | service_name |             |                                                |
| yl_be_thread_pool_active_thread                           | 线程池活动线程数量               | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |
| yl_be_thread_pool_queue                                   | 线程池任务队列中任务数量         | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |
| yl_be_thread_pool_task                                    | 线程池执行的任务数量             | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |
| yl_be_thread_pool_largest_thread                          | 线程池曾经达到的最大峰值数量     | 数值                                                         | thread_name  |             | thread_name ：线程名称                         |

| metric（<font color='red'>yga</font>）   | metric说明(用途)          | 值/采集数据类型 | 必选label                 | 可选label |
| ---------------------------------------- | ------------------------- | --------------- | ------------------------- | --------- |
| yl_health                                | 当前服务健康状态          | 0-开启，1-关闭  | service_name              |           |
| yl_be_yga_config_switch                  | 当前服务各个配置开关情况  | 0-开启，1-关闭  | serviceName,region        |           |
| yl_be_yga_config                         | 配置信息展示              | 0               | serviceName,region        |           |
| yl_be_yga_http_region_forward            | 基于区域的转发次数        | Counter         | region,toRegion,toAddress | biz       |
| yl_be_yga_http_region_payload_bytes      | 基于区域的转发负载大小    | Summary         | region,toRegion,toAddress |           |
| yl_be_yga_http_region_delay_mills        | 基于区域的转发时延        | Summary         | region,toRegion,toAddress |           |
| yl_be_yga_http_no_token_url_access       | 基于url的无token访问      | Counter         | region                    |           |
| yl_be_yga_tcp_region_forward             | TCP基于区域的转发次数     | Counter         | region,toRegion,toAddress | biz       |
| yl_be_yga_tcp_region_payload_bytes       | TCP基于区域的转发负载大小 | Summary         | region,toRegion,toAddress |           |
| yl_be_yga_im_conn_num                    | im当前活动连接数          | Gauge           | region,address            |           |
| yl_be_yga_http_conn_num                  | http当前活跃链接数        | Gauge           | region,address            |           |
| yl_be_yga_error_code                     | 错误码统计                | Summary         | code,name                 | region    |
| yl_be_yga_http_region_forward_seconds    | 处理http转发请求耗时      | Histogram       | region,toRegion,toAddress | biz       |
| yl_be_yga_http_region_costs_seconds      | yga下游处理耗时           | Histogram       | region,toRegion,toAddress | biz       |
| jvm/processor/uptime/files/log4j2        | 系统类指标搜集项          | -               | -                         | -         |
| yl_be_yga_netty_direct_memory_used_ratio | netty直接内存使用百分比   | Gauge           | id                        |           |

| metric（<font color='red'>pushbackend、pushfrontend</font>） | metric说明(用途) | 值/采集数据类型 | 必选label   | 可选label                  |
| ------------------------------------------------------------ | ---------------- | --------------- | ----------- | -------------------------- |
| yl_be_push_msg_nums                                          | 推送消息数       | Summary         | serviceName | region,biz,channel,subTags |
| yl_be_push_msg_delay_seconds                                 | 推送消息耗时     | Summary         | serviceName | region,biz,channel,subTags |

| metric（<font color='red'>yregister</font>） | metric说明(用途)                 | 值   | 必选label  | 可选label | 备注                                                         |
| -------------------------------------------- | -------------------------------- | ---- | ---------- | --------- | ------------------------------------------------------------ |
| yl_be_yregister_meeting_count                | meeting通道各型号注册数（前100） | 数值 | model_name |           | total、各型号名称（VC200、VC800等），加上total，最多有101个lable |
| yl_be_yregister_phone_count                  | phone通道各型号注册数（前100）   | 数值 | model_name |           | total、各型号名称（VC200、VC800等），加上total，最多有101个lable |

| metric（<font color='red'>regulator</font>） | metric说明(用途) | 值   | 必选label | 可选label | 备注 |
| -------------------------------------------- | ---------------- | ---- | --------- | --------- | ---- |
| yl_be_regulator_http_conn_num                | 连接数数量       | 数值 |           |           |      |
| yl_be_regulator_dm_conn_num                  | dm长连接数数量   | 数值 |           |           |      |



## d. YBDP

### 1.基础metrics

| metric        | metric说明(用途) | 值            | 必选label | 可选label |
| ------------- | ---------------- | ------------- | --------- | --------- |
| yl_health     | 服务健康检查     | 0/正常;1/异常 |           |           |
| yl_start_time | 服务启动时间     | 时间戳        |           |           |

### 2.业务metrics


| metric（<font color='red'>rocketmq-proxy</font>） | metric说明(用途)                                   | 值        | 必选label      | 可选label | 备注 |
| ------------------------------------------------- | -------------------------------------------------- | --------- | -------------- | --------- | ---- |
| yl_ynn_rocketmq_proxy_consumer_instance           | 当前存活的 consumer 实例数                         | Gauge     |                |           |      |
| yl_ynn_rocketmq_proxy_producer_instance           | 当前存活的 producer 实例数                         | Gauge     |                |           |      |
| yl_ynn_rocketmq_proxy_consumer_message_total      | pull 到的消息总数                                  | Counter   | result         |           |      |
| yl_ynn_rocketmq_proxy_consumer_message_total      | push 出的消息总数                                  | Counter   | method, result |           |      |
| yl_ynn_rocketmq_proxy_consumer_pull_delay_seconds | consumer pull 到消息距离消息存入 mq 的延迟分布指标 | Histogram | client_id      |           |      |

| metric（<font color='red'>redis-proxy</font>）   | 类型                   | 单位   | 说明（用途）                 | label名称                              | 备注                                   |
| ------------------------------------------------ | ---------------------- | ------ | ---------------------------- | -------------------------------------- | -------------------------------------- |
| yl_ybsp_redis_proxy_cmd_duration_seconds         | Histogram(0.01, 2, 12) | second | 命令执行延迟                 | method：redis命令                      | 显示命令执行延迟所占各个时间端的百分比 |
| yl_ybsp_redis_proxy_error_total                  | Counter                | short  | redis错误次数                | method: 错误的redis命令 type：错误类型 | 显示错误频率                           |
| yl_ybsp_redis_proxy_request_total                | Counter                | short  | redis请求数                  | method：redis命令                      | 显示TPS                                |
| yl_ybsp_redis_proxy_session                      | Guage                  | short  | 当前连接的终端数             |                                        | 显示连接数                             |
| yl_ybsp_redis_proxy_pub_total                    | Counter                | short  | publish的某个订阅消息的次数  | key：订阅的Key                         | 统计次数                               |
| yl_ybsp_redis_proxy_input_bandwidth_bytes_total  | Counter                | byte   | input带宽                    | app: 客户端服务名                      | 统计流入带宽流量                       |
| yl_ybsp_redis_proxy_output_bandwidth_bytes_total | Counter                | byte   | output带宽                   | app: 客户端服务名                      | 统计流出带宽流量                       |
| yl_ybsp_redis_proxy_backends                     | Gauge                  | short  | proxy与redis的连接数         | addr: redis地址 type：连接类型         |                                        |
| yl_ybsp_redis_proxy_alert_total                  | Counter                | short  | 告警metric，计数+1就需要告警 | app: 客户端服务名 type：告警类型       | 计数+1就需要告警                       |
| yl_ybsp_redis_proxy_cfg_config_warn_total        | Counter                | short  | 配置服务告警metrics          | name: 配置key                          |                                        |

| metric（<font color='red'>idbuilder</font>）     | 类型      | 单位   | 说明（用途）                         | label名称           | 备注 |
| ------------------------------------------------ | --------- | ------ | ------------------------------------ | ------------------- | ---- |
| yl_ybsp_idbuilder_grpc_server_multi_ids_total    | Histogram | short  | grpc调用批量ids的次数                | grpc_code id_from   |      |
| yl_ybsp_idbuilder_grpc_server_duration_seconds   | Histogram | second | grpc耗时分布                         | grpc_code id_from   |      |
| yl_ybsp_idbuilder_thrift_server_started_total    | Counter   | short  | thrift被请求次数                     | thrift_code id_from |      |
| yl_ybsp_idbuilder_thrift_server_duration_seconds | Histogram | second | thrift耗时分布                       | thrift_code id_from |      |
| yl_ybsp_idbuilder_thrift_server_multi_ids_total  | Histogram | short  | thrift调用批量ids的次数              | thrift_code id_from |      |
| yl_ybsp_idbuilder_distribute_started_total       | Counter   | short  | idbuilder分布式node_id切换次数，耗时 | action              |      |
| yl_ybsp_idbuilder_error_total                    | Counter   | short  | error统计                            | type                |      |

| metric（<font color='red'>kvpubsub</font>）      | 类型      | 单位   | 说明（用途）                | label名称                                       | 备注                            |
| ------------------------------------------------ | --------- | ------ | --------------------------- | ----------------------------------------------- | ------------------------------- |
| yl_ybsp_kvpubsub_error_total                     | Counter   | short  | RPC错误次数                 | app: 业务名 region：所在区域 method：调用方法名 | 显示统计错误次数                |
| yl_ybsp_kvpubsub_rpc_cmd_duration_seconds        | Histogram | Second | RPC命令执行时间             | app: 业务名 region：所在区域 method：调用方法名 | 显示命令执行延迟                |
| yl_ybsp_kvpubsub_rpc_method_msg_recv_bytes_total | Counter   | byte   | 消息接收字节数              | app: 业务名 region：所在区域 method：调用方法名 | 显示接收字节数的频率            |
| yl_ybsp_kvpubsub_rpc_method_msg_send_bytes_total | Counter   | byte   | 消息发送字节数              | app: 业务名 region：所在区域 method：调用方法名 | 显示发送字节数的频率            |
| yl_ybsp_kvpubsub_rpc_method_total                | Counter   | short  | 命令调用次数                | app: 业务名 region：所在区域 method：调用方法名 | 显示命令调用次数频率            |
| yl_ybsp_kvpubsub_rpc_sub_concurrent              | Guage     | short  | 订阅命令并发数              | app: 业务名 region：所在区域 method：调用方法名 | 显示并发数                      |
| yl_ybsp_kvpubsub_rpc_sub_pub_total               | Counter   | short  | 订阅通告发送次数            | app: 业务名 region：所在区域 method：调用方法名 | 显示订阅通告发送频率            |
| yl_ybsp_kvpubsub_redis_error_total               | Counter   | short  | redis错误次数               | type：                                          | 显示redis错误次数               |
| yl_ybsp_kvpubsub_redis_sub_change_total          | Counter   | short  | 收到redis订阅变更次数       | type：订阅变更key                               | 显示redis发来的订阅变更次数     |
| yl_ybsp_kvpubsub_redis_sub_total                 | Counter   | short  | kvpubsub跟redis的订阅连接数 | type：订阅channel                               | 显示kvpubsub跟redis的订阅连接数 |
| yl_ybsp_kvpubsub_cfg_config_warn_total           | Counter   | short  | kvpubsub配置服务告警        | name: 配置服务Key                               |                                 |

| metric（<font color='red'>dbhook</font>） | 单位 | 是否必选 | 类型    | 介绍                                   | label名称                |
| ----------------------------------------- | ---- | -------- | ------- | -------------------------------------- | ------------------------ |
| yl_dbhook_queries_total                   |      | 是       | counter | 访问这个实例请求                       |                          |
| yl_dbhook_transactions_total              |      | 是       | counter | 访问这个实例事务数                     |                          |
| yl_dbhook_connections                     |      | 是       | Gauge   | 访问当前实例的总连接数                 |                          |
| yl_dbhook_audit_error_total               |      | 是       | counter | 审计线程健康检查，异常解析跳过输出个数 |                          |
| yl_dbhook_error_total                     |      | 是       | counter | 服务错误计数                           | type: load_cfg/watch_cfg |

| metric（<font color='red'>drainer</font>） | 类型                  | 单位    | 说明（用途）           | label名称         | 备注                           |
| ------------------------------------------ | --------------------- | ------- | ---------------------- | ----------------- | ------------------------------ |
| yl_ynn_drainer_consumer_pull_time_seconds  | Histogram(0.01,2,14)  | seconds | 从MQ-Proxy拉取消息耗时 | 无                | 示例，显示QPS和拉取消息延迟    |
| yl_ynn_drainer_consumer_binlog_size_total  | Counter               | Bytes   | 拉取消息的字节数       | 无                | 示例，显示某段时间内消费的大小 |
| yl_ynn_drainer_consumer_binlog_count_total | Counter               | short   | 拉取消息的个数         | 无                | 示例，显示某段时间内消费的个数 |
| yl_ynn_drainer_p2c_duration_seconds        | Histogram(1,2,10)     | seconds | 生产到消费耗时         | 无                | 示例，显示99的耗时统计         |
| yl_ynn_drainer_error_total                 | Counter               | short   | 消费时的错误次数       | type: 错误类型    | 示例，按错误类型区分           |
| yl_ynn_drainer_event_total                 | Counter               | short   | 执行DML事件的统计      | type: 事件类型    | 示例，显示执行DML事件的频率    |
| yl_ynn_drainer_execute_duration_seconds    | Histogram(0.01,4,8)   | seconds | 执行DMLs的耗时         | 无                | 示例，显示99的耗时统计         |
| yl_ynn_drainer_query_duration_seconds      | Histogram(0.001,2,14) | seconds | 执行数据库Query的耗时  | type: exec/commit | 示例，显示99的耗时统计         |

| metric（<font color='red'>pump</font>）           | 类型                  | 单位      | 说明（用途）             | label名称                | 备注                               |
| ------------------------------------------------- | --------------------- | --------- | ------------------------ | ------------------------ | ---------------------------------- |
| yl_ynn_pump_storage_size_bytes                    | Gauge                 | bytes     | 存储容量和用量           | type: available/capacity | 示例                               |
| yl_ynn_pump_storage_gc_ts                         | Gauge                 | Date&Time | GC清理时间               | 无                       | 示例                               |
| yl_ynn_pump_storage_max_commit_ts                 | Gauge                 | Date&Time | 当前存储binlog的CommitTs | 无                       | 示例                               |
| yl_ynn_pump_storage_query_tikv_total              | Counter               | short     | 查询TIKV的次数           | 无                       | 示例                               |
| yl_ynn_pump_storage_error_total                   | Counter               | short     | 存储错误的次数           | type: 存储错误阶段       | 示例，显示存储阶段的错误次数的频率 |
| yl_ynn_pump_storage_write_binlog_duration_seconds | Histogram(0.001,2,14) | seconds   | 写入磁盘耗时             | type: 写入阶段           | 示例，显示99和95的写入延迟         |
| yl_ynn_pump_storage_write_binlog_bytes            | Histogram(128,2,14)   | bytes     | 写入的字节数             | type: single/batch       | 示例，显示99和95的写入字节数       |
| yl_ynn_pump_rpc_write_binlog_duration_seconds     | Histogram(0.001,2,14) | seconds   | TIDB调用接口写binlog耗时 | label: succ/fail         | 示例，显示QPS和写入延迟            |
| yl_ynn_pump_producer_binlog_duration_seconds      | Histogram(0.01,2,14)  | seconds   | 发送消息到MQ的耗时       | type: succ/fail          | 示例，显示QPS和发送延迟            |
| yl_ynn_pump_producer_binlog_bytes                 | Histogram(1024,2,14)  | seconds   | 发送消息的字节数         | 无                       | 示例                               |

| metric（<font color='red'>sync-manager</font>）   | metric说明(用途)            | 值        | 必选label                    | 可选label | 备注 |
| ------------------------------------------------- | --------------------------- | --------- | ---------------------------- | --------- | ---- |
| yl_ynn_sync_manager_dump_request_duration_seconds | 请求 dump_server 的响应延迟 | Histrgram | act_region, function, result |           |      |
| yl_ynn_sync_manager_revise_failed_total           | 稽查失败计数                | Counter   | db, tab                      |           |      |
| yl_ynn_sync_manager_revise_diff_total             | 稽查不一致数据量计数        | Counter   | db, tab                      |           |      |

| metric（<font color='red'>tlpush</font>） | 类型                 | 单位    | 说明（用途） | label名称 | 备注 |
| ----------------------------------------- | -------------------- | ------- | ------------ | --------- | ---- |
| yl_im_tlpush_error_total                  | Counter              | short   | 错误次数     | type      | 无   |
| yl_im_tlpush_rpc_method_duration_seconds  | Histogram(0.01,2,14) | seconds | 接口调用耗时 | method    | 无   |
| yl_im_tlpush_rpc_method_total             | Counter              | short   | 接口调用次数 | method    | 无   |

| metric（<font color='red'>tlstore</font>） | 类型                 | 单位    | 说明（用途） | label名称 | 备注 |
| ------------------------------------------ | -------------------- | ------- | ------------ | --------- | ---- |
| yl_im_tlstore_error_total                  | Counter              | short   | 错误次数     | type      | 无   |
| yl_im_tlstore_rpc_method_duration_seconds  | Histogram(0.01,2,14) | seconds | 接口调用耗时 | method    | 无   |
| yl_im_tlstore_rpc_method_total             | Counter              | short   | 接口调用次数 | method    | 无   |

| metric（<font color='red'>cfgagent</font>） | metric说明(用途)         | 值   | 必选label | 可选label | 备注 |
| ------------------------------------------- | ------------------------ | ---- | --------- | --------- | ---- |
| WatchKeySize                                | 在监听etcd key 的数量    | 数值 |           | item      | 示例 |
| CfgSize                                     | 还在watch 配置的连接数量 | 数值 |           | item      | 示例 |

| metric（<font color='red'>dump</font>） | metric说明(用途) | 值        | 必选label        | 可选label | 备注 |
| --------------------------------------- | ---------------- | --------- | ---------------- | --------- | ---- |
| yl_ynn_dump_node_num                    | dump 节点数量    | Gauge     |                  |           |      |
| yl_ynn_dump_db_exec_duration_seconds    | 数据库执行延迟   | Histogram | function, method |           |      |

| metric（<font color='red'>jaeger-analytics</font>） | 类型      | 单位   | 说明（用途）        | label名称                                                    | 备注                                               |
| --------------------------------------------------- | --------- | ------ | ------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| trace_latency_seconds                               | histogram | second | 链路延迟            | cross_region: 链路是否跨区域 rootSpan: 链路根节点 environment：链路属于哪个环境 | 显示所有链路的平均延迟，同一张表展示               |
| mq_latency_seconds                                  | histogram | second | MQ生产消费延迟      | rootSpan: 链路根节点 region：区域 topic： 消费主题 consumer：消费者 | 显示所有MQ的平均延迟，同一张表展示                 |
| network_latency_seconds                             | histogram | second | 各区域YGA之间的延迟 | client: 客户端 server：服务端 environment: 链路属于哪个环境  |                                                    |
| request_total                                       | Counter   | Int    | 各个服务接口QPS     | service_name：服务名 operation：接口名                       | 所有服务和接口显示在同一张表上，可以分析TOP10 接口 |

| metric（<font color='red'>web-rds-sync-manager</font>） | metric说明(用途)     | 值   | 必选label    | 可选label | 备注 |
| ------------------------------------------------------- | -------------------- | ---- | ------------ | --------- | ---- |
| service_request_rate_per_second                         | 请求速率(每秒请求数) | 数值 | service_name | item      | 示例 |

### 3.告警metrics

| metric（<font color='red'>dbhook</font>）                    | 说明               | 告警类型     |
| ------------------------------------------------------------ | ------------------ | ------------ |
| rate(yl_dbhook_error_total[1m]) > 0                          | 存储发生错误       | 故障警告     |
| **metric（<font color='red'>drainer</font>）**               | **说明**           | **告警类型** |
| rate(yl_ynn_drainer_error_total[1m]) > 0                     | 消费时落盘失败     | 故障警告     |
| **metric（<font color='red'>pump</font>）**                  | **说明**           | **告警类型** |
| rate(yl_ynn_pump_storage_error_total[1m]) > 0                | 存储发生错误       | 故障警告     |
| rate(yl_ynn_pump_rpc_write_binlog_duration_seconds[1m]) > 2s | 存储速度慢         | 问题警告     |
| rate(yl_ynn_pump_producer_binlog_duration_seconds[1m]) > 30s | 生产速度慢(GA网络) | 问题警告     |
