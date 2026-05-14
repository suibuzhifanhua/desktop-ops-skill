# 进程 / 服务管理参考

## 查看进程

### Windows
```powershell
# 查所有进程（含 PID、CPU、内存）
Get-Process | Sort-Object CPU -Descending | Select-Object -First 20
# 查占用指定端口的进程
netstat -ano | findstr :8080
# 通过 PID 查进程名
tasklist /FI "PID eq 12345"
```

### macOS / Linux
```bash
# 按 CPU 排序
ps aux --sort=-%cpu | head -20
# 查端口占用
lsof -i :8080
ss -tulnp | grep 8080
```

---

## 结束进程

### Windows
```powershell
# 按名称（友好）
Stop-Process -Name "notepad" -Force
# 按 PID（精确）
taskkill /PID 12345 /F
# 结束进程树
taskkill /PID 12345 /F /T
```

### macOS / Linux
```bash
kill -9 <PID>
pkill -f "process_name"
```

---

## Windows 服务管理

```powershell
# 查看所有服务状态
Get-Service | Where-Object {$_.Status -eq "Stopped"} | Select-Object Name, DisplayName

# 启动 / 停止 / 重启
Start-Service -Name "wuauserv"
Stop-Service -Name "wuauserv"
Restart-Service -Name "Spooler"

# 设置启动类型
Set-Service -Name "SysMain" -StartupType Disabled  # 禁用 Superfetch

# sc 命令（兼容旧系统）
sc start "servicename"
sc stop "servicename"
sc query "servicename"
```

---

## 端口占用处理

```powershell
# Windows：找到占用 3000 端口的进程并结束
$pid = (netstat -ano | Select-String ":3000 ").ToString().Trim().Split(" ")[-1]
taskkill /PID $pid /F
```

```bash
# Linux/macOS
fuser -k 3000/tcp
```

---

## 常见服务说明

| 服务名 | 功能 | 建议 |
|--------|------|------|
| SysMain | Superfetch 预加载 | SSD 可禁用 |
| WSearch | Windows Search 索引 | 不常搜索可禁用 |
| wuauserv | Windows Update | 保持自动 |
| Spooler | 打印机后台处理 | 不用打印机可停止 |
| wscsvc | Windows Security Center | 保持运行 |
