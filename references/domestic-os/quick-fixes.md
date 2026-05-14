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

---

## 🖥️ 远程桌面类

### 用 Windows 远程桌面（RDP）访问国产系统

> 适用系统：统信 UOS、深度 Deepin（DDE 桌面环境）  
> 适用场景：公司内网/家庭局域网，想从 Windows 电脑直接用「远程桌面连接」访问国产系统

**原理说明**

国产系统默认没有 RDP 服务，需要安装两样东西配合使用：
- `x11vnc`：把当前桌面画面"共享"出来
- `xrdp`：提供 RDP 协议入口，让 Windows 的远程桌面可以连进来

---

**第一步：安装 x11vnc**

打开终端，执行：

```bash
sudo apt install x11vnc
```

安装完成后，先手动初始化一下（直接输入 `x11vnc` 回车运行一次即可，看到输出信息后 `Ctrl+C` 中断）：

```bash
x11vnc
```

---

**第二步：创建 x11vnc 开机自启服务**

用 nano（或 vim）编辑服务配置文件：

```bash
sudo nano /usr/lib/systemd/system/x11vnc.service
```

把下面这段内容完整粘贴进去：

```ini
[Unit]
Description="x11vnc"
Requires=display-manager.service
After=display-manager.service

[Service]
ExecStart=/usr/bin/x11vnc -auth guess -loop -forever -safer -shared -ultrafilexfer -bg -o /var/log/x11vnc.log
ExecStop=/usr/bin/killall x11vnc

[Install]
WantedBy=multi-user.target
```

nano 保存方式：`Ctrl+O` → 回车确认 → `Ctrl+X` 退出

保存后依次执行以下三条命令：

```bash
sudo systemctl daemon-reload
sudo systemctl enable x11vnc.service
sudo systemctl restart x11vnc.service
```

---

**第三步：安装 xrdp**

```bash
sudo apt install xrdp
```

安装完成后编辑 xrdp 配置文件：

```bash
sudo nano /etc/xrdp/xrdp.ini
```

滚动到文件**最末尾**，添加下面这一行：

```
exec dde
```

> 这行的作用是告诉 xrdp 登录后加载 DDE（深度桌面环境）。  
> 如果是银河麒麟 UKUI 桌面，改成 `exec ukui-session`。

保存退出后依次执行：

```bash
sudo systemctl restart xrdp
sudo systemctl enable xrdp
```

---

**第四步：重启电脑，然后从 Windows 连接**

重启国产系统，确保服务正常加载。重启后：

1. 先查一下国产系统的局域网 IP（终端执行 `ip a`，找 `inet` 后面那个 `192.168.x.x`）
2. 在 Windows 按 `Win + R` 输入 `mstsc` 打开远程桌面连接
3. 输入国产系统的 IP 地址 → 点"连接"
4. 输入国产系统的用户名和密码 → 进入桌面

---

**验证服务状态（可选）**

重启后如果连不上，先检查两个服务是否正常运行：

```bash
sudo systemctl status x11vnc.service
sudo systemctl status xrdp
```

两个都显示 `active (running)` 说明服务没问题，再检查 IP 和网络连通性。

> ⚠️ 默认 RDP 端口为 3389，防火墙有拦截的话需要放行该端口。  
> ⚠️ 此方案适用于局域网内网，不建议直接暴露到公网。

---

## 💡 待补充

> 本文档将根据实际运维经验持续更新。
> 遇到国产系统相关问题，提供问题描述 + 解决方法后会在此归类整理。

---

*最后更新：2026-05-14*
