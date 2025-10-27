<div align="center">
  <h1>Granite-Duo-v1</h1>
</div>

<!-- Badges Section -->
<div align="center">

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)


**An agentic AI system implementing the Reflection design pattern using IBM's Granite3-MoE:1B model**

[Features](#-features) • [Quick Start](#-quick-start) • [Contributing](#-contributing)

</div>

<div align="center">
  <img src="https://github.com/Jewelzufo/granite-duo-v1/blob/main/1000068993%20(1).jpg?raw=true" alt="Ollama and IBM logo with cyberpunk theme" width="650" height="350" />
  <h2>Privacy-First Multi-Agent AI Learning System</h2>
  <p>
    <em>No cloud dependencies • No data sharing • Complete transparency</em>
  </p>
</div>


## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Advanced Usage](#-advanced-usage)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [References](#-references)

---

## 🎯 Overview

This project implements a **production-ready dual-agent system** that leverages the **Reflection agentic design pattern**. Two specialized AI agents collaborate iteratively to produce high-quality responses:

- **Generator Agent** 🔨 Creates comprehensive, well-researched initial responses
- **Critic Agent** 👀 Evaluates outputs and provides constructive, actionable feedback  
- **Coordinator** 🎛️ Orchestrates the iterative refinement process for optimal results

Perfect for research, content creation, code generation, and complex problem-solving tasks.

---

## ✨ Features

- ⚡ **Lightweight & Efficient** - Runs on ~2-4GB RAM using 1B parameter Mixture-of-Experts model
- 🔄 **Iterative Refinement** - Up to 3 rounds of generator-critic feedback loops
- 🎯 **Early Convergence** - Detects quality thresholds and stops early when appropriate
- 📊 **Full History Tracking** - Complete conversation logs for analysis and debugging
- 🛠️ **Self-Healing** - Auto-installs dependencies and pulls models on first run
- 🎨 **Beautiful UI** - Rich terminal output with progress indicators and structured formatting
- 🔧 **Highly Configurable** - Template-based configuration with 5 built-in presets (research, creative, technical, quick, thorough)
- 📚 **Well-Documented** - 8 complete examples covering diverse use cases

---

## 🏗️ Architecture

### System Flow

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│    Dual-Agent Coordinator               │
│  ┌───────────────────────────────────┐  │
│  │  Iteration Loop (max 3)           │  │
│  │                                   │  │
│  │  1️⃣  Generator Phase              │  │
│  │     Create comprehensive response │  │
│  │                                   │  │
│  │  2️⃣  Critic Phase (if not final)  │  │
│  │     Evaluate & provide feedback   │  │
│  │                                   │  │
│  │  3️⃣  Convergence Check            │  │
│  │     Stop if quality threshold met │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
       │
       ▼
┌──────────────────┐
│Final Refined     │
│Response          │
└──────────────────┘
```

### Reflection Pattern (4-Phase Cycle)

1. **Generator Phase** - Initial comprehensive response creation
2. **Critic Phase** - Quality evaluation and gap identification
3. **Feedback Integration** - Incorporation of constructive feedback
4. **Iteration** - Repeat until convergence or max iterations

---

## 📋 Prerequisites

### System Requirements
- **Python:** 3.8 or higher
- **RAM:** 2-4 GB minimum
- **Disk Space:** ~5 GB (for model download)
- **OS:** macOS, Linux, or Windows

### Software Requirements

**Ollama** (LLM Runtime)
- Download: [ollama.com](https://ollama.com/download)
- macOS/Linux: `curl -fsSL https://ollama.com/install.sh | sh`
- Windows: Download installer from website

---

## ⚙️ Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/dual-agent-granite.git
cd dual-agent-granite
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install requests>=2.31.0 rich>=13.7.0
```

### Step 3: Start Ollama Service

```bash
# macOS/Linux
ollama serve

# Windows
# Launch the Ollama application from your Applications folder
```

### Step 4: Verify Setup

```bash
# The system will auto-pull the model on first run, or manually:
ollama pull granite3-moe:1b
```

---

## 🚀 Quick Start

### Interactive Mode

```bash
python dual_agent_granite.py
```

Then select from:
1. Pre-configured example queries
2. Enter your own custom query

### Programmatic Usage

```python
from dual_agent_granite import OllamaClient, DualAgentCoordinator

# Initialize the system
client = OllamaClient()
coordinator = DualAgentCoordinator(client)

# Run a query
result = coordinator.run(
    user_query="Explain quantum computing in simple terms",
    max_iterations=3,
    verbose=True
)

# Access results
print(result['final_response'])
print(f"Converged: {result['converged']}")
print(f"Iterations: {result['iterations']}")
```

### Output Structure

```python
{
    'final_response': str,          # Final refined answer
    'iterations': int,               # Number of iterations performed
    'converged': bool,               # Quality threshold met?
    'history': List[Dict],           # Full conversation history
    'generator_calls': int,          # Total generator invocations
    'critic_calls': int              # Total critic invocations
}
```

---

## 📚 Usage Guide

### 8 Complete Examples

The `examples.py` file includes 8 working demonstrations:

| Example | Use Case | Focus |
|---------|----------|-------|
| Basic Query | General questions | Default behavior |
| Technical Question | Specialized topics | Statistics & metrics |
| Creative Task | Writing & ideation | High temperature (0.9) |
| Code Generation | Programming tasks | Code quality review |
| Comparative Analysis | Multi-dimensional comparison | Thorough analysis |
| Minimal Iterations | Quick responses | Speed optimization |
| Batch Processing | Multiple queries | Efficiency at scale |
| History Tracking | Evolution analysis | Iteration-by-iteration breakdown |

Run examples:
```bash
python examples.py
```

---

## 🔧 Configuration

### Basic Configuration

Create a `config.py` from `config_template.py`:

```bash
cp config_template.py config.py
```

### Common Settings

**Agent Behavior**
```python
GENERATOR_CONFIG = {
    "temperature": 0.7,      # Creativity (0.0-1.0)
    "max_tokens": 2048,      # Response length
    "top_p": 0.9,           # Nucleus sampling
}

CRITIC_CONFIG = {
    "temperature": 0.5,      # Lower for analytical feedback
    "max_tokens": 1024,      # Shorter feedback
    "top_p": 0.8,
}
```

**Iteration Control**
```python
MAX_ITERATIONS = 3          # Max refinement cycles
CONVERGENCE_KEYWORDS = [
    "no significant improvements needed",
    "response is comprehensive and accurate",
    "quality is satisfactory"
]
```

### Use Case Presets

Five built-in presets optimize for different scenarios:

```python
from config import PRESETS

# Research: High accuracy, low temperature
preset = PRESETS['research']  # temp: 0.3, iterations: 3

# Creative: High creativity, multiple iterations
preset = PRESETS['creative']  # temp: 0.9, iterations: 3

# Technical: Precision focused
preset = PRESETS['technical']  # temp: 0.2, iterations: 2

# Quick: Speed over perfection
preset = PRESETS['quick']  # temp: 0.5, iterations: 1

# Thorough: Exhaustive analysis
preset = PRESETS['thorough']  # temp: 0.4, iterations: 5
```

---

## 🔍 Advanced Usage

### Custom Temperature Settings

Adjust creativity for different task types:

```python
# Factual queries (0.2-0.4)
coordinator.generator.config.temperature = 0.3
coordinator.critic.config.temperature = 0.4

# Balanced (0.5-0.7)
coordinator.generator.config.temperature = 0.6
coordinator.critic.config.temperature = 0.5

# Creative tasks (0.8-1.0)
coordinator.generator.config.temperature = 0.9
coordinator.critic.config.temperature = 0.7
```

### Batch Processing

```python
queries = [
    "What is Docker?",
    "Explain Kubernetes",
    "What are microservices?"
]

coordinator = DualAgentCoordinator(client)
results = []

for query in queries:
    result = coordinator.run(query, max_iterations=2, verbose=False)
    results.append(result)
```


### Custom System Prompts

```python
from dual_agent_granite import Agent, AgentConfig, AgentRole

custom_config = AgentConfig(
    name="CustomGenerator",
    role=AgentRole.GENERATOR,
    system_prompt="Your custom system prompt here...",
    temperature=0.6
)

custom_agent = Agent(custom_config, client)
```

---

## 📊 Performance

### Granite3-MoE:1B Specifications

| Metric | Value |
|--------|-------|
| Model Parameters | 1 billion (Mixture of Experts) |
| Context Length | 4096 tokens |
| Training Data | 10+ trillion tokens |
| Memory Usage | 2-4 GB RAM |
| Latency (single inference) | 1-3 seconds |
| Full cycle (3 iterations) | 10-20 seconds |

### Optimization Tips

1. **Reduce Iterations** - Start with `max_iterations=2` for speed
2. **Lower max_tokens** - Default 2048 is generous; try 1024
3. **GPU Acceleration** - Ollama supports CUDA/Metal for faster inference
4. **Query Specificity** - Better queries = fewer refinement cycles needed
5. **Temperature Tuning** - Lower temp = fewer iterations for convergence

---

## 🐛 Troubleshooting

### Issue: Ollama not running

**Error:** Connection refused to `localhost:11434`

**Solution:**
```bash
# Start Ollama service
ollama serve

# Verify connection
curl http://localhost:11434/api/tags
```

### Issue: Model not found

**Error:** Model `granite3-moe:1b` not available

**Solution:**
```bash
# Manual model pull
ollama pull granite3-moe:1b

# List available models
ollama list
```

### Issue: Slow responses

**Error:** Script takes >30 seconds for 3 iterations

**Solutions:**
1. Reduce iterations: `max_iterations=2`
2. Lower max_tokens: `max_tokens=1024`
3. Enable GPU: Check Ollama GPU settings
4. Use smaller model: `granite3-dense:2b`

### Issue: Out of memory

**Error:** Process killed or "OutOfMemory" error

**Solutions:**
1. Close other applications
2. Use smaller model or lower max_tokens
3. Increase system RAM (requires 2-4GB minimum)
4. Check Ollama memory allocation settings

### Issue: Import errors

**Error:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**
```bash
pip install --upgrade requests rich
```

### Issue: Permission denied

**Error:** Running on Windows with admin restrictions

**Solution:**
```bash
# Run PowerShell as Administrator
python dual_agent_granite.py
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved:

### Reporting Issues

- Use GitHub Issues with clear titles
- Include Python version and OS
- Provide reproduction steps
- Attach error logs/tracebacks

### Enhancement Suggestions

- Feature requests: Describe use case and expected behavior
- Performance improvements: Include benchmark data
- Documentation: Identify unclear sections

### Code Contributions

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes with clear commit messages
4. **Test** your changes: `python examples.py`
5. **Follow** code style: `black dual_agent_granite.py`
6. **Submit** a Pull Request with description

### Areas for Enhancement

- [ ] Tool-calling capabilities (web search, code execution)
- [ ] RAG (Retrieval-Augmented Generation) integration
- [ ] Supervisor agent for 3+ agent orchestration
- [ ] Streaming response support
- [ ] Performance metrics dashboard
- [ ] Fine-tuning utilities
- [ ] Multi-language support
- [ ] FastAPI/REST API wrapper
- [ ] Docker containerization
- [ ] Evaluation frameworks

### Code Style

- Add docstrings to functions
- Use type hints for clarity

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the LICENSE file for details.

**Key Permissions:**
- ✅ Commercial use
- ✅ Modification & Distribution
- ✅ Patent use
- ✅ Private use

**Requirements:**
- ⚠️ Include license and copyright notice
- ⚠️ Document significant changes
- ⚠️ Include NOTICE file if distributing

---

## 📚 References

### Agentic AI Patterns
- [Anthropic's Multi-Agent Systems Research](https://www.anthropic.com/engineering/multi-agent-research-system)
- [DeepLearning.AI: Agentic Patterns](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)
- [LangGraph: Multi-Agent Overview](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)

### IBM Granite Models
- [Ollama Granite Models](https://ollama.com/blog/ibm-granite)
- [Granite3-MoE on Ollama](https://ollama.com/library/granite3-moe)
- [IBM Granite GitHub](https://github.com/ibm-granite)

### Model Optimization
- [Ollama Documentation](https://ollama.com)
- [Mixture of Experts Research](https://arxiv.org/abs/2101.03961)

---

## 👤 Author

**Julian A. Gonzalez, IBM Champion 2025**

This is an independent open-source project created to demonstrate modern agentic AI design patterns using IBM's Granite models.

**DISCLAIMER:** This is **NOT an official IBM product**. This project is independently maintained and uses IBM's open-source Granite models under the Apache 2.0 license.

---

## 🌟 Acknowledgments

- **IBM Granite Team** - For the excellent Granite3-MoE model and their continued efforts into Granite
- **Ollama Project** - For the containerized model runtime
- **Rich Library** - For beautiful terminal UI
- **Open Source Community** - For continuous inspiration

---

<div align="center">

**Built with ❤️ using IBM Granite and Ollama**

⭐ If you find this useful, consider starring the repository!

[↑ Back to top](#-dual-agent-system-ibm-granite3-moe1b)
