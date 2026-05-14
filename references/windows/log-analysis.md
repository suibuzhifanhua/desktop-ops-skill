# 日志查看 & 错误分析参考

## Windows 事件查看器

```powershell
# 查看最近 50 条系统错误
Get-EventLog -LogName System -EntryType Error -Newest 50 | Select-Object TimeGenerated, Source, EventID, Message | Format-Table -AutoSize

# 查看应用程序崩溃
Get-EventLog -LogName Application -EntryType Error -Newest 30 | Where-Object {$_.Source -like "*fault*" -or $_.EventID -eq 1000}

# 按时间范围查询
Get-EventLog -LogName System -After (Get-Date).AddHours(-24) -EntryType Error,Warning

# 使用 Get-WinEvent（更强大，支持过滤）
Get-WinEvent -FilterHashtable @{LogName='System'; Level=2; StartTime=(Get-Date).AddHours(-1)}

# 导出日志
Get-EventLog -LogName System -Newest 100 | Export-Csv C:\Temp\system_log.csv -NoTypeInformation
```

### 常见重要 Event ID

| Event ID | 来源 | 含义 |
|----------|------|------|
| 1000 | Application Error | 应用程序崩溃 |
| 1001 | Windows Error Reporting | 崩溃报告 |
| 6008 | EventLog | 意外关机 |
| 41 | Kernel-Power | 意外重启（内核崩溃） |
| 4625 | Security | 登录失败 |
| 7034 | Service Control Manager | 服务意外终止 |
| 7031 | Service Control Manager | 服务崩溃并重启 |

---

## BSOD 蓝屏分析

```powershell
# 查看最近蓝屏信息
Get-EventLog -LogName System -Source "BugCheck" -Newest 5

# 蓝屏转储文件位置
# 小内存转储：C:\Windows\Minidump\
# 完整转储：C:\Windows\MEMORY.DMP

# 用 WinDbg 分析（[下载 WinDbg Preview（Microsoft Store）](https://apps.microsoft.com/detail/9PGJGD53TN86) 或搜索"WinDbg"安装）
# windbg -z C:\Windows\Minidump\xxxx.dmp
# !analyze -v

# 在线分析工具：[WhoCrashed](https://www.resplendence.com/whocrashed)（推荐）
```

常见蓝屏代码：

| 代码 | 原因 |
|------|------|
| IRQL_NOT_LESS_OR_EQUAL | 驱动内存访问错误 |
| MEMORY_MANAGEMENT | 内存硬件故障 |
| SYSTEM_SERVICE_EXCEPTION | 系统驱动异常 |
| DRIVER_IRQL_NOT_LESS_OR_EQUAL | 驱动问题（看错误参数中的驱动名） |
| CRITICAL_PROCESS_DIED | 关键系统进程崩溃 |
| PAGE_FAULT_IN_NONPAGED_AREA | 内存/驱动问题 |

---

## 应用日志路径速查

| 应用 | 日志位置 |
|------|---------|
| Windows 系统 | `C:\Windows\Logs\` |
| IIS | `C:\inetpub\logs\LogFiles\` |
| SQL Server | SSMS → 管理 → SQL Server 日志 |
| Docker Desktop | `%APPDATA%\Docker\log.txt` |
| WSL2 | `%LOCALAPPDATA%\Packages\...` |
| Python 应用 | 按 logging 配置，通常在项目目录 |
| Node.js / PM2 | `~/.pm2/logs/` |
| Nginx (Linux) | `/var/log/nginx/error.log` |
| Apache (Linux) | `/var/log/apache2/error.log` |

---

## Linux 日志工具

```bash
# systemd journal（现代发行版）
journalctl -xe                          # 最近错误（详细）
journalctl -u nginx --since "1 hour ago"  # 指定服务日志
journalctl -b -1                        # 上次启动的日志
journalctl --disk-usage                 # 日志磁盘占用

# 传统 syslog
tail -f /var/log/syslog
grep -i error /var/log/syslog | tail -50

# 内核日志
dmesg | tail -50
dmesg | grep -i "error\|fail\|warn" | tail -20
```

---

## 日志分析技巧

1. **先看时间**：错误发生时间是否与用户反馈一致
2. **找 CRITICAL/ERROR 级别**：过滤低级别噪音
3. **关联上下文**：错误前后 5 行通常有根因
4. **搜索 Event ID**：直接搜 `Windows Event ID XXXX` 找解决方案
5. **循环错误**：同一错误反复出现 → 未修复的根本问题
