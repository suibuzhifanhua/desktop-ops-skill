# Windows 11 桌面优化指南

> 适用于高配 PC（大内存 + NVMe 全固态）的系统优化实践

---

## 一、核心优化项

### 1. 关闭休眠 — 释放磁盘空间

**原理**：休眠文件 `hiberfil.sys` 用于保存内存快照以便休眠恢复，占用约为物理内存的 40%。大内存配置下（64GB+）可浪费数十 GB。桌面机基本不需要休眠功能。

**判断标准**：物理内存 ≥ 32GB 且为台式机 → 建议关闭。

**操作**：
```powershell
powercfg -h off
```

**验证**：
```powershell
Test-Path C:\hiberfil.sys    # 应为 False
```

---

### 2. 电源计划切换至「高性能」或「卓越性能」

**原理**：默认「平衡」模式会动态降频以省电。对于编译、AI 推理、渲染等 CPU 密集型任务，降频直接导致性能损失。

**操作**：
```powershell
# 查看可用计划
powercfg /list

# 切换到高性能（通用）
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# 如果有卓越性能（部分版本）：
# powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61
```

---

### 3. 禁用 DiagTrack（遥测服务）

**原理**：Connected User Experiences and Telemetry 持续收集应用使用、性能数据、系统配置并上传微软。后台 CPU 和网络占用不可忽略，且涉及隐私。

**操作**：
```powershell
Stop-Service DiagTrack -Force
Set-Service DiagTrack -StartupType Disabled
```

**验证**：
```powershell
Get-Service DiagTrack | Select Status, StartType
# Status: Stopped, StartType: Disabled
```

---

### 4. 禁用 WSearch（Windows 搜索索引）

**原理**：对文件内容建立全文索引以加速搜索。在 NVMe 固态上直接遍历已足够快，索引收益极小，反而持续产生写入和 CPU 开销。

**适用条件**：系统盘为 NVMe SSD → 建议关闭。HDD 用户不建议关闭。

**操作**：
```powershell
Stop-Service WSearch -Force
Set-Service WSearch -StartupType Disabled
```

---

### 5. 禁用 SysMain（Superfetch）

**原理**：分析使用习惯，预加载常用应用到内存。NVMe 直接从 SSD 加载已足够快（数秒内），预加载收益微乎其微，反而占用内存和 I/O。

**适用条件**：系统盘为 NVMe SSD → 建议关闭。

**操作**：
```powershell
Stop-Service SysMain -Force
Set-Service SysMain -StartupType Disabled
```

---

### 6. 禁用非必要的子系统服务

**场景示例**：如果安装了第三方安卓模拟器（如 MuMu、应用宝），Windows 自带的 WSA（安卓子系统）就是冗余的。

**操作**（以 WSA 为例）：
```powershell
Stop-Service WSAIFabricSvc -Force
Set-Service WSAIFabricSvc -StartupType Disabled
```

**通用原则**：定期审查运行中的自动服务，对比实际使用需求，关掉冗余项。

---

## 二、常见待优化服务清单

| 优先级 | 服务名 | 说明 | 关闭条件 |
|--------|--------|------|----------|
| 高 | DoSvc | Delivery Optimization，Windows 更新 P2P 分发 | 不需要贡献上传带宽 |
| 高 | DusmSvc | 数据使用量统计 | 不需要流量统计 |
| 中 | WpnService | Windows 推送通知 | 桌面机 |
| 中 | 第三方下载工具服务 | 如迅雷常驻后台 | 打开软件时会自动拉起 |
| 低 | Spooler | 打印后台处理 | 不接打印机 |
| 低 | PcaSvc | 程序兼容性助手 | 不运行老旧软件 |

---

## 三、诊断命令速查

```powershell
# 系统概览
Get-CimInstance Win32_OperatingSystem | Select Caption, Version, LastBootUpTime

# CPU
Get-CimInstance Win32_Processor | Select Name, NumberOfCores, NumberOfLogicalProcessors

# 内存
Get-CimInstance Win32_PhysicalMemory | Select Manufacturer, Speed, @{N='GB';E={[math]::Round($_.Capacity/1GB,1)}}

# GPU
Get-CimInstance Win32_VideoController | Where Name -notlike '*Microsoft*' | Select Name, @{N='VRAM_GB';E={[math]::Round($_.AdapterRAM/1GB,1)}}

# 磁盘
Get-PhysicalDisk | Select FriendlyName, MediaType, HealthStatus, @{N='SizeGB';E={[math]::Round($_.Size/1GB,1)}}
Get-PSDrive -PSProvider FileSystem | Select Name, @{N='UsedGB';E={[math]::Round($_.Used/1GB,1)}}, @{N='FreeGB';E={[math]::Round($_.Free/1GB,1)}}

# 内存 Top 进程
Get-Process | Sort WorkingSet64 -Descending | Select -First 10 Name, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,0)}}

# 休眠文件大小
if (Test-Path C:\hiberfil.sys) { [math]::Round((Get-Item C:\hiberfil.sys).Length/1GB,1) }

# 当前电源计划
powercfg /getactivescheme

# 自启服务
Get-Service | Where { $_.StartType -eq 'Automatic' -and $_.Status -eq 'Running' } | Select Name, DisplayName

# 开机启动项
Get-CimInstance Win32_StartupCommand | Select Name, Command

# 磁盘健康与对齐
Get-PhysicalDisk | Select FriendlyName, HealthStatus
fsutil behavior query DisableDeleteNotify   # 0 = TRIM 已启用
```

---

## 四、管理员权限执行方法

部分操作需要管理员权限。受限环境下可通过脚本文件 + RunAs 提权：

```powershell
# 1. 将操作写入 .ps1 脚本文件
# 2. 通过 Start-Process -Verb RunAs 提权执行
Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "<script.ps1>"' -Verb RunAs -Wait
# 3. 验证结果
# 4. 删除临时脚本
```

**注意**：RunAs 会弹出 UAC 窗口，需手动确认。

---

## 五、NVIDIA 驱动排查技巧

如果 `nvidia-smi` 报错但怀疑 GPU 仍在工作，可通过 WMI 直接查询 GPU 进程占用：

```powershell
# 列出每个 GPU 引擎的占用情况
Get-CimInstance -Namespace "root/cimv2" -ClassName Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine | 
    Select Name, @{N='Util';E={"$($_.UtilizationPercentage)%"}}

# 查找特定进程的 GPU 占用（如 PID 12345）
Get-CimInstance -Namespace "root/cimv2" -ClassName Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine | 
    Where Name -like '*pid_12345*' -and UtilizationPercentage -gt 0
```

若 WMI 能查到进程在独立显卡引擎上有占用，则驱动正常，仅是 NVML 监控组件有问题。

---

*生成时间：2026-05-25*
