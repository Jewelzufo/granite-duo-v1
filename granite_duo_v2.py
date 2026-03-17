#!/usr/bin/env python3
"""
Multi-Agent System with Context Management using IBM Granite and LFM
Author: Julian A. Gonzalez (Enhanced)
Pattern: Researcher-Critic with Context Storage

This implementation creates a multi-agent system where:
- Agent 1 (Generator): Produces initial responses (granite3-moe:1b)
- Agent 2 (Critic): Evaluates and provides constructive feedback (granite3-moe:1b)
- Agent 3 (LFM Analyzer): Analyzes conversation and creates summaries (lfm2.5-thinking:1.2b)
- Agent 4 (Context Storage): Manages context storage and retrieval (granite4:350m-h)
- Coordinator: Manages the interaction loop and convergence

Copyright 2025 Julian A. Gonzalez, 

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
    LFM_ANALYZER = "lfm_analyzer"
    CONTEXT_STORAGE = "context_storage"

@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    role: AgentRole
    system_prompt: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 2048

@dataclass
class ConversationState:
    """State management for agent conversations"""
    user_query: str
    generator_output: str = ""
    critic_feedback: str = ""
    context_summary: str = ""  # NEW: Current context summary
    iteration: int = 0
    max_iterations: int = 3
    history: List[Dict] = field(default_factory=list)
    converged: bool = False

# ============================================================================
# SYSTEM PROMPTS (Optimized for each model)
# ============================================================================

GENERATOR_SYSTEM_PROMPT = """You are a Generator Agent specializing in creating comprehensive, accurate responses.

Your responsibilities:
- Analyze user queries carefully and provide detailed, well-structured responses
- Draw upon your knowledge to give informative answers
- Be clear, concise, and accurate
- Structure your responses with proper formatting when appropriate
- If you receive feedback, incorporate it to improve your response
- Use the provided context summary to maintain consistency across iterations

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

LFM_ANALYZER_SYSTEM_PROMPT = """You are a Context Analysis Agent specializing in analyzing conversation flow and creating concise summaries.

Your responsibilities:
- Analyze the user query, the current response, and critic feedback
- Review any previous context summary if available
- Identify key information, improvements made, and remaining gaps
- Create a brief but comprehensive summary (2-4 sentences) that captures essential context
- Focus on facts, key arguments, and improvement areas

Output ONLY the summary text, with no labels or additional formatting."""

CONTEXT_STORAGE_SYSTEM_PROMPT = """You are a Context Storage Agent specializing in managing conversation context.

Your responsibilities:
- Store conversation summaries securely and concisely
- When storing: Confirm with "Context stored:" followed by 2-3 key bullet points
- When retrieving: Return the stored context exactly as saved
- Maintain context format and structure
- Ensure context is ready for use by other agents

Be concise and structured in your confirmations and retrievals."""

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

Critic Feedback:
{context['feedback']}"""
                
                if context.get('context_summary'):
                    prompt += f"""

Stored Context Summary:
{context['context_summary']}"""

                prompt += """

Please provide an improved response that addresses the feedback while maintaining quality and incorporating the context."""
            else:
                prompt = f"User Query: {input_text}\n\nProvide a comprehensive response:"
                
        elif self.config.role == AgentRole.CRITIC:
            prompt = f"""Original Query: {context['query']}

Response to Evaluate:
{input_text}

Provide constructive feedback following the specified format."""
            
        elif self.config.role == AgentRole.LFM_ANALYZER:
            # Input is already prepared analysis text
            prompt = input_text
            
        elif self.config.role == AgentRole.CONTEXT_STORAGE:
            # Store the summary
            prompt = f"""Store this conversation summary:

{input_text}

Confirm with: "Context stored:" followed by 2-3 key bullet points."""
        
        response = self.client.generate(
            prompt=prompt,
            system=self.config.system_prompt,
            model=self.config.model,
            temperature=self.config.temperature
        )
        
        return response

# ============================================================================
# MULTI-AGENT COORDINATOR
# ============================================================================

class MultiAgentCoordinator:
    """Coordinates interaction between Generator, Critic, LFM Analyzer, and Context Storage agents"""
    
    def __init__(self, client: OllamaClient):
        self.client = client
        
        # Initialize agents
        self.generator = Agent(
            AgentConfig(
                name="Generator",
                role=AgentRole.GENERATOR,
                system_prompt=GENERATOR_SYSTEM_PROMPT,
                model="granite3-moe:1b"
            ),
            client
        )
        
        self.critic = Agent(
            AgentConfig(
                name="Critic",
                role=AgentRole.CRITIC,
                system_prompt=CRITIC_SYSTEM_PROMPT,
                model="granite3-moe:1b"
            ),
            client
        )
        
        # NEW: LFM Analyzer Agent
        self.lfm_analyzer = Agent(
            AgentConfig(
                name="LFM_Analyzer",
                role=AgentRole.LFM_ANALYZER,
                system_prompt=LFM_ANALYZER_SYSTEM_PROMPT,
                model="lfm2.5-thinking:1.2b",
                temperature=0.3  # Lower temp for analytical focus
            ),
            client
        )
        
        # NEW: Context Storage Agent
        self.context_storage = Agent(
            AgentConfig(
                name="Context_Storage",
                role=AgentRole.CONTEXT_STORAGE,
                system_prompt=CONTEXT_STORAGE_SYSTEM_PROMPT,
                model="granite4:350m-h",
                temperature=0.1  # Very low temp for consistency
            ),
            client
        )
    
    def run(self, user_query: str, max_iterations: int = 3, verbose: bool = True) -> Dict:
        """Run the multi-agent system with context management"""
        
        state = ConversationState(
            user_query=user_query,
            max_iterations=max_iterations
        )
        
        if verbose:
            console.print(Panel(
                f"[bold cyan]Starting Multi-Agent Processing with Context Management[/bold cyan]\n"
                f"Query: {user_query}\n"
                f"Max Iterations: {max_iterations}",
                title="🤖 Multi-Agent System"
            ))
        
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
                
                # Build context for generator
                context = {
                    'query': user_query,
                    'feedback': state.critic_feedback if iteration > 0 else None,
                    'previous_response': state.generator_output if iteration > 0 else None,
                    'context_summary': state.context_summary
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
                    
                    critic_context = {'query': user_query}
                    state.critic_feedback = self.critic.process(
                        state.generator_output,
                        critic_context
                    )
                    
                    progress.remove_task(task)
                    
                    if verbose:
                        console.print(Panel(
                            state.critic_feedback,
                            title=f"[yellow]Critic Feedback (Iteration {state.iteration})",
                            border_style="yellow"
                        ))
                    
                    # Check for early convergence
                    if "no significant improvements needed" in state.critic_feedback.lower():
                        state.converged = True
                        if verbose:
                            console.print("[green]✓ Converged: Response quality satisfactory[/green]")
                        break
                    
                    # NEW: LFM Analyzer phase
                    task = progress.add_task(
                        f"[magenta]Iteration {state.iteration}/{max_iterations}: LFM analyzing context...",
                        total=None
                    )
                    
                    # Prepare analysis input for LFM
                    analysis_input = f"""Please analyze the following conversation state and create a concise summary:

User Query: {user_query}
Iteration: {state.iteration}
Current Response: {state.generator_output}
Critic Feedback: {state.critic_feedback}
Previous Context Summary: {state.context_summary if state.context_summary else "None"}

Create a 2-4 sentence summary that captures:
1. Key points of the current response
2. Main criticisms or improvement areas
3. What should be focused on in the next iteration

Summary:"""
                    
                    # LFM creates new summary
                    try:
                        state.context_summary = self.lfm_analyzer.process(analysis_input)
                    except Exception as e:
                        console.print(f"[red]LFM Analyzer error: {e}[/red]")
                        state.context_summary = "Error in context analysis."
                    
                    progress.remove_task(task)
                    
                    # NEW: Context Storage phase
                    task = progress.add_task(
                        f"[blue]Iteration {state.iteration}/{max_iterations}: Context Storage updating...",
                        total=None
                    )
                    
                    # Store the new summary
                    try:
                        storage_response = self.context_storage.process(state.context_summary)
                    except Exception as e:
                        console.print(f"[red]Context Storage error: {e}[/red]")
                        storage_response = "Context storage failed."
                    
                    progress.remove_task(task)
                    
                    if verbose:
                        console.print(Panel(
                            f"[bold]LFM Analysis:[/bold]\n{state.context_summary}\n\n"
                            f"[bold]Storage:[/bold]\n{storage_response}",
                            title=f"[magenta]Context Management (Iteration {state.iteration})",
                            border_style="magenta"
                        ))
                
                # Store history
                state.history.append({
                    'iteration': state.iteration,
                    'generator_output': state.generator_output,
                    'critic_feedback': state.critic_feedback if iteration < max_iterations - 1 else None,
                    'context_summary': state.context_summary
                })
        
        return {
            'final_response': state.generator_output,
            'iterations': state.iteration,
            'converged': state.converged,
            'history': state.history,
            'generator_calls': self.generator.call_count,
            'critic_calls': self.critic.call_count,
            'lfm_calls': self.lfm_analyzer.call_count,
            'context_storage_calls': self.context_storage.call_count
        }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_prerequisites():
    """Check if all prerequisites are met"""
    console.print("[bold]Checking Prerequisites...[/bold]")
    
    client = OllamaClient()
    if not client.check_ollama_status():
        console.print("[red]✗ Ollama is not running![/red]")
        console.print("\nPlease start Ollama:")
        console.print("  - On macOS/Linux: Run 'ollama serve' in a terminal")
        console.print("  - On Windows: Start the Ollama application")
        return False
    console.print("[green]✓ Ollama is running[/green]")
    
    # Check all required models
    required_models = [
        ("granite3-moe:1b", "Granite 3 MoE"),
        ("lfm2.5-thinking:1.2b", "LFM 2.5 Thinking"),
        ("granite4:350m-h", "Granite 4 350m")
    ]
    
    for model_name, display_name in required_models:
        if not client.check_model_availability(model_name):
            console.print(f"[yellow]⚠ {display_name} ({model_name}) not found[/yellow]")
            console.print(f"Pulling {display_name}... This may take a few minutes.")
            try:
                subprocess.run(
                    ["ollama", "pull", model_name],
                    check=True,
                    capture_output=False
                )
                console.print(f"[green]✓ {display_name} downloaded successfully[/green]")
            except subprocess.CalledProcessError:
                console.print(f"[red]✗ Failed to download {display_name}[/red]")
                return False
        else:
            console.print(f"[green]✓ {display_name} model available[/green]")
    
    return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    console.print(Panel.fit(
        "[bold cyan]IBM Granite Multi-Agent System with Context Management[/bold cyan]\n"
        "[dim]Powered by granite3-moe:1b, lfm2.5-thinking:1.2b, and granite4:350m-h via Ollama[/dim]",
        border_style="cyan"
    ))
    
    # Check prerequisites
    if not check_prerequisites():
        return
    
    console.print("\n" + "="*70 + "\n")
    
    # Initialize system
    client = OllamaClient()
    coordinator = MultiAgentCoordinator(client)
    
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
    
    # Run the multi-agent system
    console.print("\n" + "="*70 + "\n")
    result = coordinator.run(user_query, max_iterations=3, verbose=True)
    
    # Display final results
    console.print("\n" + "="*70 + "\n")
    console.print(Panel(
        f"[bold green]Processing Complete![/bold green]\n\n"
        f"Iterations: {result['iterations']}\n"
        f"Converged: {'Yes' if result['converged'] else 'No'}\n"
        f"Generator Calls: {result['generator_calls']}\n"
        f"Critic Calls: {result['critic_calls']}\n"
        f"LFM Analyzer Calls: {result['lfm_calls']}\n"
        f"Context Storage Calls: {result['context_storage_calls']}",
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