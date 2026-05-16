# 网络诊断参考

## 基础连通性检测

```powershell
# Windows
ping 8.8.8.8 -n 4          # 基础连通
tracert 8.8.8.8             # 路由追踪
pathping 8.8.8.8            # 延迟+丢包综合分析
Test-NetConnection -ComputerName github.com -Port 443  # 端口测试
nslookup github.com         # DNS 解析
```

```bash
# macOS / Linux
ping -c 4 8.8.8.8
traceroute 8.8.8.8
dig github.com
nc -zv github.com 443       # 端口测试
curl -I https://github.com  # HTTP 连通
```

---

## DNS 问题排查

```powershell
# Windows：刷新 DNS 缓存
ipconfig /flushdns

# 查看当前 DNS 服务器
Get-DnsClientServerAddress

# 临时改 DNS（国内推荐：114.114.114.114 / 腾讯 119.29.29.29 / 阿里 223.5.5.5）
Set-DnsClientServerAddress -InterfaceAlias "以太网" -ServerAddresses 114.114.114.114,8.8.8.8
```

```bash
# Linux
sudo systemd-resolve --flush-caches
cat /etc/resolv.conf
```

---

## IP / 路由配置

```powershell
# Windows 查看所有网卡信息
ipconfig /all
Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4"}

# 路由表
route print
netstat -r

# 重置网络（⚠️ 会重置 Winsock 和 TCP/IP 栈）
netsh winsock reset
netsh int ip reset
ipconfig /release && ipconfig /renew
```

---

## 代理配置

```powershell
# Windows 查看当前代理
netsh winhttp show proxy

# 设置代理
netsh winhttp set proxy 127.0.0.1:7890

# 取消代理
netsh winhttp reset proxy

# 环境变量方式（适合命令行工具）
$env:http_proxy = "http://127.0.0.1:7890"
$env:https_proxy = "http://127.0.0.1:7890"
```

```bash
# Linux/macOS
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export no_proxy=localhost,127.0.0.1
```

---

## 防火墙排查

```powershell
# Windows：查看防火墙状态
Get-NetFirewallProfile | Select-Object Name, Enabled

# 测试特定端口是否被防火墙拦截
Test-NetConnection -ComputerName localhost -Port 3000

# 临时关闭防火墙（排查用，⚠️ 排查后记得开启）
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# 添加入站规则
New-NetFirewallRule -DisplayName "Allow Port 3000" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow
```

---

## 常见网络错误速查

| 错误 | 可能原因 | 处理方式 |
|------|---------|---------|
| DNS 解析失败 | DNS 服务器不通 / 缓存问题 | `ipconfig /flushdns`，换 DNS |
| 连接超时 | 防火墙/代理/路由问题 | `tracert` 定位断点 |
| SSL 证书错误 | 系统时间不对 / 证书过期 | 同步时间，检查证书 |
| 端口不通 | 防火墙拦截 / 服务未启动 | `Test-NetConnection` 确认 |
| 网速慢 | 带宽占用 / QoS / DNS 慢 | `netstat -b` 查带宽占用进程 |

---

## 电脑有网但显示无法连接网络（NCSI 修复）

> 来源：[Fisheep的新世界](https://fisheep.fun/yummy/100)

电脑实际上有网络连接，但系统却显示"无法连接网络"。这是 Windows NLA（Network Location Awareness）服务的 NCSI 检测配置异常导致的。

**修复方法**：新建 `.reg` 文件，写入以下内容后双击导入：

```reg
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet]
"ActiveDnsProbeContent"="131.107.255.255"
"ActiveDnsProbeContentV6"="fd3e:4f5a:5b81::1"
"ActiveDnsProbeHost"="dns.msftncsi.com"
"ActiveDnsProbeHostV6"="dns.msftncsi.com"
"ActiveWebProbeContent"="Microsoft NCSI"
"ActiveWebProbeContentV6"="Microsoft NCSI"
"ActiveWebProbeHost"="www.msftncsi.com"
"ActiveWebProbeHostV6"="ipv6.msftncsi.com"
"ActiveWebProbePath"="ncsi.txt"
"ActiveWebProbePathV6"="ncsi.txt"
"CaptivePortalTimer"=dword:00000000
"CaptivePortalTimerBackOffIncrementsInSeconds"=dword:00000005
"CaptivePortalTimerMaxInSeconds"=dword:0000001e
"EnableActiveProbing"=dword:00000001
"PassivePollPeriod"=dword:0000000f
"StaleThreshold"=dword:0000001e
"WebTimeout"=dword:00000023

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet\ManualProxies]
```

导入后**重启电脑**生效。此脚本将 NCSI 参数恢复为微软默认值，修复网络状态误判。

---

## 解决网络拥塞问题（TCP 拥塞控制算法调优）

> 适用于网络延迟高、带宽跑不满、视频卡顿等拥塞场景。

### 方法一：PowerShell（推荐）

```powershell
# 以管理员身份运行 PowerShell

# 查看当前所有 TCP 配置模板
Get-NetTCPSetting

# 查看当前拥塞控制算法
Get-NetTCPSetting | Select-Object SettingName, CongestionProvider

# 设置为 CTCP（适用于 Internet 模板）
Set-NetTCPSetting -SettingName "InternetCustom" -CongestionProvider CTCP

# 或者设置 DatacenterCustom 模板（内网/高速链路）
Set-NetTCPSetting -SettingName "DatacenterCustom" -CongestionProvider CTCP
```

### 方法二：netsh 新语法

```cmd
# 以管理员身份运行 CMD

# 查看当前 supplemental 配置
netsh int tcp show supplemental

# 设置 Internet 模板的拥塞算法
netsh int tcp set supplemental template=internet congestionprovider=ctcp
```

### 可用的 CongestionProvider 值

| 值 | 说明 |
|---|---|
| `CTCP` | 复合 TCP，高带宽延迟场景较好 |
| `DCTCP` | 数据中心 TCP，低延迟内网 |
| `default` | 恢复默认（CUBIC） |
| `None` | 不使用拥塞控制扩展 |

### 验证是否生效

```powershell
Get-NetTCPSetting | Select-Object SettingName, CongestionProvider
```

> **注意**：上述操作需要**管理员权限**打开 PowerShell/CMD。如果主要目的是优化远程连接（如 RustDesk）质量，服务器端开启 BBR 的收益远大于客户端改 CTCP。
