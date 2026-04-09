# DrawIO 跨平台本地导出规范

## 目标

在不使用管理员权限、不上传远程服务的前提下，实现跨平台自动导出。

## Provider 策略

固定为本地链路：

1. `local-cli`（本机已安装或 bootstrap 下载的 draw.io CLI）
2. `user-node`（可选；通过 `DRAWIO_USER_NODE_CMD` 显式配置）

禁止使用 `remote-export`。

## 默认参数

- `formats`: `png,svg`
- `png_scale`: `4`
- `provider`: `auto`
- `auto_fix`: `false`
- `max_iterations`: `2`

## 统一导出命令

```bash
python scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4
```

## 导出产物清单（Artifact Manifest）

导出成功后输出 JSON，至少包含：

- `provider`
- `input`
- `outputs[]`（每项包含 `format` 和 `path`）
- PNG 输出额外包含 `scale`

## 错误码

- `E_UNSUPPORTED_PROVIDER`: 传入了不支持的 provider
- `E_NO_PROVIDER`: 本地 provider 不可用
- `E_INPUT_NOT_FOUND`: 输入文件不存在
- `E_EXPORT_FAILED`: 导出命令执行失败

## 约束

- 只允许本地导出，不允许远程上传 XML。
- 只允许用户态安装，不允许系统级修改。
