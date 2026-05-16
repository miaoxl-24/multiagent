# Multi-Agent Customer Service System

基于 LangGraph 和 LangChain 的多 Agent 智能客服系统，支持旅游路线规划、笑话生成、对联创作等多种功能。

## 功能特性

- **智能分类路由**：自动识别用户问题类型并分配给对应 Agent 处理
- **旅游规划**：提供专业的旅游路线规划建议
- **笑话生成**：根据用户需求生成幽默笑话
- **对联创作**：自动生成创意对联
- **流式输出**：支持实时流式输出，带来更好的用户体验

## 项目结构

```
Multiagent/
├── Director.py           # 主程序入口，包含 Agent 逻辑
├── config/
│   ├── load_key.py       # API Key 加载工具
│   ├── DirectorSever.py  # 服务配置
│   └── Keys.json         # API Key 存储（需用户创建）
└── README.md
```

## 环境要求

- Python 3.10+
- 百炼 API Key（阿里云通义千问）

## 安装部署

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd Multiagent
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

在 `config/` 目录下创建 `Keys.json` 文件：

```json
{
  "BAILIAN_API_KEY": "your-bailian-api-key-here"
}
```

获取百炼 API Key：https://bailian.console.aliyun.com/

### 5. 运行程序

```bash
python Director.py
```

## 使用示例

```
用户输入: 给我讲一个郭德纲的笑话
系统会自动分类并调用 joke_node 生成笑话
```

## 技术栈

- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent 编排框架
- [LangChain](https://python.langchain.com/) - LLM 应用开发框架
- [通义千问](https://help.aliyun.com/zh/dashscope/) - 阿里云大语言模型

## License

MIT License
