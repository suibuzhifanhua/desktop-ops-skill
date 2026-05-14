# 开机启动项 & 计划任务参考

## Windows 启动项管理

### 查看启动项位置

```powershell
# 注册表启动项（当前用户）
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
# 注册表启动项（所有用户）
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Run

# 启动文件夹
# 当前用户：%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
# 所有用户：%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup
explorer shell:startup
explorer shell:common startup
```

### 禁用 / 启用启动项

```powershell
# 通过注册表删除启动项
Remove-ItemProperty -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -Name "SomeApp"

# 通过任务管理器（推荐，有界面）
# taskmgr → 启动 Tab
```

---

## Windows 计划任务

```powershell
# 列出所有计划任务（含状态）
Get-ScheduledTask | Select-Object TaskName, State, TaskPath | Sort-Object TaskPath

# 查看任务详情
Get-ScheduledTask -TaskName "MyBackup" | Get-ScheduledTaskInfo

# 创建每日 9 点运行的任务
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\Scripts\backup.ps1"
Register-ScheduledTask -TaskName "DailyBackup" -Trigger $trigger -Action $action -RunLevel Highest

# 禁用 / 删除任务
Disable-ScheduledTask -TaskName "SomeTask"
Unregister-ScheduledTask -TaskName "SomeTask" -Confirm:$false

# 手动运行
Start-ScheduledTask -TaskName "DailyBackup"
```

---

## Linux Crontab

```bash
# 编辑当前用户 crontab
crontab -e

# 常用时间格式
# 分 时 日 月 周
# 0 9 * * 1-5    周一到周五 9:00
# */15 * * * *   每15分钟
# 0 2 * * 0      每周日 2:00

# 查看 crontab
crontab -l

# 系统级（root）
sudo crontab -e
# 或放到 /etc/cron.d/ /etc/cron.daily/ /etc/cron.weekly/

# 查看 cron 日志
grep CRON /var/log/syslog | tail -20
journalctl -u cron --since "1 hour ago"
```

---

## macOS LaunchAgent / LaunchDaemon

```bash
# 用户级（登录后运行）：~/Library/LaunchAgents/
# 系统级（开机运行）：/Library/LaunchDaemons/

# 加载 / 卸载
launchctl load ~/Library/LaunchAgents/com.example.myjob.plist
launchctl unload ~/Library/LaunchAgents/com.example.myjob.plist

# 列出所有 LaunchAgent
launchctl list | grep -v com.apple

# plist 模板
cat > ~/Library/LaunchAgents/com.myapp.backup.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.myapp.backup</string>
    <key>ProgramArguments</key>
    <array><string>/usr/bin/python3</string><string>/Users/me/backup.py</string></array>
    <key>StartCalendarInterval</key>
    <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
    <key>StandardOutPath</key><string>/tmp/backup.log</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
EOF
```

---

## 开机慢排查步骤

1. `msconfig` → 启动 → 禁用非必要项
2. 任务管理器 → 启动 → 按"启动影响"排序
3. 事件查看器 → 应用程序和服务日志 → Microsoft → Windows → Diagnostics-Performance → Operational
4. 检查杀软是否扫描启动文件夹
