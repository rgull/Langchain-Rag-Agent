# LangChain Agent with Memory and MCP Integration

A sophisticated LangChain-based AI agent system featuring persistent memory, middleware support, and Model Context Protocol (MCP) server integration. This project demonstrates advanced agent capabilities including human-in-the-loop workflows, conversation summarization, and tool integration.

## 🚀 Features

- **Intelligent Agent System**: Built with LangChain and LangGraph for robust agent orchestration
- **Persistent Memory**: SQLite-based checkpointing for conversation history and agent state
- **MCP Integration**: Seamless integration with Model Context Protocol servers for extensible tooling
- **Human-in-the-Loop**: Interactive middleware for approval workflows (e.g., email sending)
- **Conversation Summarization**: Automatic message summarization to manage context length
- **Multiple Tools**: Email tools, weather tools, and MCP-based tools (math operations)
- **Configurable LLM**: Support for Groq models with easy configuration
- **Modular Architecture**: Clean separation of concerns with organized modules

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Architecture](#architecture)
- [Components](#components)
- [MCP Servers](#mcp-servers)
- [Dependencies](#dependencies)
- [Development](#development)

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LangChain
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   Create a `.env` file in the project root with the following variables:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   MODEL_NAME=qwen/qwen3-32b
   ```

## ⚙️ Configuration

The project uses Pydantic settings for configuration management. Create a `.env` file in the root directory with:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=your_preferred_model_name
```

### Available Configuration Options

- `GROQ_API_KEY`: Your Groq API key (required)
- `MODEL_NAME`: The LLM model to use (default: `qwen/qwen3-32b`)

Configuration is loaded from `src/config/settings.py` using Pydantic Settings.

## 📁 Project Structure

```
LangChain/
├── mcp_servers/              # Model Context Protocol servers
│   ├── math_server.py        # Math operations MCP server
│   └── weather_server.py     # Weather service MCP server
├── src/
│   ├── agents/               # Agent definitions
│   │   └── agent.py          # Main agent builder
│   ├── config/               # Configuration management
│   │   └── settings.py       # Settings and environment variables
│   ├── memory/               # Memory and checkpointing
│   │   └── sqlite_saver.py  # SQLite-based state persistence
│   ├── middlewares/          # Agent middlewares
│   │   ├── human_in_the_loop_middleware.py  # Human approval workflow
│   │   ├── summarization_middleware.py      # Conversation summarization
│   │   └── interrupt_handlers/              # Interrupt handling
│   │       └── send_email_interrupt_handler.py
│   ├── models/               # LLM model configurations
│   │   └── llm.py           # LLM initialization
│   ├── prompts/              # System prompts
│   │   └── system_prompt.py  # Agent system prompt
│   ├── tools/                # Agent tools
│   │   ├── email_tool.py    # Email sending/reading tools
│   │   ├── mcp_tools.py     # MCP tool integration
│   │   └── weather_tool.py  # Weather tool
│   ├── utils/                # Utility functions
│   ├── *.ipynb               # Jupyter notebooks for experimentation
│   └── main.py               # Application entry point
├── storage/                  # Data storage
│   └── agent_memory.db      # SQLite database for agent memory
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🎯 Usage

### Running the Agent

1. **Start MCP Servers** (if using HTTP transport)

   For the weather server (HTTP):
   ```bash
   python mcp_servers/weather_server.py
   ```
   This will start the server on `http://127.0.0.1:8000/mcp`

2. **Run the main application**
   ```bash
   python src/main.py
   ```

3. **Interact with the agent**
   - Type your questions or commands
   - Type `q` to quit
   - When email sending is requested, you'll be prompted to approve or reject

### Example Interactions

```
You: What's the weather in New York?
AI: [Uses weather tool and responds]

You: Send an email to john@example.com with subject "Hello" and body "Hi there"
AI: [Interrupts for approval]
Process was interrupted. Action required
Approve or reject?: approve
AI: Email sent to john@example.com...

You: Calculate 15 + 27
AI: [Uses math MCP tool and responds]
```

## 🏗️ Architecture

### Agent Flow

```
User Input
    ↓
Main Loop (main.py)
    ↓
Agent (LangGraph)
    ↓
Middleware Layer
    ├── SummarizationMiddleware (manages context length)
    └── HumanInTheLoopMiddleware (handles approvals)
    ↓
Tool Selection & Execution
    ├── Email Tools
    ├── MCP Tools (Math, Weather)
    └── Other Tools
    ↓
Response Generation
    ↓
Memory Persistence (SQLite)
    ↓
User Output
```

### Key Components

1. **Agent Builder** (`src/agents/agent.py`): Constructs the LangChain agent with tools, prompts, and middlewares
2. **LLM Configuration** (`src/models/llm.py`): Configures the Groq chat model
3. **Memory System** (`src/memory/sqlite_saver.py`): Persists conversation state using SQLite
4. **Middleware Stack**: Enhances agent capabilities with summarization and human approval
5. **Tool Integration**: Combines custom tools with MCP server tools

## 🔌 Components

### Agents

The agent is built using LangChain's `create_agent` function, which creates a LangGraph-based agent with:
- Custom system prompts
- Multiple tools (email, MCP-based)
- Middleware stack
- Persistent checkpointing

### Tools

#### Email Tools
- `send_email_tool`: Sends emails (requires human approval)
- `read_email_tool`: Reads emails by ID

#### MCP Tools
Dynamically loaded from MCP servers:
- **Math Server**: Provides `add` and `multiply` functions
- **Weather Server**: Provides `get_weather` function

### Middlewares

#### SummarizationMiddleware
- Automatically summarizes conversation history when message count exceeds threshold
- Trigger: After 10 messages
- Keeps: Last 3 messages + summary

#### HumanInTheLoopMiddleware
- Interrupts agent execution for human approval on specific actions
- Currently configured for `send_email_tool`
- Supports: `approve`, `edit`, `reject` decisions

### Memory

The agent uses SQLite-based checkpointing to persist:
- Conversation history
- Agent state
- Tool execution history
- Thread-based conversations (supports multiple conversation threads)

## 🌐 MCP Servers

### Math Server (`mcp_servers/math_server.py`)

A FastMCP server providing mathematical operations:
- `add(a: int, b: int)`: Adds two numbers
- `multiply(a: int, b: int)`: Multiplies two numbers

**Transport**: stdio

### Weather Server (`mcp_servers/weather_server.py`)

A FastMCP server providing weather information:
- `get_weather(location: str)`: Returns weather for a location

**Transport**: HTTP (streamable-http)

**Note**: Update the path in `src/tools/mcp_tools.py` to match your system's path structure.

## 📦 Dependencies

### Core Dependencies

- **langchain** (1.2.4): Core LangChain framework
- **langgraph** (1.0.6): Agent orchestration
- **langchain-groq** (1.1.1): Groq LLM integration
- **langchain-mcp-adapters** (0.2.1): MCP server integration
- **langgraph-checkpoint-sqlite** (3.0.3): SQLite checkpointing
- **mcp** (1.26.0): Model Context Protocol
- **pydantic-settings** (2.12.0): Configuration management

### Development Dependencies

- **jupyter**: For notebook-based experimentation
- **ipython**: Enhanced Python shell

See `requirements.txt` for the complete list of dependencies.

## 🛠️ Development

### Running MCP Servers

**Math Server (stdio)**:
```bash
python mcp_servers/math_server.py
```

**Weather Server (HTTP)**:
```bash
python mcp_servers/weather_server.py
# Server runs on http://127.0.0.1:8000/mcp
```

### Adding New Tools

1. Create a tool function in `src/tools/`
2. Decorate with `@tool` from `langchain.tools`
3. Add to the tools list in `src/agents/agent.py`

### Adding New Middlewares

1. Create middleware function in `src/middlewares/`
2. Import and add to middleware list in `src/agents/agent.py`

### Adding New MCP Servers

1. Create MCP server in `mcp_servers/`
2. Register in `src/tools/mcp_tools.py` in the `MultiServerMCPClient` configuration

### Notebooks

The project includes several Jupyter notebooks for experimentation:
- `agent_with_memory.ipynb`: Memory and checkpointing examples
- `custom_middleware.ipynb`: Middleware customization
- `langchain-with-huggingface.ipynb`: HuggingFace integration examples
- `middleware.ipynb`: Middleware usage patterns
- `notebook.ipynb`: General experimentation

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- The email tools are currently mock implementations - replace with actual email service integration for production use

## 📝 Notes

- The project uses absolute paths in `mcp_tools.py` - update these to match your system
- The weather server must be running before starting the main application if using HTTP transport
- SQLite database is created automatically in the `storage/` directory
- Thread IDs can be customized in `main.py` for multi-conversation support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- LangChain team for the excellent framework
- Groq for providing fast LLM inference
- MCP community for the Model Context Protocol specification

---

**Happy Coding! 🚀**



