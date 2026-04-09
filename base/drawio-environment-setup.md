# DrawIO 环境初始化（无管理员权限）

## 设计原则

- 无管理员权限（不使用 UAC/sudo）
- 首次运行允许联网下载依赖
- 所有缓存和安装目录仅在当前用户目录

## 标准流程

1. 预检：

```bash
python scripts/drawio_preflight.py
```

2. 预检不满足时执行 bootstrap：

```bash
python scripts/drawio_bootstrap.py --non-admin
```

可选参数：

```bash
# 仅查看将下载的 draw.io 资产
python scripts/drawio_bootstrap.py --non-admin --dry-run

# 强制重新下载并覆盖本地 CLI 配置
python scripts/drawio_bootstrap.py --non-admin --force
```

3. 再执行导出：

```bash
python scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4
```

## 平台路径

- Windows：`%LOCALAPPDATA%/drawio-skill`
- macOS：`~/Library/Application Support/drawio-skill`
- Linux：`~/.local/share/drawio-skill`

## 常见问题

### 1. 没有可用 provider

表现：`E_NO_PROVIDER`

处理：
- 先运行 `drawio_bootstrap.py --non-admin`
- 检查网络是否可访问 `github.com` 和 `api.github.com`

### 2. 导出命令失败

表现：`E_EXPORT_FAILED`

处理：
- 检查输入 `.drawio` 文件是否可被 draw.io 打开
- 检查输出目录权限
- 强制重新下载本地 CLI：`python scripts/drawio_bootstrap.py --non-admin --force`

### 3. 输入路径错误

表现：`E_INPUT_NOT_FOUND`

处理：
- 确认 `--input` 路径存在
