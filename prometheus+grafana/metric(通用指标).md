# 通用指标

## nodejs koa

| name（<font color='red'>nodejs koa</font>） | 指标类型  | 含义以及应用                                                 |
| ------------------------------------------- | --------- | ------------------------------------------------------------ |
| nodejs_eventloop_lag_seconds                | gauge     | Lag of event loop in seconds                                 |
| nodejs_eventloop_lag_min_seconds            | gauge     | The minimum recorded event loop delay                        |
| nodejs_eventloop_lag_max_seconds            | gauge     | The maximum recorded event loop delay                        |
| nodejs_eventloop_lag_mean_seconds           | gauge     | The mean of the recorded event loop delays                   |
| nodejs_eventloop_lag_stddev_seconds         | gauge     | The standard deviation of the recorded event loop delays     |
| nodejs_eventloop_lag_p50_seconds            | gauge     | The 50th percentile of the recorded event loop delays        |
| nodejs_eventloop_lag_p90_seconds            | gauge     | The 90th percentile of the recorded event loop delays        |
| nodejs_eventloop_lag_p99_seconds            | gauge     | The 99th percentile of the recorded event loop delays        |
| nodejs_active_handles                       | gauge     | Number of active libuv handles grouped by handle type. Every handle type is C++ class name |
| nodejs_active_handles_total                 | gauge     | Total number of active handles                               |
| nodejs_active_requests                      | gauge     | Number of active libuv requests grouped by request type. Every request type is C++ class name |
| nodejs_active_requests_total                | gauge     | Total number of active requests                              |
| nodejs_heap_size_total_bytes                | gauge     | Process heap size from Node.js in bytes                      |
| nodejs_heap_size_used_bytes                 | gauge     | Process heap size used from Node.js in bytes                 |
| nodejs_external_memory_bytes                | gauge     | Node.js external memory size in bytes                        |
| nodejs_heap_space_size_total_bytes          | gauge     | Process heap space size total from Node.js in bytes          |
| nodejs_heap_space_size_used_bytes           | gauge     | Process heap space size used from Node.js in bytes           |
| nodejs_heap_space_size_available_bytes      | gauge     | Process heap space size available from Node.js in bytes      |
| nodejs_version_info                         | gauge     | Node.js version info.                                        |
| nodejs_gc_duration_seconds                  | histogram | Garbage collection duration by kind, one of major, minor, incremental or weakcb |
| app_version                                 | gauge     | The service version by package.json                          |
| http_request_duration_seconds               | histogram | Duration of HTTP requests in seconds                         |
| http_request_size_bytes                     | histogram | Size of HTTP requests in bytes                               |

## java_springboot 

### jvm-memory-buffer

- 标签
  - id:
    - jvm_buffer_count | jvm_buffer_total_capacity_bytes | jvm_buffer_memory_used_bytes: 取值`direct | mapped`
    - jvm_memory_committed_bytes | jvm_memory_used_bytes | jvm_memory_max_bytes: 取值`Code Cache | Metaspace | Compressed Class Space | Eden Space | Survivor Space | Tenured Gen`
  - area:
    - jvm_memory_committed_bytes | jvm_memory_used_bytes | jvm_memory_max_bytes:取值`heap | nonheap`

| Metric name                     | Metric type | Labels/tags | 说明                                                         |
| ------------------------------- | ----------- | ----------- | ------------------------------------------------------------ |
| jvm_buffer_count                | Gauge       | `id`        | An estimate of the number of buffers in the pool             |
| started or peak was reset       |             |             |                                                              |
| jvm_buffer_total_capacity_bytes | Gauge       | `id`        | An estimate of the total capacity of the buffers in this pool |
| jvm_buffer_memory_used_bytes    | Gauge       | `id`        | An estimate of the memory that the Java virtual machine is using for this buffer pool |
| jvm_memory_used_bytes           | Gauge       | `area`,`id` | The amount of used memory                                    |
| jvm_memory_max_bytes            | Gauge       | `area`,`id` | The maximum amount of memory in bytes that can be used for memory management |
| jvm_memory_committed_bytes      | Gauge       | `area`,`id` | The amount of memory in bytes that is committed for the Java virtual machine to use |

### jvm-class

| Metric name                | Metric type | Labels/tags | 说明                                                         |
| -------------------------- | ----------- | ----------- | ------------------------------------------------------------ |
| jvm_classes_loaded         | Gauge       |             | The number of classes that are currently loaded in the Java virtual machine |
| jvm_classes_unloaded_total | Counter     |             | The total number of classes unloaded since the Java virtual machine has started execution |

### jvm-threads

| Metric name        | Metric type | Labels/tags | 说明                                                         |
| ------------------ | ----------- | ----------- | ------------------------------------------------------------ |
| jvm_threads_live   | Gauge       |             | The current number of live threads including both daemon and non-daemon threads |
| jvm_threads_daemon | Gauge       |             | The current number of live daemon threads                    |
| jvm_threads_peak   | Gauge       |             | The peak live thread count since the Java virtual machine    |

### jvm-gc

- 标签
  - action: 取值`end of minor GC`
  - cause: 取值`Allocation Failure`

| Metric name                         | Metric type | Labels/tags      | 说明                                                         |
| ----------------------------------- | ----------- | ---------------- | ------------------------------------------------------------ |
| jvm_gc_memory_promoted_bytes_total  | Counter     |                  | Count of positive increases in the size of the old generation memory pool before GC to after GC |
| jvm_gc_max_data_size_bytes          | Gauge       |                  | Max size of old generation memory pool                       |
| jvm_gc_pause_seconds                | Summary     | `action`,`cause` | Time spent in GC pause                                       |
| jvm_gc_pause_seconds_max            | Gauge       | `action`,`cause` | Time spent in GC pause                                       |
| jvm_gc_live_data_size_bytes         | Gauge       |                  | Size of old generation memory pool after a full GC           |
| jvm_gc_memory_allocated_bytes_total | Counter     |                  | Incremented for an increase in the size of the young generation memory pool after one GC to before the next |

### tomcat

- 标签
  - name: 取值`default`

| Metric name            | Metric type | Labels/tags | 说明         |
| ---------------------- | ----------- | ----------- | ------------ |
| tomcat_threads_current | Gauge       | `name`      | 当前线程数量 |

### http

- 标签
  - exception: 取值`None`
  - method: 取值`http请求方法`
  - status: 取值`http状态码`
  - uri: 取值`具体uri`

| Metric name                      | Metric type | Labels/tags                         | 说明                                                         |
| -------------------------------- | ----------- | ----------------------------------- | ------------------------------------------------------------ |
| http_server_requests_seconds     | Summary     | `exception`,`method`,`status`,`uri` | http服务端请求延时                                           |
| http_server_requests_seconds_max | Gauge       | `exception`,`method`,`status`,`uri` | http服务端请求延时一段时间内的最大值，时间范围为指标抓取间隔https://stackoverflow.com/questions/57247185/spring-boot-actuator-max-property |



## go client

| name                             | 含义以及应用                                             |
| -------------------------------- | -------------------------------------------------------- |
| go_gc_duration_seconds           | GC垃圾收集延时                                           |
| go_goroutines                    | 当前并发执行单元数量                                     |
| go_info                          | 版本号                                                   |
| go_memstats_alloc_bytes          | 分配且在使用的内存大小                                   |
| go_memstats_alloc_bytes_total    | 总分配出的内存大小。配合rate计算内存增长率               |
| go_memstats_buck_hash_sys_bytes  | Number of bytes used by the profiling bucket hash table. |
| go_memstats_frees_total          | 释放的内存总量。配合rate计算内存释放率                   |
| go_memstats_gc_cpu_fraction      | 自程序启动以来，GC所使用的程序可用CPU时间的百分比        |
| go_memstats_gc_sys_bytes         | 用于垃圾收集系统元数据的字节数                           |
| go_memstats_heap_alloc_bytes     | 已分配且仍在使用的堆字节数                               |
| go_memstats_heap_idle_bytes      | 等待使用的堆字节数                                       |
| go_memstats_heap_inuse_bytes     | 正在使用的堆字节数                                       |
| go_memstats_heap_objects         | 分配对象的数量                                           |
| go_memstats_heap_released_bytes  | 释放到操作系统的堆字节数                                 |
| go_memstats_heap_sys_bytes       | 从系统获得的堆字节数                                     |
| go_memstats_last_gc_time_seconds | 上一次垃圾收集从1970年开始的秒数                         |
| go_memstats_lookups_total        | 指针查找的总数                                           |
| go_memstats_mallocs_total        | mallos的总数                                             |
| go_memstats_mcache_inuse_bytes   | mcache结构使用的字节数                                   |
| go_memstats_mcache_sys_bytes     | 从系统中获得的mcache结构所使用的字节数                   |
| go_memstats_mspan_inuse_bytes    | mspan结构使用的字节数                                    |
| go_memstats_mspan_sys_bytes      | 从system获得的mspan结构使用的字节数                      |
| go_memstats_next_gc_bytes        | 将发生下一次垃圾收集时的堆字节数                         |
| go_memstats_other_sys_bytes      | 用于其他系统分配的字节数                                 |
| go_memstats_stack_inuse_bytes    | 堆栈分配器使用的字节数                                   |
| go_memstats_stack_sys_bytes      | 从系统获得的堆栈分配器字节数                             |
| go_memstats_sys_bytes            | 从系统获得的字节数                                       |
| go_threads                       | 创建的OS线程数                                           |
| process_cpu_seconds_total        | 用户和系统CPU花费的总时间(以秒为单位)                    |
| process_max_fds                  | 打开的文件描述符的最大数目                               |
| process_open_fds                 | 打开的文件描述符的数目                                   |
| process_resident_memory_bytes    | 常驻内存大小(字节)                                       |
| process_start_time_seconds       | 从unix时代开始的进程启动时间(秒)                         |
| process_virtual_memory_bytes     | 虚拟内存大小(字节)                                       |
| process_virtual_memory_max_bytes | 可用虚拟内存的最大数量(以字节为单位)                     |

## redis_exporter 

### allocator

> [redis内存机制](https://redis.io/topics/memory-optimization)
>  当删除key时，redis不会将内存返还给系统。假设原有5G的数据，现在删除了2G的key，但是rss不会降低，即使redis宣称用户内存（used）是3G，因为潜在的内存分配器不会简单的释放内存。举例来说，大多数已删除的key和现存的key在同一个内存页中，所以无法释放内存。但是如果新插入2G数据，那么内存分配器会复用空闲的内存块，所以你删除2G旧数据和插入2G新数据之后，redis的内存RSS无明显变化。所以当rss很高，used很低时，内存碎片率（内存碎片率=rss/used）很高，这时新增的数据可以继续插入，不会导致redis oom的情况。监控redis内存的时候需要关注的是used/total，而不是rss/total。
>  根据以上的redis内存机制，得出结论：
>
> - 需要按照内存使用的峰值来配置redis的内存资源
> - 关注used/total内存配置告警
> - 给redis设置maxmemory，否则会吃掉系统所有内存

| 指标名称                        | 说明                       |
| ------------------------------- | -------------------------- |
| redis_active_defrag_running     | 活跃磁盘碎片清理工具的数量 |
| redis_allocator_active_bytes    | 活跃内存                   |
| redis_allocator_allocated_bytes | 已分配内存                 |
| redis_allocator_frag_bytes      | 内存碎片大小               |
| redis_allocator_frag_ratio      | 内存碎片率                 |
| redis_allocator_resident_bytes  | ?                          |
| redis_allocator_rss_bytes       | rss内存大小                |
| redis_allocator_rss_ratio       | rss ratio                  |
|                                 |                            |

### 持久化（AOF & RDB）

> [redis持久化](https://redis.io/topics/persistence)
>
> - RDB：指定的时间间隔执行数据集的时间点快照
>   - 优点:
>     - 压缩率高
>     - 恢复快
>   - 缺点:
>     - 数据丢失：遇到极端情况，会丢失几分钟的数据
>     - 性能影响：当数据量很大时，fork的子进程会占用较多的资源，可能影响redis正常服务
> - AOF：记录收到的每一个操作形成aof文件
>   - 优点:
>     - 数据可靠：实时写入，遇到极端情况可以恢复最新数据
>     - 策略灵活：可配置不同的fsync策略，以达到性能和备份的平衡
>   - 缺点:
>     - AOF文件比RDB大
>     - 数据恢复速度较RDB慢
> - rewrite: aof大小达到临界值时，fork一个子进程，创建一个临时文件，遍历数据库，将每个key、value对输出到临时文件。输出格式就是Redis的命令，但是为了减小文件大小，会将多个key、value对集合起来用一条命令表达。在rewrite期间的写操作会保存在内存的rewrite buffer中，rewrite成功后这些操作也会复制到临时文件中，在最后临时文件会代替AOF文件。

| 指标名称                               | 说明                    |
| -------------------------------------- | ----------------------- |
| redis_aof_current_rewrite_duration_sec | 当前rewrite持续时间     |
| redis_aof_enabled                      | 开启aof：value=1        |
| redis_aof_last_bgrewrite_status        | 上次bgrewrite状态       |
| redis_aof_last_cow_size_bytes          | ?                       |
| redis_aof_last_rewrite_duration_sec    | 上次rewrite持续时间     |
| redis_aof_last_write_status            | 上次aof写操作状态       |
| redis_aof_rewrite_in_progress          | 进行中的rewrite操作数量 |
| redis_aof_rewrite_scheduled            | 计划中的rewrite操作     |
| redis_rdb_bgsave_in_progress           | 进行中的bgsave操作      |
| redis_rdb_changes_since_last_save      | 上次落盘后改变的数据量  |
| redis_rdb_current_bgsave_duration_sec  | 当前bgsave持续时间      |
| redis_rdb_last_bgsave_duration_sec     | 上次bgsave持续时间      |
| redis_rdb_last_bgsave_status           | 上次bgsave状态          |
| redis_rdb_last_cow_size_bytes          | ?                       |
| redis_rdb_last_save_timestamp_seconds  | 上次落盘时间戳          |

### client

| 指标名称                                    | 说明                     |
| ------------------------------------------- | ------------------------ |
| redis_blocked_clients                       | 阻塞的客户端             |
| redis_client_recent_max_input_buffer_bytes  | 客户端最近输入最大buffer |
| redis_client_recent_max_output_buffer_bytes | 客户端最近输出最大buffer |
| redis_connected_clients                     | 已连接的客户端           |
| redis_connected_slaves                      | 已连接的slave数量        |
| redis_connections_received_total            | 接受的连接总量           |
|                                             |                          |

### cluster

| 指标名称              | 说明                  |
| --------------------- | --------------------- |
| redis_cluster_enabled | 开启集群模式，value=1 |

### commands

| 指标名称                              | 说明           |
| ------------------------------------- | -------------- |
| redis_commands_duration_seconds_total | 命令持续时间   |
| redis_commands_processed_total        | 命令执行总量   |
| redis_commands_total                  | 命令总调用次数 |
|                                       |                |

### config

| 指标名称                | 说明               |
| ----------------------- | ------------------ |
| redis_config_maxclients | 配置最大client数量 |
| redis_config_maxmemory  | 配置最大内存       |
| redis_commands_total    | 命令总调用次数     |

### key

| 指标名称                             | 说明                                |
| ------------------------------------ | ----------------------------------- |
| redis_db_keys                        | Total number of keys by DB          |
| redis_db_keys_expiring               | Total number of expiring keys by DB |
| redis_db_avg_ttl_seconds             | Avg TTL in seconds                  |
| redis_defrag_hits                    | 内存碎片整理命中                    |
| redis_defrag_key_hits                | 内存碎片整理key命中                 |
| redis_defrag_key_misses              | 内存碎片整理key未命中               |
| redis_defrag_misses                  | 内存碎片整理未命中                  |
| redis_evicted_keys_total             | 驱逐的key数量                       |
| redis_expired_keys_total             | 过期的key数量                       |
| redis_expired_time_cap_reached_total |                                     |
| redis_key_size                       | key大小                             |
| redis_key_value                      | key的值                             |
| redis_keyspace_hits_total            | 命中的key                           |
| redis_keyspace_misses_total          | 未命中的key                         |

### 资源

| 指标名称                                 | 说明                     |
| ---------------------------------------- | ------------------------ |
| redis_cpu_sys_children_seconds_total     | fork子进程cpu sys 时间   |
| redis_cpu_sys_seconds_total              | 主进程cpu sys 时间       |
| redis_cpu_user_children_seconds_total    | fork子进程cpu user 时间  |
| redis_cpu_user_seconds_total             | 主进程cpu user 时间      |
| redis_memory_max_bytes                   | 内存总大小               |
| redis_memory_used_bytes                  | 内存大小，不包含内存碎片 |
| redis_memory_used_dataset_bytes          | 数据集内存大小           |
| redis_memory_used_lua_bytes              | lua内存大小              |
| redis_memory_used_overhead_bytes         | overhead内存大小         |
| redis_memory_used_peak_bytes             | 内存峰值                 |
| redis_memory_used_rss_bytes              | rss内存大小              |
| redis_memory_used_scripts_bytes          | script使用的内存大小     |
| redis_memory_used_startup_bytes          | startup使用的内存大小    |
| redis_mem_clients_normal                 | 客户端连接占用内存       |
| redis_mem_clients_slaves                 | ?                        |
| redis_mem_fragmentation_bytes            | 碎片内存大小             |
| redis_mem_fragmentation_ratio            | 内存碎片率               |
| redis_mem_not_counted_for_eviction_bytes | 未计算的驱逐内存?        |

### others

| 指标名称                                   | 说明                   |
| ------------------------------------------ | ---------------------- |
| redis_last_slow_execution_duration_seconds | 最近一次慢查询持续时间 |
| redis_latest_fork_seconds                  | 最近一次fork子进程耗时 |
| redis_loading_dump_file                    |                        |
| redis_master_repl_offset                   |                        |

### **告警规则配置**

| 规则                                                 | 含义                     |
| ---------------------------------------------------- | ------------------------ |
| redis_memory_used_bytes/redis_memory_max_bytes > 0.9 | 使用内存大于90%          |
| redis_last_slow_execution_duration_seconds > ?       | 最近一次慢查询时间大于?s |
| redis_blocked_clients > 0                            | 出现客户端阻塞           |

## rocketmq-exporter

### **Broker**

| Name                  | Exposed information                               |
| --------------------- | ------------------------------------------------- |
| `rocketmq_broker_tps` | Broker produces the number of messages per second |
| `rocketmq_broker_qps` | Broker consumes messages per second               |

### **Producer**

| Name                             | Exposed information                                          |
| -------------------------------- | ------------------------------------------------------------ |
| `rocketmq_producer_tps`          | The number of messages produced per second per topic         |
| `rocketmq_producer_message_size` | The size of a message produced per second by a topic (in bytes) |
| `rocketmq_producer_offset`       | The progress of a topic's production message                 |

### Consumer Groups

| Name                                       | Exposed information                                          |
| ------------------------------------------ | ------------------------------------------------------------ |
| `rocketmq_consumer_tps`                    | The number of messages consumed per second by a consumer group |
| `rocketmq_consumer_message_size`           | The size of the message consumed by the consumer group per second (in bytes) |
| `rocketmq_consumer_offset`                 | Progress of consumption message for a consumer group         |
| `rocketmq_group_get_latency`               | Consumer latency on some topic for one queue                 |
| `rocketmq_group_get_latency_by_storetime ` | Consumption delay time of a consumer group                   |
| `rocketmq_message_accumulation`            | How far Consumer offset lag behind                           |

### Consumer

| Name                                     | Exposed information                                |
| ---------------------------------------- | -------------------------------------------------- |
| `rocketmq_client_consume_fail_msg_count` | The number of messages consumed fail in one hour   |
| `rocketmq_client_consume_fail_msg_tps`   | The number of messages consumed fail per second    |
| `rocketmq_client_consume_ok_msg_tps`     | The number of messages consumed success per second |
| `rocketmq_client_consume_rt`             | The average time of consuming every message        |
| `rocketmq_client_consumer_pull_rt `      | The average time of pulling every message          |
| `rocketmq_client_consumer_pull_tps`      | The number of messages pulled by client per second |

## node-exporter

### arp

ARP 统计信息(`/proc/net/arp`)

| 指标名称         | 说明                            |
| ---------------- | ------------------------------- |
| node_arp_entries | 按网络接口设备统计的 arp 条目数 |

### conntrack

| 指标名称                        | 说明                         |
| ------------------------------- | ---------------------------- |
| node_nf_conntrack_entries       | 当前为连接跟踪分配的流项数目 |
| node_nf_conntrack_entries_limit | 连接跟踪表的最大大小         |

### cpu

| 指标名称                         | label                                                        | 说明                                            |
| -------------------------------- | ------------------------------------------------------------ | ----------------------------------------------- |
| node_cpu_seconds_total           | "cpu", "mode"                                                | cpu在每种模式下花费的秒数                       |
| node_cpu_info                    | "package", "core", "cpu", "vendor", "family", "model", "model_name", "microcode", "stepping", "cachesize" | cpu 信息`/proc/cpuinfo`, `--collector.cpu.info` |
| node_cpu_guest_seconds_total     | "cpu", "mode"                                                | 运行的虚机 cpu 时间 统计                        |
| node_cpu_core_throttles_total    | "package", "core"                                            | cpu 核心频率调节的次数                          |
| node_cpu_package_throttles_total | "package"                                                    | cpu package 调节次数                            |

- mode 主要有以下几种

| mode       | 说明                                                    | metric                       |
| ---------- | ------------------------------------------------------- | ---------------------------- |
| user       | 用户态时间花费                                          | node_cpu_seconds_total       |
| nice       | 在低优先级的用户模式中花费的时间                        | node_cpu_seconds_total       |
| system     | 内核态时间花费                                          | node_cpu_seconds_total       |
| iowait     | 等待 I/O 完成花费的时间(这个值并不完全可靠，原因如下: ) | node_cpu_seconds_total       |
| idle       | 在空闲任务中花费的时间                                  | node_cpu_seconds_total       |
| irq        | 中断的时间                                              | node_cpu_seconds_total       |
| softirq    | 软中断时间                                              | node_cpu_seconds_total       |
| steal      | 虚拟机环境下，被宿主机或其他虚机"窃取"的时间(共享环境)  | node_cpu_seconds_total       |
| guest      | 虚拟机消耗的 cpu 时间                                   | node_cpu_guest_seconds_total |
| guest_nice | 在低优先级的 虚拟机 花费的时间                          | node_cpu_guest_seconds_total |

**cpufreq**

| 指标名称                             | label | 说明                                  |
| ------------------------------------ | ----- | ------------------------------------- |
| node_cpu_frequency_hertz             | cpu   | 当前 cpu 频率                         |
| node_cpu_frequency_min_hertz         | cpu   | 最小 cpu 频率                         |
| node_cpu_frequency_max_hertz         | cpu   | 最大 cpu 频率                         |
| node_cpu_scaling_frequency_hertz     | cpu   | 内核视角(内核频率控制器)当前 cpu 频率 |
| node_cpu_scaling_frequency_min_hertz | cpu   | 内核视角(内核频率控制器)最小 cpu 频率 |
| node_cpu_scaling_frequency_max_hertz | cpu   | 内核视角(内核频率控制器)最大 cpu 频率 |

### diskstats

| 指标名称                                    | label  | 说明                                                         |
| ------------------------------------------- | ------ | ------------------------------------------------------------ |
| node_disk_reads_completed_total             | device | 成功完成的读的总次数                                         |
| node_disk_reads_merged_total                | device | 合并读的总次数                                               |
| node_disk_read_bytes_total                  | device | 成功读取的总字节数                                           |
| node_disk_read_time_seconds_total           | device | 所有读操作花费的总时间                                       |
| node_disk_writes_completed_total            | device | 成功完成的写的总次数                                         |
| node_disk_writes_merged_total               | device | 合并写的总次数                                               |
| node_disk_written_bytes_total               | device | 成功写入的总字节数                                           |
| node_disk_write_time_seconds_total          | device | 所有写操作花费的总时间                                       |
| node_disk_io_now                            | device | 当前正在处理的 I/O 操作数(排队数)                            |
| node_disk_io_time_seconds_total             | device | 所有 I/O 操作花费的总时间                                    |
| node_disk_io_time_weighted_seconds_total    | device | I/O 操作花费的**加权**总时间(每一次请求结束后，这个值会增加这个请求的处理时间乘以当前的队列长度) |
| node_disk_discards_completed_total          | device | 成功完成的丢弃操作的总次数                                   |
| node_disk_discards_merged_total             | device | 合并的丢弃操作总次数                                         |
| node_disk_discarded_sectors_total           | device | 成功丢弃的扇区的总数                                         |
| node_disk_discard_time_seconds_total        | device | 所有丢弃操作花费的时间                                       |
| node_disk_flush_requests_total              | device | 刷盘成功完成的总次数                                         |
| node_disk_flush_requests_time_seconds_total | device | 刷盘花费的总时间                                             |

### entropy

| 指标名称                    | label | 说明              |
| --------------------------- | ----- | ----------------- |
| node_entropy_available_bits | 无    | 可用的 熵 bits 位 |

### filefd

| 指标名称              | label | 说明             |
| --------------------- | ----- | ---------------- |
| node_filefd_allocated | 无    | 已分配文件句柄数 |
| node_filefd_maximum   | 无    | 最大文件句柄数   |

### filesystem

| 指标名称                     | label                            | 说明                                     |
| ---------------------------- | -------------------------------- | ---------------------------------------- |
| node_filesystem_size_bytes   | "device", "mountpoint", "fstype" | 文件系统大小(bytes)                      |
| node_filesystem_free_bytes   | "device", "mountpoint", "fstype" | 文件系统空闲(free)空间(bytes)            |
| node_filesystem_avail_bytes  | "device", "mountpoint", "fstype" | 文件系统可用(non-root user)空间(bytes)   |
| node_filesystem_files        | "device", "mountpoint", "fstype" | 文件系统的`file nodes`(inode)总数量      |
| node_filesystem_files_free   | "device", "mountpoint", "fstype" | 文件系统空闲的`file nodes`(inode)总数量  |
| node_filesystem_readonly     | "device", "mountpoint", "fstype" | 文件系统只读状态                         |
| node_filesystem_device_error | "device", "mountpoint", "fstype" | 在获取给定设备的统计信息时是否发生错误。 |

### ipvs

| 指标名称                               | label                                                        | 说明                  |
| -------------------------------------- | ------------------------------------------------------------ | --------------------- |
| node_ipvs_connections_total            | 无                                                           | ipvs 连接总数         |
| node_ipvs_incoming_packets_total       | 无                                                           | 传入数据包的总数      |
| node_ipvs_outgoing_packets_total       | 无                                                           | 传出数据包的总数      |
| node_ipvs_incoming_bytes_total         | 无                                                           | 传入数据的总量(bytes) |
| node_ipvs_outgoing_bytes_total         | 无                                                           | 传出数据的总量(bytes) |
| node_ipvs_backend_connections_active   | `local_address`,`local_port`,`remote_address`,`remote_port`,`proto`,`local_mark` | 当前**活动的**连接    |
| node_ipvs_backend_connections_inactive | `local_address`,`local_port`,`remote_address`,`remote_port`,`proto`,`local_mark` | 当前**不活动的** 连接 |
| node_ipvs_backend_weight               | `local_address`,`local_port`,`remote_address`,`remote_port`,`proto`,`local_mark` | 连接后端权重          |

### loadavg

| 指标名称    | label | 说明       |
| ----------- | ----- | ---------- |
| node_load1  | 无    | 1min 负载  |
| node_load5  | 无    | 5min 负载  |
| node_load15 | 无    | 15min 负载 |

### meminfo

> meminfo metric 收集器，内存信息收集自 `/proc/meminfo`。
>  metric 名称是动态生成的：
>
> 1. 替换括号(Active(anon) -> Active_anon);
> 2. 值带单位(kB, 默认都假定是 kB)，metric 名字以 `_bytes` 结尾

> **AnonPages** vs. **Cached**
>  户进程的内存页分为两种：**file-backed pages**（与文件对应的内存页），和 **anonymous pages**（匿名页）
>
> - **file-backed pages** 包括: 所有的 **page cache**(Mapped,比如shared libraries、可执行程序的文件、mmap的文件等)、 **shared memory(tmpfs)**、**mmap shared anonymous pages** ...
> - **anonymous pages** 包括: **mmap private anonymous pages**、**Transparent HugePages**、
>    **Anonymous Pages** 是与用户进程共存的，一旦进程退出，则Anonymous pages也释放，不像page cache即使文件与进程不关联了还可以缓存

| 指标名称                            | label | 说明                                                         |
| ----------------------------------- | ----- | ------------------------------------------------------------ |
| node_memory_MemTotal_bytes          | 无    | 可用内存总数(比真实物理内存要少，内核预留占用(dmidecode -t memory)) |
| node_memory_MemFree_bytes           | 无    | free 内存(LowFree+HighFree)                                  |
| node_memory_MemAvailable_bytes      | 无    | 可用内存(无需 swapping)的**估算值**                          |
| node_memory_Buffers_bytes           | 无    | 裸磁盘块设备的缓存(此部分不宜过大，一般为 20MB),主要包括: 直接读写块设备、以及文件系统元数据(metadata)比如SuperBlock所使用的缓存页 |
| node_memory_Cached_bytes            | 无    | 从磁盘读取文件的内存缓存(页)缓存。不包括SwapCached           |
| node_memory_SwapCached_bytes        | 无    | 读取文件的内存缓存(页)缓存。曾经被换出的内存会被换回, 但仍然在交换文件中。 |
| node_memory_Active_bytes            | 无    | 活动的内存(最近有使用的内存，如无必要一般不会被回收)         |
| node_memory_Inactive_bytes          | 无    | 不活动的内存(一般可用回收以供其他目的使用)                   |
| node_memory_Active_anon_bytes       | 无    | 活动的匿名内存                                               |
| node_memory_Inactive_anon_bytes     | 无    | 不活动的匿名内存                                             |
| node_memory_Active_file_bytes       | 无    | 活动的文件的内存缓存                                         |
| node_memory_Inactive_file_bytes     | 无    | 不活动的文件的内存缓存                                       |
| node_memory_Unevictable_bytes       | 无    |                                                              |
| node_memory_Mlocked_bytes           | 无    |                                                              |
| node_memory_HighTotal_bytes         | 无    | 用户态 所能使用的以及還剩餘多少的使用空間 https://www.kernel.org/doc/Documentation/vm/highmem.txt |
| node_memory_HighFree_bytes          | 无    |                                                              |
| node_memory_LowTotal_bytes          | 无    | 低内存区域的内存量。这是内核可以直接寻址的内存。所有内核数据结构都需要放入低内存中。 |
| node_memory_LowFree_bytes           | 无    |                                                              |
| node_memory_MmapCopy_bytes          | 无    |                                                              |
| node_memory_SwapTotal_bytes         | 无    | swap 内存总量                                                |
| node_memory_SwapFree_bytes          | 无    | 未使用的交换空间内存                                         |
| node_memory_Dirty_bytes             | 无    | 正在等待写回磁盘的内存                                       |
| node_memory_Writeback_bytes         | 无    | 正在积极写回磁盘的内存                                       |
| node_memory_AnonPages_bytes         | 无    | 映射到用户空间页表的 `Non-file backed` 页                    |
| node_memory_Mapped_bytes            | 无    | 已经被映射到内存中的文件(使用mmap(2))，比如库。              |
| node_memory_Shmem_bytes             | 无    | [tmpfs(5)](https://man7.org/linux/man-pages/man5/tmpfs.5.html)文件系统中消耗的内存量。 |
| node_memory_KReclaimable_bytes      | 无    | 内核在内存压力下试图回收的内核分配内存。包括`SReclaimable`，和其他包含收缩器(shrinker)的**直接分配内存** |
| node_memory_Slab_bytes              | 无    | 内核内数据结构缓存. (参加 [slabinfo](https://man7.org/linux/man-pages/man5/slabinfo.5.html)) |
| node_memory_SReclaimable_bytes      | 无    | Slab的一部分，可被回收，比如 caches 缓存                     |
| node_memory_SUnreclaim_bytes        | 无    | Slab的一部分，不可被回收                                     |
| node_memory_KernelStack_bytes       | 无    | 分配给内核堆栈的内存量                                       |
| node_memory_PageTables_bytes        | 无    | 专用于最低级别页表的内存量                                   |
| node_memory_Quicklists_bytes        | 无    |                                                              |
| node_memory_NFS_Unstable_bytes      | 无    | NFS页面被发送到服务器，但还没有提交到稳定的存储              |
| node_memory_Bounce_bytes            | 无    | 内存用于块设备的 "bounce buffers"                            |
| node_memory_WritebackTmp_bytes      | 无    | 由 FUSE 用于临时回写缓冲区的内存                             |
| node_memory_CommitLimit_bytes       | 无    | 这是当前系统上可分配的内存总量，以千字节表示。只有在启用严格的超额承诺统计(模式2 /proc/sys/vm/overcom‐mit_memory)时，才会遵守这一限制。这个限制是根据/proc/sys/vm/overcommit_memory下面描述的公式计算的。更多细节，请参阅内核源文件[Documentation/vm/overcommit-account.rst](https://www.kernel.org/doc/Documentation/vm/overcommit-accounting) |
| node_memory_Committed_AS_bytes      | 无    | 当前分配给系统的内存量。提交内存是进程分配的所有内存的总和，即使这些内存还没有被进程“使用”。如果一个进程分配了1 GB的内存(使用malloc(3)或类似的内存)，但是只接触了其中的300 MB，那么即使它已经为整个1 GB的地址空间分配了，它也只使用了300 MB的内存。这1 GB的内存已经由VM“提交”，可以由分配应用程序在任何时候使用。在系统上启用严格的过度提交(/proc/sys/vm/overcommit_memory中的模式2)时，将不允许超过CommitLimit的分配。如果需要保证进程在成功分配内存后不会因为内存不足而失败，那么这是非常有用的。 |
| node_memory_VmallocTotal_bytes      | 无    | vmalloc内存区域的总大小                                      |
| node_memory_VmallocUsed_bytes       | 无    | 所使用的vmalloc区域的数量。 从Linux 4.4开始，不再计算此字段，并且将其硬编码为0。请参见/ proc / vmallocinfo。 |
| node_memory_VmallocChunk_bytes      | 无    | 空闲的vmalloc区域的最大连续块。 从Linux 4.4开始，不再计算该字段并将其硬编码为0。请参见/ proc / vmallocinfo。 |
| node_memory_HardwareCorrupted_bytes | 无    | 当系统检测到内存的硬件故障时，会把有问题的页面删除掉，不再使用。HardwareCorrupted统计了删除掉的内存页的总大小 |
| node_memory_LazyFree_bytes          | 无    |                                                              |
| node_memory_AnonHugePages_bytes     | 无    | `Non-file backed huge pages` 映射到 用户空间 页表。          |
| node_memory_ShmemHugePages_bytes    | 无    | 分配给巨页的共享内存(shmem)和[tmpfs(5)](https://man7.org/linux/man-pages/man5/tmpfs.5.html)所使用的内存。 |
| node_memory_ShmemPmdMapped_bytes    | 无    | 巨页的共享内存映射到用户空间                                 |
| node_memory_CmaTotal_bytes          | 无    | CMA（连续内存分配器）页面总数                                |
| node_memory_CmaFree_bytes           | 无    | CMA（连续内存分配器）空闲页面                                |
| node_memory_HugePages_Total         | 无    | 巨页池的大小                                                 |
| node_memory_HugePages_Free          | 无    | 巨页池中尚未分配的 巨页 数量                                 |
| node_memory_HugePages_Rsvd          | 无    | 这是已承诺从池中分配但尚未进行分配的巨页的数量。这些保留的巨页保证了应用程序在发生故障时能够从巨页池中分配巨页。 |
| node_memory_HugePages_Surp          | 无    | 这是池中大于/proc/sys/vm/nr_hugepages中值的巨页数量。巨页的最大剩余数量由/proc/sys/vm/nr_overcommit_hugepages控制。 |
| node_memory_Hugepagesize_bytes      | 无    | 巨页的大小                                                   |
| node_memory_DirectMap4k_bytes       | 无    | 由内核在4kB页面中线性映射的RAM字节数。                       |
| node_memory_DirectMap4M_bytes       | 无    | 由内核在4MB页面中线性映射的RAM字节数。                       |
| node_memory_DirectMap2M_bytes       | 无    | 由内核在2MB页面中线性映射的RAM字节数。                       |
| node_memory_DirectMap1G_bytes       | 无    | 由内核在1GB页面中线性映射的RAM字节数。                       |

### netclass

| 指标名称                                | label                                                  | 说明                                                         |
| --------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| node_network_info                       | device, address, broadcast, duplex, operstate, ifalias | 网络接口信息( /sys/class/net/), 值总是 1                     |
| node_network_address_assign_type        | device                                                 | 指示地址分配类型。可能的值是(  0: permanent address  1: randomly generated  2: stolen from another device  3: set using dev_set_mac_address) |
| node_network_carrier                    | device                                                 | 指示接口的当前物理链接状态。可能的值是(  0: 接口状态 down  1: 接口状态 up) |
| node_network_carrier_changes_total      | device                                                 | 32位无符号整数，计算链接状态从 `down -> up` 和 `up -> down` 变化的次数 |
| node_network_carrier_up_changes_total   | device                                                 | 32位无符号整数，`up` 状态的次数                              |
| node_network_carrier_down_changes_total | device                                                 | 32位无符号整数，`down` 状态的次数                            |
| node_network_device_id                  | device                                                 | 指示设备唯一标识符。格式是十六进制值。 这用于消除可能堆叠的接口（例如VLAN接口）的歧义，但仍具有与其父设备相同的MAC地址。 |
| node_network_dormant                    | device                                                 | 指示接口是否处于休眠状态。可能的值是(  0: 接口不是休眠状态  1: 接口是休眠状态 )  除非执行了基于请求的认证(例如:802.1x)，否则请求软件可以使用此属性来表示设备不可用。'link_mode'属性也将反映休眠状态。 |
| node_network_flags                      | device                                                 | 指示接口标志为十六进制的位掩码。 有关所有可能值和标志语义的列表，请参见 `include/uapi/linux/if.h` |
| node_network_iface_id                   | device                                                 | `/sys/class/net/<iface>/ifindex` 用十进制数表示系统范围的接口唯一索引标识符。 此属性用于将接口标识符映射到接口名称。它在整个网络堆栈中用于指定特定于接口的请求/事件。 |
| node_network_iface_link                 | device                                                 | 指示接口链接到的系统范围的接口唯一索引标识符。 格式为十进制。 此属性用于解析接口链接，链接和堆栈。 物理接口具有相同的 “ifindex” 和 “iflink” 值。 |
| node_network_iface_link_mode            | device                                                 | 指示接口链接模式，以十进制数表示。 此属性应与 “dormant” 属性一起使用，以确定接口的可用性。 可能的值是(  0: 默认链接模式  1: 休眠链接模式 ) |
| node_network_mtu_bytes                  | device                                                 | 表示接口当前配置的MTU值，以字节和十进制格式表示。具体值取决于所使用的低级接口协议。 除非更改，否则以太网设备的“mtu”属性值将为1500。 |
| node_network_name_assign_type           | device                                                 | 指示名称分配类型。可能的值是(  1: 由内核枚举，可能以不可预测的方式  2: 可预测地由内核命名  3: 由用户空间命名  4: 重命名) |
| node_network_net_dev_group              | device                                                 | 表示接口网络设备组的十进制整数。 默认值为0，它对应于初始网络设备组。 可以更改组以影响路由决策（请参阅：`net/ipv4/fib_rules` 和 `net/ipv6/fib6_rules.c`）。 |
| node_network_speed_bytes                | device                                                 | 指示接口的最新或当前速度值。值是一个整数，表示以 Mbps 为单位的链接速度。此属性仅对实现 `ethtool get_link_ksettings` 方法的接口（主要是以太网）有效 |
| node_network_transmit_queue_length      | device                                                 | 表示接口发送队列len的数据包数量（整数值）。值取决于接口的类型，除非另有配置，否则以太网适配器的默认值为 `1000` |
| node_network_protocol_type              | device                                                 | 表示接口协议类型的十进制值。 有关所有可能的值，请参见 `include/uapi/linux/if_arp.h` |

### netdev

| 指标名称                               | label  | 说明                               |
| -------------------------------------- | ------ | ---------------------------------- |
| node_network_receive_bytes_total       | device | 接口接收的字节数                   |
| node_network_receive_packets_total     | device | 接口接收的包数量                   |
| node_network_receive_errs_total        | device | 接口设备驱动检测到的接收错误       |
| node_network_receive_drop_total        | device | 接口设备驱动丢弃的接收包数量       |
| node_network_receive_fifo_total        | device | 接口接收的 FIFO 缓冲区错误的数量   |
| node_network_receive_frame_total       | device | 接口接收的数据包帧错误的数量。     |
| node_network_receive_compressed_total  | device | 由设备驱动程序接收的压缩包的数目。 |
| node_network_receive_multicast_total   | device | 由设备驱动程序接收的多播帧的数目。 |
| node_network_transmit_bytes_total      | device | 接口发送的字节数                   |
| node_network_transmit_packets_total    | device | 接口发送的包数量                   |
| node_network_transmit_errs_total       | device | 接口设备驱动检测到的发送错误       |
| node_network_transmit_drop_total       | device | 接口设备驱动丢弃的发送包数量       |
| node_network_transmit_fifo_total       | device | 接口发送的 FIFO 缓冲区错误的数量   |
| node_network_transmit_frame_total      | device | 接口发送的数据包帧错误的数量。     |
| node_network_transmit_compressed_total | device | 由设备驱动程序发送的压缩包的数目。 |
| node_network_transmit_multicast_total  | device | 由设备驱动程序发送的多播帧的数目。 |

### schedstat

| 指标名称                             | label | 说明                          |
| ------------------------------------ | ----- | ----------------------------- |
| node_schedstat_running_seconds_total | cpu   | CPU 花费在运行进程上的秒数    |
| node_schedstat_waiting_seconds_total | cpu   | 等待该 CPU 的处理所花费的秒数 |
| node_schedstat_timeslices_total      | cpu   | CPU 执行的时间片数量          |

### sockstat

| 指标名称                   | label | 说明                    |
| -------------------------- | ----- | ----------------------- |
| node_sockstat_sockets_used | 无    | 正在使用的 ipv4 sockets |

**node_sockstat_<protocol>_<name>**

protocol 取值:

- TCP
- UDP
- UDPLITE
- RAW
- FRAG
- TCP6
- UDP6
- UDPLITE6
- RAW6
- FRAG6

name 取值：

- inuse   正在使用（正在侦听）的套接字数量
- orphan  无主（孤儿，不属于任何进程）的TCP连接数（无用、待销毁的TCP socket数）
- tw      等待关闭的TCP连接数。(TIME_WAIT )
- alloc   已分配（已建立、已申请到sk_buff）的TCP套接字数量
- mem     套接字缓冲区使用量(单位是 内存页)
- memory  (单位是 bytes)

### softnet

CPU 处理的网络包统计

| 指标名称                          | label | 说明                           |
| --------------------------------- | ----- | ------------------------------ |
| node_softnet_processed_total      | cpu   | 已经处理的 包数量              |
| node_softnet_dropped_total        | cpu   | 已丢弃的包数量                 |
| node_softnet_times_squeezed_total | cpu   | 处理数据包超出配额的次数(溢出) |

### stat

| 指标名称                    | label | 说明                         |
| --------------------------- | ----- | ---------------------------- |
| node_intr_total             | cpu   | 服务的中断次数统计           |
| node_context_switches_total | cpu   | 上下文切换次数统计           |
| node_forks_total            | cpu   | 进程 fork 数量统计           |
| node_boot_time_seconds      | cpu   | 系统启动时间， unixtimestamp |
| node_procs_running          | cpu   | 处于可运行状态的进程数       |
| node_procs_blocked          | cpu   | 等待I/O完成的已阻止进程数    |

### timex

| 指标名称                                | label | 说明                                                         |
| --------------------------------------- | ----- | ------------------------------------------------------------ |
| node_timex_offset_seconds               | 无    | Time offset in between local system and reference clock.     |
| node_timex_frequency_adjustment_ratio   | 无    | Local clock frequency adjustment.                            |
| node_timex_maxerror_seconds             | 无    | Maximum error in seconds.                                    |
| node_timex_estimated_error_seconds      | 无    | Estimated error in seconds.                                  |
| node_timex_status                       | 无    | Value of the status array bits.                              |
| node_timex_loop_time_constant           | 无    | Phase-locked loop time constant.                             |
| node_timex_tick_seconds                 | 无    | Seconds between clock ticks.                                 |
| node_timex_pps_frequency_hertz          | 无    | Pulse per second frequency.                                  |
| node_timex_pps_jitter_seconds           | 无    | Pulse per second jitter.                                     |
| node_timex_pps_shift_seconds            | 无    | Pulse per second interval duration.                          |
| node_timex_pps_stability_hertz          | 无    | Pulse per second stability, average of recent frequency changes. |
| node_timex_pps_jitter_total             | 无    | Pulse per second count of jitter limit exceeded events.      |
| node_timex_pps_calibration_total        | 无    | Pulse per second count of calibration intervals.             |
| node_timex_pps_error_total              | 无    | Pulse per second count of calibration errors.                |
| node_timex_pps_stability_exceeded_total | 无    | Pulse per second count of stability limit exceeded events.   |
| node_timex_tai_offset_seconds           | 无    | International Atomic Time (TAI) offset.                      |
| node_timex_sync_status                  | 无    | Is clock synchronized to a reliable server (1 = yes, 0 = no). |

### udp_queues

| 指标名称        | label     | 说明                                                         |
| --------------- | --------- | ------------------------------------------------------------ |
| node_udp_queues | queue, ip | Number of allocated memory in the kernel for UDP datagrams in bytes. |

**queue** 取值: tx, rx

**ip** 取值: v4, v6

### uname

| 指标名称        | label                                               | 说明                          |
| --------------- | --------------------------------------------------- | ----------------------------- |
| node_uname_info | sysname,release,version,machine,nodename,domainname | uname 系统调用提供的 系统信息 |

### xfs

| 指标名称                                             | label  | 说明                                                         |
| ---------------------------------------------------- | ------ | ------------------------------------------------------------ |
| node_xfs_extent_allocation_extents_allocated_total   | device | Number of extents allocated for a filesystem.                |
| node_xfs_extent_allocation_blocks_allocated_total    | device | Number of blocks allocated for a filesystem.                 |
| node_xfs_extent_allocation_extents_freed_total       | device | Number of extents freed for a filesystem.                    |
| node_xfs_extent_allocation_blocks_freed_total        | device | Number of blocks freed for a filesystem.                     |
| node_xfs_allocation_btree_lookups_total              | device | Number of allocation B-tree lookups for a filesystem.        |
| node_xfs_allocation_btree_compares_total             | device | Number of allocation B-tree compares for a filesystem.       |
| node_xfs_allocation_btree_records_inserted_total     | device | Number of allocation B-tree records inserted for a filesystem. |
| node_xfs_allocation_btree_records_deleted_total      | device | Number of allocation B-tree records deleted for a filesystem. |
| node_xfs_block_mapping_reads_total                   | device | Number of block map for read operations for a filesystem.    |
| node_xfs_block_mapping_writes_total                  | device | Number of block map for write operations for a filesystem.   |
| node_xfs_block_mapping_unmaps_total                  | device | Number of block unmaps (deletes) for a filesystem.           |
| node_xfs_ block_mapping_extent_list_insertions_total | device | Number of extent list insertions for a filesystem.           |
| node_xfs_block_mapping_extent_list_deletions_total   | device | Number of extent list deletions for a filesystem.            |
| node_xfs_block_mapping_extent_list_lookups_total     | device | Number of extent list lookups for a filesystem.              |
| node_xfs_block_mapping_extent_list_compares_total    | device | Number of extent list compares for a filesystem.             |
| node_xfs_block_map_btree_lookups_total               | device | Number of block map B-tree lookups for a filesystem.         |
| node_xfs_block_map_btree_compares_total              | device | Number of block map B-tree compares for a filesystem.        |
| node_xfs_block_map_btree_records_inserted_total      | device | Number of block map B-tree records inserted for a filesystem. |
| node_xfs_block_map_btree_records_deleted_total       | device | Number of block map B-tree records deleted for a filesystem. |
| node_xfs_directory_operation_lookup_total            | device | Number of file name directory lookups which miss the operating systems directory name lookup cache. |
| node_xfs_directory_operation_create_total            | device | Number of times a new directory entry was created for a filesystem. |
| node_xfs_directory_operation_remove_total            | device | Number of times an existing directory entry was created for a filesystem. |
| node_xfs_directory_operation_getdents_total          | device | Number of times the directory getdents operation was performed for a filesystem. |
| node_xfs_read_calls_total                            | device | Number of read(2) system calls made to files in a filesystem. |
| node_xfs_write_calls_total                           | device | Number of write(2) system calls made to files in a filesystem. |
| node_xfs_vnode_active_total                          | device | Number of vnodes not on free lists for a filesystem.         |
| node_xfs_vnode_allocate_total                        | device | Number of times vn_alloc called for a filesystem.            |
| node_xfs_vnode_get_total                             | device | Number of times vn_get called for a filesystem.              |
| node_xfs_vnode_hold_total                            | device | Number of times vn_hold called for a filesystem.             |
| node_xfs_vnode_release_total                         | device | Number of times vn_rele called for a filesystem.             |
| node_xfs_vnode_reclaim_total                         | device | Number of times vn_reclaim called for a filesystem.          |
| node_xfs_vnode_remove_total                          | device | Number of times vn_remove called for a filesystem.           |

### time

| 指标名称          | label | 说明                                       |
| ----------------- | ----- | ------------------------------------------ |
| node_time_seconds | 无    | System time in seconds since epoch (1970). |

### mdadm
- state 取值:
  - active
  - inactive
  - recovering
  - resync
| 指标名称               | label         | 说明                                           |
| ---------------------- | ------------- | ---------------------------------------------- |
| node_md_state          | state, device | Indicates the state of md-device.              |
| node_md_disks          | device, state | Number of active/failed/spare disks of device. |
| node_md_disks_required | device        | Total number of disks of device.               |
| node_md_blocks         | device        | Total number of blocks on device.              |
| node_md_blocks_synced  | device        | Number of blocks synced on device.             |

## coredns

### cache

| 指标名称                   | 说明                                    |
| -------------------------- | --------------------------------------- |
| coredns_cache_hits_total   | dns缓存命中总量，`type=(denial,succes)` |
| coredns_cache_misses_total | dns缓存未命中总量                       |
| coredns_cache_size         | dns缓存大小                             |

### request

| 指标名称                             | 说明                                                      |
| ------------------------------------ | --------------------------------------------------------- |
| coredns_dns_request_count_total      | 总请求数量                                                |
| coredns_dns_request_duration_seconds | 请求时延histogram类型指标                                 |
| coredns_dns_request_size_bytes       | 请求包大小histogram类型指标                               |
| coredns_dns_request_type_count_total | 不同类型指标请求总量，`type=(A,AAAA,CNAME,PTR,SRV,other)` |

### response

| 指标名称                               | 说明                                                         |
| -------------------------------------- | ------------------------------------------------------------ |
| coredns_dns_response_rcode_count_total | 响应码总量，`rcode=(NOERROR,NXDOMAIN,SERVFAIL)`，其中如果新增`SERVFAIL`表示出现解析异常 |
| coredns_dns_response_size_bytes        | 响应包大小histogram类型指标                                  |

### forward

| 指标名称                                   | 说明                                                         |
| ------------------------------------------ | ------------------------------------------------------------ |
| coredns_forward_request_count_total        | 请求转发延迟histogram指标，`to=<dst_dns>`                    |
| coredns_forward_response_rcode_count_total | 请求转发响应码总量，`rcode=(NOERROR,NXDOMAIN,SERVFAIL)`，其中如果新增`SERVFAIL`表示出现解析异常 |
| coredns_forward_request_duration_seconds   | 请求转发时延histogram类型指标                                |
| coredns_forward_sockets_open               | 转发打开的套接字数量                                         |

### health

| 指标名称                                | 说明                |
| --------------------------------------- | ------------------- |
| coredns_health_request_duration_seconds | /health接口请求延迟 |
| coredns_panic_count_total               | 异常中断次数        |

### health

| 指标名称               | 说明               |
| ---------------------- | ------------------ |
| coredns_plugin_enabled | 插件状态，enable=1 |

### 告警规则配置

| 规则                                                         | 含义         |
| ------------------------------------------------------------ | ------------ |
| rate(coredns_panic_count_total[1m]) > 0                      | 程序异常中断 |
| rate(coredns_forward_response_rcode_count_total{rcode="SERVFAIL"}[1m]) > 0 | 转发解析异常 |
| rate(coredns_dns_response_rcode_count_total{rcode="SERVFAIL"}[1m]) > 0 | 解析异常     |

## kube-state-metrics

### certificatesigningrequests

| Metric name                                | Metric type | Labels/tags                              | Status | 说明 |
| ------------------------------------------ | ----------- | ---------------------------------------- | ------ | ---- |
| kube_certificatesigningrequest_created     | Gauge       | `certificatesigningrequest`              | STABLE |      |
| kube_certificatesigningrequest_condition   | Gauge       | `certificatesigningrequest`, `condition` | STABLE |      |
| kube_certificatesigningrequest_labels      | Gauge       | `certificatesigningrequest`              | STABLE |      |
| kube_certificatesigningrequest_cert_length | Gauge       | `certificatesigningrequest`              | STABLE |      |

- condition 取值: `approved|denied`

### configmaps

| Metric name                              | Metric type | Labels/tags              | Status       | 说明 |
| ---------------------------------------- | ----------- | ------------------------ | ------------ | ---- |
| kube_configmap_info                      | Gauge       | `configmap`, `namespace` | STABLE       |      |
| kube_configmap_created                   | Gauge       | `configmap`, `namespace` | STABLE       |      |
| kube_configmap_metadata_resource_version | Gauge       | `configmap`, `namespace` | EXPERIMENTAL |      |

### cronjobs

| Metric name                                 | Metric type | Labels/tags                                           | Status | 说明                                                     |
| ------------------------------------------- | ----------- | ----------------------------------------------------- | ------ | -------------------------------------------------------- |
| kube_cronjob_info                           | Gauge       | `cronjob`,`namespace`,`schedule`,`concurrency_policy` | STABLE |                                                          |
| kube_cronjob_labels                         | Gauge       | `cronjob`,`namespace`,`label_CRONJOB_LABEL`           | STABLE |                                                          |
| kube_cronjob_created                        | Gauge       | `cronjob`,`namespace`,                                | STABLE | cronjob 创建时间                                         |
| kube_cronjob_next_schedule_time             | Gauge       | `cronjob`,`namespace`,                                | STABLE | 下次调度时间                                             |
| kube_cronjob_status_active                  | Gauge       | `cronjob`,`namespace`,                                | STABLE | 当前正在执行                                             |
| kube_cronjob_status_last_schedule_time      | Gauge       | `cronjob`,`namespace`,                                | STABLE | 上次调度时间                                             |
| kube_cronjob_spec_suspend                   | Gauge       | `cronjob`,`namespace`,                                | STABLE | 暂停任务标志                                             |
| kube_cronjob_spec_starting_deadline_seconds | Gauge       | `cronjob`,`namespace`,                                | STABLE | 无论出于什么原因错过调度时间后，最多还能延迟执行的时间点 |

> - schedule: 调度表, 规则类似 linux crontab
> - concurrency_policy: job 并发策略

### daemonsets

| Metric name                                    | Metric type | Labels/tags                                      | Status | 说明 |
| ---------------------------------------------- | ----------- | ------------------------------------------------ | ------ | ---- |
| kube_daemonset_created                         | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_status_current_number_scheduled | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_status_desired_number_scheduled | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_status_number_available         | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_status_number_misscheduled      | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_status_number_ready             | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_status_number_unavailable       | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_updated_number_scheduled        | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_metadata_generation             | Gauge       | `daemonset`, `namespace`,                        | STABLE |      |
| kube_daemonset_labels                          | Gauge       | `daemonset`, `namespace`,`label_DAEMONSET_LABEL` | STABLE |      |

### deployments

| Metric name                                                 | Metric type | Labels/tags                                     | Status | 说明                                                     |
| ----------------------------------------------------------- | ----------- | ----------------------------------------------- | ------ | -------------------------------------------------------- |
| kube_deployment_status_replicas                             | Gauge       | `deployment`, `namespace`,                      | STABLE | 当前副本数                                               |
| kube_deployment_status_replicas_available                   | Gauge       | `deployment`, `namespace`,                      | STABLE | 可用副本数                                               |
| kube_deployment_status_replicas_unavailable                 | Gauge       | `deployment`, `namespace`,                      | STABLE | 不可用副本数                                             |
| kube_deployment_status_replicas_updated                     | Gauge       | `deployment`, `namespace`,                      | STABLE | 已经更新的副本数                                         |
| kube_deployment_status_observed_generation                  | Gauge       | `deployment`, `namespace`,                      | STABLE | 变更次数                                                 |
| kube_deployment_status_condition                            | Gauge       | `deployment`, `namespace`, `condition`,`status` | STABLE | 各种情况的状态                                           |
| kube_deployment_spec_replicas                               | Gauge       | `deployment`, `namespace`,                      | STABLE | 期望副本数                                               |
| kube_deployment_spec_paused                                 | Gauge       | `deployment`, `namespace`,                      | STABLE | 暂停更新的副本数，`kubectl rollout pause deployment XXX` |
| kube_deployment_spec_strategy_rollingupdate_max_unavailable | Gauge       | `deployment`, `namespace`,                      | STABLE | 滚动更新过程中，最大不可用副本数                         |
| kube_deployment_spec_strategy_rollingupdate_max_surge       | Gauge       | `deployment`, `namespace`,                      | STABLE | 滚动更新过程中，所有副本数最多可超期望副本数             |
| kube_deployment_metadata_generation                         | Gauge       | `deployment`, `namespace`,                      | STABLE | 表示期望状态(spec)的特定生成的序列号。                   |
| kube_deployment_labels                                      | Gauge       | `deployment`, `namespace`,                      | STABLE | 标签                                                     |
| kube_deployment_created                                     | Gauge       | `deployment`, `namespace`,                      | STABLE | 创建时间                                                 |

- condition:
- status: `true|false|unknown`

### endpoints

| Metric name                     | Metric type | Labels/tags                                     | Status | 说明 |
| ------------------------------- | ----------- | ----------------------------------------------- | ------ | ---- |
| kube_endpoint_address_not_ready | Gauge       | `endpoint`, `namespace`,                        | STABLE |      |
| kube_endpoint_address_available | Gauge       | `endpoint`, `namespace`,                        | STABLE |      |
| kube_endpoint_info              | Gauge       | `endpoint`, `namespace`,                        | STABLE |      |
| kube_endpoint_labels            | Gauge       | `endpoint`, `namespace`, `label_ENDPOINT_LABEL` | STABLE |      |
| kube_endpoint_created           | Gauge       | `endpoint`, `namespace`,                        | STABLE |      |

### horizontalpodautoscalers

| Metric name                      | Metric type | Labels/tags                                            | Status       | 说明 |
| -------------------------------- | ----------- | ------------------------------------------------------ | ------------ | ---- |
| kube_hpa_labels                  | Gauge       | `hpa`, `namespace`                                     | STABLE       |      |
| kube_hpa_metadata_generation     | Gauge       | `hpa`, `namespace`                                     | STABLE       |      |
| kube_hpa_spec_max_replicas       | Gauge       | `hpa`, `namespace`                                     | STABLE       |      |
| kube_hpa_spec_min_replicas       | Gauge       | `hpa`, `namespace`                                     | STABLE       |      |
| kube_hpa_spec_target_metric      | Gauge       | `hpa`, `namespace`,`metric_name`, `metric_target_type` | EXPERIMENTAL |      |
| kube_hpa_status_condition        | Gauge       | `hpa`, `namespace`,`condition`, `status`               | STABLE       |      |
| kube_hpa_status_current_replicas | Gauge       | `hpa`, `namespace`                                     | STABLE       |      |
| kube_hpa_status_desired_replicas | Gauge       | `hpa`, `namespace`                                     | STABLE       |      |

> - metric_target_type: `value|utilization|average`
> - status: `true|false|unknown`

### ingresses

| Metric name                            | Metric type | Labels/tags                                                  | Status       | 说明 |
| -------------------------------------- | ----------- | ------------------------------------------------------------ | ------------ | ---- |
| kube_ingress_info                      | Gauge       | `ingress`, `namespace`,                                      | STABLE       |      |
| kube_ingress_labels                    | Gauge       | `ingress`, `namespace`, `label_INGRESS_LABEL`                | STABLE       |      |
| kube_ingress_created                   | Gauge       | `ingress`, `namespace`,                                      | STABLE       |      |
| kube_ingress_metadata_resource_version | Gauge       | `ingress`, `namespace`,                                      | EXPERIMENTAL |      |
| kube_ingress_path                      | Gauge       | `ingress`, `namespace`, `host`, `path`, `service_name`,`service_port` | STABLE       |      |
| kube_ingress_tls                       | Gauge       | `ingress`, `namespace`, `tls_host`, `secret`                 | STABLE       |      |

> secret: tls secret name

### jobs

| Metric name                           | Metric type | Labels/tags                                                  | Status | 说明 |
| ------------------------------------- | ----------- | ------------------------------------------------------------ | ------ | ---- |
| kube_job_info                         | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_labels                       | Gauge       | `job_name`, `namespace`, `label_JOB_LABEL`                   | STABLE |      |
| kube_job_owner                        | Gauge       | `job_name`, `namespace`, `owner_kind`, `owner_name`, `owner_is_controller` | STABLE |      |
| kube_job_spec_parallelism             | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_spec_completions             | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_spec_active_deadline_seconds | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_status_active                | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_status_succeeded             | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_status_failed                | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_status_start_time            | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_status_completion_time       | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_complete                     | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_failed                       | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |
| kube_job_created                      | Gauge       | `job_name`, `namespace`,                                     | STABLE |      |

### limitranges

| Metric name             | Metric type | Labels/tags                                                 | Status | 说明 |
| ----------------------- | ----------- | ----------------------------------------------------------- | ------ | ---- |
| kube_limitrange         | Gauge       | `limitrange`, `namespace`, `resource`, `type`, `constraint` | STABLE |      |
| kube_limitrange_created | Gauge       | `limitrange`, `namespace`,                                  | STABLE |      |

- type: `Pod | Container | PersistentVolumeClaim`

### mutatingwebhookconfigurations

| Metric name                                                 | Metric type | Labels/tags                                 | Status       | 说明 |
| ----------------------------------------------------------- | ----------- | ------------------------------------------- | ------------ | ---- |
| kube_mutatingwebhookconfiguration_info                      | Gauge       | `mutatingwebhookconfiguration`, `namespace` | EXPERIMENTAL |      |
| kube_mutatingwebhookconfiguration_created                   | Gauge       | `mutatingwebhookconfiguration`, `namespace` | EXPERIMENTAL |      |
| kube_mutatingwebhookconfiguration_metadata_resource_version | Gauge       | `mutatingwebhookconfiguration`, `namespace` | EXPERIMENTAL |      |

### namespaces

| Metric name                     | Metric type | Labels/tags                        | Status       | 说明 |
| ------------------------------- | ----------- | ---------------------------------- | ------------ | ---- |
| kube_namespace_created          | Gauge       | `namespace`                        | STABLE       |      |
| kube_namespace_labels           | Gauge       | `namespace` ,`label_NS_LABEL`      | STABLE       |      |
| kube_namespace_status_condition | Gauge       | `namespace` ,`condition` ,`status` | EXPERIMENTAL |      |
| kube_namespace_status_phase     | Gauge       | `namespace` ,`status`              | STABLE       |      |

- condition: `NamespaceDeletionDiscoveryFailure | NamespaceDeletionContentFailure | NamespaceDeletionGroupVersionParsingFailure`
- kube_namespace_status_condition -- status: `true | false | unknown`
- kube_namespace_status_phase     -- status: `Active | Terminating`

### networkpolicies

| Metric name                           | Metric type | Labels/tags                  | Status       | 说明 |
| ------------------------------------- | ----------- | ---------------------------- | ------------ | ---- |
| kube_networkpolicy_created            | Gauge       | `namespace`, `networkpolicy` | EXPERIMENTAL |      |
| kube_networkpolicy_labels             | Gauge       | `namespace`, `networkpolicy` | EXPERIMENTAL |      |
| kube_networkpolicy_spec_egress_rules  | Gauge       | `namespace`, `networkpolicy` | EXPERIMENTAL |      |
| kube_networkpolicy_spec_ingress_rules | Gauge       | `namespace`, `networkpolicy` | EXPERIMENTAL |      |

### nodes

| Metric name                               | Metric type | Labels/tags                                                  | Status       | 说明 |
| ----------------------------------------- | ----------- | ------------------------------------------------------------ | ------------ | ---- |
| kube_node_info                            | Gauge       | `node`, `kernel_version`,  `os_image`,  `container_runtime_version`,  `kubelet_version`,  `kubeproxy_version`,  `pod_cidr`,  `provider_id` | STABLE       |      |
| kube_node_labels                          | Gauge       | `node`, `label_NODE_LABEL`                                   | STABLE       |      |
| kube_node_role                            | Gauge       | `node`, `role`                                               | EXPERIMENTAL |      |
| kube_node_spec_unschedulable              | Gauge       | `node`                                                       |              |      |
| kube_node_spec_taint                      | Gauge       | `node`, `key`,  `value`,  `effect`                           | STABLE       |      |
| kube_node_status_phase                    | Gauge       | `node`, `phase`                                              | DEPRECATED   |      |
| kube_node_status_capacity                 | Gauge       | `node`, `resource`,  `unit`                                  | STABLE       |      |
| kube_node_status_capacity_cpu_cores       | Gauge       | `node`                                                       | DEPRECATED   |      |
| kube_node_status_capacity_memory_bytes    | Gauge       | `node`                                                       | DEPRECATED   |      |
| kube_node_status_capacity_pods            | Gauge       | `node`                                                       | DEPRECATED   |      |
| kube_node_status_allocatable              | Gauge       | `node`, `resource`,  `unit`                                  | STABLE       |      |
| kube_node_status_allocatable_cpu_cores    | Gauge       | `node`                                                       | DEPRECATED   |      |
| kube_node_status_allocatable_memory_bytes | Gauge       | `node`                                                       | DEPRECATED   |      |
| kube_node_status_allocatable_pods         | Gauge       | `node`                                                       | DEPRECATED   |      |
| kube_node_status_condition                | Gauge       | `node`, `condition`,  `status`                               | STABLE       |      |
| kube_node_created                         | Gauge       | `node`                                                       | STABLE       |      |

> - phase: `Pending | Running | Terminated`
> - status: `true | false | unkown`

### persistentvolumeclaims

| Metric name                                                | Metric type | Labels/tags                                                  | Status       | 说明 |
| ---------------------------------------------------------- | ----------- | ------------------------------------------------------------ | ------------ | ---- |
| kube_persistentvolumeclaim_access_mode                     | Gauge       | `access_mode`, `namespace`, `persistentvolumeclaim`          | STABLE       |      |
| kube_persistentvolumeclaim_info                            | Gauge       | `namespace`, `persistentvolumeclaim`, `storageclass`, `volumename` | STABLE       |      |
| kube_persistentvolumeclaim_labels                          | Gauge       | `persistentvolumeclaim`, `namespace`, `label_PERSISTENTVOLUMECLAIM_LABEL` | STABLE       |      |
| kube_persistentvolumeclaim_resource_requests_storage_bytes | Gauge       | `namespace`, `persistentvolumeclaim`                         | STABLE       |      |
| kube_persistentvolumeclaim_status_condition                | Gauge       | `namespace` , `persistentvolumeclaim`, `type`, `status`      | EXPERIMENTAL |      |
| kube_persistentvolumeclaim_status_phase                    | Gauge       | `namespace`, `persistentvolumeclaim`, `phase`                | STABLE       |      |

> - status: `true | false | unknown`
> - phase:  `Pending | Bound | Lost`

Note:

- A special `<none>` string will be used if PVC has no storage class.

### persistentvolumes

| Metric name                          | Metric type | Labels/tags                                        | Status | 说明 |
| ------------------------------------ | ----------- | -------------------------------------------------- | ------ | ---- |
| kube_persistentvolume_capacity_bytes | Gauge       | `persistentvolume`                                 | STABLE |      |
| kube_persistentvolume_status_phase   | Gauge       | `persistentvolume`, `phase`                        | STABLE |      |
| kube_persistentvolume_labels         | Gauge       | `persistentvolume`, `label_PERSISTENTVOLUME_LABEL` | STABLE |      |
| kube_persistentvolume_info           | Gauge       | `persistentvolume`, `storageclass`                 | STABLE |      |

> - phase: `Bound | Failed | Pending | Available | Released`

### poddisruptionbudgets

| Metric name                                             | Metric type | Labels/tags                        | Status | 说明 |
| ------------------------------------------------------- | ----------- | ---------------------------------- | ------ | ---- |
| kube_poddisruptionbudget_created                        | Gauge       | `poddisruptionbudget`, `namespace` | STABLE |      |
| kube_poddisruptionbudget_status_current_healthy         | Gauge       | `poddisruptionbudget`, `namespace` | STABLE |      |
| kube_poddisruptionbudget_status_desired_healthy         | Gauge       | `poddisruptionbudget`, `namespace` | STABLE |      |
| kube_poddisruptionbudget_status_pod_disruptions_allowed | Gauge       | `poddisruptionbudget`, `namespace` | STABLE |      |
| kube_poddisruptionbudget_status_expected_pods           | Gauge       | `poddisruptionbudget`, `namespace` | STABLE |      |
| kube_poddisruptionbudget_status_observed_generation     | Gauge       | `poddisruptionbudget`, `namespace` | STABLE |      |

### pods

| Metric name                                           | Metric type | Labels/tags                                                  | Status     | 说明 |
| ----------------------------------------------------- | ----------- | ------------------------------------------------------------ | ---------- | ---- |
| kube_pod_info                                         | Gauge       | `pod`, `namespace`, `host_ip`,`pod_ip`,`node`,`created_by_kind`,`created_by_name`,`uid`,`priority_class` | STABLE     |      |
| kube_pod_start_time                                   | Gauge       | `pod`, `namespace`                                           |            |      |
| kube_pod_completion_time                              | Gauge       | `pod`, `namespace`                                           | STABLE     |      |
| kube_pod_owner                                        | Gauge       | `pod`, `namespace`, `owner_kind`,`owner_name`, `owner_is_controller` | STABLE     |      |
| kube_pod_labels                                       | Gauge       | `pod`, `namespace`, `label_POD_LABEL`                        | STABLE     |      |
| kube_pod_status_phase                                 | Gauge       | `pod`, `namespace`, `phase`                                  | STABLE     |      |
| kube_pod_status_ready                                 | Gauge       | `pod`, `namespace`, `condition`                              | STABLE     |      |
| kube_pod_status_scheduled                             | Gauge       | `pod`, `namespace`, `condition`                              | STABLE     |      |
| kube_pod_container_info                               | Gauge       | `container`, `pod`, `namespace`, `image`, `image_id`,`container_id` | STABLE     |      |
| kube_pod_container_status_waiting                     | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_container_status_waiting_reason              | Gauge       | `container`, `pod`, `namespace`, `reason`                    | STABLE     |      |
| kube_pod_container_status_running                     | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_container_status_terminated                  | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_container_status_terminated_reason           | Gauge       | `container`, `pod`, `namespace`, `reason`                    | STABLE     |      |
| kube_pod_container_status_last_terminated_reason      | Gauge       | `container`, `pod`, `namespace`, `reason`                    | STABLE     |      |
| kube_pod_container_status_ready                       | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_container_status_restarts_total              | Counter     | `container`, `namespace`, `pod`                              | STABLE     |      |
| kube_pod_container_resource_requests_cpu_cores        | Gauge       | `container`, `pod`, `namespace`, `node`                      | DEPRECATED |      |
| kube_pod_container_resource_requests                  | Gauge       | `resource`, `unit`, `container`, `pod`, `namespace`, `node`  | STABLE     |      |
| kube_pod_container_resource_requests_memory_bytes     | Gauge       | `container`, `pod`, `namespace`, `node`                      | DEPRECATED |      |
| kube_pod_container_resource_limits_cpu_cores          | Gauge       | `container`, `pod`, `namespace`, `node`                      | DEPRECATED |      |
| kube_pod_container_resource_limits                    | Gauge       | `resource`, `unit`, `container`, `pod`, `namespace`, `node`  | STABLE     |      |
| kube_pod_container_resource_limits_memory_bytes       | Gauge       | `container`, `pod`, `namespace`, `node`                      | DEPRECATED |      |
| kube_pod_created                                      | Gauge       | `pod`, `namespace`                                           |            |      |
| kube_pod_restart_policy                               | Gauge       | `pod`, `namespace`, `type`                                   | STABLE     |      |
| kube_pod_init_container_info                          | Gauge       | `container`, `pod`, `namespace`, `image`, `image_id`, `container_id` | STABLE     |      |
| kube_pod_init_container_status_waiting                | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_init_container_status_waiting_reason         | Gauge       | `container`, `pod`, `namespace`, `reason`                    | STABLE     |      |
| kube_pod_init_container_status_running                | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_init_container_status_terminated             | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_init_container_status_terminated_reason      | Gauge       | `container`, `pod`, `namespace`, `reason`                    | STABLE     |      |
| kube_pod_init_container_status_last_terminated_reason | Gauge       | `container`, `pod`, `namespace`, `reason`                    | STABLE     |      |
| kube_pod_init_container_status_ready                  | Gauge       | `container`, `pod`, `namespace`                              | STABLE     |      |
| kube_pod_init_container_status_restarts_total         | Counter     | `container`, `namespace`, `pod`                              | STABLE     |      |
| kube_pod_init_container_resource_limits               | Gauge       | `resource`, `unit`, `container`, `pod`, `namespace`, `node`  | STABLE     |      |
| kube_pod_spec_volumes_persistentvolumeclaims_info     | Gauge       | `pod`, `namespace`, `volume`, `persistentvolumeclaim`        | STABLE     |      |
| kube_pod_spec_volumes_persistentvolumeclaims_readonly | Gauge       | `pod`, `namespace`, `volume`, `persistentvolumeclaim`        | STABLE     |      |
| kube_pod_status_scheduled_time                        | Gauge       | `pod`, `namespace`                                           | STABLE     |      |
| kube_pod_status_unschedulable                         | Gauge       | `pod`, `namespace`                                           | STABLE     |      |

> **reason**:
>
> - kube_pod_container_status_waiting_reason: `ContainerCreating | CrashLoopBackOff | ErrImagePull | ImagePullBackOff | CreateContainerConfigError | InvalidImageName | CreateContainerError`
> - kube_pod_container_status_terminated_reason: `OOMKilled | Error | Completed | ContainerCannotRun | DeadlineExceeded`
> - kube_pod_container_status_last_terminated_reason: `OOMKilled | Error | Completed | ContainerCannotRun | DeadlineExceeded`
> - kube_pod_init_container_status_waiting_reason: `ContainerCreating | CrashLoopBackOff | ErrImagePull | ImagePullBackOff | CreateContainerConfigError`
> - kube_pod_init_container_status_terminated_reason: `OOMKilled | Error | Completed | ContainerCannotRun | DeadlineExceeded`
> - kube_pod_init_container_status_last_terminated_reason: `OOMKilled | Error | Completed | ContainerCannotRun | DeadlineExceeded`

> **condition**:
>
> - kube_pod_status_ready: `true | false | unknown`
> - kube_pod_status_scheduled: `true | false | unknown`

> **phase**:
>
> - kube_pod_status_phase: `Pending | Running | Succeeded | Failed | Unknown`

> **type**:
>
> - kube_pod_restart_policy:  `Always | Never | OnFailure`

### replicasets

| Metric name                                   | Metric type | Labels/tags                                                  | Status | 说明 |
| --------------------------------------------- | ----------- | ------------------------------------------------------------ | ------ | ---- |
| kube_replicaset_status_replicas               | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_status_fully_labeled_replicas | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_status_ready_replicas         | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_status_observed_generation    | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_spec_replicas                 | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_metadata_generation           | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_labels                        | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_created                       | Gauge       | `replicaset`, `namespace`                                    | STABLE |      |
| kube_replicaset_owner                         | Gauge       | `replicaset`, `namespace`, `owner_kind`, `owner_name`, `owner_is_controller` | STABLE |      |

### replicationcontrollers

| Metric name                                              | Metric type | Labels/tags                          | Status | 说明 |
| -------------------------------------------------------- | ----------- | ------------------------------------ | ------ | ---- |
| kube_replicationcontroller_status_replicas               | Gauge       | `replicationcontroller, `namespace`  | STABLE |      |
| kube_replicationcontroller_status_fully_labeled_replicas | Gauge       | `replijcationcontroller, `namespace` | STABLE |      |
| kube_replicationcontroller_status_ready_replicas         | Gauge       | `replicationcontroller, `namespace`  | STABLE |      |
| kube_replicationcontroller_status_available_replicas     | Gauge       | `replicationcontroller, `namespace`  | STABLE |      |
| kube_replicationcontroller_status_observed_generation    | Gauge       | `replicationcontroller, `namespace`  | STABLE |      |
| kube_replicationcontroller_spec_replicas                 | Gauge       | `replicationcontroller, `namespace`  | STABLE |      |
| kube_replicationcontroller_metadata_generation           | Gauge       | `replicationcontroller, `namespace`  | STABLE |      |
| kube_replicationcontroller_created                       | Gauge       | `replicationcontroller, `namespace`  | STABLE |      |

### resourcequota

| Metric name                | Metric type | Labels/tags                                     | Status | 说明 |
| -------------------------- | ----------- | ----------------------------------------------- | ------ | ---- |
| kube_resourcequota         | Gauge       | `resourcequota` `namespace`, `resource`, `type` | STABLE |      |
| kube_resourcequota_created | Gauge       | `resourcequota` `namespace`                     | STABLE |      |

### secrets

| Metric name                           | Metric type | Labels/tags                                 | Status       | 说明 |
| ------------------------------------- | ----------- | ------------------------------------------- | ------------ | ---- |
| kube_secret_info                      | Gauge       | `secret`, `namespace`                       | STABLE       |      |
| kube_secret_type                      | Gauge       | `secret`, `namespace`, `type`               | STABLE       |      |
| kube_secret_labels                    | Gauge       | `secret`, `namespace`, `label_SECRET_LABEL` | STABLE       |      |
| kube_secret_created                   | Gauge       | `secret`, `namespace`                       | STABLE       |      |
| kube_secret_metadata_resource_version | Gauge       | `secret`, `namespace`                       | EXPERIMENTAL |      |

### services

| Metric name                               | Metric type | Labels/tags                                                  | Status | 说明 |
| ----------------------------------------- | ----------- | ------------------------------------------------------------ | ------ | ---- |
| kube_service_info                         | Gauge       | `service`, `namespace`, `cluster_ip`, `external_name`, `load_balancer_ip` | STABLE |      |
| kube_service_labels                       | Gauge       | `service`, `namespace`, `label_SERVICE_LABEL`                | STABLE |      |
| kube_service_created                      | Gauge       | `service`, `namespace`                                       | STABLE |      |
| kube_service_spec_type                    | Gauge       | `service`, `namespace`, `type`                               | STABLE |      |
| kube_service_spec_external_ip             | Gauge       | `service`, `namespace`, `external_ip`                        | STABLE |      |
| kube_service_status_load_balancer_ingress | Gauge       | `service`, `namespace`, `ip`, `hostname`                     | STABLE |      |

> **type**:
>
> - kube_service_spec_type: `ClusterIP | NodePort | LoadBalancer | ExternalName`

### statefulsets

| Metric name                                 | Metric type | Labels/tags                                           | Status | 说明 |
| ------------------------------------------- | ----------- | ----------------------------------------------------- | ------ | ---- |
| kube_statefulset_status_replicas            | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_status_replicas_current    | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_status_replicas_ready      | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_status_replicas_updated    | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_status_observed_generation | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_replicas                   | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_metadata_generation        | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_created                    | Gauge       | `statefulset`, `namespace`                            | STABLE |      |
| kube_statefulset_labels                     | Gauge       | `statefulset`, `namespace`, `label_STATEFULSET_LABEL` | STABLE |      |
| kube_statefulset_status_current_revision    | Gauge       | `statefulset`, `namespace`, `revision`                | STABLE |      |
| kube_statefulset_status_update_revision     | Gauge       | `statefulset`, `namespace`, `revision`                | STABLE |      |

### storageclasses

| Metric name               | Metric type | Labels/tags                                                  | Status | 说明 |
| ------------------------- | ----------- | ------------------------------------------------------------ | ------ | ---- |
| kube_storageclass_info    | Gauge       | `storageclass`, `provisioner`, `reclaimPolicy`, `volumeBindingMode` | STABLE |      |
| kube_storageclass_labels  | Gauge       | `storageclass`, `label_STORAGECLASS_LABEL`                   | STABLE |      |
| kube_storageclass_created | Gauge       | `storageclass`                                               | STABLE |      |

### validatingwebhookconfigurations

| Metric name                                                  | Metric type | Labels/tags                                   | Status       | 说明 |
| ------------------------------------------------------------ | ----------- | --------------------------------------------- | ------------ | ---- |
| kube_validatingwebhookconfiguration_info                     | Gauge       | `validatingwebhookconfiguration`, `namespace` | EXPERIMENTAL |      |
| kube_validatingwebhookconfiguration_created                  | Gauge       | `validatingwebhookconfiguration`, `namespace` | EXPERIMENTAL |      |
| kube_validatingwebhookconfiguration_metadata_resource_version | Gauge       | `validatingwebhookconfiguration`, `namespace` | EXPERIMENTAL |      |

### volumeattachments

| Metric name                                        | Metric type | Labels/tags                                        | Status       | 说明 |
| -------------------------------------------------- | ----------- | -------------------------------------------------- | ------------ | ---- |
| kube_volumeattachment_info                         | Gauge       | `volumeattachment`, `attacher`, `nodeName`         | EXPERIMENTAL |      |
| kube_volumeattachment_created                      | Gauge       | `volumeattachment`                                 | EXPERIMENTAL |      |
| kube_volumeattachment_labels                       | Gauge       | `volumeattachment`, `label_VOLUMEATTACHMENT_LABEL` | EXPERIMENTAL |      |
| kube_volumeattachment_spec_source_persistentvolume | Gauge       | `volumeattachment`, `volumename`                   | EXPERIMENTAL |      |
| kube_volumeattachment_status_attached              | Gauge       | `volumeattachment`                                 | EXPERIMENTAL |      |
| kube_volumeattachment_status_attachment_metadata   | Gauge       | `volumeattachment`, `metadata_METADATA_KEY`        | EXPERIMENTAL |      |

### verticalpodautoscalers

| Metric name                                                  | Metric type | Labels/tags                                                  | Status       | 说明 |
| ------------------------------------------------------------ | ----------- | ------------------------------------------------------------ | ------------ | ---- |
| kube_verticalpodautoscaler_spec_resourcepolicy_container_policies_minallowed | Gauge       | `container`, `namespace`, `resource`,`target_api_version`, `target_kind`, `target_name`,  `unit`, `verticalpodautoscaler` | EXPERIMENTAL |      |
| kube_verticalpodautoscaler_spec_resourcepolicy_container_policies_maxallowed | Gauge       | `container`, `namespace`, `resource`,`target_api_version`, `target_kind`, `target_name`,  `unit`, `verticalpodautoscaler` | EXPERIMENTAL |      |
| kube_verticalpodautoscaler_status_recommendation_containerrecommendations_lowerbound | Gauge       | `container`, `namespace`, `resource`,`target_api_version`, `target_kind`, `target_name`,  `unit`, `verticalpodautoscaler` | EXPERIMENTAL |      |
| kube_verticalpodautoscaler_status_recommendation_containerrecommendations_target | Gauge       | `container`, `namespace`, `resource`,`target_api_version`, `target_kind`, `target_name`,  `unit`, `verticalpodautoscaler` | EXPERIMENTAL |      |
| kube_verticalpodautoscaler_status_recommendation_containerrecommendations_uncappedtarget | Gauge       | `container`, `namespace`, `resource`,`target_api_version`, `target_kind`, `target_name`,  `unit`, `verticalpodautoscaler` | EXPERIMENTAL |      |
| kube_verticalpodautoscaler_status_recommendation_containerrecommendations_upperbound | Gauge       | `container`, `namespace`, `resource`,`target_api_version`, `target_kind`, `target_name`,  `unit`, `verticalpodautoscaler` | EXPERIMENTAL |      |
| kube_verticalpodautoscaler_labels                            | Gauge       | `label_app`, `namespace`, `target_api_version`, `target_kind`, `target_name`,  `verticalpodautoscaler` | EXPERIMENTAL |      |
| kube_verticalpodautoscaler_spec_updatepolicy_updatemode      | Gauge       | `namespace`, `target_api_version`, `target_kind`, `target_name`,  `update_mode`, `verticalpodautoscaler` | EXPERIMENTAL |      |

> - **resource**: `cpu | memory`
> - **unit**: `cores | byte`

## kubelet cadvisor

### cpu

| 指标名称                                  | type  | label | 说明                                                  |
| ----------------------------------------- | ----- | ----- | ----------------------------------------------------- |
| container_cpu_user_seconds_total          | Gauge |       | Cumulative user cpu time consumed in seconds.         |
| container_cpu_system_seconds_total        |       |       | Cumulative system cpu time consumed in seconds.       |
| container_cpu_usage_seconds_total         |       | cpu   | Cumulative cpu time consumed in seconds.              |
| container_cpu_cfs_periods_total           |       |       | Number of elapsed enforcement period intervals.       |
| container_cpu_cfs_throttled_periods_total |       |       | Number of throttled period intervals.                 |
| container_cpu_cfs_throttled_seconds_total |       |       | Total time duration the container has been throttled. |

- cpu: total 或者 cpuxx

### memory

| 指标名称                           | Metric type | label                   | 说明                                                         |
| ---------------------------------- | ----------- | ----------------------- | ------------------------------------------------------------ |
| container_memory_cache             | Gauge       |                         | Number of bytes of page cache memory.                        |
| container_memory_rss               | Gauge       |                         | Size of RSS in bytes.                                        |
| container_memory_mapped_file       | Gauge       |                         | Size of memory mapped files in bytes.                        |
| container_memory_swap              | Gauge       |                         | Container swap usage in bytes.                               |
| container_memory_failcnt           | Counter     |                         | Number of memory usage hits limits                           |
| container_memory_usage_bytes       | Gauge       |                         | Current memory usage in bytes, including all memory regardless of when it was accessed |
| container_memory_max_usage_bytes   | Gauge       |                         | Maximum memory usage recorded in bytes                       |
| container_memory_working_set_bytes | Gauge       |                         | Current working set in bytes.                                |
| container_memory_failures_total    | Counter     | "failure_type", "scope" | Cumulative count of memory allocation failures.              |

- failure_type:
  - pgfault
  - pgmajfault
- scope
  - container
  - hierarchy

### cpuLoad

| 指标名称                       | Metric type | label | 说明                                                         |
| ------------------------------ | ----------- | ----- | ------------------------------------------------------------ |
| container_cpu_load_average_10s | Gauge       |       | Value of container cpu load average over the last 10 seconds. |
| container_tasks_state          | Gauge       | state | Number of tasks in given state                               |

- state:
  - sleeping
  - running
  - stopped
  - uninterruptible
  - iowaiting

### diskIO

| 指标名称                                    | type    | label  | 说明                                         |
| ------------------------------------------- | ------- | ------ | -------------------------------------------- |
| container_fs_reads_bytes_total              | Counter | device | Cumulative count of bytes read               |
| container_fs_reads_total                    | Counter | device | Cumulative count of reads completed          |
| container_fs_sector_reads_total             | Counter | device | Cumulative count of sector reads completed   |
| container_fs_reads_merged_total             | Counter | device | Cumulative count of reads merged             |
| container_fs_read_seconds_total             | Counter | device | Cumulative count of seconds spent reading    |
| container_fs_writes_bytes_total             | Counter | device | Cumulative count of bytes written            |
| container_fs_writes_total                   | Counter | device | Cumulative count of writes completed         |
| container_fs_sector_writes_total            | Counter | device | Cumulative count of sector writes completed  |
| container_fs_writes_merged_total            | Counter | device | Cumulative count of writes merged            |
| container_fs_write_seconds_total            | Counter | device | Cumulative count of seconds spent writing    |
| container_fs_io_current                     | Gauge   | device | Number of I/Os currently in progress         |
| container_fs_io_time_seconds_total          | Counter | device | Cumulative count of seconds spent doing I/Os |
| container_fs_io_time_weighted_seconds_total | Counter | device | Cumulative weighted I/O time in seconds      |

### disk

| 指标名称                  | type  | label  | 说明                                                         |
| ------------------------- | ----- | ------ | ------------------------------------------------------------ |
| container_fs_inodes_free  | Gauge | device | Number of available Inodes                                   |
| container_fs_inodes_total | Gauge | device | Number of Inodes                                             |
| container_fs_limit_bytes  | Gauge | device | Number of bytes that can be consumed by the container on this filesystem. |
| container_fs_usage_bytes  | Gauge | device | Number of bytes that are consumed by the container on this filesystem. |

### network

| 指标名称                                         | type    | label     | 说明                                                      |
| ------------------------------------------------ | ------- | --------- | --------------------------------------------------------- |
| container_network_receive_bytes_total            | Counter | interface | Cumulative count of bytes received                        |
| container_network_receive_packets_total          | Counter | interface | Cumulative count of packets received                      |
| container_network_receive_packets_dropped_total  | Counter | interface | Cumulative count of packets dropped while receiving       |
| container_network_receive_errors_total           | Counter | interface | Cumulative count of errors encountered while receiving    |
| container_network_transmit_bytes_total           | Counter | interface | Cumulative count of bytes transmitted                     |
| container_network_transmit_packets_total         | Counter | interface | Cumulative count of packets transmitted                   |
| container_network_transmit_packets_dropped_total | Counter | interface | Cumulative count of packets dropped while transmitting    |
| container_network_transmit_errors_total          | Counter | interface | Cumulative count of errors encountered while transmitting |

### accelerator

| 指标名称                                 | type  | label               | 说明                                                         |
| ---------------------------------------- | ----- | ------------------- | ------------------------------------------------------------ |
| container_accelerator_memory_total_bytes | Gauge | make, model, acc_id | Total accelerator memory.                                    |
| container_accelerator_memory_used_bytes  | Gauge | make, model, acc_id | Total accelerator memory allocated.                          |
| container_accelerator_duty_cycle         | Gauge | make, model, acc_id | Percent of time over the past sample period during which the accelerator was actively processing. |

### process

| 指标名称                   | type  | label  | 说明                                                         |
| -------------------------- | ----- | ------ | ------------------------------------------------------------ |
| container_processes        | Gauge |        | Number of processes running inside the container.            |
| container_file_descriptors | Gauge |        | Number of open file descriptors for the container.           |
| container_sockets          | Gauge |        | Number of open sockets for the container.                    |
| container_threads_max      | Gauge |        | Maximum number of threads allowed inside the container, infinity if value is zero |
| container_threads          | Gauge |        | Number of threads running inside the container               |
| container_ulimits_soft     | Gauge | ulimit | Soft ulimit values for the container root process. Unlimited if -1, except priority and nice |

------

### sched

| 指标名称                                       | type    | label | 说明                                                         |
| ---------------------------------------------- | ------- | ----- | ------------------------------------------------------------ |
| container_cpu_schedstat_run_seconds_total      | Counter |       | Time duration the processes of the container have run on the CPU. |
| container_cpu_schedstat_runqueue_seconds_total | Counter |       | Time duration processes of the container have been waiting on a runqueue. |
| container_cpu_schedstat_run_periods_total      | Counter |       | Number of times processes of the cgroup have run on the cpu  |

### tcp

| 指标名称                           | type  | label     | 说明                                          |
| ---------------------------------- | ----- | --------- | --------------------------------------------- |
| container_network_tcp_usage_total  | Gauge | tcp_state | tcp connection usage statistic for container  |
| container_network_tcp6_usage_total | Gauge | tcp_state | tcp6 connection usage statistic for container |

- tcp_state:
  - established
  - synsent
  - synrecv
  - finwait1
  - finwait2
  - timewait
  - close
  - closewait
  - lastack
  - listen
  - closing

### udp

| 指标名称                           | type  | label     | 说明                                          |
| ---------------------------------- | ----- | --------- | --------------------------------------------- |
| container_network_udp_usage_total  | Gauge | udp_state | udp connection usage statistic for container  |
| container_network_udp6_usage_total | Gauge | udp_state | udp6 connection usage statistic for container |

- udp_state：
  - listen
  - dropped
  - rxqueued
  - txqueued

## kubelet

### /metrics/probes

| 指标名称                   | type    | label                                             | 说明                                                         |
| -------------------------- | ------- | ------------------------------------------------- | ------------------------------------------------------------ |
| prober_probe_total         | Counter | probe_type,result,container,pod,namespace,pod_uid | Cumulative number of a liveness, readiness or startup probe for a container by result. |
| process_start_time_seconds | Guage   |                                                   | Start time of the process since unix epoch in seconds.       |

### /metrics/resource/v1alpha1

| 指标名称                           | type  | label | 说明                                                         |
| ---------------------------------- | ----- | ----- | ------------------------------------------------------------ |
| node_cpu_usage_seconds_total       | Guage |       | Cumulative cpu time consumed by the node in core-seconds     |
| node_memory_working_set_bytes      | Guage |       | Current working set of the node in bytes                     |
| container_cpu_usage_seconds_total  | Guage |       | Cumulative cpu time consumed by the container in core-seconds |
| container_memory_working_set_bytes | Guage |       | Current working set of the container in bytes                |

### /metrics

| 指标名称                                     | type      | label                                                        | 说明                                                         |
| -------------------------------------------- | --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| kubelet_node_name                            | Gauge     | node                                                         | The node's name. The count is always 1.                      |
| kubelet_containers_per_pod_count             | Histogram |                                                              | The number of containers per pod.                            |
| kubelet_pod_worker_duration_seconds          | Histogram | operation_type                                               | Duration in seconds to sync a single pod. Broken down by operation type: create, update, or sync |
| kubelet_pod_start_duration_seconds           | Histogram |                                                              | Duration in seconds for a single pod to go from pending to running. |
| kubelet_cgroup_manager_duration_seconds      | Histogram | operation_type                                               | Duration in seconds for cgroup manager operations. Broken down by method. |
| kubelet_pod_worker_start_duration_seconds    | Histogram |                                                              | Duration in seconds from seeing a pod to starting a worker.  |
| kubelet_pleg_relist_duration_seconds         | Histogram |                                                              | Duration in seconds for relisting pods in PLEG.              |
| kubelet_pleg_discard_events                  | Counter   |                                                              | The number of discard events in PLEG.                        |
| kubelet_pleg_relist_interval_seconds         | Histogram |                                                              | Interval in seconds between relisting in PLEG.               |
| kubelet_runtime_operations_total             | Counter   | operation_type                                               | Cumulative number of runtime operations by operation type.   |
| kubelet_runtime_operations_duration_seconds  | Histogram | operation_type                                               | Duration in seconds of runtime operations. Broken down by operation type. |
| kubelet_runtime_operations_errors_total      | Counter   | operation_type                                               | Cumulative number of runtime operation errors by operation type. |
| kubelet_evictions                            | Counter   | eviction_signal                                              | Cumulative number of pod evictions by eviction signal        |
| kubelet_eviction_stats_age_seconds           | Histogram | eviction_signal                                              | Time between when stats are collected, and when pod is evicted based on those stats by eviction signal |
| kubelet_device_plugin_registration_total     | Counter   | resource_name                                                | Cumulative number of device plugin registrations. Broken down by resource name. |
| kubelet_device_plugin_alloc_duration_seconds | Histogram | resource_name                                                | Duration in seconds to serve a device plugin Allocation request. Broken down by resource name. |
| kubelet_node_config_assigned                 | Gauge     | node_config_source,node_config_uid,node_config_resource_version,node_config_kubelet_key | The node's understanding of intended config. The count is always 1. |
| kubelet_node_config_active                   | Gauge     | node_config_source,node_config_uid,node_config_resource_version,node_config_kubelet_key | The config source the node is actively using. The count is always 1. |
| kubelet_node_config_last_known_good          | Gauge     | node_config_source,node_config_uid,node_config_resource_version,node_config_kubelet_key | The config source the node will fall back to when it encounters certain errors. The count is always 1. |
| kubelet_node_config_error                    | Gauge     |                                                              | This metric is true (1) if the node is experiencing a configuration-related error, false (0) otherwise. |
| kubelet_run_podsandbox_duration_seconds      | Histogram | runtime_handler                                              | Duration in seconds of the run_podsandbox operations. Broken down by RuntimeClass. |
| kubelet_run_podsandbox_errors_total          | Counter   | runtime_handler                                              | Cumulative number of the run_podsandbox operation errors by RuntimeClass. |
| kubelet_running_pod_count                    | Gauge     |                                                              | Number of pods currently running                             |
| kubelet_running_container_count              | Gauge     | container_state                                              | Number of containers currently running                       |

## filebeat exporter

### health

| Metric 名称 | Metric 类型 | 标签 | 含义说明 |
| ----------- | ----------- | ---- | -------- |
| filebeat_up | Gauge       |      |          |

### system

- period: `1`, `5`, `15`

| Metric 名称                     | Metric 类型 | 标签   | 含义说明                                                     |
| ------------------------------- | ----------- | ------ | ------------------------------------------------------------ |
| filebeat_system_cpu_cores_total | Gauge       |        |                                                              |
| filebeat_system_load            | Gauge       | period |                                                              |
| filebeat_system_load_norm       | Gauge       | period | 标准化 cpu 负载， `filebeat_system_load / filebeat_system_cpu_cores_total` |

### beat

- mode: `system`, `user`

| Metric 名称                     | Metric 类型 | 标签 | 含义说明 |
| ------------------------------- | ----------- | ---- | -------- |
| filebeat_cpu_time_seconds_total | Counter     | mode |          |
| filebeat_cpu_ticks_total        | Counter     | mode |          |
| filebeat_uptime_seconds_total   | Counter     |      |          |
| filebeat_memstats_gc_next_total | Counter     |      |          |
| filebeat_memstats_memory_alloc  | Gauge       |      |          |
| filebeat_memstats_memory        | Gauge       |      |          |
| filebeat_memstats_rss           | Gauge       |      |          |
| filebeat_runtime_goroutines     | Gauge       |      |          |

### libbeat

- module:
  - filebeat_libbeat_config: `running`, `starts`, `stops`
- filebeat_libbeat_output_events
- type:
  - filebeat_libbeat_output_events: `acked`, `active`, `batches`, `dropped`, `duplicates`, `failed`
  - filebeat_libbeat_pipeline_queue: `acked`
  - filebeat_libbeat_pipeline_events: `active`, `dropped`, `failed`, `filtered`, `published`, `retry`
  - filebeat_libbeat_output_total:    `logstash` ...

| Metric 名称                                | Metric 类型 | 标签   | 含义说明 |
| ------------------------------------------ | ----------- | ------ | -------- |
| filebeat_libbeat_config_reloads_total      | Counter     |        |          |
| filebeat_libbeat_config                    | Gauge       | module |          |
| filebeat_libbeat_output_read_bytes_total   | Counter     |        |          |
| filebeat_libbeat_output_read_errors_total  | Counter     |        |          |
| filebeat_libbeat_output_write_bytes_total  | Counter     |        |          |
| filebeat_libbeat_output_write_errors_total | Counter     |        |          |
| filebeat_libbeat_output_events             | untyped     | type   |          |
| filebeat_libbeat_pipeline_clients          | Gauge       |        |          |
| filebeat_libbeat_pipeline_queue            | untyped     | type   |          |
| filebeat_libbeat_pipeline_events           | untyped     | type   |          |
| filebeat_libbeat_output_total              | Counter     | type   |          |

### registrar

- writes: `fail`, `success`, `total`
- state: `cleanup`, `current`, `update`

| Metric 名称               | Metric 类型 | 标签   | 含义说明 |
| ------------------------- | ----------- | ------ | -------- |
| filebeat_registrar_writes | Gauge       | writes |          |
| filebeat_registrar_states | Gauge       | state  |          |

### filebeat

- event: `active`, `added`, `done`
- harvester: `closed`, `open_files`, `running`, `skipped`, `started`
- files: `renamed`, `truncated`

| Metric 名称                 | Metric 类型 | 标签      | 含义说明 |
| --------------------------- | ----------- | --------- | -------- |
| filebeat_filebeat_events    | untyped     | event     |          |
| filebeat_filebeat_harvester | untyped     | harvester |          |
| filebeat_filebeat_input_log | untyped     | files     |          |

### metricbeat

- event: `success`, `failures`

| Metric 名称                       | Metric 类型 | 标签  | 含义说明 |
| --------------------------------- | ----------- | ----- | -------- |
| metricbeat_system_cpu             | Counter     | event |          |
| metricbeat_system_filesystem      | Counter     | event |          |
| metricbeat_system_fsstat          | Counter     | event |          |
| metricbeat_system_load            | Counter     | event |          |
| metricbeat_system_memory          | Counter     | event |          |
| metricbeat_system_network         | Counter     | event |          |
| metricbeat_system_process         | Counter     | event |          |
| metricbeat_system_process_summary | Counter     | event |          |
| metricbeat_system_uptime          | Counter     | event |          |

### auditd

| Metric 名称                 | Metric 类型 | 标签 | 含义说明 |
| --------------------------- | ----------- | ---- | -------- |
| auditd_kernel_lost          | Gauge       |      |          |
| auditd_reassembler_seq_gaps | Gauge       |      |          |
| auditd_received_msgs        | Gauge       |      |          |
| auditd_userspace_lost       | Gauge       |      |          |

## elasticsearch exporter

### 1.1. 集群状态

- 以下指标均包含 `cluster` 的 label
- `type` label 取值： `active`, `active_primary`, `unassigned`, `initializing`, `relocating`

| Metric 名称                              | Metric 类型 | 标签 | 含义说明            |
| ---------------------------------------- | ----------- | ---- | ------------------- |
| es_cluster_status                        | Gauge       |      | 集群状态            |
| es_cluster_nodes_number                  | Gauge       |      | 集群节点数          |
| es_cluster_datanodes_number              | Gauge       |      | 集群**数据**节点数  |
| es_cluster_shards_active_percent         | Gauge       |      | active 分片占比     |
| es_cluster_shards_number                 | Gauge       | type | 分片数量            |
| es_cluster_pending_tasks_number          | Gauge       |      | pending 任务数      |
| es_cluster_task_max_waiting_time_seconds | Gauge       |      | 任务的最大等待时间  |
| es_cluster_is_timedout_bool              | Gauge       |      | 集群是否超时        |
| es_cluster_inflight_fetch_number         | Gauge       |      | 飞行中的 fetch 数量 |

### 1.2. 节点状态

- **以下指标均包含 `cluster`, `node`, `nodeid` 的 label**

#### 1.2.1. 节点角色

- role

| Metric 名称       | Metric 类型 | 标签 | 含义说明 |
| ----------------- | ----------- | ---- | -------- |
| es_node_role_bool | Gauge       | role | 节点角色 |

#### 1.2.2. 索引全局状态

- type: `source`, `target`

| Metric 名称                                    | Metric 类型 | 标签 | 含义说明                                        |
| ---------------------------------------------- | ----------- | ---- | ----------------------------------------------- |
| es_indices_doc_number                          | Gauge       |      | 文档总数                                        |
| es_indices_doc_deleted_number                  | Gauge       |      | 已删除文档数量                                  |
| es_indices_store_size_bytes                    | Gauge       |      | 索引存储占用空间字节数                          |
| es_indices_indexing_delete_count               | Gauge       |      | 正在删除的文档数量                              |
| es_indices_indexing_delete_current_number      | Gauge       |      | 当前文档删除的速率                              |
| es_indices_indexing_delete_time_seconds        | Gauge       |      | 删除文档所花费的时间                            |
| es_indices_indexing_index_count                | Gauge       |      | 正在索引的文档数量                              |
| es_indices_indexing_index_current_number       | Gauge       |      | 正在索引的文档速率                              |
| es_indices_indexing_index_failed_count         | Gauge       |      | 索引文档失败的计数                              |
| es_indices_indexing_index_time_seconds         | Gauge       |      | 索引文档所花费的时间                            |
| es_indices_indexing_noop_update_count          | Gauge       |      | noop文档更新的计数                              |
| es_indices_indexing_is_throttled_bool          | Gauge       |      | 索引是否正在限流状态                            |
| es_indices_indexing_throttle_time_seconds      | Gauge       |      | 限流花费的时间                                  |
| es_indices_get_count                           | Gauge       |      | get命令计数                                     |
| es_indices_get_time_seconds                    | Gauge       |      | get命令时所花费的时间                           |
| es_indices_get_exists_count                    | Gauge       |      | 使用get命令时，现有文档的计数                   |
| es_indices_get_exists_time_seconds             | Gauge       |      | Time spent while existing documents get command |
| es_indices_get_missing_count                   | Gauge       |      | get命令时丢失文档的计数                         |
| es_indices_get_missing_time_seconds            | Gauge       |      | Time spent while missing documents get command  |
| es_indices_get_current_number                  | Gauge       |      | get 命令的当前速率                              |
| es_indices_search_open_contexts_number         | Gauge       |      | 搜索打开上下文的数量                            |
| es_indices_search_fetch_count                  | Gauge       |      | 搜索获取的计数                                  |
| es_indices_search_fetch_current_number         | Gauge       |      | 当前的搜索获取速率                              |
| es_indices_search_fetch_time_seconds           | Gauge       |      | 搜索时所花费的时间                              |
| es_indices_search_query_count                  | Gauge       |      | 搜索查询次数                                    |
| es_indices_search_query_current_number         | Gauge       |      | 当前搜索查询率                                  |
| es_indices_search_query_time_seconds           | Gauge       |      | 搜索查询所花费的时间                            |
| es_indices_search_scroll_count                 | Gauge       |      | scroll 搜索数                                   |
| es_indices_search_scroll_current_number        | Gauge       |      | scroll 搜索速率                                 |
| es_indices_search_scroll_time_seconds          | Gauge       |      | scroll 搜索花费的时间                           |
| es_indices_merges_current_number               | Gauge       |      | 当前的合并率                                    |
| es_indices_merges_current_docs_number          | Gauge       |      | 合并文档的当前速率                              |
| es_indices_merges_current_size_bytes           | Gauge       |      | 当前合并字节的速率                              |
| es_indices_merges_total_number                 | Gauge       |      | 合并数                                          |
| es_indices_merges_total_time_seconds           | Gauge       |      | 合并时花费的时间                                |
| es_indices_merges_total_docs_count             | Gauge       |      | 文档合并数                                      |
| es_indices_merges_total_size_bytes             | Gauge       |      | 合并文档的字节数                                |
| es_indices_merges_total_stopped_time_seconds   | Gauge       |      | 合并进程停止时所花费的时间                      |
| es_indices_merges_total_throttled_time_seconds | Gauge       |      | 节流时合并所花费的时间                          |
| es_indices_merges_total_auto_throttle_bytes    | Gauge       |      | Bytes merged while throttling                   |
| es_indices_refresh_total_count                 | Gauge       |      | Count of refreshes                              |
| es_indices_refresh_total_time_seconds          | Gauge       |      | Time spent while refreshes                      |
| es_indices_refresh_listeners_number            | Gauge       |      | Number of refresh listeners                     |
| es_indices_flush_total_count                   | Gauge       |      | Count of flushes                                |
| es_indices_flush_total_time_seconds            | Gauge       |      | Total time spent while flushes                  |
| es_indices_querycache_cache_count              | Gauge       |      | Count of queries in cache                       |
| es_indices_querycache_cache_size_bytes         | Gauge       |      | Query cache size                                |
| es_indices_querycache_evictions_count          | Gauge       |      | Count of evictions in query cache               |
| es_indices_querycache_hit_count                | Gauge       |      | Count of hits in query cache                    |
| es_indices_querycache_memory_size_bytes        | Gauge       |      | Memory usage of query cache                     |
| es_indices_querycache_miss_number              | Gauge       |      | Count of misses in query cache                  |
| es_indices_querycache_total_number             | Gauge       |      | Count of usages of query cache                  |
| es_indices_fielddata_memory_size_bytes         | Gauge       |      | Memory usage of field date cache                |
| es_indices_fielddata_evictions_count           | Gauge       |      | Count of evictions in field data cache          |
| es_indices_percolate_count                     | Gauge       |      | Count of percolates                             |
| es_indices_percolate_current_number            | Gauge       |      | Rate of percolates                              |
| es_indices_percolate_memory_size_bytes         | Gauge       |      | Percolate memory size                           |
| es_indices_percolate_queries_count             | Gauge       |      | Count of queries percolated                     |
| es_indices_percolate_time_seconds              | Gauge       |      | Time spent while percolating                    |
| es_indices_completion_size_bytes               | Gauge       |      | Size of completion suggest statistics           |
| es_indices_segments_number                     | Gauge       |      | Current number of segments                      |
| es_indices_segments_memory_bytes               | Gauge       |      | Memory used by segments                         |
| es_indices_suggest_current_number              | Gauge       |      | Current rate of suggests                        |
| es_indices_suggest_count                       | Gauge       |      | Count of suggests                               |
| es_indices_suggest_time_seconds                | Gauge       |      | Time spent while making suggests                |
| es_indices_requestcache_memory_size_bytes      | Gauge       |      | 用于请求缓存的内存                              |
| es_indices_requestcache_hit_count              | Gauge       |      | 请求缓存命中数量                                |
| es_indices_requestcache_miss_count             | Gauge       |      | 请求缓存misss数量                               |
| es_indices_requestcache_evictions_count        | Gauge       |      | 请求缓存中的收回数                              |
| es_indices_recovery_current_number             | Gauge       | type | Current number of recoveries                    |
| es_indices_recovery_throttle_time_seconds      | Gauge       |      | Time spent while throttling recoveries          |

#### 1.2.3. transport 状态

| Metric 名称                     | Metric 类型 | 标签 | 含义说明           |
| ------------------------------- | ----------- | ---- | ------------------ |
| es_transport_server_open_number | Gauge       |      | 服务器开启的连接数 |
| es_transport_rx_packets_count   | Gauge       |      | 收到包数量         |
| es_transport_tx_packets_count   | Gauge       |      | 发送包数量         |
| es_transport_rx_bytes_count     | Gauge       |      | 收到字节数         |
| es_transport_tx_bytes_count     | Gauge       |      | 发送字节数         |

#### 1.2.4. HTTP 状态

| Metric 名称                | Metric 类型 | 标签 | 含义说明           |
| -------------------------- | ----------- | ---- | ------------------ |
| es_http_open_server_number | Gauge       |      | 服务器开启的连接数 |
| es_http_open_total_count   | Gauge       |      | 开启的连接数量统计 |

#### 1.2.5. 线程池 状态

- `name`: 线程名
- `type`：`threads`, `active`, `largest`, `completed`, `rejected`, `queue`

| Metric 名称                  | Metric 类型 | 标签       | 含义说明                         |
| ---------------------------- | ----------- | ---------- | -------------------------------- |
| es_threadpool_threads_number | Gauge       | name, type | Number of threads in thread pool |
| es_threadpool_threads_count  | Gauge       | name, type | Count of threads in thread pool  |
| es_threadpool_tasks_number   | Gauge       | name, type | Number of tasks in thread pool   |

#### 1.2.6. Ingest 指标

- pipeline: pipeline 名称
- processor: processor 名称

| Metric 名称                                     | Metric 类型 | 标签                | 含义说明                        |
| ----------------------------------------------- | ----------- | ------------------- | ------------------------------- |
| es_ingest_total_count                           | Gauge       |                     | Ingestion total number          |
| es_ingest_total_time_seconds                    | Gauge       |                     | Ingestion total time in seconds |
| es_ingest_total_current                         | Gauge       |                     | Ingestion total current         |
| es_ingest_total_failed_count                    | Gauge       |                     | Ingestion total failed          |
| es_ingest_pipeline_total_count                  | Gauge       | pipeline            | Ingestion total number          |
| es_ingest_pipeline_total_time_seconds           | Gauge       | pipeline            | Ingestion total time in seconds |
| es_ingest_pipeline_total_current                | Gauge       | pipeline            | Ingestion total current         |
| es_ingest_pipeline_total_failed_count           | Gauge       | pipeline            | Ingestion total failed          |
| es_ingest_pipeline_processor_total_count        | Gauge       | pipeline, processor | Ingestion total number          |
| es_ingest_pipeline_processor_total_time_seconds | Gauge       | pipeline, processor | Ingestion total time in seconds |
| es_ingest_pipeline_processor_total_current      | Gauge       | pipeline, processor | Ingestion total current         |
| es_ingest_pipeline_processor_total_failed_count | Gauge       | pipeline, processor | Ingestion total failed          |

#### 1.2.7. 断路器(Circuit breaker) 指标

| Metric 名称                       | Metric 类型 | 标签 | 含义说明                       |
| --------------------------------- | ----------- | ---- | ------------------------------ |
| es_circuitbreaker_estimated_bytes | Gauge       | name | Circuit breaker estimated size |
| es_circuitbreaker_limit_bytes     | Gauge       | name | Circuit breaker size limit     |
| es_circuitbreaker_overhead_ratio  | Gauge       | name | Circuit breaker overhead ratio |
| es_circuitbreaker_tripped_count   | Gauge       | name | Circuit breaker tripped count  |

#### 1.2.8. script 指标

| Metric 名称                     | Metric 类型 | 标签 | 含义说明                             |
| ------------------------------- | ----------- | ---- | ------------------------------------ |
| es_script_cache_evictions_count | Gauge       |      | Number of evictions in scripts cache |
| es_script_compilations_count    | Gauge       |      | Number of scripts compilations       |

#### 1.2.9. 进程 指标

| Metric 名称                             | Metric 类型 | 标签 | 含义说明              |
| --------------------------------------- | ----------- | ---- | --------------------- |
| es_process_cpu_percent                  | Gauge       |      | ES进程使用的CPU百分比 |
| es_process_cpu_time_seconds             | Gauge       |      | ES进程使用的CPU时间   |
| es_process_mem_total_virtual_bytes      | Gauge       |      | ES进程使用的内存      |
| es_process_file_descriptors_open_number | Gauge       |      | 打开的文件描述符      |
| es_process_file_descriptors_max_number  | Gauge       |      | 最大文件描述符        |

#### 1.2.10. jvm 指标

- pool: `old`, `young`, `survivor`
- gc: `old`, `young`
- bufferpool:

| Metric 名称                            | Metric 类型 | 标签       | 含义说明               |
| -------------------------------------- | ----------- | ---------- | ---------------------- |
| es_jvm_uptime_seconds                  | Gauge       |            | JVM uptime             |
| es_jvm_mem_heap_max_bytes              | Gauge       |            | 堆中使用的最大内存     |
| es_jvm_mem_heap_used_bytes             | Gauge       |            | 堆中使用的内存         |
| es_jvm_mem_heap_used_percent           | Gauge       |            | 堆中使用的内存百分比   |
| es_jvm_mem_nonheap_used_bytes          | Gauge       |            | 堆外内存使用量         |
| es_jvm_mem_heap_committed_bytes        | Gauge       |            | 堆中提交的字节数       |
| es_jvm_mem_nonheap_committed_bytes     | Gauge       |            | 堆外内存提交的字节数   |
| es_jvm_mem_pool_max_bytes              | Gauge       | pool       | 内存池的最大使用量     |
| es_jvm_mem_pool_peak_max_bytes         | Gauge       | pool       | 内存池的最大使用峰值   |
| es_jvm_mem_pool_used_bytes             | Gauge       | pool       | 内存池中已使用内存     |
| es_jvm_mem_pool_peak_used_bytes        | Gauge       | pool       | 内存池中使用的内存峰值 |
| es_jvm_threads_number                  | Gauge       |            | 线程数                 |
| es_jvm_threads_peak_number             | Gauge       |            | 线程数峰值             |
| es_jvm_gc_collection_count             | Gauge       | gc         | GC收集计数             |
| es_jvm_gc_collection_time_seconds      | Gauge       | gc         | GC收集所花费的时间     |
| es_jvm_bufferpool_number               | Gauge       | bufferpool | 缓冲池数量             |
| es_jvm_bufferpool_total_capacity_bytes | Gauge       | bufferpool | 缓冲池提供的总容量     |
| es_jvm_bufferpool_used_bytes           | Gauge       | bufferpool | 缓冲池中已使用的内存   |
| es_jvm_classes_loaded_number           | Gauge       |            | 加载类的计数           |
| es_jvm_classes_total_loaded_number     | Gauge       |            | 加载类的总数           |
| es_jvm_classes_unloaded_number         | Gauge       |            | 未加载类的计数         |

#### 1.2.11. OS 指标

| Metric 名称                        | Metric 类型 | 标签 | 含义说明        |
| ---------------------------------- | ----------- | ---- | --------------- |
| es_os_cpu_percent                  | Gauge       |      | cpu 使用百分比  |
| es_os_load_average_one_minute      | Gauge       |      | 1分钟 cpu 负载  |
| es_os_load_average_five_minutes    | Gauge       |      | 5分钟 cpu 负载  |
| es_os_load_average_fifteen_minutes | Gauge       |      | 15分钟 cpu 负载 |
| es_os_mem_free_bytes               | Gauge       |      | free 内存       |
| es_os_mem_free_percent             | Gauge       |      | free 内存百分比 |
| es_os_mem_used_bytes               | Gauge       |      | used 内存       |
| es_os_mem_used_percent             | Gauge       |      | used 内存百分比 |
| es_os_mem_total_bytes              | Gauge       |      | 总内存          |
| es_os_swap_free_bytes              | Gauge       |      | swap free 内存  |
| es_os_swap_used_bytes              | Gauge       |      | swap used 内存  |
| es_os_swap_total_bytes             | Gauge       |      | swap 总内存     |

#### 1.2.12. FS 指标

- path: 数据路径
- mount:  挂载点
- type: 文件系统类型

| Metric 名称                  | Metric 类型 | 标签              | 含义说明                                   |
| ---------------------------- | ----------- | ----------------- | ------------------------------------------ |
| fs_total_total_bytes         | Gauge       |                   | Total disk space for all mount points      |
| fs_total_available_bytes     | Gauge       |                   | Available disk space for all mount points  |
| fs_total_free_bytes          | Gauge       |                   | Free disk space for all mountpoints        |
| fs_most_usage_free_bytes     | Gauge       | path              | Free disk space for most used mountpoint   |
| fs_most_usage_total_bytes    | Gauge       | path              | Total disk space for most used mountpoint  |
| fs_least_usage_free_bytes    | Gauge       | path              | Free disk space for least used mountpoint  |
| fs_least_usage_total_bytes   | Gauge       | path              | Total disk space for least used mountpoint |
| fs_path_total_bytes          | Gauge       | path, mount, type | Total disk space                           |
| fs_path_available_bytes      | Gauge       | path, mount, type | Available disk space                       |
| fs_path_free_bytes           | Gauge       | path, mount, type | Free disk space                            |
| fs_io_total_operations       | Gauge       |                   | Total IO operations                        |
| fs_io_total_read_operations  | Gauge       |                   | Total IO read operations                   |
| fs_io_total_write_operations | Gauge       |                   | Total IO write operations                  |
| fs_io_total_read_bytes       | Gauge       |                   | Total IO read bytes                        |
| fs_io_total_write_bytes      | Gauge       |                   | Total IO write bytes                       |

### 1.3. ES 配置 指标

| Metric 名称                                                 | Metric 类型 | 标签 | 含义说明                                    |
| ----------------------------------------------------------- | ----------- | ---- | ------------------------------------------- |
| cluster_routing_allocation_disk_threshold_enabled           | Gauge       |      | Disk allocation decider is enabled          |
| cluster_routing_allocation_disk_watermark_low_bytes         | Gauge       |      | Low watermark for disk usage in bytes       |
| cluster_routing_allocation_disk_watermark_high_bytes        | Gauge       |      | High watermark for disk usage in bytes      |
| cluster_routing_allocation_disk_watermark_flood_stage_bytes | Gauge       |      | Flood stage for disk usage in bytes         |
| cluster_routing_allocation_disk_watermark_low_pct           | Gauge       |      | Low watermark for disk usage in pct         |
| cluster_routing_allocation_disk_watermark_high_pct          | Gauge       |      | High watermark for disk usage in pct        |
| cluster_routing_allocation_disk_watermark_flood_stage_pct   | Gauge       |      | Flood stage watermark for disk usage in pct |

### 1.4. 详细索引状态

> !!! 默认禁用

- index:
- context:
- type:

| Metric 名称                                  | Metric 类型 | 标签                       | 含义说明                                          |
| -------------------------------------------- | ----------- | -------------------------- | ------------------------------------------------- |
| index_status                                 | Gauge       | `index`                    | Index status                                      |
| index_replicas_number                        | Gauge       | `index`                    | Number of replicas                                |
| index_shards_number                          | Gauge       | `index`, `type`            | Number of shards                                  |
| index_doc_number                             | Gauge       | `index`, `context`         | Total number of documents                         |
| index_doc_deleted_number                     | Gauge       | `index`, `context`         | Number of deleted documents                       |
| index_store_size_bytes                       | Gauge       | `index`, `context`         | Store size of the indices in bytes                |
| index_indexing_delete_count                  | Gauge       | `index`, `context`         | Count of documents deleted                        |
| index_indexing_delete_current_number         | Gauge       | `index`, `context`         | Current rate of documents deleted                 |
| index_indexing_delete_time_seconds           | Gauge       | `index`, `context`         | Time spent while deleting documents               |
| index_indexing_index_count                   | Gauge       | `index`, `context`         | Count of documents indexed                        |
| index_indexing_index_current_number          | Gauge       | `index`, `context`         | Current rate of documents indexed                 |
| index_indexing_index_failed_count            | Gauge       | `index`, `context`         | Count of failed to index documents                |
| index_indexing_index_time_seconds            | Gauge       | `index`, `context`         | Time spent while indexing documents               |
| index_indexing_noop_update_count             | Gauge       | `index`, `context`         | Count of noop document updates                    |
| index_indexing_is_throttled_bool             | Gauge       | `index`, `context`         | Is indexing throttling ?                          |
| index_indexing_throttle_time_seconds         | Gauge       | `index`, `context`         | Time spent while throttling                       |
| index_get_count                              | Gauge       | `index`, `context`         | Count of get commands                             |
| index_get_time_seconds                       | Gauge       | `index`, `context`         | Time spent while get commands                     |
| index_get_exists_count                       | Gauge       | `index`, `context`         | Count of existing documents when get command      |
| index_get_exists_time_seconds                | Gauge       | `index`, `context`         | Time spent while existing documents get command   |
| index_get_missing_count                      | Gauge       | `index`, `context`         | Count of missing documents when get command       |
| index_get_missing_time_seconds               | Gauge       | `index`, `context`         | Time spent while missing documents get command    |
| index_get_current_number                     | Gauge       | `index`, `context`         | Current rate of get commands                      |
| index_search_open_contexts_number            | Gauge       | `index`, `context`         | Number of search open contexts                    |
| index_search_fetch_count                     | Gauge       | `index`, `context`         | Count of search fetches                           |
| index_search_fetch_current_number            | Gauge       | `index`, `context`         | Current rate of search fetches                    |
| index_search_fetch_time_seconds              | Gauge       | `index`, `context`         | Time spent while search fetches                   |
| index_search_query_count                     | Gauge       | `index`, `context`         | Count of search queries                           |
| index_search_query_current_number            | Gauge       | `index`, `context`         | Current rate of search queries                    |
| index_search_query_time_seconds              | Gauge       | `index`, `context`         | Time spent while search queries                   |
| index_search_scroll_count                    | Gauge       | `index`, `context`         | Count of search scrolls                           |
| index_search_scroll_current_number           | Gauge       | `index`, `context`         | Current rate of search scrolls                    |
| index_search_scroll_time_seconds             | Gauge       | `index`, `context`         | Time spent while search scrolls                   |
| index_merges_current_number                  | Gauge       | `index`, `context`         | Current rate of merges                            |
| index_merges_current_docs_number             | Gauge       | `index`, `context`         | Current rate of documents merged                  |
| index_merges_current_size_bytes              | Gauge       | `index`, `context`         | Current rate of bytes merged                      |
| index_merges_total_number                    | Gauge       | `index`, `context`         | Count of merges                                   |
| index_merges_total_time_seconds              | Gauge       | `index`, `context`         | Time spent while merging                          |
| index_merges_total_docs_count                | Gauge       | `index`, `context`         | Count of documents merged                         |
| index_merges_total_size_bytes                | Gauge       | `index`, `context`         | Count of bytes of merged documents                |
| index_merges_total_stopped_time_seconds      | Gauge       | `index`, `context`         | Time spent while merge process stopped            |
| index_merges_total_throttled_time_seconds    | Gauge       | `index`, `context`         | Time spent while merging when throttling          |
| index_merges_total_auto_throttle_bytes       | Gauge       | `index`, `context`         | Bytes merged while throttling                     |
| index_refresh_total_count                    | Gauge       | `index`, `context`         | Count of refreshes                                |
| index_refresh_total_time_seconds             | Gauge       | `index`, `context`         | Time spent while refreshes                        |
| index_refresh_listeners_number               | Gauge       | `index`, `context`         | Number of refresh listeners                       |
| index_flush_total_count                      | Gauge       | `index`, `context`         | Count of flushes                                  |
| index_flush_total_time_seconds               | Gauge       | `index`, `context`         | Total time spent while flushes                    |
| index_querycache_cache_count                 | Gauge       | `index`, `context`         | Count of queries in cache                         |
| index_querycache_cache_size_bytes            | Gauge       | `index`, `context`         | Query cache size                                  |
| index_querycache_evictions_count             | Gauge       | `index`, `context`         | Count of evictions in query cache                 |
| index_querycache_hit_count                   | Gauge       | `index`, `context`         | Count of hits in query cache                      |
| index_querycache_memory_size_bytes           | Gauge       | `index`, `context`         | Memory usage of query cache                       |
| index_querycache_miss_number                 | Gauge       | `index`, `context`         | Count of misses in query cache                    |
| index_querycache_total_number                | Gauge       | `index`, `context`         | Count of usages of query cache                    |
| index_fielddata_memory_size_bytes            | Gauge       | `index`, `context`         | Memory usage of field date cache                  |
| index_fielddata_evictions_count              | Gauge       | `index`, `context`         | Count of evictions in field data cache            |
| index_completion_size_bytes                  | Gauge       | `index`, `context`         | Size of completion suggest statistics             |
| index_segments_number                        | Gauge       | `index`, `context`         | Current number of segments                        |
| index_segments_memory_bytes                  | Gauge       | `index`, `context`, `type` | Memory used by segments                           |
| index_suggest_current_number                 | Gauge       | `index`, `context`         | Current rate of suggests                          |
| index_suggest_count                          | Gauge       | `index`, `context`         | Count of suggests                                 |
| index_suggest_time_seconds                   | Gauge       | `index`, `context`         | Time spent while making suggests                  |
| index_requestcache_memory_size_bytes         | Gauge       | `index`, `context`         | Memory used for request cache                     |
| index_requestcache_hit_count                 | Gauge       | `index`, `context`         | Number of hits in request cache                   |
| index_requestcache_miss_count                | Gauge       | `index`, `context`         | Number of misses in request cache                 |
| index_requestcache_evictions_count           | Gauge       | `index`, `context`         | Number of evictions in request cache              |
| index_recovery_current_number                | Gauge       | `index`, `context`, `type` | Current number of recoveries                      |
| index_recovery_throttle_time_seconds         | Gauge       | `index`, `context`         | Time spent while throttling recoveries            |
| index_translog_operations_number             | Gauge       | `index`, `context`         | Current number of translog operations             |
| index_translog_size_bytes                    | Gauge       | `index`, `context`         | Translog size                                     |
| index_translog_uncommitted_operations_number | Gauge       | `index`, `context`         | Current number of uncommitted translog operations |
| index_translog_uncommitted_size_bytes        | Gauge       | `index`, `context`         | Translog uncommitted size                         |
| index_warmer_current_number                  | Gauge       | `index`, `context`         | Current number of warmer                          |
| index_warmer_time_seconds                    | Gauge       | `index`, `context`         | Time spent during warmers                         |
| index_warmer_count                           | Gauge       | `index`, `context`         | Counter of warmers                                |

## logstash exporter

### basic

| Metric 名称 | Metric 类型 | 标签 | 含义说明            |
| ----------- | ----------- | ---- | ------------------- |
| logstash_up | Gauge       |      | 0：未存活， 1：存活 |

### events

| Metric 名称                                   | Metric 类型 | 标签 | 含义说明 |
| --------------------------------------------- | ----------- | ---- | -------- |
| logstash_events_in                            | Gauge       |      |          |
| logstash_events_filtered                      | Gauge       |      |          |
| logstash_events_out                           | Gauge       |      |          |
| logstash_events_duration_in_millis            | Gauge       |      |          |
| logstash_events_queue_push_duration_in_millis | Gauge       |      |          |

### pipelines

- pipeline
- id
- name
- field

| Metric 名称                                                  | Metric 类型 | 标签                      | 含义说明 |
| ------------------------------------------------------------ | ----------- | ------------------------- | -------- |
| logstash_pipeline_events_duration_in_millis                  | Gauge       | pipeline                  |          |
| logstash_pipeline_events_in                                  | Gauge       | pipeline                  |          |
| logstash_pipeline_events_filtered                            | Gauge       | pipeline                  |          |
| logstash_pipeline_events_out                                 | Gauge       | pipeline                  |          |
| logstash_pipeline_events_queue_push_duration_in_millis       | Gauge       | pipeline                  |          |
| logstash_pipeline_plugins_filters_events_duration_in_millis  | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_filters_events_in                  | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_filters_events_out                 | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_filters_failures                   | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_filters_matches                    | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_filters_patterns_per_field         | Gauge       | pipeline, id, name, field |          |
| logstash_pipeline_plugins_inputs_current_connections         | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_inputs_events_out                  | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_filters_events_out                 | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_inputs_events_queue_push_duration_in_millis | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_inputs_peak_connections            | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_bulk_requests_responses_200 | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_bulk_requests_successes    | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_bulk_requests_with_errors  | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_documents_non_retryable_failures | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_documents_successes        | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_events_duration_in_millis  | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_events_in                  | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_plugins_outputs_events_out                 | Gauge       | pipeline, id, name        |          |
| logstash_pipeline_queue_capacity_max_queue_size_in_bytes     | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_capacity_max_unread_events           | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_capacity_page_capacity_in_bytes      | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_capacity_queue_size_in_bytes         | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_data_free_space_in_bytes             | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_events                               | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_events_count                         | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_max_queue_size_in_bytes              | Gauge       | pipeline                  |          |
| logstash_pipeline_queue_queue_size_in_bytes                  | Gauge       | pipeline                  |          |
| logstash_pipeline_reloads_failures                           | Gauge       | pipeline                  |          |
| logstash_pipeline_reloads_last_success_timestamp             | Gauge       | pipeline                  |          |
| logstash_pipeline_reloads_successes                          | Gauge       | pipeline                  |          |

### reloads

| Metric 名称                | Metric 类型 | 标签 | 含义说明 |
| -------------------------- | ----------- | ---- | -------- |
| logstash_reloads_failures  | Gauge       |      |          |
| logstash_reloads_successes | Gauge       |      |          |

### jvm

| Metric 名称                                                | Metric 类型 | 标签 | 含义说明 |
| ---------------------------------------------------------- | ----------- | ---- | -------- |
| logstash_jvm_gc_collectors_old_collection_count            | Gauge       |      |          |
| logstash_jvm_gc_collectors_old_collection_time_in_millis   | Gauge       |      |          |
| logstash_jvm_gc_collectors_young_collection_count          | Gauge       |      |          |
| logstash_jvm_gc_collectors_young_collection_time_in_millis | Gauge       |      |          |
| logstash_jvm_mem_heap_committed_in_bytes                   | Gauge       |      |          |
| logstash_jvm_mem_heap_max_in_bytes                         | Gauge       |      |          |
| logstash_jvm_mem_heap_used_in_bytes                        | Gauge       |      |          |
| logstash_jvm_mem_heap_used_percent                         | Gauge       |      |          |
| logstash_jvm_mem_non_heap_committed_in_bytes               | Gauge       |      |          |
| logstash_jvm_mem_non_heap_used_in_bytes                    | Gauge       |      |          |
| logstash_jvm_mem_pools_old_committed_in_bytes              | Gauge       |      |          |
| logstash_jvm_mem_pools_old_max_in_bytes                    | Gauge       |      |          |
| logstash_jvm_mem_pools_old_peak_max_in_bytes               | Gauge       |      |          |
| logstash_jvm_mem_pools_old_peak_used_in_bytes              | Gauge       |      |          |
| logstash_jvm_mem_pools_old_used_in_bytes                   | Gauge       |      |          |
| logstash_jvm_mem_pools_survivor_committed_in_bytes         | Gauge       |      |          |
| logstash_jvm_mem_pools_survivor_max_in_bytes               | Gauge       |      |          |
| logstash_jvm_mem_pools_survivor_peak_max_in_bytes          | Gauge       |      |          |
| logstash_jvm_mem_pools_survivor_peak_used_in_bytes         | Gauge       |      |          |
| logstash_jvm_mem_pools_survivor_used_in_bytes              | Gauge       |      |          |
| logstash_jvm_mem_pools_young_committed_in_bytes            | Gauge       |      |          |
| logstash_jvm_mem_pools_young_max_in_bytes                  | Gauge       |      |          |
| logstash_jvm_mem_pools_young_peak_max_in_bytes             | Gauge       |      |          |
| logstash_jvm_mem_pools_young_peak_used_in_bytes            | Gauge       |      |          |
| logstash_jvm_mem_pools_young_used_in_bytes                 | Gauge       |      |          |
| logstash_jvm_threads_count                                 | Gauge       |      |          |
| logstash_jvm_threads_peak_count                            | Gauge       |      |          |
| logstash_jvm_uptime_in_millis                              | Gauge       |      |          |

### process

| Metric 名称                                 | Metric 类型 | 标签 | 含义说明 |
| ------------------------------------------- | ----------- | ---- | -------- |
| logstash_process_cpu_load_average_15m       | Gauge       |      |          |
| logstash_process_cpu_load_average_1m        | Gauge       |      |          |
| logstash_process_cpu_load_average_5m        | Gauge       |      |          |
| logstash_process_cpu_percent                | Gauge       |      |          |
| logstash_process_cpu_total_in_millis        | Gauge       |      |          |
| logstash_process_max_file_descriptors       | Gauge       |      |          |
| logstash_process_mem_total_virtual_in_bytes | Gauge       |      |          |
| logstash_process_open_file_descriptors      | Gauge       |      |          |
| logstash_process_peak_open_file_descriptors | Gauge       |      |          |

### logstash-exporter

#### process

| Metric 名称                   | Metric 类型 | 标签 | 含义说明 |
| ----------------------------- | ----------- | ---- | -------- |
| process_cpu_seconds_total     | Gauge       |      |          |
| process_max_fds               | Gauge       |      |          |
| process_open_fds              | Gauge       |      |          |
| process_resident_memory_bytes | Gauge       |      |          |
| process_start_time_seconds    | Gauge       |      |          |
| process_virtual_memory_bytes  | Gauge       |      |          |

#### go

| Metric 名称                           | Metric 类型 | 标签     | 含义说明 |
| ------------------------------------- | ----------- | -------- | -------- |
| go_gc_duration_seconds                | summary     | quantile |          |
| go_gc_duration_seconds_sum            | summary     |          |          |
| go_gc_duration_seconds_count          | summary     |          |          |
| go_goroutines                         | gauge       |          |          |
| go_memstats_alloc_bytes               | gauge       |          |          |
| go_memstats_alloc_bytes_total         | counter     |          |          |
| go_memstats_buck_hash_sys_bytes       | gauge       |          |          |
| go_memstats_frees_total               | counter     |          |          |
| go_memstats_gc_sys_bytes              | gauge       |          |          |
| go_memstats_heap_alloc_bytes          | gauge       |          |          |
| go_memstats_heap_idle_bytes           | gauge       |          |          |
| go_memstats_heap_inuse_bytes          | gauge       |          |          |
| go_memstats_heap_objects              | gauge       |          |          |
| go_memstats_heap_released_bytes_total | counter     |          |          |
| go_memstats_heap_sys_bytes            | gauge       |          |          |
| go_memstats_last_gc_time_seconds      | gauge       |          |          |
| go_memstats_lookups_total             | counter     |          |          |
| go_memstats_mallocs_total             | counter     |          |          |
| go_memstats_mcache_inuse_bytes        | gauge       |          |          |
| go_memstats_mcache_sys_bytes          | gauge       |          |          |
| go_memstats_mspan_inuse_bytes         | gauge       |          |          |
| go_memstats_mspan_sys_bytes           | gauge       |          |          |
| go_memstats_next_gc_bytes             | gauge       |          |          |
| go_memstats_other_sys_bytes           | gauge       |          |          |
| go_memstats_stack_inuse_bytes         | gauge       |          |          |
| go_memstats_stack_sys_bytes           | gauge       |          |          |
| go_memstats_sys_bytes                 | gauge       |          |          |

## prometheus metrics

### dialer

- 标签
  - dialer_name: 取值`prometheus配置中设置的job_name对应的值`
  - reason: 取值`refused | resolution | timeout | unknown`，连接失败的原因
  - listener_name: 取值`http`，监听端口名称

| Metric name                                 | Metric type | Labels/tags            | 说明                              |
| ------------------------------------------- | ----------- | ---------------------- | --------------------------------- |
| net_conntrack_dialer_conn_attempted_total   | Counter     | `dialer_name`          | job中的target尝试的连接总次数     |
| net_conntrack_dialer_conn_closed_total      | Counter     | `dialer_name`          | job中的target已关闭连接的总次数   |
| net_conntrack_dialer_conn_established_total | Counter     | `dialer_name`          | job中的target建立的连接成功总次数 |
| net_conntrack_dialer_conn_failed_total      | Counter     | `dialer_name`,`reason` | job中的target建立的连接失败总次数 |
| net_conntrack_listener_conn_accepted_total  | Counter     | `listener_name`        | 监听端口(9090)的连接总次数        |
| net_conntrack_listener_conn_closed_total    | Counter     | `listener_name`        | 对给定名称的侦听器关闭的连接总数  |

### remote_read

| Metric name                        | Metric type | Labels/tags | 说明                                 |
| ---------------------------------- | ----------- | ----------- | ------------------------------------ |
| prometheus_api_remote_read_queries | Gauge       |             | 当前正在执行或等待的远程读查询的数量 |

### build

| Metric name           | Metric type | Labels/tags                               | 说明                                 |
| --------------------- | ----------- | ----------------------------------------- | ------------------------------------ |
| prometheus_build_info | Gauge       | `branch`,`goversion`,`revision`,`version` | 标签包含此版本prometheus构建相关信息 |

### config_reloader

| Metric name                                             | Metric type | Labels/tags | 说明                             |
| ------------------------------------------------------- | ----------- | ----------- | -------------------------------- |
| prometheus_config_last_reload_success_timestamp_seconds | Gauge       |             | 最后一次成功重新加载配置的时间戳 |
| prometheus_config_last_reload_successful                | Gauge       |             | 最后一次配置重新加载尝试是否成功 |

### engine_query

- 标签
  - slice: 取值`inner_eval | prepare_time | queue_time | result_sort`，表示查询操作内不同步骤的耗时时间
  - quantile: 取值`0.5 | 0.9 | 0.99`，分表代表不同分位数

| Metric name                              | Metric type | Labels/tags        | 说明                             |
| ---------------------------------------- | ----------- | ------------------ | -------------------------------- |
| prometheus_engine_queries                | Gauge       |                    | 当前正在执行查询或等待查询的数量 |
| prometheus_engine_queries_concurrent_max | Gauge       |                    | 并发查询的最大数量               |
| prometheus_engine_query_duration_seconds | Summary     | `slice`,`quantile` | 查询耗时分位数                   |

### http

- 标签
  - handler: 取值`访问路径`，如`/ | /-/reload | /alerts`等
  - le
    - prometheus_http_request_duration_seconds: 取值`0.1 | 0.2 | 0.4 | 1 | 3 | 8 | 20 | 60 | 120 | +Inf`
    - prometheus_http_response_size_bytes: 取值`100 | 1000 | 10000 | 100000 | 1e+06 | 1e+07 | 1e+08 | 1e+09 | +Inf`

| Metric name                              | Metric type | Labels/tags    | 说明               |
| ---------------------------------------- | ----------- | -------------- | ------------------ |
| prometheus_http_request_duration_seconds | Histogram   | `handler`,`le` | http接口请求耗时   |
| prometheus_http_response_size_bytes      | Histogram   | `handler`,`le` | http接口响应包大小 |

### notifications

- 标签
  - alertmanager: 取值`http://<alertmanager>/api/v1/alerts`
  - quantile: 取值`0.5 | 0.9 | 0.99`

| Metric name                                       | Metric type | Labels/tags               | 说明                                         |
| ------------------------------------------------- | ----------- | ------------------------- | -------------------------------------------- |
| prometheus_notifications_alertmanagers_discovered | Gauge       |                           | 已发现并处于活动状态的alertmanager的数量     |
| prometheus_notifications_dropped_total            | Counter     |                           | 发送到Alertmanager时由于错误而删除的警报总数 |
| prometheus_notifications_queue_capacity           | Gauge       |                           | 警报通知队列的容量，默认10k                  |
| prometheus_notifications_queue_length             | Gauge       |                           | 队列中的警报通知数                           |
| prometheus_notifications_errors_total             | Counter     | `alertmanager`            | 通知错误总量                                 |
| prometheus_notifications_latency_seconds          | Summary     | `alertmanager`,`quantile` | 通知发送延时                                 |
| prometheus_notifications_sent_total               | Counter     | `alertmanager`            | 通知发送总量                                 |

### remote_storage

| Metric name                                                  | Metric type | Labels/tags | 说明                                                         |
| ------------------------------------------------------------ | ----------- | ----------- | ------------------------------------------------------------ |
| prometheus_remote_storage_highest_timestamp_in_seconds       | Gauge       |             | 通过Appender接口进入远程存储的最高时间戳                     |
| prometheus_remote_storage_samples_in_total                   | Counter     |             | 在远程存储中的样本数量                                       |
| prometheus_remote_storage_string_interner_zero_reference_releases_total | Counter     |             | The number of times release has been called for strings that are not interned |

### rule

- 标签
  - quantile: 取值`0.5 | 0.9 | 0.99`，分表代表不同分位数
  - rule_group: 取值`prometheus配置中的规则组名称`

| Metric name                                             | Metric type | Labels/tags  | 说明                                 |
| ------------------------------------------------------- | ----------- | ------------ | ------------------------------------ |
| prometheus_rule_evaluation_duration_seconds             | Summary     | `quantile`   | 规则评估持续延时分位数               |
| prometheus_rule_evaluation_failures_total               | Counter     |              | 规则评估失败的总数                   |
| prometheus_rule_evaluations_total                       | Counter     |              | 规则评估的总数                       |
| prometheus_rule_group_duration_seconds                  | Summary     | `quantile`   | 规则组评估持续延时分位数             |
| prometheus_rule_group_interval_seconds                  | Gauge       | `rule_group` | 规则组的汇聚间隔时间                 |
| prometheus_rule_group_iterations_missed_total           | Counter     |              | 在规则组汇聚间隔时间内消失的告警数量 |
| prometheus_rule_group_iterations_total                  | Counter     |              | 规则组评估的总次数                   |
| prometheus_rule_group_last_duration_seconds             | Gauge       | `rule_group` | 上次规则组评估的持续时间             |
| prometheus_rule_group_last_evaluation_timestamp_seconds | Gauge       | `rule_group` | 上次规则组计算的时间戳               |
| prometheus_rule_group_rules                             | Gauge       | `rule_group` | 规则的数量                           |

### sd

- 标签
  - call: 取值`调用的服务名称`
  - endpoint: 取值`端点名称`
  - quantile: 取值`0.5 | 0.9 | 0.99`，分表代表不同分位数
  - rule_group: 取值`prometheus配置中的规则组名称`

| Metric name                                           | Metric type | Labels/tags                  | 说明                                |
| ----------------------------------------------------- | ----------- | ---------------------------- | ----------------------------------- |
| prometheus_sd_consul_rpc_duration_seconds             | Summary     | `call`,`endpoint`,`quantile` | consul RPC调用延时分位数            |
| prometheus_sd_consul_rpc_failures_total               | Counter     |                              | consul RPC调用失败次数              |
| prometheus_sd_discovered_targets                      | Gauge       |                              | 当前发现的target数量                |
| prometheus_sd_dns_lookup_failures_total               | Counter     | `quantile`                   | DNS-SD查询失败的次数                |
| prometheus_sd_dns_lookups_total                       | Counter     |                              | DNS-SD查询总次数                    |
| prometheus_sd_file_mtime_seconds                      | Gauge       |                              | 读取sd文件的时间戳                  |
| prometheus_sd_file_read_errors_total                  | Counter     |                              | 读取sd文件错误次数                  |
| prometheus_sd_file_scan_duration_seconds              | Summary     | `quantile`                   | sd文件扫描的持续时间                |
| prometheus_sd_kubernetes_cache_last_resource_version  | Gauge       |                              | sd Kubernetes API的最后一个资源版本 |
| prometheus_sd_kubernetes_cache_list_duration_seconds  | Gauge       |                              | sd Kubernetes API调用的持续时间     |
| prometheus_sd_kubernetes_cache_list_items             | Summary     |                              | sd Kubernetes API中列表项的计数     |
| prometheus_sd_kubernetes_cache_list_total             | Counter     |                              | sd 列表操作的总数                   |
| prometheus_sd_kubernetes_cache_short_watches_total    | Counter     |                              | 短时间watch次数                     |
| prometheus_sd_kubernetes_cache_watch_duration_seconds | Summary     |                              | watch持续时间                       |
| prometheus_sd_kubernetes_cache_watch_events           | Summary     |                              | API上监视中的项数                   |
| prometheus_sd_kubernetes_cache_watches_total          | Counter     |                              | watch操作的总数                     |
| prometheus_sd_kubernetes_events_total                 | Counter     |                              | 处理的Kubernetes事件的数量          |
| prometheus_sd_received_updates_total                  | Counter     |                              | 从SD提供程序接收的更新事件总数      |
| prometheus_sd_updates_total                           | Counter     |                              | 发送给SD使用者的更新事件总数        |

### target

- 标签
  - interval: 取值`prometheus配置中设置的采集间隔`，比如15s、30s等
  - quantile: 取值`0.01 | 0.05 | 0.5 | 0.9 | 0.99`，分表代表不同分位数
  - scrape_job: 取值`prometheus配置中设置的job_name对应的值`

| Metric name                                                | Metric type | Labels/tags           | 说明                                             |
| ---------------------------------------------------------- | ----------- | --------------------- | ------------------------------------------------ |
| prometheus_target_interval_length_seconds                  | Summary     | `interval`,`quantile` | 采集实际间隔时间                                 |
| prometheus_target_scrape_pool_reloads_failed_total         | Counter     |                       | 采集池重新加载失败的总次数                       |
| prometheus_target_scrape_pool_reloads_total                | Counter     |                       | 采集池重新加载的总次数                           |
| prometheus_target_scrape_pool_sync_total                   | Counter     | `scrape_job`          | 采集池中被执行同步操作的总次数                   |
| prometheus_target_scrape_pools_failed_total                | Counter     |                       | 创建采集池失败总次数                             |
| prometheus_target_scrape_pools_total                       | Counter     |                       | 创建采集池总尝试次数                             |
| prometheus_target_scrapes_sample_duplicate_timestamp_total | Counter     |                       | 由于时间戳重复但值不同而被拒绝的样本数量         |
| prometheus_target_scrapes_sample_out_of_bounds_total       | Counter     |                       | 由于时间戳超出时间范围而被拒绝的样本总数         |
| prometheus_target_scrapes_sample_out_of_order_total        | Counter     |                       | 由于没有超出预期值而被拒收的样品总数             |
| prometheus_target_sync_length_seconds                      | Summary     |                       | 采集池同步实际时间间隔                           |
| prometheus_target_scrapes_cache_flush_forced_total         | Counter     |                       | 当采集失败时，采集缓存因为变得大而被刷新了多少次 |

### tsdb

- 标签
  - le:
    - prometheus_tsdb_compaction_chunk_range_seconds: 取值`100 | 400 | 1600 | 6400 | ... | 2.62144e+07 | +Inf`
    - prometheus_tsdb_compaction_chunk_samples: 取值`4 | 6 | 9 | 13.5 | 20.25 | 30.375 | ... | 345.990234375 | +Inf`
    - prometheus_tsdb_compaction_duration_seconds: 取值`1 | 2 | 4 | 8 | ... | 512 | +Inf`
    - prometheus_tsdb_tombstone_cleanup_seconds: 取值`0.005 | 0.01 | 0.025 | 0.05 | 0.1 | 0.25 | 0.5 | 1 | 2.5 | 5 | 10 | +Inf`
  - quantile: 取值`0.5 | 0.9 | 0.99`

| Metric name                                       | Metric type | Labels/tags  | 说明                                                         |
| ------------------------------------------------- | ----------- | ------------ | ------------------------------------------------------------ |
| prometheus_tsdb_blocks_loaded                     | Gauge       |              | tsdb当前加载的数据块的数量                                   |
| prometheus_tsdb_checkpoint_creations_failed_total | Counter     |              | tsdb创建检查点失败的总数                                     |
| prometheus_tsdb_checkpoint_creations_total        | Counter     |              | tsdb创建检查点的总数                                         |
| prometheus_tsdb_checkpoint_deletions_failed_total | Counter     | `scrape_job` | tsdb创建检查点失败的总数                                     |
| prometheus_tsdb_checkpoint_deletions_total        | Counter     |              | tsdb删除检查点的总数                                         |
| prometheus_tsdb_compaction_chunk_range_seconds    | Histogram   | `le`         | tsdb块第一次压缩时的最终时间范围                             |
| prometheus_tsdb_compaction_chunk_samples          | Histogram   | `le`         | tsdb第一次压实的最终样品数                                   |
| prometheus_tsdb_compaction_chunk_size_bytes       | Histogram   | `le`         | tsdb第一次压缩时块的最终大小                                 |
| prometheus_tsdb_compaction_duration_seconds       | Histogram   | `le`         | tsdb压缩运行持续时间                                         |
| prometheus_tsdb_compaction_populating_block       | Gauge       |              | tsdb块是否正在写入磁盘，当块正在写入磁盘时，设置为1          |
| prometheus_tsdb_compactions_failed_total          | Counter     |              | tsdb对分区失败的压缩的总数                                   |
| prometheus_tsdb_compactions_total                 | Counter     |              | tsdb为分区执行的压缩总数                                     |
| prometheus_tsdb_compactions_triggered_total       | Counter     |              | tsdb为分区触发的压缩总数                                     |
| prometheus_tsdb_head_active_appenders             | Gauge       |              | tsdb当前活动的appender事务数                                 |
| prometheus_tsdb_head_chunks                       | Gauge       |              | tsdb在头块(in-memory，数据prometheus内存中1-3小时的数据，每2小时将数据刷到磁盘中。在头块中，我们以压缩块的形式存储样本;每个块由多达120个样本组成，当我们创建一个新的块时，旧的块就被称为“满了”。[链接](https://grafana.com/blog/2020/06/10/new-in-prometheus-v2.19.0-memory-mapping-of-full-chunks-of-the-head-block-reduces-memory-usage-by-as-much-as-40/))中的块的数量。dashboard展示 |
| prometheus_tsdb_head_chunks_created_total         | Counter     |              | tsdb在头块中创建的块的总数                                   |
| prometheus_tsdb_head_chunks_removed_total         | Counter     |              | tsdb在头块移除的块的总数                                     |
| prometheus_tsdb_head_gc_duration_seconds          | Summary     | `quantile`   | tsdb在头块中进行垃圾收集的运行时间                           |
| prometheus_tsdb_head_max_time                     | Gauge       |              | tsdb头块的最大时间戳。单位由库的使用者决定                   |
| prometheus_tsdb_head_max_time_seconds             | Gauge       |              | tsdb头块的最大时间戳                                         |
| prometheus_tsdb_head_min_time                     | Gauge       |              | tsdb头块的最小时间戳。单位由库的使用者决定                   |
| prometheus_tsdb_head_min_time_seconds             | Gauge       |              | tsdb头块的最小时间戳                                         |
| prometheus_tsdb_head_samples_appended_total       | Counter     |              | tsdb附加样本总数。rate计算append样本速率                     |
| prometheus_tsdb_head_series                       | Gauge       |              | tsdb头块中的时间序列总数。dashboard展示                      |
| prometheus_tsdb_head_series_created_total         | Counter     |              | tsdb头块中的时间序列创建总数                                 |
| prometheus_tsdb_head_series_not_found_total       | Counter     |              | tsdb头块中未找到的时间序列请求的总数                         |
| prometheus_tsdb_head_series_removed_total         | Counter     |              | tsdb在头块移除的时间序列总数                                 |
| prometheus_tsdb_head_truncations_failed_total     | Counter     |              | tsdb头块截断失败的总数                                       |
| prometheus_tsdb_head_truncations_total            | Counter     |              | tsdb头块截断的总数                                           |
| prometheus_tsdb_lowest_timestamp                  | Gauge       |              | tsdb数据库中存储的最低时间戳值。单位由库的使用者决定         |
| prometheus_tsdb_lowest_timestamp_seconds          | Gauge       |              | tsdb数据库中存储的最低时间戳值                               |
| prometheus_tsdb_reloads_failures_total            | Counter     |              | tsdb数据库从磁盘重新加载块数据失败的次数                     |
| prometheus_tsdb_reloads_total                     | Counter     |              | tsdb数据库从磁盘重新加载块数据的次数                         |
| prometheus_tsdb_size_retentions_total             | Counter     |              | tsdb由于超过最大字节数而删除块的次数                         |
| prometheus_tsdb_storage_blocks_bytes              | Gauge       |              | tsdb当前所有块用于本地存储的字节数                           |
| prometheus_tsdb_symbol_table_size_bytes           | Gauge       |              | tsdb磁盘上符号表(symbol table 就是键值对)的大小              |
| prometheus_tsdb_time_retentions_total             | Counter     |              | tsdb由于超过最大时间限制而删除块的次数                       |
| prometheus_tsdb_tombstone_cleanup_seconds         | Histogram   | `le`         | The time taken to recompact block to remove tombstones       |
| prometheus_tsdb_vertical_compactions_total        | Counter     |              | tsdb对重叠块进行压缩的总数                                   |
| prometheus_tsdb_wal_completed_pages_total         | Counter     |              | tsdb wal 完成页面的总数                                      |
| prometheus_tsdb_wal_corruptions_total             | Counter     |              | tsdb wal 数据损坏的总数                                      |
| prometheus_tsdb_wal_fsync_duration_seconds        | Summary     | `quantile`   | tsdb wal 同步用时，summary类型                               |
| prometheus_tsdb_wal_page_flushes_total            | Counter     |              | tsdb wal 刷新页面的总数                                      |
| prometheus_tsdb_wal_segment_current               | Gauge       |              | tsdb当前写入的WAL段索引                                      |
| prometheus_tsdb_wal_truncate_duration_seconds     | Summary     | `quantile`   | tsdb wal截断用时                                             |
| prometheus_tsdb_wal_truncations_failed_total      | Counter     |              | tsdb 失败的WAL截断总数                                       |
| prometheus_tsdb_wal_truncations_total             | Counter     |              | tsdb wal试图截断的总数                                       |

### metric_handler

- 标签
  - code: 取值`http状态码`，如200、404、500等

| Metric name                                | Metric type | Labels/tags | 说明                         |
| ------------------------------------------ | ----------- | ----------- | ---------------------------- |
| promhttp_metric_handler_requests_in_flight | Gauge       |             | 目前服务的采集数量           |
| promhttp_metric_handler_requests_total     | Counter     | `code`      | 按HTTP状态代码计算的抓取总数 |

### scrape

| Metric name                           | Metric type | Labels/tags      | 说明                                                         |
| ------------------------------------- | ----------- | ---------------- | ------------------------------------------------------------ |
| scrape_duration_seconds               | Gauge       | `job`,`instance` | scrape耗时                                                   |
| scrape_samples_scraped                | Gauge       | `job`,`instance` | 目标暴露的样本数                                             |
| scrape_series_added                   | Gauge       | `job`,`instance` | 新时间序列大概数量                                           |
| up                                    | Gauge       | `job`,`instance` | 目标健康状态                                                 |
| scrape_samples_post_metric_relabeling | Gauge       | `job`,`instance` | the number of samples remaining after metric relabeling was applied |

### treecache

| Metric name                                       | Metric type | Labels/tags | 说明                     |
| ------------------------------------------------- | ----------- | ----------- | ------------------------ |
| prometheus_treecache_watcher_goroutines           | Gauge       |             | 当前监视goroutines的数量 |
| prometheus_treecache_zookeeper_failures_total     | Counter     |             | ZooKeeper失败的总数      |
| prometheus_template_text_expansion_failures_total | Counter     |             | 模板文本扩展失败的总数   |

### grpc

- 标签
  - grpc_code: 取值`Aborted | AlreadyExists | Canceled | DataLoss | DeadlineExceeded | FailedPrecondition | Internal | InvalidArgument | NotFound | OK | OutOfRange | PermissionDenied | ResourceExhausted | Unauthenticated | Unavailable | Unimplemented | Unknown`
  - grpc_method:
  - grpc_service:
  - grpc_type:
  - le: 取值`0.001 | 0.01 | 0.1 | 0.3 | 0.6 | 1 | 3 | ... | 120 | +Inf`

| Metric name                    | Metric type | Labels/tags                                               | 说明                                             |
| ------------------------------ | ----------- | --------------------------------------------------------- | ------------------------------------------------ |
| grpc_server_handled_total      | Counter     | `grpc_code`,`grpc_method`,`grpc_service`,`grpc_type`      | 服务器上完成的rpc总数，无论成功还是失败          |
| grpc_server_handling_seconds   | Histogram   | `grpc_code`,`grpc_method`,`grpc_service`,`grpc_type`,`le` | 服务器在应用程序级处理的gRPC的响应延迟(秒)直方图 |
| grpc_server_msg_received_total | Counter     | `grpc_method`,`grpc_service`,`grpc_type`                  | 服务器上接收的RPC流消息总数                      |
| grpc_server_msg_sent_total     | Counter     | `grpc_method`,`grpc_service`,`grpc_type`                  | 服务器上发送的RPC流消息总数                      |
| grpc_server_started_total      | Counter     | `grpc_method`,`grpc_service`,`grpc_type`                  | 服务器上启动的rpc总数                            |
