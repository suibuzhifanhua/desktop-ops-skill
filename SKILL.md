---
name: desktop-ops
description: >
  日常桌面运维智能助手，支持 Windows 与国产系统（统信 UOS / 银河麒麟 / 深度 Deepin 等）。
  覆盖场景：进程/服务管理、磁盘清理与存储分析、网络诊断（ping/DNS/端口）、系统性能排查、
  开机启动项管理、驱动与更新问题、文件权限与注册表操作、定时任务、日志查看、
  软件安装/卸载/修复、远程桌面与 SSH、硬件故障排查（开机无反应/黑屏/自动关机）、
  系统文件修复（sfc/DISM/fsck）、弹窗广告拦截、多开软件、DNS 配置、U 盘热插拔、共享打印机。
  触发词：电脑慢、程序打不开、网络连不上、磁盘满了、端口占用、服务挂了、开机自启、
  开机黑屏、系统文件损坏、C盘满了、弹窗广告、打印机连不上、麒麟装软件、UOS驱动、
  统信系统、国产系统运维等。
---

# Desktop Ops — 日常桌面运维助手

## ⚡ 系统分支快速路由

> 用户提问时请先说明系统类型，以便精准匹配解决方案：
> - **Windows 问题** → 进入 [Windows 分支](#-windows-分支)
> - **国产系统问题**（统信 UOS / 银河麒麟 / 深度 Deepin / 中标麒麟等）→ 进入 [国产系统分支](#-国产系统分支)

---

## 🪟 Windows 分支

### 诊断流程

1. **收集信息**：OS 版本、报错原文、触发时机、近期变更
2. **复现最小场景**：确定是否可重现、是否特定用户/环境
3. **查日志**：系统日志 → 应用日志 → 自定义日志
4. **定位根因**：逐层排查（硬件 → 驱动 → OS → 应用 → 配置）
5. **修复并验证**：执行修复命令，重现验证，记录结论

### 常用场景速查

#### 1. 进程 / 服务管理
- 参考：[references/windows/process-service.md](references/windows/process-service.md)
- 触发词：进程占用、服务挂了、程序卡死、端口占用、杀进程

#### 2. 磁盘清理 & 存储分析
- 参考：[references/windows/disk-storage.md](references/windows/disk-storage.md)
- 触发词：磁盘满了、C盘空间、大文件、清理缓存、temp 目录

#### 3. 网络诊断
- 参考：[references/windows/network-diag.md](references/windows/network-diag.md)
- 触发词：网络断了、ping 不通、DNS 解析失败、代理配置、端口被封

#### 4. 系统性能排查
- 参考：[references/windows/performance.md](references/windows/performance.md)
- 触发词：CPU 100%、内存泄漏、卡顿、风扇狂转、GPU 占用高

#### 5. 开机启动项 & 计划任务
- 参考：[references/windows/startup-tasks.md](references/windows/startup-tasks.md)
- 触发词：开机慢、自启动、计划任务、Task Scheduler

#### 6. 日志查看 & 错误分析
- 参考：[references/windows/log-analysis.md](references/windows/log-analysis.md)
- 触发词：蓝屏、事件查看器、崩溃日志、BSOD、应用报错、Event ID

#### 7. 权限 & 注册表
- 参考：[references/windows/permission-registry.md](references/windows/permission-registry.md)
- 触发词：拒绝访问、权限不足、注册表、UAC、TrustedInstaller

#### 8. 软件安装 / 卸载 / 修复
- 参考：[references/windows/software-mgmt.md](references/windows/software-mgmt.md)
- 触发词：安装失败、卸载残留、dll 缺失、VC++ 运行库、修复安装

#### 9. 实战杂问题速查（持续更新）
- 参考：[references/windows/quick-fixes.md](references/windows/quick-fixes.md)
- 触发词：开机无反应、BIOS 卡住、系统文件损坏、sfc、DISM、无法删除文件夹、
  C盘满了、卓越性能、关闭休眠、打印机连不上、两个微信、弹窗广告、查 SSD/HDD、
  内存条型号、DNS 推荐、黑屏重置显卡、验证哈希值、U盘热插拔、映射盘断开

---

## 🇨🇳 国产系统分支

> 适用：统信 UOS、银河麒麟 Kylin V10、深度 Deepin、中标麒麟 NeoKylin 等

### 诊断流程

1. **确认系统版本**：`cat /etc/os-release` + `uname -r`
2. **确认架构**：`uname -m`（x86_64 / aarch64 / loongarch64）
3. **查包管理器日志**：apt / yum / rpm 操作记录
4. **定位根因**：硬件兼容 → 驱动 → 系统配置 → 应用层
5. **修复并验证**：执行命令，重启验证，记录结论

### 常用场景速查

#### 1. 实战杂问题速查（持续更新）
- 参考：[references/domestic-os/quick-fixes.md](references/domestic-os/quick-fixes.md)
- 触发词：统信UOS、银河麒麟、Deepin、国产系统装软件、驱动问题、输入法、
  兼容模式、麒麟应用商店、UOS 激活、deb 安装失败、国产系统远程桌面、
  xrdp、x11vnc、Windows连接麒麟、RDP访问UOS

---

## 🔧 通用诊断脚本

运行 `scripts/sysinfo.py` 可一键采集系统基本信息（OS/CPU/内存/磁盘/网络接口）：

```bash
python scripts/sysinfo.py
```

---

## 📋 输出规范

- 给出**具体命令**，明确标注适用系统（Windows / UOS / 麒麟 / 通用 Linux）
- 危险操作（删除、注册表修改、强制结束系统进程）前加 ⚠️ 警告
- 修复步骤编号，方便用户逐步执行
- 结尾附**验证方法**，确认问题已解决
