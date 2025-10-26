#!/usr/bin/env python3
"""
Dual-Agent System using IBM Granite3-MoE:1B via Ollama
Author: Julian A. Gonzalez, IBM Champion 2025
Pattern: Researcher-Critic (Reflection Pattern)

This implementation creates a dual-agent system where:
- Agent 1 (Generator): Produces initial responses
- Agent 2 (Critic): Evaluates and provides constructive feedback
- Coordinator: Manages the interaction loop and convergence

Copyright 2024 Julian A. Gonzalez, IBM Champion 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import subprocess
import sys
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time

# ============================================================================
# INSTALL REQUIRED PACKAGES
# ============================================================================

def install_packages():
    """Install required packages if not already installed."""
    required_packages = [
        'requests',
        'rich',  # For beautiful terminal output
    ]
    
    print("Checking and installing required packages...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")

# Install packages before importing
install_packages()

import requests
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# ============================================================================
# CONFIGURATION
# ============================================================================

class AgentRole(Enum):
    """Agent role definitions"""
    GENERATOR = "generator"
    CRITIC = "critic"

@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    role: AgentRole
    system_prompt: str
    model: str = "granite3-moe:1b"
    temperature: float = 0.7
    max_tokens: int = 2048

@dataclass
class ConversationState:
    """State management for agent conversations"""
    user_query: str
    generator_output: str = ""
    critic_feedback: str = ""
    iteration: int = 0
    max_iterations: int = 3
    history: List[Dict] = field(default_factory=list)
    converged: bool = False

# ============================================================================
# SYSTEM PROMPTS (Optimized for Granite3-MoE)
# ============================================================================

GENERATOR_SYSTEM_PROMPT = """You are a Generator Agent specializing in creating comprehensive, accurate responses.

Your responsibilities:
- Analyze user queries carefully and provide detailed, well-structured responses
- Draw upon your knowledge to give informative answers
- Be clear, concise, and accurate
- Structure your responses with proper formatting when appropriate
- If you receive feedback, incorporate it to improve your response

Focus on quality and completeness. Your response will be reviewed by a Critic Agent."""

CRITIC_SYSTEM_PROMPT = """You are a Critic Agent specializing in evaluating and improving responses.

Your responsibilities:
- Review the Generator's response critically but constructively
- Identify gaps, inaccuracies, or areas for improvement
- Provide specific, actionable feedback
- Suggest concrete improvements
- Acknowledge what was done well
- Focus on substance over style

Format your feedback as:
STRENGTHS: [What was done well]
IMPROVEMENTS NEEDED: [Specific issues to address]
SUGGESTIONS: [Concrete recommendations]

Be thorough but fair. Your goal is to help improve the response, not to criticize unnecessarily."""

# ============================================================================
# OLLAMA CLIENT
# ============================================================================

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/generate"
        
    def check_ollama_status(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_model_availability(self, model_name: str) -> bool:
        """Check if the specified model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(model_name in model.get('name', '') for model in models)
        except:
            pass
        return False
    
    def generate(
        self, 
        prompt: str, 
        system: str = "", 
        model: str = "granite3-moe:1b",
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """Generate a response from the model"""
        
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system,
            "stream": stream,
            "options": {
                "temperature": temperature,
            }
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return f"Error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================================================
# AGENT IMPLEMENTATION
# ============================================================================

class Agent:
    """Base Agent class"""
    
    def __init__(self, config: AgentConfig, client: OllamaClient):
        self.config = config
        self.client = client
        self.call_count = 0
    
    def process(self, input_text: str, context: Optional[Dict] = None) -> str:
        """Process input and generate response"""
        self.call_count += 1
        
        # Build the prompt based on agent role
        if self.config.role == AgentRole.GENERATOR:
            if context and context.get('feedback'):
                prompt = f"""Original Query: {context['query']}

Previous Response:
{context['previous_response']}

Feedback from Critic:
{context['feedback']}

Please provide an improved response that addresses the feedback while maintaining quality."""
            else:
                prompt = f"User Query: {input_text}\n\nProvide a comprehensive response:"
        else:  # CRITIC
            prompt = f"""Original Query: {context['query']}

Response to Evaluate:
{input_text}

Provide constructive feedback following the specified format."""
        
        response = self.client.generate(
            prompt=prompt,
            system=self.config.system_prompt,
            model=self.config.model,
            temperature=self.config.temperature
        )
        
        return response

# ============================================================================
# DUAL-AGENT COORDINATOR
# ============================================================================

class DualAgentCoordinator:
    """Coordinates interaction between Generator and Critic agents"""
    
    def __init__(self, client: OllamaClient):
        self.client = client
        
        # Initialize agents
        self.generator = Agent(
            AgentConfig(
                name="Generator",
                role=AgentRole.GENERATOR,
                system_prompt=GENERATOR_SYSTEM_PROMPT
            ),
            client
        )
        
        self.critic = Agent(
            AgentConfig(
                name="Critic",
                role=AgentRole.CRITIC,
                system_prompt=CRITIC_SYSTEM_PROMPT
            ),
            client
        )
    
    def run(self, user_query: str, max_iterations: int = 3, verbose: bool = True) -> Dict:
        """Run the dual-agent system"""
        
        state = ConversationState(
            user_query=user_query,
            max_iterations=max_iterations
        )
        
        if verbose:
            console.print(Panel(
                f"[bold cyan]Starting Dual-Agent Processing[/bold cyan]\n"
                f"Query: {user_query}\n"
                f"Max Iterations: {max_iterations}",
                title="🤖 Dual-Agent System"
            ))
        
        # Initial generation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            for iteration in range(max_iterations):
                state.iteration = iteration + 1
                
                # Generator phase
                task = progress.add_task(
                    f"[cyan]Iteration {state.iteration}/{max_iterations}: Generator thinking...",
                    total=None
                )
                
                if iteration == 0:
                    state.generator_output = self.generator.process(user_query)
                else:
                    context = {
                        'query': user_query,
                        'previous_response': state.generator_output,
                        'feedback': state.critic_feedback
                    }
                    state.generator_output = self.generator.process(user_query, context)
                
                progress.remove_task(task)
                
                if verbose:
                    console.print(Panel(
                        state.generator_output,
                        title=f"[green]Generator Response (Iteration {state.iteration})",
                        border_style="green"
                    ))
                
                # Critic phase (skip on last iteration)
                if iteration < max_iterations - 1:
                    task = progress.add_task(
                        f"[yellow]Iteration {state.iteration}/{max_iterations}: Critic analyzing...",
                        total=None
                    )
                    
                    context = {
                        'query': user_query
                    }
                    state.critic_feedback = self.critic.process(
                        state.generator_output,
                        context
                    )
                    
                    progress.remove_task(task)
                    
                    if verbose:
                        console.print(Panel(
                            state.critic_feedback,
                            title=f"[yellow]Critic Feedback (Iteration {state.iteration})",
                            border_style="yellow"
                        ))
                    
                    # Check for convergence
                    if "no significant improvements needed" in state.critic_feedback.lower():
                        state.converged = True
                        if verbose:
                            console.print("[green]✓ Converged: Response quality satisfactory[/green]")
                        break
                
                # Store history
                state.history.append({
                    'iteration': state.iteration,
                    'generator_output': state.generator_output,
                    'critic_feedback': state.critic_feedback if iteration < max_iterations - 1 else None
                })
        
        return {
            'final_response': state.generator_output,
            'iterations': state.iteration,
            'converged': state.converged,
            'history': state.history,
            'generator_calls': self.generator.call_count,
            'critic_calls': self.critic.call_count
        }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_prerequisites():
    """Check if all prerequisites are met"""
    console.print("[bold]Checking Prerequisites...[/bold]")
    
    # Check Ollama
    client = OllamaClient()
    if not client.check_ollama_status():
        console.print("[red]✗ Ollama is not running![/red]")
        console.print("\nPlease start Ollama:")
        console.print("  - On macOS/Linux: Run 'ollama serve' in a terminal")
        console.print("  - On Windows: Start the Ollama application")
        return False
    console.print("[green]✓ Ollama is running[/green]")
    
    # Check model
    if not client.check_model_availability("granite3-moe:1b"):
        console.print("[yellow]⚠ granite3-moe:1b model not found[/yellow]")
        console.print("\nPulling model... This may take a few minutes.")
        try:
            subprocess.run(
                ["ollama", "pull", "granite3-moe:1b"],
                check=True,
                capture_output=False
            )
            console.print("[green]✓ Model downloaded successfully[/green]")
        except subprocess.CalledProcessError:
            console.print("[red]✗ Failed to download model[/red]")
            return False
    else:
        console.print("[green]✓ granite3-moe:1b model available[/green]")
    
    return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    console.print(Panel.fit(
        "[bold cyan]IBM Granite Dual-Agent System[/bold cyan]\n"
        "[dim]Powered by granite3-moe:1b via Ollama[/dim]",
        border_style="cyan"
    ))
    
    # Check prerequisites
    if not check_prerequisites():
        return
    
    console.print("\n" + "="*70 + "\n")
    
    # Initialize system
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    # Example queries to demonstrate the system
    example_queries = [
        "Explain the key principles of quantum computing in simple terms.",
        "What are the main differences between supervised and unsupervised learning?",
        "How can I optimize Python code for better performance?"
    ]
    
    console.print("[bold]Choose a query or enter your own:[/bold]")
    for i, query in enumerate(example_queries, 1):
        console.print(f"  {i}. {query}")
    console.print(f"  {len(example_queries) + 1}. Enter custom query")
    
    choice = console.input("\n[bold cyan]Your choice (1-4): [/bold cyan]")
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(example_queries):
            user_query = example_queries[choice_num - 1]
        elif choice_num == len(example_queries) + 1:
            user_query = console.input("[bold cyan]Enter your query: [/bold cyan]")
        else:
            console.print("[red]Invalid choice![/red]")
            return
    except ValueError:
        console.print("[red]Invalid input![/red]")
        return
    
    # Run the dual-agent system
    console.print("\n" + "="*70 + "\n")
    result = coordinator.run(user_query, max_iterations=3, verbose=True)
    
    # Display final results
    console.print("\n" + "="*70 + "\n")
    console.print(Panel(
        f"[bold green]Processing Complete![/bold green]\n\n"
        f"Iterations: {result['iterations']}\n"
        f"Converged: {'Yes' if result['converged'] else 'No'}\n"
        f"Generator Calls: {result['generator_calls']}\n"
        f"Critic Calls: {result['critic_calls']}",
        title="📊 Statistics",
        border_style="green"
    ))
    
    console.print(Panel(
        Markdown(result['final_response']),
        title="[bold cyan]Final Refined Response",
        border_style="cyan"
    ))

if __name__ == "__main__":
    main()
