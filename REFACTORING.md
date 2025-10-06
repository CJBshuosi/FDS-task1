# 重构说明文档 (Refactoring Documentation)

## 重构概述

本次重构将 FDS-task1 项目从简单的脚本结构重构为标准的 Python 包结构，大大提高了代码的可维护性、可读性和可扩展性。

## 重构分支

- **分支名称**: `refactor`
- **基于**: `main` 分支
- **提交**: 2 个重构提交

## 主要改进

### 1. 标准化项目结构

**重构前:**
```
FDS-task1/
├── main.py
├── task1_1/
│   └── Compute_vector_clocks.py
├── task1_2/
│   └── Build_G.py
├── task1_3/
│   └── reduction_redundant_edges.py
└── data_vector/
```

**重构后:**
```
FDS-task1/
├── src/                          # 源代码目录
│   ├── __init__.py
│   ├── main.py                   # 主入口（带 CLI）
│   ├── vector_clock/             # 向量时钟模块
│   │   ├── __init__.py
│   │   └── compute.py
│   ├── graph/                    # 图构建和分析模块
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   └── reduction.py
│   └── utils/                    # 工具模块
│       ├── __init__.py
│       └── io.py
├── data_vector/                  # 数据目录
├── requirements.txt              # 依赖列表
├── setup.py                      # 包安装配置
├── .gitignore                    # Git 忽略文件
├── README.md                     # 项目文档
└── REFACTORING.md               # 本文档
```

### 2. 代码质量改进

#### a) 类型提示 (Type Hints)
所有函数都添加了完整的类型提示，提高代码可读性和 IDE 支持。

**示例:**
```python
# 重构前
def find_root(data):
    for branch in data:
        ...

# 重构后
def find_root(data: Dict[str, Dict[str, List[str]]]) -> Tuple[str, str]:
    """
    Find the root event (event with no parents) in the DAG.
    ...
    """
```

#### b) 文档字符串 (Docstrings)
所有模块和函数都添加了详细的文档字符串，包括：
- 功能描述
- 参数说明
- 返回值说明
- 异常说明
- 使用示例

#### c) 改进的命名规范
- `causally_precedes` → `is_causally_before` (更清晰)
- `build_edges` → `build_causal_edges` (更具描述性)
- `reduction` → `reduce_transitive_edges` (更明确)

#### d) 错误处理
添加了完善的异常处理和错误消息。

### 3. 模块化设计

#### vector_clock 模块
- `compute.py`: 向量时钟计算
  - `find_root()`: 查找根事件
  - `get_parents()`: 获取父事件
  - `build_event_graph()`: 构建事件图
  - `kahns_algorithm()`: Kahn 拓扑排序
  - `compute_vector_clock()`: 计算向量时钟

#### graph 模块
- `builder.py`: 图构建
  - `is_causally_before()`: 判断因果关系
  - `build_causal_edges()`: 构建因果边
  - `create_graph()`: 创建 NetworkX 图
  
- `reduction.py`: 图简化
  - `compute_reachability()`: 计算可达性
  - `reduce_transitive_edges()`: 传递边简化

#### utils 模块
- `io.py`: I/O 操作
  - `load_json()`: 加载 JSON 文件
  - `save_json()`: 保存 JSON 文件
  - `export_graph_to_dot()`: 导出 DOT 图

### 4. 增强的主程序

#### 命令行界面 (CLI)
使用 `argparse` 添加了完整的 CLI 支持：

```bash
# 基本使用
python -m src.main

# 详细输出
python -m src.main -v

# 自定义输入输出
python -m src.main -i custom_data.json -o output/

# 跳过某些步骤
python -m src.main --no-full-graph
```

#### 支持的选项
- `-i, --input`: 输入文件路径
- `-o, --output-dir`: 输出目录
- `--no-full-graph`: 跳过完整图生成
- `--no-reduced-graph`: 跳过简化图生成
- `-v, --verbose`: 详细输出模式
- `-h, --help`: 帮助信息

### 5. 项目配置文件

#### requirements.txt
列出所有 Python 依赖：
- networkx>=3.0
- pydot>=1.4.2

#### setup.py
支持 pip 安装：
```bash
pip install -e .
```

#### .gitignore
标准 Python 项目忽略规则。

#### README.md
包含：
- 项目介绍
- 安装说明
- 使用示例
- API 文档
- 算法说明

## 兼容性

旧代码（`task1_1/`, `task1_2/`, `task1_3/`）仍然保留在项目中作为参考，不影响新代码运行。

## 使用方法

### 方法 1: 作为模块运行
```bash
python -m src.main -v
```

### 方法 2: 直接运行
```bash
cd src
python main.py -v
```

### 方法 3: 安装后使用
```bash
pip install -e .
fds-analyze -v
```

## 测试验证

重构后的代码已通过测试：
```bash
$ python -m src.main -v
Loading data from data_vector/FDS_data.json...
Computing vector clocks...
Computed vector clocks for 8 events
Vector clocks: {'B1': [0, 1, 0, 0], 'B2': [0, 2, 0, 0], ...}
Saved vector clocks to data_vector/vector_clocks.json
Building full causal graph...
Full graph: 8 nodes, 19 edges
Saved full graph to data_vector/full_edges.dot
Reducing transitive edges...
Reduced graph: 8 nodes, 9 edges
Saved reduced graph to data_vector/reduced_edges.dot
✓ Causal analysis completed successfully!
```

## 下一步建议

### 短期改进
1. 添加单元测试（使用 pytest）
2. 添加代码格式化配置（black, flake8）
3. 添加类型检查配置（mypy）
4. 添加 CI/CD 配置

### 中期改进
1. 支持更多输入格式
2. 添加图可视化功能
3. 性能优化（大规模数据）
4. 添加更多分析功能

### 长期改进
1. Web 界面
2. 实时分析
3. 分布式处理
4. 机器学习集成

## 贡献者

- FDS Team

## 参考资料

- Vector Clocks: Lamport, L. "Time, clocks, and the ordering of events in a distributed system"
- Kahn's Algorithm: https://www.baeldung.com/cs/dag-topological-sort
- NetworkX Documentation: https://networkx.org/
