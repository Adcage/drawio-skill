# DrawIO 自动布局检查与修复（可选）

## 触发条件

仅当用户明确要求“检查重叠/自动修复/优化布局”时启用。

默认关闭：`auto_fix=false`。

## 检查规则

- 节点重叠（bounding box 相交）
- 节点越界（超出 pageWidth/pageHeight）
- 最小间距不足（节点之间距离小于 `min_spacing`）

## 执行方式

### 仅检查

```bash
python scripts/drawio_layout_check.py --input examples/minimal.drawio --min-spacing 20
```

### 修复并输出新文件

```bash
python scripts/drawio_auto_fix.py --input examples/minimal.drawio --output outputs/minimal.fixed.drawio --min-spacing 20 --max-iterations 2
```

### 导出时一并修复

```bash
python scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4 --auto-fix --max-iterations 2
```

## 终止条件

- 问题全部清零
- 达到最大迭代次数（默认 2）

## 注意

- 自动修复只做几何层规则，不保证业务语义布局最优。
- 若修复后仍有问题，应人工调整关键节点坐标。
