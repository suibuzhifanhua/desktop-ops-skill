---
name: desktop-ops
description: >
  日常桌面运维智能助手（Windows / macOS / Linux），覆盖以下场景时自动触发：
  进程/服务管理（查进程、杀进程、服务启停）、磁盘清理与存储分析、网络诊断
  （ping/tracert/端口检测/代理配置）、系统性能排查（CPU/CPU 占用）、
  开机启动项管理、驱动与更新问题、文件权限与注册表操作、定时任务管理、
  日志查看与错误分析、软件安装/卸载/修复、远程桌面与 SSH 连接问题、
  硬件故障排查（开机无反应/黑屏/自动关机）、系统文件修复（sfc/DISM）、
  弹窗广告拦截、多开软件、DNS 配置、U 盘热插拔、共享打印机连接问题。
  当用户描述"电脑慢"、"某某程序打不开"、"网络连不上"、"磁盘满了"、
  "端口占用"、"服务挂了"、"开机自启"、"开机黑屏"、"系统文件损坏"、
  "C盘满了"、"弹窗广告"、"打印机连不上"等运维问题时触发本 Skill。
---

# Desktop Ops — 日常桌面运维助手

## 诊断流程总则

1. **收集信息**：OS 版本、报错原文、触发时机、近期变更
2. **复现最小场景**：确定是否可重现、是否特定用户/环境
3. **查日志**：系统日志 → 应用日志 → 自定义日志
4. **定位根因**：逐层排查（硬件 → 驱动 → OS → 应用 → 配置）
5. **修复并验证**：执行修复命令，重现验证，记录结论

---

## 常用场景速查

### 1. 进程 / 服务管理
- 参考：[references/process-service.md](references/process-service.md)
- 触发词：进程占用、服务挂了、程序卡死、端口占用、杀进程

### 2. 磁盘清理 & 存储分析
- 参考：[references/disk-storage.md](references/disk-storage.md)
- 触发词：磁盘满了、C盘空间、大文件、清理缓存、temp 目录

### 3. 网络诊断
- 参考：[references/network-diag.md](references/network-diag.md)
- 触发词：网络断了、ping 不通、DNS 解析失败、代理配置、端口被封

### 4. 系统性能排查
- 参考：[references/performance.md](references/performance.md)
- 触发词：CPU 100%、内存泄漏、卡顿、风扇狂转、GPU 占用高

### 5. 开机启动项 & 计划任务
- 参考：[references/startup-tasks.md](references/startup-tasks.md)
- 触发词：开机慢、自启动、计划任务、crontab、Task Scheduler

### 6. 日志查看 & 错误分析
- 参考：[references/log-analysis.md](references/log-analysis.md)
- 触发词：蓝屏、事件查看器、崩溃日志、BSOD、应用报错、Event ID

### 7. 权限 & 注册表
- 参考：[references/permission-registry.md](references/permission-registry.md)
- 触发词：拒绝访问、权限不足、注册表、UAC、TrustedInstaller

### 8. 软件安装 / 卸载 / 修复
- 参考：[references/software-mgmt.md](references/software-mgmt.md)
- 触发词：安装失败、卸载残留、dll 缺失、VC++ 运行库、修复安装

### 9. 桌面运维杂问题速查（实战经验积累）
- 参考：[references/quick-fixes.md](references/quick-fixes.md)
- 触发词：开机无反应、BIOS 卡住、系统文件损坏、sfc、DISM、无法删除文件夹、
  找不到控制面板、C盘满了、卓越性能、关闭休眠、打印机连不上、两个微信、
  弹窗广告、查 SSD/HDD、内存条型号、DNS 推荐、黑屏重置显卡、阿里云卸载监控、
  验证哈希值、最近打开的文件、U盘热插拔、映射盘断开

---

## 通用诊断脚本

运行 `scripts/sysinfo.py` 可一键采集系统基本信息（OS/CPU/内存/磁盘/网络接口），
结果直接粘贴到对话中，帮助快速定位问题。

```bash
python scripts/sysinfo.py
```

---

## 输出规范

- 给出**具体命令**，注明 Windows / macOS / Linux 适用范围
- 危险操作（删除、注册表修改、强制结束系统进程）前加 ⚠️ 警告
- 修复步骤编号，方便用户逐步执行
- 结尾附**验证方法**，确认问题已解决
