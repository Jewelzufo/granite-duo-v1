<div align="center">
       <h1>Granite-Duo-v1</h1>
       <i>Julian A. Gonzalez, 10-25-2025</i>
</div>
<div align="center">
       <img src="https://github.com/Jewelzufo/granite-duo-v1/blob/main/1000068993%20(1).jpg?raw=true" alt="Ollama and IBM logo with cyberpunk theme" width="650" height="400" />
       <h2>Dual-Agent System: IBM Granite3-MoE:1B</h2>
       
</div>


## 🎯 Overview

This project uses a dual-agent system that leverages the Reflection agentic design pattern. Two specialized agents collaborate iteratively to produce high-quality responses:

- **Generator Agent**: Creates comprehensive initial responses
- **Critic Agent**: Evaluates outputs and provides constructive feedback
- **Coordinator**: Manages the iterative refinement process

## 🏗️ Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Dual-Agent Coordinator          │
│  ┌───────────────────────────────┐  │
│  │  Iteration Loop (max 3)       │  │
│  │                               │  │
│  │  ┌─────────────┐              │  │
│  │  │  Generator  │──────┐       │  │
│  │  │    Agent    │      │       │  │
│  │  └─────────────┘      │       │  │
│  │         │              │       │  │
│  │         ▼              │       │  │
│  │  ┌─────────────┐      │       │  │
│  │  │   Critic    │      │       │  │
│  │  │    Agent    │      │       │  │
│  │  └─────────────┘      │       │  │
│  │         │              │       │  │
│  │         ▼              │       │  │
│  │  [Feedback Loop]───────┘       │  │
│  │                               │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│Final Response│
└──────────────┘
```

## 🔬 Agentic Design Pattern: Reflection

This implementation follows the **Reflection Pattern**, one of the four core agentic AI design patterns:

1. **Generator Phase**: The Generator agent produces an initial comprehensive response
2. **Critic Phase**: The Critic agent evaluates the response and provides structured feedback
3. **Refinement Phase**: The Generator incorporates feedback to produce an improved response
4. **Iteration**: This process repeats for up to 3 iterations or until convergence

## 📋 Prerequisites

### 1. Ollama Installation

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com](https://ollama.com/download)

### 2. Python Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Quick Start

### Step 1: Install Dependencies

The script automatically installs required packages, but you can pre-install them:

```bash
pip install requests rich
```

### Step 2: Start Ollama

```bash
# The script will automatically pull the model if needed
ollama serve
```

### Step 3: Run the Dual-Agent System

```bash
python dual_agent_granite.py
```

## 💡 Usage Examples

### Interactive Mode

When you run the script, you'll see:

```
Choose a query or enter your own:
  1. Explain the key principles of quantum computing in simple terms.
  2. What are the main differences between supervised and unsupervised learning?
  3. How can I optimize Python code for better performance?
  4. Enter custom query

Your choice (1-4):
```

### Programmatic Usage

```python
from dual_agent_granite import OllamaClient, DualAgentCoordinator

# Initialize
client = OllamaClient()
coordinator = DualAgentCoordinator(client)

# Run query
result = coordinator.run(
    user_query="Explain neural networks in simple terms",
    max_iterations=3,
    verbose=True
)

# Access results
print(result['final_response'])
print(f"Converged: {result['converged']}")
print(f"Total iterations: {result['iterations']}")
```

## 🔧 Configuration

### Agent Parameters

You can customize agent behavior by modifying the `AgentConfig`:

```python
AgentConfig(
    name="Generator",
    role=AgentRole.GENERATOR,
    system_prompt=GENERATOR_SYSTEM_PROMPT,
    model="granite3-moe:1b",  # Model to use
    temperature=0.7,           # Creativity (0.0-1.0)
    max_tokens=2048           # Max response length
)
```

### System Prompts

Customize agent behavior by editing the system prompts:

- `GENERATOR_SYSTEM_PROMPT`: Defines Generator agent's role and behavior
- `CRITIC_SYSTEM_PROMPT`: Defines Critic agent's evaluation criteria

### Iteration Control

```python
# Adjust convergence behavior
result = coordinator.run(
    user_query="Your question",
    max_iterations=5,  # Maximum refinement cycles
    verbose=True       # Show detailed output
)
```

## 📊 Output Structure

The system returns a comprehensive result dictionary:

```python
{
    'final_response': str,      # Final refined answer
    'iterations': int,          # Number of iterations performed
    'converged': bool,          # Whether quality threshold was met
    'history': List[Dict],      # Full conversation history
    'generator_calls': int,     # Total Generator invocations
    'critic_calls': int        # Total Critic invocations
}
```

## 🎯 Use Cases

### 1. Research & Analysis
- Literature reviews
- Technical documentation
- Comparative analyses

### 2. Content Creation
- Blog posts and articles
- Technical tutorials
- Educational materials

### 3. Code Development
- Code generation with review
- Debugging assistance
- Documentation writing

### 4. Problem Solving
- Complex reasoning tasks
- Strategic planning
- Decision support

## 🧪 Advanced Features

### Custom Agent Roles

Extend the system with specialized agents:

```python
class CustomAgent(Agent):
    def process(self, input_text: str, context: Optional[Dict] = None) -> str:
        # Custom processing logic
        return super().process(input_text, context)
```

### Multi-Model Support

Use different Granite models:

```python
# For larger tasks
config.model = "granite3-moe:3b"

# For dense models
config.model = "granite3-dense:2b"
config.model = "granite3-dense:8b"
```

### Convergence Detection

The system automatically detects when quality is satisfactory:

```python
# In critic feedback, certain phrases trigger convergence:
- "no significant improvements needed"
- "response is comprehensive and accurate"
- "quality is satisfactory"
```

## 📈 Performance Characteristics

### Granite3-MoE:1B Specifications

- **Parameters**: 1 billion (Mixture of Experts)
- **Context Length**: 4096 tokens
- **Training Data**: 10+ trillion tokens
- **Latency**: Optimized for low-latency inference
- **Use Cases**: On-device, tool-use, RAG

### Benchmarks

Typical performance on standard hardware:
- **Single inference**: 1-3 seconds
- **Full dual-agent cycle (3 iterations)**: 10-20 seconds
- **Memory usage**: ~2-4 GB RAM

## 🔍 Troubleshooting

### Issue: Ollama not running

```bash
# Start Ollama service
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

### Issue: Model not found

```bash
# Manually pull the model
ollama pull granite3-moe:1b

# List available models
ollama list
```

### Issue: Slow responses

- Reduce `max_iterations` from 3 to 2
- Decrease `max_tokens` in AgentConfig
- Use GPU acceleration if available

### Issue: Import errors

```bash
# Reinstall dependencies
pip install --upgrade requests rich
```

## 🌟 Best Practices

1. **Query Formulation**: Be specific and clear in your queries
2. **Iteration Tuning**: Start with 2-3 iterations for most tasks
3. **Temperature Settings**: 
   - Use 0.3-0.5 for factual queries
   - Use 0.7-0.9 for creative tasks
4. **Monitoring**: Enable verbose mode during development
5. **Resource Management**: Close the coordinator when done

## 📚 References

### Agentic Patterns
- [Anthropic's Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [DeepLearning.AI: Agentic Design Patterns](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)

### IBM Granite Models
- [Ollama Granite Models](https://ollama.com/blog/ibm-granite)
- [Granite3-MoE on Ollama](https://ollama.com/library/granite3-moe)

### Multi-Agent Systems
- [LangGraph Multi-Agent Overview](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Additional agent roles (Planner, Executor, etc.)
- Tool integration (web search, code execution)
- Performance optimizations
- Extended model support
- Evaluation metrics

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

The same license as IBM Granite models, ensuring compatibility and permissive use.

**Key permissions:**
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Patent use
- ✅ Private use

**Conditions:**
- Include license and copyright notice
- State changes made to the code
- Include NOTICE file if distributing

For third-party dependencies and attributions, see [NOTICE](NOTICE) file.

## 👤 Author

**Julian A. Gonzalez, IBM Champion 2025**

**IMPORTANT DISCLAIMER:** This is an independent project created by Julian A. Gonzalez and is **NOT an official IBM product**.

This project uses IBM's open-source Granite models (licensed under Apache 2.0) via Ollama.


---

**Built with ❤️ using IBM Granite and Ollama**
