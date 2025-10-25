# Configuration Template for Dual-Agent System
# Copy this file to 'config.py' and customize as needed
#
# Author: Julian A. Gonzalez, IBM Champion 2025
# DISCLAIMER: This is an independent project and is NOT an official IBM product.
#
# Copyright 2024 Julian A. Gonzalez, IBM Champion 2025
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Ollama server settings
OLLAMA_BASE_URL = "http://localhost:11434"

# Model selection
DEFAULT_MODEL = "granite3-moe:1b"

# Alternative models (uncomment to use)
# DEFAULT_MODEL = "granite3-moe:3b"        # Larger MoE model
# DEFAULT_MODEL = "granite3-dense:2b"      # Dense model variant
# DEFAULT_MODEL = "granite3-dense:8b"      # Larger dense model

# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

# Generator Agent Settings
GENERATOR_CONFIG = {
    "temperature": 0.7,      # Creativity level (0.0-1.0)
    "max_tokens": 2048,      # Maximum response length
    "top_p": 0.9,           # Nucleus sampling threshold
}

# Critic Agent Settings
CRITIC_CONFIG = {
    "temperature": 0.5,      # Lower for more analytical feedback
    "max_tokens": 1024,      # Feedback is typically shorter
    "top_p": 0.8,
}

# ============================================================================
# SYSTEM PROMPTS (Customize agent behavior)
# ============================================================================

CUSTOM_GENERATOR_PROMPT = """You are an expert Generator Agent with deep knowledge across multiple domains.

Your mission:
- Provide comprehensive, well-researched responses
- Structure information clearly with examples when helpful
- Be accurate and cite reasoning when making claims
- Adapt your tone to the query (technical for tech questions, accessible for general topics)
- If uncertain, acknowledge limitations rather than speculating

Quality standards:
- Clarity: Easy to understand
- Completeness: Cover all aspects of the query
- Accuracy: Factually correct
- Relevance: Stay focused on the question

When you receive feedback, carefully consider it and improve your response accordingly."""

CUSTOM_CRITIC_PROMPT = """You are a meticulous Critic Agent specializing in quality assurance.

Your responsibilities:
- Evaluate responses for accuracy, completeness, and clarity
- Identify gaps, errors, or areas needing improvement
- Provide specific, actionable feedback
- Recognize what was done well
- Suggest concrete improvements

Feedback structure:
✓ STRENGTHS: What works well
⚠ IMPROVEMENTS NEEDED: Specific issues found
→ SUGGESTIONS: How to address the issues

Be thorough but constructive. Your goal is continuous improvement, not perfection."""

# ============================================================================
# COORDINATION SETTINGS
# ============================================================================

# Maximum iterations before stopping
MAX_ITERATIONS = 3

# Enable verbose logging
VERBOSE_MODE = True

# Convergence detection keywords (if found in critic feedback, stop early)
CONVERGENCE_KEYWORDS = [
    "no significant improvements needed",
    "response is comprehensive and accurate",
    "quality is satisfactory",
    "meets all requirements",
    "excellent response"
]

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Request timeout (seconds)
REQUEST_TIMEOUT = 120

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Context management
MAX_CONTEXT_LENGTH = 4096  # tokens

# Performance optimization
ENABLE_CACHING = True
CACHE_TTL = 3600  # seconds

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "dual_agent.log",
    "console": True
}

# ============================================================================
# USE CASE PRESETS
# ============================================================================

# Preset configurations for common use cases

PRESETS = {
    "research": {
        "generator_temperature": 0.3,
        "critic_temperature": 0.4,
        "max_iterations": 3,
        "focus": "accuracy and completeness"
    },
    
    "creative": {
        "generator_temperature": 0.9,
        "critic_temperature": 0.7,
        "max_iterations": 3,
        "focus": "originality and engagement"
    },
    
    "technical": {
        "generator_temperature": 0.2,
        "critic_temperature": 0.3,
        "max_iterations": 2,
        "focus": "precision and technical accuracy"
    },
    
    "quick": {
        "generator_temperature": 0.5,
        "critic_temperature": 0.5,
        "max_iterations": 1,
        "focus": "speed over perfection"
    },
    
    "thorough": {
        "generator_temperature": 0.4,
        "critic_temperature": 0.3,
        "max_iterations": 5,
        "focus": "exhaustive analysis"
    }
}

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
To use custom configuration:

1. Copy this file to 'config.py'
2. Modify settings as needed
3. Import in your script:

    from config import GENERATOR_CONFIG, CRITIC_CONFIG
    
    coordinator.generator.config.temperature = GENERATOR_CONFIG['temperature']
    coordinator.critic.config.temperature = CRITIC_CONFIG['temperature']

4. Or use presets:

    from config import PRESETS
    
    preset = PRESETS['research']
    coordinator.generator.config.temperature = preset['generator_temperature']
    coordinator.critic.config.temperature = preset['critic_temperature']
"""
