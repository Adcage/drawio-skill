# DrawIO基础知识参考

## 概述

本文档提供DrawIO图表绘制的基础知识，适用于所有图表类型。在绘制具体图表前，建议先了解这些基础概念。

---

## 一、文件基础结构

### 1.1 完整XML结构

```xml
<mxfile host="65bd71144e">
    <diagram name="图表名称" id="diagram-001">
        <mxGraphModel dx="1800" dy="1104"
                      grid="1" gridSize="10"
                      guides="1" tooltips="1"
                      connect="1" arrows="1"
                      fold="1" page="1"
                      pageScale="1"
                      pageWidth="1400" pageHeight="1200"
                      math="0" shadow="1">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <!-- 在此添加图形元素 -->
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

### 1.2 关键参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `dx/dy` | 视图缩放和偏移 | dx="1800" dy="1104" |
| `grid` | 是否启用网格 | "1"（启用）或 "0"（关闭）|
| `gridSize` | 网格大小 | "10" |
| `pageWidth` | 画布宽度 | 1400-2000 |
| `pageHeight` | 画布高度 | 800-1200 |
| `shadow` | 是否启用阴影 | "1"（推荐）|

**画布尺寸建议**：
- 简单流程：1400 x 800
- 中等复杂度：1400 x 1000
- 复杂流程：1400 x 1200 或更大

---

## 二、核心元素类型

### 2.1 mxCell基础概念

DrawIO中的所有元素都是`mxCell`，分为两种类型：

#### **顶点元素（Vertex）**
表示节点、形状、对象等独立元素。

```xml
<mxCell id="node1"
        value="节点文本"
        style="样式属性"
        parent="1"
        vertex="1">
    <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

#### **边元素（Edge）**
表示连接线、箭头等连接关系。

```xml
<mxCell id="edge1"
        value="连接线文本"
        style="样式属性"
        parent="1"
        source="node1"
        target="node2"
        edge="1">
    <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 2.2 必需属性

| 属性 | 说明 | 示例 |
|------|------|------|
| `id` | 元素唯一标识 | "node1", "edge2" |
| `parent` | 父元素ID | "1"（通常是根容器）|
| `vertex` | 是否为顶点 | "1"（顶点）|
| `edge` | 是否为边 | "1"（连接线）|
| `source` | 连接线起点ID | "node1" |
| `target` | 连接线终点ID | "node2" |

---

## 三、几何属性 (Geometry)

### 3.1 顶点几何属性

```xml
<mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
```

| 属性 | 说明 | 单位 |
|------|------|------|
| `x` | 左上角X坐标 | 像素 |
| `y` | 左上角Y坐标 | 像素 |
| `width` | 元素宽度 | 像素 |
| `height` | 元素高度 | 像素 |

### 3.2 边几何属性

```xml
<mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="150" as="sourcePoint"/>
    <mxPoint x="400" y="150" as="targetPoint"/>
</mxGeometry>
```

**relative="1"**: 使用相对定位，自动连接到source和target元素。

---

## 四、样式属性 (Style)

### 4.1 样式字符串格式

样式属性是由分号分隔的键值对字符串：

```
style="fillColor=#3366CC;strokeColor=#3366CC;fontColor=#FFFFFF;fontSize=16"
```

### 4.2 常用样式属性

#### **颜色属性**

| 属性 | 说明 | 示例 |
|------|------|------|
| `fillColor` | 填充颜色 | `#3366CC` |
| `strokeColor` | 边框颜色 | `#3366CC` |
| `fontColor` | 文字颜色 | `#FFFFFF` |

#### **尺寸和边框**

| 属性 | 说明 | 示例 |
|------|------|------|
| `fontSize` | 字体大小 | `16` |
| `strokeWidth` | 边框宽度 | `2` |
| `rounded` | 圆角 | `1`（启用）|

#### **形状类型**

| 属性值 | 说明 | 用途 |
|--------|------|------|
| `shape=rectangle` | 矩形 | 通用容器 |
| `shape=ellipse` | 椭圆 | 用例、状态 |
| `shape=umlActor` | UML参与者 | 用例图 |
| `shape=umlLifeline` | 生命线 | 时序图 |
| `shape=rhombus` | 菱形 | 决策节点 |
| `shape=hexagon` | 六边形 | 准备/数据 |

#### **线条样式**

| 属性 | 说明 | 值 |
|------|------|-----|
| `dashed` | 虚线 | `1`（虚线）`0`（实线）|
| `endArrow` | 终点箭头 | `classic`（标准箭头）<br>`block`（实心箭头）<br>`none`（无箭头）|
| `startArrow` | 起点箭头 | 同上 |
| `edgeStyle` | 边样式 | `orthogonalEdgeStyle`（直角）<br>`elbowEdgeStyle`（肘形）|

---

## 五、统一配色方案

### 5.1 核心颜色体系

**所有图表类型必须遵循以下配色方案：**

```javascript
主色调    = #3366CC  // 深蓝色 - 主要组件、界面层、参与者
副色调1   = #22D3EE  // 青色 - 服务层、次要功能
副色调2   = #27BC9F  // 绿色 - 控制层、可选功能
副色调3   = #6FA3FF  // 浅蓝 - 数据层、子流程
副色调4   = #8B5CF6  // 紫色 - 特殊组件、第三方集成
强调色    = #EF4444  // 红色 - 错误、异常、警告
```

### 5.2 分层架构颜色（适用于时序图、BCE图等）

| 层级 | 颜色 | 用途 |
|------|------|------|
| **界面层** | `#3366CC` | 用户界面、UI组件 |
| **控制层** | `#27BC9F` | 控制器、请求处理 |
| **服务层** | `#22D3EE` | 业务逻辑、服务 |
| **数据层** | `#6FA3FF` | 数据库、缓存 |

### 5.3 辅助元素颜色

| 元素类型 | 背景色 | 边框色 | 用途 |
|---------|--------|--------|------|
| **前置说明** | `#FFFFCC` | `#999999` | 前置条件注释 |
| **分支说明** | `#FFF4E6` | `#FF9800` | 条件分支标记 |
| **错误说明** | `#FFE6E6` | `#EF4444` | 错误原因注释 |
| **生命线** | - | `#666666` | 对象生命线（虚线）|

### 5.4 文本颜色规范

```javascript
// 深色背景上使用白色文字
fillColor=#3366CC → fontColor=#FFFFFF

// 浅色背景上使用深色文字
fillColor=#FFFFCC → fontColor=#333333
```

---

## 六、常用元素模板

### 6.1 矩形容器

```xml
<mxCell id="rect1"
        value="矩形容器"
        style="rounded=0;whiteSpace=wrap;html=1;
               fillColor=#3366CC;strokeColor=#3366CC;
               fontColor=#FFFFFF;fontSize=16;"
        parent="1" vertex="1">
    <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

### 6.2 圆角矩形

```xml
<mxCell id="roundRect1"
        value="圆角矩形"
        style="rounded=1;whiteSpace=wrap;html=1;
               fillColor=#22D3EE;strokeColor=#22D3EE;
               fontColor=#FFFFFF;fontSize=16;"
        parent="1" vertex="1">
    <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```

### 6.3 椭圆

```xml
<mxCell id="ellipse1"
        value="椭圆"
        style="ellipse;whiteSpace=wrap;html=1;
               fillColor=#6FA3FF;strokeColor=#6FA3FF;
               fontColor=#FFFFFF;fontSize=16;"
        parent="1" vertex="1">
    <mxGeometry x="100" y="300" width="120" height="60" as="geometry"/>
</mxCell>
```

### 6.4 菱形（决策节点）

```xml
<mxCell id="diamond1"
        value="决策"
        style="rhombus;whiteSpace=wrap;html=1;
               fillColor=#8B5CF6;strokeColor=#8B5CF6;
               fontColor=#FFFFFF;fontSize=16;"
        parent="1" vertex="1">
    <mxGeometry x="100" y="400" width="120" height="80" as="geometry"/>
</mxCell>
```

### 6.5 标准连接线（实线箭头）

```xml
<mxCell id="edge1"
        value="调用"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;
               orthogonalLoop=1;jettySize=auto;html=1;
               strokeColor=#3366CC;strokeWidth=2;
               endArrow=classic;fontSize=14;"
        parent="1" source="rect1" target="ellipse1" edge="1">
    <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 6.6 虚线箭头（返回消息）

```xml
<mxCell id="edge2"
        value="返回"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;
               orthogonalLoop=1;jettySize=auto;html=1;
               strokeColor=#3366CC;strokeWidth=2;
               dashed=1;dashPattern=8 8;
               endArrow=classic;fontSize=14;"
        parent="1" source="ellipse1" target="rect1" edge="1">
    <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 七、布局原则

### 7.1 元素间距

| 场景 | 推荐间距 |
|------|---------|
| 水平间距 | 150-200px |
| 垂直间距 | 100-150px |
| 最小间距 | 80px |
| 分组间距 | 200-300px |

### 7.2 对齐原则

✅ **统一对齐** - 同层级元素左对齐或居中对齐
✅ **垂直分布** - 垂直方向等间距分布
✅ **水平分布** - 水平方向等间距分布
✅ **网格吸附** - 启用网格时，坐标为gridSize的倍数

### 7.3 元素大小规范

| 元素类型 | 推荐宽度 | 推荐高度 |
|---------|---------|---------|
| 普通矩形 | 120-180 | 60-80 |
| 参与者/Actor | 60 | 120 |
| 用例椭圆 | 160 | 80 |
| 类图矩形 | 180-240 | 120-200 |
| 决策菱形 | 120 | 80 |
| 注释框 | 200-300 | 60-100 |

---

## 八、ID命名规范

### 8.1 推荐命名模式

```javascript
// 顶点元素
actor-1, actor-2          // 参与者
ui-1, ui-2                // 界面元素
controller-1              // 控制器
service-1                 // 服务
db-1                      // 数据库
uc-1, uc-2                // 用例
class-1                   // 类

// 边元素
edge-1, edge-2            // 通用连接线
msg-1, msg-2              // 消息
call-1                    // 调用
return-1                  // 返回
assoc-1                   // 关联

// 辅助元素
note-1                    // 注释
frame-1                   // 框架
group-1                   // 分组
```

### 8.2 ID规则

✅ **唯一性** - 同一diagram中ID必须唯一
✅ **描述性** - 使用有意义的前缀
✅ **连续性** - 同类元素使用连续编号
✅ **小写** - 推荐使用小写字母
✅ **连字符** - 使用连字符分隔单词

---

## 九、特殊元素

### 9.1 文本标签

```xml
<mxCell id="label1"
        value="这是一个说明文本"
        style="text;html=1;strokeColor=none;fillColor=none;
               align=center;verticalAlign=middle;
               whiteSpace=wrap;rounded=0;
               fontSize=14;fontColor=#333333;"
        parent="1" vertex="1">
    <mxGeometry x="100" y="50" width="200" height="30" as="geometry"/>
</mxCell>
```

### 9.2 注释框

```xml
<mxCell id="note1"
        value="注释说明"
        style="shape=note;whiteSpace=wrap;html=1;
               backgroundOutline=1;darkOpacity=0.05;
               fillColor=#FFFFCC;strokeColor=#999999;
               fontColor=#333333;fontSize=14;"
        parent="1" vertex="1">
    <mxGeometry x="500" y="100" width="200" height="80" as="geometry"/>
</mxCell>
```

### 9.3 分组容器

```xml
<mxCell id="group1"
        value="系统边界"
        style="swimlane;whiteSpace=wrap;html=1;
               fillColor=#f5f5f5;strokeColor=#666666;
               fontColor=#333333;fontSize=16;"
        parent="1" vertex="1">
    <mxGeometry x="50" y="50" width="600" height="400" as="geometry"/>
</mxCell>
```

---

## 十、质量检查清单

### 10.1 结构检查

- [ ] XML格式正确，可被DrawIO解析
- [ ] 所有mxCell有唯一ID
- [ ] root元素包含id="0"和id="1"
- [ ] 所有元素的parent属性正确

### 10.2 样式检查

- [ ] 使用统一配色方案
- [ ] 字体大小一致（推荐16）
- [ ] 深色背景使用白色文字
- [ ] 浅色背景使用深色文字

### 10.3 布局检查

- [ ] 元素无重叠
- [ ] 间距合理统一
- [ ] 对齐整齐
- [ ] 连接线不穿过其他元素

### 10.4 语义检查

- [ ] 连接线的source和target正确
- [ ] 箭头方向表达正确的关系
- [ ] 标签文字清晰准确
- [ ] 符合对应图表类型的UML规范

---

## 十一、常见问题

### Q1: 如何确保元素ID唯一？

A: 使用有意义的前缀+编号，如`actor-1`, `service-2`。在生成XML前检查是否有重复ID。

### Q2: 连接线为什么不显示？

A: 检查：
1. source和target的ID是否存在
2. edge="1"属性是否设置
3. geometry是否包含relative="1"

### Q3: 中文显示乱码怎么办？

A: 确保：
1. 文件编码为UTF-8
2. XML声明包含encoding="UTF-8"
3. value属性中的中文正确转义

### Q4: 如何让线条不穿过其他元素？

A:
1. 调整元素位置，留出足够空间
2. 使用`edgeStyle=orthogonalEdgeStyle`（直角线）
3. 手动添加waypoint调整路径

### Q5: 画布太小怎么办？

A: 调整mxGraphModel的pageWidth和pageHeight属性：
```xml
pageWidth="2000" pageHeight="1500"
```

---

## 十二、快速参考表

### 颜色速查

```
主色调: #3366CC    副色调1: #22D3EE    副色调2: #27BC9F
副色调3: #6FA3FF   副色调4: #8B5CF6    强调色: #EF4444
白色: #FFFFFF      深灰: #333333       浅灰: #999999
黄色注释: #FFFFCC  橙色分支: #FFF4E6   红色错误: #FFE6E6
```

### 常用形状速查

```
rectangle    - 矩形           ellipse      - 椭圆
rhombus      - 菱形           hexagon      - 六边形
umlActor     - UML参与者      umlLifeline  - UML生命线
cylinder     - 圆柱体         note         - 注释
swimlane     - 泳道           cloud        - 云形
```

### 箭头样式速查

```
classic      - 标准箭头       block        - 实心箭头
open         - 开放箭头       none         - 无箭头
diamond      - 菱形箭头       oval         - 椭圆箭头
```

---

## 总结

掌握这些DrawIO基础知识后，您可以：

1. ✅ 理解DrawIO文件的XML结构
2. ✅ 创建各种基本图形元素
3. ✅ 应用统一的配色方案
4. ✅ 设置正确的样式属性
5. ✅ 建立元素间的连接关系
6. ✅ 进行合理的布局设计

在绘制具体图表时，请参考对应的图表类型文档（如时序图、用例图等），它们会基于这些基础知识提供更具体的规范和示例。

---

**版本**: 1.0.0
**最后更新**: 2024-12-20
