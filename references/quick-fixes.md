# 桌面运维常见杂问题速查（来自实战经验积累）

> 本文档收录了日常桌面运维中高频出现的小问题与解决方案，持续更新。
> 使用 Ctrl+F 搜索关键词快速定位。

---

## 🔌 开机 / 硬件类

### 按电源键无反应，无法开机
1. 检查电源线、电源插座是否通电，排查 UPS/拖线板故障；
2. 若确认有电仍不开机，拆机取出主板**纽扣电池**（CR2032），等待约 2 分钟后重新装回；
3. 年代久远机器（5 年以上）建议直接更换纽扣电池（电池电压低会导致 BIOS 设置丢失）；
4. 台式机检查机箱前面板跳线是否松动（Power SW 针脚）。

### 停在 BIOS 界面，按键盘无法进入系统
1. 先换一个键盘排除键盘问题（BIOS 下 USB 键盘有时需要启用 Legacy USB 支持）；
2. 若 BIOS 界面有提示硬盘异常，可尝试按 **F1** 继续进入系统，但这只是临时措施；
3. **根本原因大概率是硬盘故障**，立即备份数据：
   - 进系统后用 CrystalDiskInfo 查看硬盘 S.M.A.R.T. 状态
   - 若出现红色警告项（"注意" 或 "异常"）说明硬盘即将报废，尽快换盘

### 突然断电自动关机（非停电）
1. 检查电源接头是否松动；
2. 清理机箱内积灰，检查散热风扇是否运转；
3. 若排除以上，打开机箱取出**纽扣电池**，用手指轻轻摩擦金属触点后重新装入；
4. 若频繁发生，检查是否 CPU 过热触发了热保护（CPU 超过 90°C 会自动关机）。

---

## 💻 系统 / 文件类

### 系统文件损坏修复（最重要的命令）

**方法一：SFC 快速修复**
```cmd
# 以管理员模式打开 CMD，输入：
sfc /scannow
```
> 等待扫描完成（约 5~15 分钟），会自动修复检测到的损坏文件。

**方法二：DISM 深度修复（当 sfc 无效时使用）**
```powershell
# 步骤 1：扫描映像，检查问题
Dism /Online /Cleanup-Image /ScanHealth

# 步骤 2：检查是否有可修复的问题
Dism /Online /Cleanup-Image /CheckHealth

# 步骤 3：从 Windows Update 拉取正确文件并还原
DISM /Online /Cleanup-image /RestoreHealth

# 步骤 4：重启后再次运行 sfc 确认修复
sfc /SCANNOW
```
> ⚠️ 步骤 3 需要联网，会消耗一定时间（10~30 分钟），请耐心等待。

### 最近打开的文件记录（找回忘记名字的文件）
```
Win + R → 输入 recent → 回车
```
> 会打开 `%AppData%\Microsoft\Windows\Recent`，列出最近访问过的所有文件和文件夹。

### 无法删除的文件夹（强制删除）
新建一个 `.bat` 文件，写入以下内容，将**目标文件夹拖拽到此 bat 文件上**即可强制删除：
```bat
DEL /F /A /Q \\?\%1
RD /S /Q \\?\%1
```
> ⚠️ 此操作不可撤销，请确认目标路径后再执行。

---

## 🖥️ Windows 设置 / 界面类

### 刚装完 Win10，桌面找不到"此电脑"或"控制面板"
```
桌面空白处右键 → 个性化 → 主题 → 桌面图标设置 → 勾选所需图标 → 确定
```

### 桌面占用 C 盘空间，如何将桌面移到其他盘
1. 在其他盘（如 D:\）新建一个文件夹，如 `D:\Desktop`；
2. 右键桌面上的任意文件 → 属性 → 位置选项卡；
3. 或直接找到 `C:\Users\你的用户名\Desktop`，右键 → 属性 → 位置 → 移动；
4. 选择 `D:\Desktop` → 确定 → 提示是否移动文件，选"是"。

### Win10 更新后 C 盘空间骤减
```
桌面找到"此电脑" → 右键 C 盘 → 属性 → 磁盘清理 → 清理系统文件 → 全部勾选 → 确定
```
> 主要清理 `Windows.old`（旧系统备份，通常 5~15GB），更新后 10 天内可清理。

### 开启 Win10 卓越性能模式（笔记本 / 高性能需求场景）
```powershell
# 管理员 PowerShell 中执行：
powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
```
> 执行后到「控制面板 → 电源选项」即可看到"卓越性能"方案，选中即可。
> 此方案会增加耗电量，不适合追求续航的笔记本日常使用。

### 关闭休眠模式（释放 C 盘空间，一般节省 4~16 GB）
```cmd
# 管理员 CMD 中执行：
powercfg -h off
```
> 关闭休眠后 `hiberfil.sys` 文件会被删除，开机速度会略慢（无法从休眠恢复）。

---

## 🖨️ 外设 / 共享类

### 连接共享打印机失败（`\\IP` 访问无效）
1. 用 IP 方式偶尔失败是正常的，改用**计算机名**连接：
   - 在打印服务器端：右键"此电脑" → 属性 → 查看"计算机名"
   - 在本机：`Win + R` → 输入 `\\计算机名` → 回车
2. 若仍失败，检查目标机器的"网络发现"和"文件共享"是否开启（控制面板 → 网络和共享中心 → 更改高级共享设置）。

### U 盘是否需要弹出才能拔
- **Win10 及以后版本**：关闭 U 盘内所有正在打开的文件后，可**直接拔出**，无需点弹出；
- **Win7 / Win8 / XP 等旧版本**：必须通过右下角托盘图标**安全弹出**后再拔，否则可能损坏文件。

### 映射网络驱动器重启后断开
```powershell
# 管理员 PowerShell 中执行（设置永不自动断开连接）：
net config server /autodisconnect:-1
```

---

## 📱 软件 / 应用类

### 同时登录两个微信
- **方法一**（推荐）：开始菜单 → 微软商店 → 搜索"微信" → 安装商店版微信；此后同时拥有桌面版 + 商店版两个微信，可各自登录不同账号。
- **方法二**：搜索网上的"微信多开 bat 工具"，运行即可多开。

### 批注 / 修订中的用户名不对（Word / WPS）
> ⚠️ **切记不要在 Windows 系统里修改用户名！** 修改系统用户名/组名会导致多个软件无法启动！

正确修改方式（以 WPS 为例，Office 同理）：
```
打开 WPS → 审阅 选项卡 → 修订 → 更改用户名
```

### 弹窗广告太多，批量屏蔽
安装 **火绒安全**（免费），开启"弹窗拦截"功能：
- 官方下载：https://www.huorong.cn/
- 安装后：火绒主界面 → 安全工具 → 弹窗拦截 → 开启

---

## ⚙️ 硬件信息查询

### 查看磁盘类型（SSD 还是 HDD）
```powershell
# 管理员 PowerShell 中执行：
get-physicaldisk
```
> 查看 **MediaType** 列：`SSD` 表示固态硬盘，`HDD` 表示机械硬盘，`Unspecified` 表示未能识别。

### 查看 CPU 核心数和内存条详情
```cmd
# 打开 CMD，输入 wmic 进入管理界面：
wmic

# 然后输入（查看内存条型号、容量、PN 号等）：
memorychip

# 查看 CPU 详情（重点看 NumberOfCores 核心数和 NumberOfLogicalProcessors 逻辑处理器数）：
cpu get *
```

---

## 🌐 网络 / DNS 类

### 万金油公共 DNS 推荐

| DNS 服务商 | 首选地址 | 备用地址 |
|-----------|---------|---------|
| 114 DNS（国内稳定） | `114.114.114.114` | `114.114.115.115` |
| 腾讯 DNSPod | `119.29.29.29` | `119.28.28.28` |
| 阿里 DNS | `223.5.5.5` | `223.6.6.6` |
| Google DNS | `8.8.8.8` | `8.8.4.4` |

> 国内日常推荐使用 **114 DNS** 或 **腾讯 DNSPod**，Google DNS 适合访问国际网站。

---

## 🔐 安全 / 文件完整性

### PowerShell 验证文件哈希值（校验下载文件是否完整）
```powershell
# 验证 SHA256（将路径替换为实际文件路径）：
certutil -hashfile "C:\Users\你的用户名\Downloads\文件名.exe" SHA256

# 或用 PowerShell 原生命令：
Get-FileHash "C:\path\to\file.exe" -Algorithm SHA256
```
> 将输出的哈希值与官网提供的哈希值对比，一致则文件完整未被篡改。

---

## 🖼️ 显卡 / 黑屏类

### 显卡异常、黑屏或花屏（快速重置显卡驱动）
```
快捷键：Win + Ctrl + Shift + B
```
> 此操作会**重置显卡驱动**（屏幕会短暂黑屏约 1 秒），无需重启，可解决部分花屏、黑屏问题。
> 注意：如果是硬件损坏导致的黑屏，此方法无效。

---

## 🐧 Linux / 服务器运维

### 阿里云服务器卸载云盾 / Aegis 监控进程
> 适用于自购 ECS 不需要阿里云监控的场景（⚠️ 企业 ECS 请与安全团队确认后再操作）

```bash
# 官方卸载脚本
wget http://update.aegis.aliyun.com/download/uninstall.sh
chmod +x uninstall.sh
./uninstall.sh

wget http://update.aegis.aliyun.com/download/quartz_uninstall.sh
chmod +x quartz_uninstall.sh
./quartz_uninstall.sh

# 手动清理残留
pkill aliyun-service
rm -fr /etc/init.d/agentwatch /usr/sbin/aliyun-service
rm -rf /usr/local/aegis*
```

---

## 🌐 浏览器 / 网络工具

### 无 U 盘、无安装包，用 VBScript 下载 Edge 安装包
> 适用场景：IE 挂了，只有网络，无法正常下载文件

新建记事本，写入以下内容，保存为 `.vbs` 文件，双击运行，等待 "Download completed" 弹窗后桌面出现安装包：

```vbs
Set winHttp = CreateObject("WinHttp.WinHttpRequest.5.1")
url = "https://go.microsoft.com/fwlink/?linkid=2108834&Channel=Stable&language=zh-cn"
winHttp.open "GET", url, False
winHttp.send ""
Set adodbStream = CreateObject("ADODB.Stream")
with adodbStream
  .type = 1
  .open
  .write winHttp.responseBody
  .savetofile "MicrosoftEdgeSetup.exe", 2
end with
msgbox "Download completed"
```

---

*最后更新：2026-05-14 | 来源：https://fisheep.fun/yummy/46*
