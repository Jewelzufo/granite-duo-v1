<h1 align="center">Granitepi-4-Nano</h1>

<p align="center">
  <img src="https://github.com/Jewelzufo/granitepi-4-nano/blob/main/granitepi4.jpg?raw=true" width="600" height="400">
</p>

**Date**: 11-01-2025 | **Version**: 1.0

**Designed by**: *Julian A. Gonzalez* - ([Linkedin](www.linkedin.com/in/julian-g-7b533129a))

**Co-Contributor**: *Thomas Mertens* - ([Linkedin](https://www.linkedin.com/in/tgmertens/))

---

![Raspberry Pi 5](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205-red?logo=raspberrypi)
![Ollama](https://img.shields.io/badge/Framework-Ollama-yellow)
![IBM Granite](https://img.shields.io/badge/Model-IBM%20Granite%204.0-blue)

---

## What This Does

Run a complete, privacy-focused large language model on your Raspberry Pi 5 with zero cloud dependency. This guide gets IBM Granite 4.0 (350M parameters) running locally in under 45 minutesno AI experience required.

---

## Prerequisites Check

Before starting, verify your setup meets these requirements:

### Hardware Requirements
- **Raspberry Pi 5 with 8GB RAM** (required)
- **32GB+ SD card** or **NVMe M.2 SSD** (SSD recommended)
- **Official USB-C power supply** (5V 5A)
- **Active cooling** (heatsink + fan recommended)

### Verify Your System

Run these commands to check compatibility:

```bash
# Check architecture (must show: aarch64)
uname -m

# Check 64-bit OS (must show: 64)
getconf LONG_BIT

# Check available RAM (should show ~7-8GB)
free -h

# Check free storage (need ~4GB)
df -h
```

✅ **All checks passed?** Continue to installation below.

❌ **Something failed?** See [Common Questions](#common-questions) for help.

---

## Installation (5 Minutes)

### Step 1: Update Your System (2 min)

```bash
sudo apt update && sudo apt full-upgrade -y
```

### Step 2: Install Ollama (1 min)

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 3: Verify Installation

```bash
ollama --version
```

You should see a version number like `0.1.20` or higher.

### Step 4: Download the Model (2-5 min)

```bash
ollama pull ibm/granite4:350m-h
```

**What's happening:** Downloads ~366 MB, expands to ~1.2 GB in RAM when running.

---

## Your First Query

### Single Question

```bash
ollama run ibm/granite4:350m-h "What is Python?"
```

**Expected:** A clear answer in ~2-5 seconds.

### Interactive Chat

```bash
ollama run ibm/granite4:350m-h
```

Now you can have a conversation. Type your questions and press Enter. Press `Ctrl+D` to exit.

**Example conversation:**
```
>>> What is machine learning?
[Claude responds...]

>>> Give me a Python example
[Claude responds...]

>>> /bye
```

✅ **It works!** You're ready to explore more in [Usage Patterns](#usage-patterns).

---

## Common Questions

### Q: Will this work on Raspberry Pi 4 or Pi 3?

**A:** Pi 4 *might* work with smaller models, but performance will be slow. Pi 3 is not recommended. **Pi 5 with 8GB RAM is strongly recommended** for Granite 4.0.

### Q: Do I need internet after setup?

**A:** No. Once the model is downloaded, everything runs 100% offline. Your data never leaves your device.

### Q: How much power does it use?

**A:** Only ~5-7 watts during inference, efficient compared to GPUs.

### Q: Can I use this for commercial projects?

**A:** Yes! Both Ollama and IBM Granite 4.0 are Apache 2.0 licensed (open source, free for commercial use).

### Q: Why Granite 4.0 instead of other models?

**A:** Granite 4.0's hybrid Mamba architecture is optimized for small devices. After testing many tiny (0.5-1gb) models on Pi 5, Granite consistently performs well with limited resources.

### Q: Can I run multiple models?

**A:** Yes, but one at a time due to memory limits. You can switch between models instantly.

### Q: The model is slow or system is freezing. What do I do?

**A:** Check temperature (`vcgencmd measure_temp`), ensure active cooling is working, and see [Performance & Optimization](#performance--optimization) below.

### Q: How do I integrate this into my app?

**A:** Use the REST API at `http://localhost:11434/api/generate`. See [Usage Patterns](#usage-patterns) for Python examples.

**More questions?** Check [Troubleshooting](#troubleshooting) or open a GitHub issue.

---

## Model Specifications

| Aspect | Details |
|--------|---------|
| **Model** | IBM Granite 4.0 (350M-H) |
| **Parameters** | 350 Million |
| **Architecture** | Hybrid Mamba-2 (SSM) |
| **Download Size** | ~366 MB |
| **Loaded Size** | ~1.2 GB RAM |
| **Inference Memory** | ~0.8GB |
| **License** | Apache 2.0 (Open Source) |
| **Languages** | 12+ (English, Spanish, French, German, Japanese, etc.) |

---

## Usage Patterns

### Essential: Command Line Queries

**Simple question:**
```bash
ollama run ibm/granite4:350m-h "How do neural networks work?"
```

**Multi-line prompt:**
```bash
ollama run ibm/granite4:350m-h "
Write a Python function that:
1. Takes a list of numbers
2. Returns the average
3. Handles empty lists
"
```

**Custom creativity level:**
```bash
# More creative (0.0-1.0)
ollama run ibm/granite4:350m-h --temperature 0.8 "Write a haiku about AI"
```

---

### Intermediate: REST API Usage

**Query via curl:**
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "ibm/granite4:350m-h",
    "prompt": "Explain dark matter",
    "stream": false
  }'
```

**Python integration:**
```python
import requests

def query_ai(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'ibm/granite4:350m-h',
            'prompt': prompt,
            'stream': False
        }
    )
    return response.json()['response']

# Use it
result = query_ai("What is quantum entanglement?")
print(result)
```

---

### Advanced: Custom Configuration

**Keep model loaded (faster subsequent queries):**
```bash
OLLAMA_KEEP_ALIVE=24h ollama run ibm/granite4:350m-h
```

**Limit threads for stability:**
```bash
# Pi 5 has 4 cores, limit to 2 for better thermal management
OLLAMA_NUM_THREADS=2 ollama run ibm/granite4:350m-h
```

**Monitor system temperature:**
```bash
# Check temp continuously
watch -n 1 'vcgencmd measure_temp'
```

**Full Python example with error handling:**
```python
import requests
import json

class LocalAI:
    def __init__(self, model="ibm/granite4:350m-h"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model
    
    def ask(self, prompt, temperature=0.7):
        try:
            response = requests.post(
                self.url,
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'temperature': temperature,
                    'stream': False
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

# Usage
ai = LocalAI()
print(ai.ask("Explain recursion in programming"))
```

**For more examples:** See [TUTORIAL.md](TUTORIAL.md) for complete integration guides.

---

## Performance & Optimization

### Benchmark Expectations

On **Raspberry Pi 5 (8GB, active cooling)**:

| Metric | Typical Performance |
|--------|---------------------|
| Model load time | 8-12 seconds (cached after first run) |
| Response time | 2-5 seconds (100-token response) |
| Throughput | 30-50 tokens/second |
| Operating temp | 55-65°C (normal with cooling) |
| Memory usage | ~1.2 GB peak |

### Optimization Tips

**1. Use an SSD instead of SD card**
- 2-3x faster model loading
- Better sustained performance

**2. Ensure proper cooling**
- Keep temperature under 70°C
- Use heatsink + active fan
- Check: `vcgencmd measure_temp`

**3. Increase swap if needed**
```bash
# Edit swap configuration
sudo nano /etc/dphys-swapfile
# Set: CONF_SWAPSIZE=2048

# Restart swap
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

**4. Keep model loaded for frequent queries**
```bash
# Keeps model in memory for 24 hours
OLLAMA_KEEP_ALIVE=24h ollama run ibm/granite4:350m-h
```

**5. Adjust thread count if overheating**
```bash
# Reduce from 4 cores to 2
OLLAMA_NUM_THREADS=2 ollama run ibm/granite4:350m-h
```

---

## Privacy & Security

This setup is **100% private** by design:

✅ **No cloud uploads** — Everything runs locally  
✅ **No internet required** — Works offline after setup  
✅ **No account needed** — No tracking, no sign-ups  
✅ **Open source** — Auditable code (Apache 2.0)  
✅ **Your data stays yours** — Medical records, code, personal notes never leave your device

**Perfect for:**
- Healthcare data analysis (HIPAA-sensitive)
- Legal document review (confidential)
- Personal journaling with AI assistance
- Proprietary business intelligence
- Code development without vendor lock-in
- Educational experiments

---

## Troubleshooting

### Model won't download

**Symptoms:** Download fails or hangs

**Solutions:**
```bash
# Retry (resumes from checkpoint)
ollama pull ibm/granite4:350m-h

# Or clear cache and retry
rm -rf ~/.ollama/models/*
ollama pull ibm/granite4:350m-h

# Check network
ping -c 3 ollama.ai
```

---

### System becomes unresponsive or very slow

**Symptoms:** System freezes, queries take 30+ seconds

**Solutions:**

1. **Check temperature:**
   ```bash
   vcgencmd measure_temp
   # Should be < 70°C
   ```

2. **Reduce thread count:**
   ```bash
   OLLAMA_NUM_THREADS=1 ollama run ibm/granite4:350m-h
   ```

3. **Increase swap:**
   ```bash
   sudo nano /etc/dphys-swapfile
   # Set: CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

4. **Use SSD instead of SD card** for better I/O performance

---

### "Connection refused" or API errors

**Symptoms:** Can't connect to `localhost:11434`

**Solutions:**
```bash
# Check if Ollama is running
systemctl status ollama

# Restart Ollama
sudo systemctl restart ollama

# Check port
sudo netstat -tlnp | grep 11434
```

---

### Model gives poor/incorrect answers

**This is expected behavior:**
- Granite 4.0 (350M) is a small model optimized for edge devices
- It's designed for general assistance, not specialized expertise
- Accuracy improves with clearer, more specific prompts

**Tips for better responses:**
- Be specific in your questions
- Provide context when needed
- Use temperature settings (lower = more focused)
- For specialized tasks, consider fine-tuning or larger models

---

### Out of memory errors

**Symptoms:** Process killed, OOM errors

**Solutions:**
```bash
# Check available memory
free -h

# Close other applications
# Increase swap (see above)

# Use lighter model (if available)
ollama pull tinyllama
```

---

### Installation fails

**Symptoms:** `install.sh` script errors

**Solutions:**
```bash
# Ensure 64-bit OS
getconf LONG_BIT  # Must show 64

# Update system first
sudo apt update && sudo apt full-upgrade -y

# Install dependencies manually
sudo apt install curl ca-certificates -y

# Retry installation
curl -fsSL https://ollama.ai/install.sh | sh
```

**Still stuck?** Open a [GitHub issue](https://github.com/Jewelzufo/granitepi-4-nano/issues) with:
- Your error message
- Output of `uname -a`
- Output of `free -h`

---

## Learn More

### Deep Dive Tutorial

For comprehensive guides including Python integration, web interfaces, and advanced configurations:

📘 **[Read TUTORIAL.md](TUTORIAL.md)** — Complete step-by-step guide with troubleshooting

### Official Resources

- **[Ollama Documentation](https://ollama.ai)** — Framework reference
- **[IBM Granite Docs](https://www.ibm.com/granite/docs/)** — Model specifications
- **[Ollama GitHub](https://github.com/ollama/ollama)** — Source code and issues
- **[Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)** — Hardware guides

### Related Projects

- **[Open WebUI](https://github.com/open-webui/open-webui)** — Web interface for Ollama
- **[LM Studio](https://lmstudio.ai/)** — GUI for managing models
- **[IBM Granite on HuggingFace](https://huggingface.co/ibm-granite)** — Model hub

### Advanced Topics

Once you've mastered the basics:

1. **Fine-tune Granite 4.0** on your domain-specific data
2. **Build a web interface** using Flask + Ollama API
3. **Integrate with Home Assistant** for voice-controlled smart home
4. **Deploy multiple Pis** for distributed inference
5. **Try other models** like TinyLlama, Phi, or LLaMA variants
6. **Create RAG pipelines** for document Q&A systems

### Community & Support

- **Issues/Bugs:** [GitHub Issues](https://github.com/Jewelzufo/granitepi-4-nano/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Jewelzufo/granitepi-4-nano/discussions)
- **Community:** r/ollama, r/raspberry_pi on Reddit
- **Professional:** IBM TechXchange community

---

## Contributing

We welcome contributions!

- Found a bug? Open an issue
- Have a better approach? Submit a PR
- Benchmarked different hardware? Share your results
- Created an interesting application? Link it in discussions

## License

- **This tutorial:** Apache 2.0 — free to use, modify, distribute
- **IBM Granite model:** Apache 2.0 — free for commercial use
- **Ollama:** MIT License

---

## Project Status

✅ **Production Ready** — Tested on Raspberry Pi 5 (8GB)  
✅ **Actively Maintained** — Following Ollama & Granite updates  
✅ **Community Supported** — Feedback and contributions welcome

**Last tested:** November 2025  
**Ollama version:** 0.1.20+  
**Raspberry Pi OS:** Bookworm 64-bit

---

<p align="center">
  <strong>Made with ❤️ for privacy advocates, AI learners, and Raspberry Pi enthusiasts</strong>
</p>

<p align="center">
  <em>Ready to dive deeper? Check out <a href="TUTORIAL.md">TUTORIAL.md</a> for advanced guides! 🚀</em>
</p>
