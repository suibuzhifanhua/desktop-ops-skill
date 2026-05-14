# 系统性能排查参考

## CPU 占用异常

```powershell
# Windows：实时 CPU 占用 Top 10
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WorkingSet

# 查看 CPU 核心使用情况
Get-WmiObject Win32_Processor | Select-Object Name, NumberOfCores, LoadPercentage

# 性能计数器（采样 5 次，每次 1 秒）
Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 5
```

### 常见 CPU 占用元凶

| 进程 | 原因 | 处理 |
|------|------|------|
| antimalware service executable | Windows Defender 扫描 | 排除开发目录 |
| SearchIndexer.exe | 索引重建 | 等待完成或暂停索引 |
| TiWorker.exe | Windows Update | 等待更新完成 |
| svchost.exe (WaaSMedic) | 更新服务 | 检查更新状态 |
| vmmem | WSL2/虚拟机 | 限制 WSL2 内存（.wslconfig） |

```ini
# 限制 WSL2 资源：%USERPROFILE%\.wslconfig
[wsl2]
memory=4GB
processors=4
swap=2GB
```

---

## 内存占用分析

```powershell
# 查看内存使用
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 Name, @{N="Mem(MB)";E={[math]::Round($_.WorkingSet/1MB,1)}}

# 系统总内存状态
Get-WmiObject Win32_OperatingSystem | Select-Object @{N="Total(GB)";E={[math]::Round($_.TotalVisibleMemorySize/1MB,2)}}, @{N="Free(GB)";E={[math]::Round($_.FreePhysicalMemory/1MB,2)}}

# 清理待机内存（需要 [RAMMap](https://learn.microsoft.com/en-us/sysinternals/downloads/rammap) 或 [EmptyStandbyList](https://learn.microsoft.com/en-us/sysinternals/downloads/rammap)，均为 Sysinternals 工具）
# EmptyStandbyList.exe workingsets
```

---

## GPU 占用排查

```powershell
# 查看 GPU 使用（Windows 10/11，需要 WMI 支持）
Get-Counter "\GPU Engine(*)\Utilization Percentage" | Select-Object -ExpandProperty CounterSamples | Where-Object {$_.CookedValue -gt 0}

# nvidia-smi（需安装 [NVIDIA 驱动](https://www.nvidia.com/Download/index.aspx)，安装后 nvidia-smi 随驱动附带）
nvidia-smi
nvidia-smi dmon -s u  # 实时监控

# 任务管理器 GPU 引擎类型含义对照表
# 3D = 渲染  Copy = 视频复制  Compute = 计算  Video Decode/Encode = 硬件编解码
```

---

## 磁盘 I/O 瓶颈

```powershell
# 查看磁盘 I/O 较高的进程
Get-Counter "\PhysicalDisk(_Total)\% Disk Time" -SampleInterval 1 -MaxSamples 3
Get-Counter "\Process(*)\IO Data Bytes/sec" | Select-Object -ExpandProperty CounterSamples | Sort-Object CookedValue -Descending | Select-Object -First 10

# 磁盘健康状态（SMART）
Get-PhysicalDisk | Get-StorageReliabilityCounter | Select-Object DeviceId, Temperature, Wear
```

---

## 启动时间分析

```powershell
# 查看上次启动时间
(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime

# 启动事件分析
# 事件 ID 6005 = 系统启动，6006 = 系统关闭
Get-EventLog -LogName System -Source "EventLog" -Newest 5 | Where-Object {$_.EventID -in 6005,6006}
```

---

## 性能基准快速参考

| 指标 | 正常范围 | 需关注 |
|------|---------|-------|
| CPU 空闲占用 | < 5% | > 20% 持续 |
| 内存可用 | > 2GB | < 500MB |
| 磁盘响应时间 | < 10ms (SSD) | > 100ms |
| 系统盘剩余 | > 15% | < 10% |
