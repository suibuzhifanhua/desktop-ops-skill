# Linux 网络优化参考

## 开启 BBR 拥塞控制算法

BBR（Bottleneck Bandwidth and RTT）是 Google 开发的 TCP 拥塞控制算法，相比 CUBIC 能显著提升高延迟、高丢包链路下的吞吐量。**Linux 内核 4.9+ 内置支持**。

### 检查内核版本

```bash
uname -r
# 输出 ≥ 4.9 即可开启 BBR
```

### 开启 BBR

```bash
# 1. 修改 sysctl 配置
cat >> /etc/sysctl.conf << 'EOF'
# TCP BBR 拥塞控制
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
EOF

# 2. 立即生效（无需重启）
sysctl -p

# 3. 验证是否生效
sysctl net.ipv4.tcp_congestion_control
# 输出 net.ipv4.tcp_congestion_control = bbr 即成功

# 4. 确认内核模块已加载
lsmod | grep bbr
```

### 一键脚本

```bash
# 适用于 Debian / Ubuntu / CentOS 7+
wget -qO- https://raw.githubusercontent.com/teddysun/across/master/bbr.sh | bash
```

### 关闭 BBR（恢复默认）

```bash
sed -i '/bbr/d' /etc/sysctl.conf
sysctl -p
# 恢复为 cubic 或 reno
```

### 各发行版注意事项

| 发行版 | 内核版本查看 | 备注 |
|--------|-------------|------|
| Ubuntu 18.04+ | `uname -r` | 默认内核已支持 |
| Debian 9+ | `uname -r` | 默认内核已支持 |
| CentOS 7 | 需升级内核到 4.9+ | `yum install kernel-ml` |
| CentOS 8+ | `uname -r` | 默认内核已支持 |

> **提示**：开启 BBR 后，服务器出口带宽利用率会明显提升，特别适合 VPS、远程桌面（如 RustDesk/Frp）等场景。
