
```yaml
#test-rules.yaml
rule_files:
    - ../test_prometheus_rules/k8s/alert-rules.yaml

evaluation_interval: 30s # 触发告警检测的时间（默认一分钟）[应小于等于for]

group_eval_order: # 下面列出的组名的顺序将是规则组的执行顺序(在给定的执行时间内)。仅针对以下提及的组保证顺序。不需要体积所有组
    - sfu-mc
    
# 所有测试均在此处列出
tests:
    - interval: 30s # 采集时间间隔，采集values的总时间(4*30s)需要大于等于eval_time
      # 所测试的metric
      input_series:
          - series: 'yl_sfu_mc_sdk_requests_total{job="test", namespace="test", app="test"}'
            values: '0 0 0 0 1'  # 最后一个值延续五分钟

      # 对上述数据进行单元测试。告警规则的单元测试。我们考虑输入文件中的告警规则
      alert_rule_test:
          - eval_time: 1m30s # 检查告警的时间间隔(从0s开始),如果alert_rules中表达式包含时间（例如：[1m]），则需要从第二个数据点开始计算，即（eval_time > for + evaluation_interval）否则（eval_time = for）。
            alertname: sfu mc终端请求速率tps大于300持续1min
            exp_alerts:
               - exp_labels:
                      severity: 2
                      job: test
                      namespace: test
                      app: test
                 exp_annotations:
                      help_url: about:blank
                      message: 终端请求速率tps大于300持续1min    
```

```yaml
#alert-rules.yaml
groups:
- name: sfu-mc
  rules:
  - alert: sfu mc终端请求速率tps大于300持续1min
    annotations:
      help_url: about:blank
      message: 终端请求速率tps大于300持续1min
    expr: |
      sum(rate(yl_sfu_mc_sdk_requests_total[1m])) by (job, namespace, app)
      == 0 
    for: 1m  # 评估等待时间，可选参数。用于表示只有当触发条件持续一段时间后才发送告警。在等待期间新产生告警的状态为pending。
    labels: 
      severity: "2"
```

