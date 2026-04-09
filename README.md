# DrawIO 图表绘制技能库

一个专业的 DrawIO 图表绘制知识库，提供完整的 UML 图表和系统设计图表绘制规范与模板。

## 📋 项目简介

本项目为 AI 助手提供专业的 DrawIO 图表绘制能力，支持多种 UML 和系统设计图表类型。通过标准化的配色方案、规范的元素样式和清晰的布局原则，能够快速生成符合 DrawIO 标准的 XML 格式文件。

## ✨ 核心特性

- **全面覆盖** - 支持 9 种常用图表类型
- **统一规范** - 标准化的配色方案和样式规范
- **即用即开** - 生成的文件可直接在 DrawIO 中打开
- **专业质量** - 遵循 UML 标准和最佳实践

## 📊 支持的图表类型

### UML 图表

| 图表类型   | 说明                         | 适用场景                   |
| ---------- | ---------------------------- | -------------------------- |
| **时序图** | 展示对象之间按时间顺序的交互 | API 调用流程、用户操作流程 |
| **用例图** | 展示系统功能和参与者关系     | 需求分析、系统功能概览     |
| **类图**   | 展示类的结构和关系           | 代码结构设计、数据模型设计 |
| **活动图** | 展示业务流程或算法流程       | 业务流程建模、算法流程展示 |
| **包图**   | 展示系统的模块化结构         | 系统架构设计、模块划分     |
| **通信图** | 展示对象间的协作关系         | 对象协作模式、消息传递关系 |

### 架构图

| 图表类型    | 说明                                  | 适用场景                   |
| ----------- | ------------------------------------- | -------------------------- |
| **BCE 图**  | 展示 Boundary-Control-Entity 三层架构 | 软件架构设计、职责分离设计 |
| **VOPC 图** | 特定领域图表                          | 根据实际用途使用           |

### 通用图表

支持流程图、架构图、思维导图等自定义图表需求。

## 🎨 统一配色方案

所有图表遵循统一的配色体系，确保视觉一致性：

| 颜色名称 | 颜色代码  | 用途                     |
| -------- | --------- | ------------------------ |
| 主色调   | `#3366CC` | 主要组件、界面层、参与者 |
| 副色调 1 | `#22D3EE` | 服务层、次要功能组件     |
| 副色调 2 | `#27BC9F` | 控制层、可选功能         |
| 副色调 3 | `#6FA3FF` | 数据层、子流程容器       |
| 副色调 4 | `#8B5CF6` | 特殊组件、第三方集成     |
| 强调色   | `#EF4444` | 错误、异常、警告         |

## 📁 项目结构

```
drawio-skill/
├── drawio/                          # 旧版图表文档
│   ├── drawio-activity-diagram.md
│   ├── drawio-agents.md
│   ├── drawio-bce.md
│   ├── drawio-class-diagram.md
│   ├── drawio-communication.md
│   ├── drawio-pkg.md
│   ├── drawio-sequence-diagram.md
│   ├── drawio-use-case.md
│   └── drawio-vopc.md
│
├── drawio-diagram/                  # 主要技能文档
│   ├── base/
│   │   └── drawio-basics.md        # DrawIO 基础知识
│   ├── diagrams/
│   │   ├── drawio-activity-diagram.md    # 活动图规范
│   │   ├── drawio-agents.md              # 通用图表规范
│   │   ├── drawio-bce.md                 # BCE 图规范
│   │   ├── drawio-class-diagram.md       # 类图规范
│   │   ├── drawio-communication.md       # 通信图规范
│   │   ├── drawio-pkg.md                 # 包图规范
│   │   ├── drawio-sequence-diagram.md    # 时序图规范
│   │   ├── drawio-use-case.md            # 用例图规范
│   │   └── drawio-vopc.md                # VOPC 图规范
│   └── SKILL.md                     # 技能总览和决策树
│
└── README.md                        # 本文件
```

## 🚀 快速开始

### 自动导出（新增）

本仓库已增加本地自动导出能力（无管理员权限、禁止远程上传）。

1. 运行预检

```bash
python scripts/drawio_preflight.py
```

2. 若预检不满足，执行用户态 bootstrap（自动下载本地 draw.io CLI）

```bash
python scripts/drawio_bootstrap.py --non-admin
```

3. 执行高质量导出（默认 `png,svg`，PNG scale=4）

```bash
python scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4
```

4. 可选：启用自动布局检查与修复

```bash
python scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4 --auto-fix --max-iterations 2
```

平台脚本入口：

- Windows: `pwsh -File scripts/run_smoke_test.ps1`
- macOS/Linux: `bash scripts/run_smoke_test.sh`

### 图表类型决策

根据需求选择合适的图表类型：

- **展示时间顺序交互** → 时序图
- **展示系统功能** → 用例图
- **展示类结构** → 类图
- **展示业务流程** → 活动图
- **展示模块架构** → 包图
- **展示对象协作** → 通信图
- **展示三层架构** → BCE 图

### 使用流程

1. 查看 `SKILL.md` 了解完整能力和决策树
2. 阅读 `base/drawio-basics.md` 了解基础知识
3. 根据需求选择对应的图表类型文档
4. 按照规范生成 DrawIO XML 代码
5. 保存为 `.drawio` 文件并在 DrawIO 中打开
6. 如需导出，调用自动导出脚本生成 `png/svg/pdf`

### 自动导出策略

- Provider 优先级：`local-cli -> user-node(可选配置)`
- 远程导出：禁用
- 默认导出格式：`png,svg`
- 默认 PNG 质量：`--png-scale 4`
- 默认自检修复：关闭（按需开启）

## 📖 文档说明

### SKILL.md

技能总览文档，包含：

- 完整的图表类型决策树
- 各图表类型详细说明
- 统一配色规范
- 工作流程和质量标准

### base/drawio-basics.md

DrawIO 基础知识，包含：

- 文件结构和关键参数
- 核心元素类型（顶点、边）
- 几何属性和样式属性
- 常用元素模板
- 布局原则和命名规范

### diagrams/\*.md

各图表类型的详细绘制规范，包含：

- 图表定位和使用场景
- 核心绘制规范
- 元素样式和布局标准
- 完整示例代码
- 质量检查清单

## 🎯 使用示例

### 示例 1：创建用户登录时序图

**需求**：展示用户登录的完整流程

**步骤**：

1. 识别关键词"时序图" → 使用 `drawio-sequence-diagram.md`
2. 识别参与者：用户、前端、后端、数据库
3. 识别消息流：输入账号密码 → 发送请求 → 验证 → 返回结果
4. 应用时序图规范生成 XML
5. 使用统一配色方案
6. 输出 `sequence-user-login.drawio`

### 示例 2：创建电商系统用例图

**需求**：展示电商系统的功能和参与者

**步骤**：

1. 识别关键词"用例图" → 使用 `drawio-use-case.md`
2. 识别参与者：用户、管理员
3. 识别用例：浏览商品、下单、支付、商品管理、订单管理
4. 建立关联关系
5. 应用用例图规范
6. 输出 `usecase-ecommerce-system.drawio`

## 📝 文件命名规范

```
[图表类型]-[主题描述].drawio
```

**示例**：

- `sequence-user-login.drawio` - 用户登录时序图
- `usecase-order-system.drawio` - 订单系统用例图
- `class-user-model.drawio` - 用户模型类图

## ✅ 质量标准

- **格式正确** - 可被 DrawIO 直接打开
- **布局合理** - 元素无重叠，间距适当
- **颜色规范** - 严格遵循配色方案
- **标签清晰** - 中文标签简洁明了
- **关系明确** - 连接线清晰，箭头方向正确
- **符合规范** - 遵循对应 UML 标准

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进本项目。

## 📄 许可证

本项目采用 MIT 许可证。

## 📮 联系方式

如有问题或建议，欢迎通过 GitHub Issues 联系。

---

**版本**: 1.0.0  
**最后更新**: 2024-12-23
