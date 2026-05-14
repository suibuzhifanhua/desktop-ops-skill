# 权限 & 注册表操作参考

## 文件权限问题

### Windows 权限修复

```powershell
# 查看文件/目录 ACL
Get-Acl "C:\SomePath" | Format-List

# 获取目录完全控制权（当前用户）
icacls "C:\SomePath" /grant "$env:USERNAME:(OI)(CI)F" /T

# 重置为继承权限
icacls "C:\SomePath" /reset /T

# 取得所有权（TrustedInstaller 文件）
takeown /f "C:\Windows\System32\something.dll" /a
icacls "C:\Windows\System32\something.dll" /grant Administrators:F
```

### 以管理员身份运行

```powershell
# 以管理员启动 PowerShell
Start-Process PowerShell -Verb RunAs

# 以管理员运行脚本
Start-Process -FilePath "script.ps1" -Verb RunAs

# 检查当前是否为管理员
([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
```

### UAC 相关

```powershell
# 查看 UAC 级别（0=关闭, 1=不降低桌面, 2=标准, 3=始终通知）
Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System -Name ConsentPromptBehaviorAdmin

# ⚠️ 临时禁用 UAC（仅排查用）
Set-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System -Name "EnableLUA" -Value 0
# 排查后恢复
Set-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System -Name "EnableLUA" -Value 1
```

---

## 注册表操作

### 常用操作

```powershell
# 读取注册表值
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" -Name ProductName

# 设置值
Set-ItemProperty "HKCU:\Software\MyApp" -Name "Setting1" -Value "value" -Type String

# 创建新键
New-Item "HKCU:\Software\MyNewApp" -Force

# 删除值（⚠️ 不可撤销）
Remove-ItemProperty "HKCU:\Software\MyApp" -Name "OldSetting"

# 删除键及子键（⚠️ 极度危险，谨慎操作）
Remove-Item "HKCU:\Software\OldApp" -Recurse
```

### 备份与恢复

```powershell
# 导出注册表键（备份）
reg export "HKCU\Software\MyApp" C:\Backup\myapp_reg_backup.reg

# 导入注册表（恢复）
reg import C:\Backup\myapp_reg_backup.reg

# 导出整个 HKCU（完整备份，文件较大）
reg export HKCU C:\Backup\HKCU_full.reg
```

---

## 常用注册表位置速查

| 功能 | 路径 |
|------|------|
| 用户启动项 | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` |
| 系统启动项 | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` |
| 文件关联 | `HKCU\Software\Classes` |
| 卸载程序列表 | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` |
| 环境变量（系统） | `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment` |
| 环境变量（用户） | `HKCU\Environment` |
| 右键菜单（文件） | `HKCR\*\shell` 或 `HKCR\*\shellex` |
| 右键菜单（桌面） | `HKCR\Directory\Background\shell` |

---

## Linux 文件权限

```bash
# 查看权限
ls -la /path/to/file
stat /path/to/file

# 修改权限（八进制）
chmod 755 script.sh    # rwxr-xr-x
chmod 644 config.ini   # rw-r--r--
chmod -R 755 /var/www  # 递归

# 修改所有者
chown user:group file
chown -R www-data:www-data /var/www

# setuid / setgid / sticky bit
chmod u+s /usr/bin/sudo   # setuid（以文件所有者权限运行）
chmod +t /tmp             # sticky bit（只有所有者可删除）

# sudo 配置
visudo
# 添加免密：username ALL=(ALL) NOPASSWD: ALL
```
