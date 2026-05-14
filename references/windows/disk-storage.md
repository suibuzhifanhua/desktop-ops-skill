# 磁盘清理 & 存储分析参考

## 快速查看磁盘占用

### Windows
```powershell
# 各驱动器剩余空间
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N="Used(GB)";E={[math]::Round($_.Used/1GB,2)}}, @{N="Free(GB)";E={[math]::Round($_.Free/1GB,2)}}

# 查某目录下各子目录大小（排序）
Get-ChildItem C:\ -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($size/1GB,2)}
} | Sort-Object SizeGB -Descending
```

### macOS / Linux
```bash
df -h
du -sh /* 2>/dev/null | sort -rh | head -20
du -sh ~/Downloads/* | sort -rh | head -20
```

---

## Windows 安全清理目标

| 目录/操作 | 说明 | 命令 |
|-----------|------|------|
| `%TEMP%` | 用户临时文件 | `rd /s /q %TEMP%` |
| `C:\Windows\Temp` | 系统临时文件 | 需管理员权限 |
| WinSxS 压缩 | 组件存储压缩 | `dism /online /cleanup-image /startcomponentcleanup` |
| 休眠文件 | hiberfil.sys | `powercfg -h off`（禁用休眠） |
| 页面文件 | pagefile.sys | 系统设置 → 高级 → 性能 |
| 旧系统备份 | Windows.old | `cleanmgr` → 清理系统文件 |

```powershell
# 磁盘清理（静默模式）
cleanmgr /sagerun:1

# DISM 清理组件存储
dism /online /cleanup-image /startcomponentcleanup /resetbase
```

---

## Docker / 开发环境清理

```bash
# Docker 清理（⚠️ 会删除未使用的镜像/容器/卷）
docker system prune -af --volumes

# npm 缓存
npm cache clean --force

# pip 缓存
pip cache purge

# conda 缓存
conda clean --all -y
```

---

## 大文件定位工具推荐

- **Windows**：WinDirStat、TreeSize Free、SpaceSniffer
- **macOS**：DaisyDisk、OmniDiskSweeper
- **Linux**：`ncdu`（`apt install ncdu`）、`dust`

---

## ⚠️ 操作注意事项

1. 删除前先确认文件用途，`%TEMP%` 内正被使用的文件会删除失败（跳过即可）
2. `Windows.old` 删除后无法回滚系统升级
3. DISM `/resetbase` 会使已安装的更新无法卸载，慎用
