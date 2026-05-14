# Windows 重装 / 升级 Win11 操作指南

> 根据实际工具整理，覆盖支持直升 / 不满足条件 / 安装过程异常 三类场景。

---

## 工具官方下载链接速查

| 工具 | 官方下载 | 说明 |
|------|---------|------|
| 🏥 PC 健康状况检查 (PC Health Check) | https://aka.ms/getpchealthcheckapp | 检测电脑是否满足 Win11 安装条件 |
| ⬆️ Windows 11 升级助手 | https://www.microsoft.com/zh-cn/software-download/windows11 | 点击"更新助手"下载 |
| 📀 Win11 原版 ISO 镜像 | https://www.microsoft.com/zh-cn/software-download/windows11 | 点击"下载 Windows 11 磁盘映像 (ISO)" |
| 🖥️ Rufus（启动盘制作） | https://rufus.ie/downloads/ | 官方最新 v4.14（含便携版 `p` 后缀） |
| 🔄 Windows 10 更新助手 | https://www.microsoft.com/zh-cn/software-download/windows10 | 点击"立即更新工具"下载 |
| 📀 Win10 原版 ISO 镜像 | https://www.microsoft.com/zh-cn/software-download/windows10 | 点击"下载 Windows 10 磁盘映像 (ISO)" |

> **所有工具均可直接点击上方链接下载**，或使用文件夹中已有的本地工具版本。

---

## 一、符合条件 → 直接升级 Win11

> **适用条件**：电脑通过 PC Health Check 检测，所有项目都打勾（CPU/TPM/ Secure Boot/ 磁盘空间等）。

### 操作步骤

**第一步：安装 PC 健康检测工具**

1. 下载并安装 [PC 健康状况检查工具](https://aka.ms/getpchealthcheckapp)（官方原名：Windows PC Health Check）
2. 运行该工具，确认所有检测项（CPU、内存、磁盘空间、TPM、Secure Boot）都显示为 ✅
3. 若有任意项为 ❌，跳转至对应问题章节处理

**第二步：运行 Win11 升级工具**

> ⚠️ **升级前必须备份！**
> - 桌面文件（C:\Users\用户名\Desktop）
> - C 盘重要资料（文档、照片、工作文件等）
> - 建议备份到外接硬盘或 D 盘

1. 确认所有检测项通过后，下载并运行 [Windows 11 更新助手](https://www.microsoft.com/zh-cn/software-download/windows11)（或使用文件夹中的 `Windows10Upgrade9252.exe`）
2. 工具会自动开始下载并升级，无需其他操作
3. 等待系统自动重启完成升级

---

## 二、升级过程常见问题与解决

### 问题 1：检测通过但提示"版本不符合"

**症状**：PC Health Check 全通过，但升级时报错"当前版本过低"。

**原因**：当前 Win10 版本不是最新。

**解决方法**：

**方案 A：系统自带更新**
```
设置 → 更新和安全 → Windows 更新 → 检查更新
→ 安装所有可用更新，重启后重试升级
```

**方案 B：使用 Win10 更新助手**
- 运行 `Windows10Upgrade9252.exe`（跳过版本检查的版本）
- 或下载官方 [Windows 10 更新助手](https://www.microsoft.com/zh-cn/software-download/windows10) → "立即更新工具"

> 目标：先将 Win10 升级到 22H2 最新版，再进行 Win11 升级。

---

### 问题 2：升级后一直回退（Rolling Back）

**症状**：Win11 安装进度到一半开始回退到原系统，反复尝试均失败。

**根本原因**：当前系统存在冲突或损坏，直接升级无法完成。

**解决方法——两步走：**

#### 第一步：重置当前系统（清理潜在冲突）

1. `设置 → 更新和安全 → 恢复 → 重置此电脑 → 初始化`
2. 选择"保留我的文件"（会清理应用和部分设置，但保留个人文件）
3. 等待重置完成

**重置过程中可能遇到的问题：**

- **进度条卡住不动**：直接断电强制关机，用 U 盘重新安装系统（见第三节）
- **要求联网跳过不了**：同时按 `Shift + F10` → 输入 `oobe\BypassNRO.cmd` → 回车 → 电脑自动重启 → 跳过按钮出现
- **要求登录微软账号**：输入以下虚假账号跳过：
  ```
  账号：nothankyou@123.com
  密码：任意内容（如 123456）
  ```
  提交后会报错"账号不存在"，然后点"下一步"即可跳过

#### 第二步：升级到最新 Win10

1. 重置完成后，进入系统
2. 运行 `设置 → 更新和安全 → Windows 更新`，将 Win10 升级到最新版（22H2）
3. 确认版本最新后，再运行 Win11 升级工具

---

### 问题 3：提示"TPM 模块未开启"或"没有 TPM 模块"

#### 情况 A：电脑根本没有 TPM 芯片

**症状**：BIOS 中完全找不到 TPM 选项，PC Health Check 显示"不支持"。

**解决方法**：无法通过绕过方式安装，**直接使用原版镜像重装 Win11**（见第三节）。

> 微软要求 TPM 2.0 是硬性要求，无法通过修改绕过。

#### 情况 B：TPM 芯片存在但未开启

**症状**：PC Health Check 显示"TPM 未配置"，但 BIOS 中有 TPM 选项。

**解决方法：进入 BIOS 开启 TPM 2.0**

1. 重启电脑，开机时按 `F2` / `Del` / `Esc`（视主板品牌而定）进入 BIOS
2. 找到以下路径之一（不同主板名称略有差异）：
   - `Security → TPM Configuration → TPM Device Selection → Enable`
   - `Advanced → PCH Configuration → TPM → Enable`
   - `Boot → CSM → Disable`（部分机型需先关闭 CSM 才能启用 TPM）
3. 设置完成后按 `F10` 保存并重启
4. 重新运行 PC Health Check，确认 TPM 项目变为 ✅
5. 继续运行 Win11 升级工具

---

## 三、硬件不支持 → U 盘重装系统

> **适用场景**：TPM 不可用 / 升级反复失败 / 需全新安装

### 准备工作

| 项目 | 说明 |
|------|------|
| U盘 | ≥ 8GB，安装过程会格式化，**提前备份 U 盘数据** |
| 正常电脑 | 用于写入镜像（可以是任意 Win10/11 系统） |
| 系统镜像 | 下载 Win11 原版 ISO（微软官网） |
| 写入工具 | [Rufus v4.14 便携版](https://github.com/pbatard/rufus/releases/download/v4.14/rufus-4.14p.exe)（推荐）或 [官网下载页面](https://rufus.ie/downloads/) |

### 操作步骤

#### 第一步：下载 Win11 镜像

下载 [Win11 原版 ISO 镜像](https://www.microsoft.com/zh-cn/software-download/windows11)：选择"下载 Windows 11 磁盘映像 (ISO)" → 选择中文简体 → 下载 ISO 文件

#### 第二步：用 Rufus 制作启动 U 盘

1. 将 U 盘插入正常电脑
2. 运行 [Rufus](https://github.com/pbatard/rufus/releases/download/v4.14/rufus-4.14p.exe)（或文件夹中的 `rufus-3.13p.exe`）
   > 官方最新 v4.14：[标准版](https://github.com/pbatard/rufus/releases/download/v4.14/rufus-4.14.exe)｜[便携版 `p`](https://github.com/pbatard/rufus/releases/download/v4.14/rufus-4.14p.exe)
3. 设备中选择你的 U 盘
4. 引导类型选择：点击"选择"按钮 → 找到下载的 Win11 ISO 文件
5. 分区方案选择：
   - **UEFI 主机的电脑**：选择 "GPT"
   - **老电脑（2012年以前）**：选择 "MBR"
6. 文件系统保持默认 `NTFS`
7. 点击"开始" → 等待写入完成（约 5~15 分钟）
8. 写入完成后，U 盘名称变为 `ESD-USB` 或保持原名，**不要格式化，直接拔掉**

#### 第三步：用 U 盘安装系统

1. 将 U 盘插入目标电脑
2. 开机按 `F12` / `F8` / `Esc`（视品牌而定）选择从 USB 启动
3. 进入 Win11 安装界面，选择语言和键盘布局
4. 点击"现在安装"
5. 输入 Win11 激活密钥（若无，可先跳过，安装完成后用数字权利激活）
6. 选择要安装的版本（专业版/家庭版）
7. 选择安装位置（若要全盘格式化，选中目标磁盘 → 新建 → 应用）
8. 等待安装完成（约 10~20 分钟），期间电脑会重启数次

> ⚠️ **安装系统会清空所有磁盘数据**，务必提前备份！

---

## 四、Win11 安装完成后必做检查

1. **检查所有驱动**：设备管理器中无黄色感叹号
2. **运行 Windows 更新**：设置 → Windows 更新 → 检查更新
3. **激活系统**：
   - Win10 升级上来的：自动激活（数字权利）
   - 新安装的：用 `slui` 命令输入密钥激活
4. **检查 BitLocker**（若开机提示加密）：选择"暂停加密"或关闭 BitLocker

---

*最后更新：2026-05-14 | 来源：桌面运维实战积累*
