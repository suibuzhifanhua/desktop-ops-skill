# 国产系统桌面运维速查（实战经验积累）

> 适用系统：统信 UOS、银河麒麟 Kylin、深度 Deepin、中标麒麟 NeoKylin 等。
> 持续更新，使用 Ctrl+F 搜索关键词快速定位。

---

## 系统基本信息

| 系统 | 内核基础 | 桌面环境 | 包管理器 |
|------|---------|---------|---------|
| 统信 UOS（家庭版/专业版） | Debian/Linux | DDE（深度桌面） | apt / deepin-store |
| 银河麒麟 V10 | Ubuntu / 龙蜥 | UKUI | apt |
| 深度 Deepin 23 | Debian | DDE | apt |
| 中标麒麟 NeoKylin | CentOS/RHEL | UKUI/GNOME | yum / rpm |

---

## 🔧 常用终端命令速查

```bash
# 查看系统版本
cat /etc/os-release

# 查看内核版本
uname -r

# 查看 CPU 核心数
nproc
lscpu

# 查看内存使用
free -h

# 查看磁盘使用
df -h

# 查看当前系统用户
whoami
```

---

## 💡 待补充

> 本文档将根据实际运维经验持续更新。
> 遇到国产系统相关问题，提供问题描述 + 解决方法后会在此归类整理。

---

*最后更新：2026-05-14*
