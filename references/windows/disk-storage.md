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

- **Windows**：[WinDirStat](https://windirstat.net/)｜[TreeSize Free](https://www.jam-software.com/treesize_free)｜[SpaceSniffer](http://www.uderzo.it/main_products/space_sniffer/)
- **macOS**：[DaisyDisk](https://daisydiskapp.com/)｜[OmniDiskSweeper](https://www.omnigroup.com/more/)
- **Linux**：[ncdu](https://dev.yorhi.nl/ncdu)（`apt install ncdu`）｜[dust](https://github.com/bootandy/dust)（`cargo install du-dust`）

---

## ⚠️ 操作注意事项

1. 删除前先确认文件用途，`%TEMP%` 内正被使用的文件会删除失败（跳过即可）
2. `Windows.old` 删除后无法回滚系统升级
3. DISM `/resetbase` 会使已安装的更新无法卸载，慎用

---

## 桌面换盘（通过注册表迁移桌面路径）

> 来源：[Fisheep的新世界](https://fisheep.fun/yummy/78)

C 盘空间不足时，可将桌面文件夹迁移到其他分区，减少系统盘占用。

### 操作步骤

1. **Win + R** 打开运行，输入 `regedit` 回车
2. 定位到：
   ```
   HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
   ```
3. 在右侧找到 **Desktop** 项，双击修改
4. 将值改为目标路径，例如 `D:\Desktop`
5. 重启或注销后生效

> ⚠️ 修改前先在目标位置创建好文件夹；修改后原桌面文件不会自动迁移，需手动复制。
