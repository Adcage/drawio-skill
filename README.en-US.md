

# DrawIO Diagram Drawing Skill Library

A professional DrawIO diagram drawing knowledge base, providing complete UML diagram and system design diagram drawing specifications and templates.

## 📋 Project Overview

This project provides AI assistants with professional DrawIO diagram drawing capabilities, supporting various UML and system design diagram types. Through standardized color schemes, consistent element styles, and clear layout principles, it can quickly generate XML format files that comply with DrawIO standards.

## ✨ Core Features

- **Comprehensive Coverage** - Supports 9 commonly used diagram types
- **Unified Standards** - Standardized color schemes and style specifications
- **Ready to Use** - Generated files can be opened directly in DrawIO
- **Professional Quality** - Follows UML standards and best practices

## 📊 Supported Diagram Types

### UML Diagrams

| Diagram Type     | Description                                      | Applicable Scenarios                        |
| ---------------- | ------------------------------------------------ | ------------------------------------------- |
| **Sequence Diagram**   | Displays time-ordered interactions between objects       | API call flows, user operation flows                |
| **Use Case Diagram**   | Displays system functions and actor relationships        | Requirement analysis, system function overview        |
| **Class Diagram**    | Displays class structures and relationships            | Code structure design, data model design          |
| **Activity Diagram**   | Displays business or algorithm processes             | Business process modeling, algorithm flow presentation  |
| **Package Diagram**   | Displays the modular structure of the system           | System architecture design, module division           |
| **Communication Diagram** | Displays collaborative relationships between objects     | Object collaboration patterns, message passing relationships |

### Architecture Diagrams

| Diagram Type      | Description                                              | Applicable Scenarios                        |
| ----------------- | -------------------------------------------------------- | ------------------------------------------- |
| **BCE Diagram**   | Displays the Boundary-Control-Entity three-layer architecture | Software architecture design, separation of concerns design |
| **VOPC Diagram**  | Domain-specific diagram                                  | Used according to actual requirements       |

### General Diagrams

Supports custom diagram requirements such as flowcharts, architecture diagrams, and mind maps.

## 🎨 Unified Color Scheme

All diagrams follow a unified color system to ensure visual consistency:

| Color Name | Color Code  | Usage                             |
| ---------- | ----------- | --------------------------------- |
| Primary    | `#3366CC`   | Main components, UI layer, actors |
| Secondary 1| `#22D3EE`   | Service layer, secondary function components |
| Secondary 2| `#27BC9F`   | Control layer, optional functions  |
| Secondary 3| `#6FA3FF`   | Data layer, sub-process containers |
| Secondary 4| `#8B5CF6`   | Special components, third-party integrations |
| Accent     | `#EF4444`   | Errors, exceptions, warnings      |

## 📁 Project Structure

```
drawio-skill/
├── SKILL.md                         # Skill overview and decision tree
├── README.md                        # Usage instructions
├── LICENSE
├── base/
│   ├── drawio-basics.md
│   ├── drawio-export-cross-platform.md
│   ├── drawio-environment-setup.md
│   └── drawio-auto-fix.md
├── diagrams/
│   ├── drawio-activity-diagram.md
│   ├── drawio-agents.md
│   ├── drawio-bce.md
│   ├── drawio-class-diagram.md
│   ├── drawio-communication.md
│   ├── drawio-pkg.md
│   ├── drawio-sequence-diagram.md
│   ├── drawio-use-case.md
│   └── drawio-vopc.md
├── scripts/
│   ├── drawio_preflight.py
│   ├── drawio_bootstrap.py
│   ├── drawio_export.py
│   ├── drawio_layout_check.py
│   └── drawio_auto_fix.py
└── examples/
    └── minimal.drawio
```

## 🚀 Quick Start

### Automatic Export (New)

This repository now includes local automatic export capabilities (no administrator privileges required, remote uploads disabled).

1. Run pre-check

```bash
python scripts/drawio_preflight.py
```

2. If the pre-check fails, run the user-mode bootstrap (automatically downloads the local draw.io CLI)

```bash
python scripts/drawio_bootstrap.py --non-admin
```

3. Execute high-quality export (default `png,svg`, PNG scale=4)

```bash
python scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4
```

4. Optional: Enable automatic layout check and fix

```bash
python scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4 --auto-fix --max-iterations 2
```

Platform script entry points:

- Windows: `pwsh -File scripts/run_smoke_test.ps1`
- macOS/Linux: `bash scripts/run_smoke_test.sh`

### Diagram Type Decision

Choose the appropriate diagram type based on your needs:

- **Display time-ordered interactions** → Sequence Diagram
- **Display system functions** → Use Case Diagram
- **Display class structure** → Class Diagram
- **Display business processes** → Activity Diagram
- **Display modular architecture** → Package Diagram
- **Display object collaboration** → Communication Diagram
- **Display three-layer architecture** → BCE Diagram

### Usage Workflow

1. Review `SKILL.md` to understand the full capabilities and decision tree
2. Read `base/drawio-basics.md` to understand the basics
3. Select the corresponding diagram type documentation based on your needs
4. Generate DrawIO XML code according to the specifications
5. Save as a `.drawio` file and open it in DrawIO
6. If export is needed, call the automatic export script to generate `png/svg/pdf`

### Automatic Export Strategy

- Provider priority: `local-cli -> user-node(optional configuration)`
- Remote export: Disabled
- Default export formats: `png,svg`
- Default PNG quality: `--png-scale 4`
- Default self-check and fix: Off (enable as needed)

## 📖 Documentation Overview

### SKILL.md

Skill overview document, containing:

- Complete diagram type decision tree
- Detailed descriptions of each diagram type
- Unified color scheme specifications
- Workflow and quality standards

### base/drawio-basics.md

DrawIO basics, containing:

- File structure and key parameters
- Core element types (vertices, edges)
- Geometric and style attributes
- Common element templates
- Layout principles and naming conventions

### diagrams/*.md

Detailed drawing specifications for each diagram type, containing:

- Diagram positioning and usage scenarios
- Core drawing specifications
- Element styles and layout standards
- Complete example code
- Quality checklists

## 🎯 Usage Examples

### Example 1: Creating a User Login Sequence Diagram

**Requirement**: Display the complete user login process

**Steps**:

1. Identify keyword "Sequence Diagram" → Use `diagrams/drawio-sequence-diagram.md`
2. Identify actors: User, Frontend, Backend, Database
3. Identify message flows: Input credentials → Send request → Validate → Return result
4. Generate XML applying sequence diagram specifications
5. Apply unified color scheme
6. Output `sequence-user-login.drawio`

### Example 2: Creating an E-commerce System Use Case Diagram

**Requirement**: Display the functions and actors of the e-commerce system

**Steps**:

1. Identify keyword "Use Case Diagram" → Use `diagrams/drawio-use-case.md`
2. Identify actors: User, Administrator
3. Identify use cases: Browse products, Place order, Payment, Product management, Order management
4. Establish association relationships
5. Apply use case diagram specifications
6. Output `usecase-ecommerce-system.drawio`

## 📝 File Naming Convention

```
[diagram-type]-[topic-description].drawio
```

**Examples**:

- `sequence-user-login.drawio` - User login sequence diagram
- `usecase-order-system.drawio` - Order system use case diagram
- `class-user-model.drawio` - User model class diagram

## ✅ Quality Standards

- **Correct Format** - Can be opened directly by DrawIO
- **Reasonable Layout** - No overlapping elements, appropriate spacing
- **Color Compliance** - Strictly follows the color scheme
- **Clear Labels** - Concise and clear labels
- **Explicit Relationships** - Clear connectors, correct arrow directions
- **Standard Compliant** - Follows corresponding UML standards

## 🤝 Contribution Guidelines

Feel free to submit Issues and Pull Requests to improve this project.

## 📄 License

This project is licensed under the MIT License.

## 📮 Contact

For questions or suggestions, feel free to contact us via GitHub Issues.
