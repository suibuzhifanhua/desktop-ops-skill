# 软件安装 / 卸载 / 修复参考

## Windows 包管理

```powershell
# winget（Windows 11 内置，Win10 可安装）
winget search "Visual Studio Code"
winget install Microsoft.VisualStudioCode
winget upgrade --all
winget uninstall Microsoft.VisualStudioCode

# Chocolatey（[安装说明](https://chocolatey.org/install)）
choco install googlechrome -y
choco upgrade all -y
choco uninstall googlechrome -y
choco list --local-only    # 已安装软件

# Scoop（适合开发工具，无需管理员）
# 安装：irm get.scoop.sh | iex
scoop install git nodejs python
scoop update *
```

---

## 安装失败排查

### 常见安装错误

| 错误 | 原因 | 处理 |
|------|------|------|
| 0x80070643 | .NET/VC++ 运行库损坏 | 修复运行库 |
| 0x80070002 | 文件未找到 | 检查安装包完整性 |
| 1603 | 安装过程错误 | 查 MSI 日志 |
| 0xC0000142 | DLL 加载失败 | 修复 VC++ 运行库 |
| Error 1935 | .NET 框架问题 | 修复 .NET |

```powershell
# 生成 MSI 详细安装日志
msiexec /i installer.msi /l*v C:\Temp\install_log.txt

# 修复所有 VC++ 运行库（推荐工具：[VisualCppRedist_AIO](https://github.com/abbodi1406/vcredist/releases/latest)）

# 修复 .NET Framework
dism /online /enable-feature /featurename:NetFx3 /all
```

---

## 卸载残留清理

```powershell
# 标准卸载
Get-WmiObject Win32_Product | Where-Object {$_.Name -like "*AppName*"} | Invoke-Method -Name Uninstall

# 强制卸载（通过 GUID）
$app = Get-WmiObject Win32_Product | Where-Object {$_.Name -eq "MyApp"}
msiexec /x $app.IdentifyingNumber /quiet

# 清理残留注册表
# HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{GUID}
# HKCU\Software\AppVendor\AppName

# 清理残留文件目录
# %APPDATA%, %LOCALAPPDATA%, %PROGRAMDATA%, C:\Program Files (x86)\
```

推荐工具：[**Revo Uninstaller**](https://www.revouninstaller.com/revo-uninstaller-free-download/)（免费版支持深度卸载+残留清理）

---

## DLL 缺失修复

```powershell
# 检查系统文件完整性
sfc /scannow

# DISM 修复（SFC 修复失败时用）
dism /online /cleanup-image /restorehealth
# 然后再次运行
sfc /scannow

# 查找 DLL 所属安装包
# 方法1：在 [Everything](https://www.voidtools.com/) 中搜索 dll 名称
# 方法2：在 DLL-files.com 查找（验证来源）
# 方法3：用 [Dependencies](https://github.com/lucasg/Dependencies/releases) 工具分析 exe 依赖
```

---

## Linux 包管理

```bash
# Debian/Ubuntu (apt)
sudo apt update && sudo apt upgrade -y
sudo apt install package-name
sudo apt remove package-name
sudo apt autoremove    # 清理孤立依赖
sudo apt --fix-broken install  # 修复损坏的包

# CentOS/RHEL (dnf/yum)
sudo dnf update -y
sudo dnf install package-name
sudo dnf remove package-name

# Arch Linux (pacman)
sudo pacman -Syu
sudo pacman -S package-name
sudo pacman -Rns package-name  # 含依赖删除

# 查找文件属于哪个包
dpkg -S /usr/bin/python3   # Debian
rpm -qf /usr/bin/python3   # RHEL
```

---

## macOS 包管理

```bash
# Homebrew
brew install package-name
brew upgrade
brew uninstall package-name
brew cleanup           # 清理旧版本
brew doctor            # 诊断 Homebrew 问题

# Mac App Store
mas list               # 已安装应用
mas install 497799835  # 通过 App ID 安装（Xcode 示例）
mas upgrade            # 更新所有应用
```

---

## 软件修复技巧

1. **先卸载重装**：大多数问题的最简解
2. **以管理员运行安装程序**：解决权限问题
3. **禁用杀软临时**：某些安装被误拦截
4. **清空 Temp 目录**：安装前删除 `%TEMP%` 内容
5. **检查磁盘空间**：C 盘至少保留 10GB 可用
6. **兼容模式运行**：老软件右键 → 属性 → 兼容性

---

## 微信 / 企业微信数据迁移（释放 C 盘空间）

> 来源：[Fisheep的新世界](https://fisheep.fun/yummy/22)

微信和企业微信的聊天记录、文件缓存默认存储在 C 盘，长期积累会占用大量空间。可通过以下方式迁移到其他分区。

### 准备工作

1. 找一个**空间充裕的非系统盘**（如 D 盘）
2. 建立一个**非中文名称的文件夹**（如 `D:\WeChatData`）
3. ⚠️ **目标文件夹必须为非中文命名**，否则可能无法正常识别

### 微信迁移步骤

1. 打开微信 → **设置**
2. 找到 **文件管理** 选项
3. 点击 **更改** 按钮
4. 选择刚才建立的空文件夹
5. 等待系统自动完成迁移

### 企业微信迁移步骤

1. 打开企业微信 → **设置**
2. 点击 **文件存储** 旁边的 **更改**
3. 选择新建的文件夹
4. 等待迁移完成

| 软件 | 迁移路径 |
|------|---------|
| 微信 | 设置 → 文件管理 → 更改 |
| 企业微信 | 设置 → 文件存储 → 更改 |
