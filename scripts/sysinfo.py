#!/usr/bin/env python3
"""
sysinfo.py - 系统基本信息一键采集
用法: python scripts/sysinfo.py
将输出粘贴到对话中帮助 AI 快速定位问题
"""
import platform
import socket
import sys
import os


def bytes_to_gb(b):
    return round(b / (1024 ** 3), 2)


def get_cpu_info():
    try:
        import psutil
        cpu = {
            "物理核心数": psutil.cpu_count(logical=False),
            "逻辑核心数": psutil.cpu_count(logical=True),
            "当前使用率": f"{psutil.cpu_percent(interval=1)}%",
            "频率(MHz)": round(psutil.cpu_freq().current, 1) if psutil.cpu_freq() else "N/A",
        }
        return cpu
    except ImportError:
        return {"错误": "psutil 未安装，运行: pip install psutil"}


def get_memory_info():
    try:
        import psutil
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "总内存(GB)": bytes_to_gb(mem.total),
            "已用(GB)": bytes_to_gb(mem.used),
            "可用(GB)": bytes_to_gb(mem.available),
            "使用率": f"{mem.percent}%",
            "交换空间(GB)": bytes_to_gb(swap.total),
        }
    except ImportError:
        return {"错误": "psutil 未安装"}


def get_disk_info():
    try:
        import psutil
        disks = []
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "挂载点": part.mountpoint,
                    "设备": part.device,
                    "文件系统": part.fstype,
                    "总大小(GB)": bytes_to_gb(usage.total),
                    "已用(GB)": bytes_to_gb(usage.used),
                    "剩余(GB)": bytes_to_gb(usage.free),
                    "使用率": f"{usage.percent}%",
                })
            except PermissionError:
                pass
        return disks
    except ImportError:
        return [{"错误": "psutil 未安装"}]


def get_network_info():
    try:
        import psutil
        interfaces = []
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for name, addr_list in addrs.items():
            stat = stats.get(name)
            for addr in addr_list:
                if addr.family == socket.AF_INET:
                    interfaces.append({
                        "网卡": name,
                        "IP": addr.address,
                        "掩码": addr.netmask,
                        "状态": "UP" if (stat and stat.isup) else "DOWN",
                        "速度(Mbps)": stat.speed if stat else "N/A",
                    })
        return interfaces
    except ImportError:
        return [{"错误": "psutil 未安装"}]


def print_section(title, data):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"  {k}: {v}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if i > 0:
                print(f"  {'-'*30}")
            for k, v in item.items():
                print(f"  {k}: {v}")


def main():
    print("\n" + "="*50)
    print("  系统信息摘要 (desktop-ops sysinfo)")
    print("="*50)

    # 基本系统信息
    sys_info = {
        "操作系统": platform.system(),
        "版本": platform.version(),
        "发行版": platform.release(),
        "架构": platform.machine(),
        "处理器": platform.processor() or "N/A",
        "主机名": socket.gethostname(),
        "Python版本": sys.version.split()[0],
    }
    print_section("操作系统", sys_info)
    print_section("CPU", get_cpu_info())
    print_section("内存", get_memory_info())

    disk_info = get_disk_info()
    print_section("磁盘", disk_info)

    net_info = get_network_info()
    print_section("网络接口", net_info)

    print(f"\n{'='*50}")
    print("  采集完成，请将以上信息粘贴到对话中")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
