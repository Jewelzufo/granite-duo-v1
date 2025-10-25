#!/usr/bin/env python3
"""
Example demonstrations of the Dual-Agent System
Shows various use cases and configuration options

Author: Julian A. Gonzalez, IBM Champion 2025

DISCLAIMER: This is an independent project and is NOT an official IBM product.

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

from dual_agent_granite import (
    OllamaClient,
    DualAgentCoordinator,
    AgentConfig,
    AgentRole,
    GENERATOR_SYSTEM_PROMPT,
    CRITIC_SYSTEM_PROMPT
)
from rich.console import Console
from rich.table import Table

console = Console()

def example_1_basic_query():
    """Example 1: Basic query with default settings"""
    console.print("\n[bold cyan]Example 1: Basic Query[/bold cyan]\n")
    
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    result = coordinator.run(
        user_query="What are the benefits of using microservices architecture?",
        max_iterations=2,
        verbose=True
    )
    
    console.print(f"\n[green]✓ Completed in {result['iterations']} iterations[/green]")
    return result

def example_2_technical_question():
    """Example 2: Technical question with full iterations"""
    console.print("\n[bold cyan]Example 2: Technical Question[/bold cyan]\n")
    
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    result = coordinator.run(
        user_query="Explain the difference between REST and GraphQL APIs, including pros and cons of each.",
        max_iterations=3,
        verbose=True
    )
    
    # Display statistics
    table = Table(title="Processing Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Iterations", str(result['iterations']))
    table.add_row("Converged", "Yes" if result['converged'] else "No")
    table.add_row("Generator Calls", str(result['generator_calls']))
    table.add_row("Critic Calls", str(result['critic_calls']))
    
    console.print(table)
    return result

def example_3_creative_task():
    """Example 3: Creative writing task"""
    console.print("\n[bold cyan]Example 3: Creative Task with Higher Temperature[/bold cyan]\n")
    
    client = OllamaClient()
    
    # Create coordinator with custom temperature for creativity
    coordinator = DualAgentCoordinator(client)
    coordinator.generator.config.temperature = 0.9  # More creative
    coordinator.critic.config.temperature = 0.5     # More analytical
    
    result = coordinator.run(
        user_query="Write a brief story about an AI that learns to appreciate art.",
        max_iterations=3,
        verbose=True
    )
    
    return result

def example_4_code_generation():
    """Example 4: Code generation and review"""
    console.print("\n[bold cyan]Example 4: Code Generation with Review[/bold cyan]\n")
    
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    result = coordinator.run(
        user_query="Write a Python function to implement a binary search algorithm with proper error handling.",
        max_iterations=3,
        verbose=True
    )
    
    return result

def example_5_comparison_analysis():
    """Example 5: Comparative analysis"""
    console.print("\n[bold cyan]Example 5: Comparative Analysis[/bold cyan]\n")
    
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    result = coordinator.run(
        user_query="Compare Python and JavaScript for backend development. Consider performance, ecosystem, and use cases.",
        max_iterations=3,
        verbose=True
    )
    
    return result

def example_6_minimal_iterations():
    """Example 6: Quick response with minimal refinement"""
    console.print("\n[bold cyan]Example 6: Quick Response Mode[/bold cyan]\n")
    
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    result = coordinator.run(
        user_query="What is machine learning?",
        max_iterations=1,  # Single pass, no refinement
        verbose=True
    )
    
    console.print(f"\n[yellow]Note: Single iteration mode - no critic feedback[/yellow]")
    return result

def example_7_batch_processing():
    """Example 7: Batch processing multiple queries"""
    console.print("\n[bold cyan]Example 7: Batch Processing[/bold cyan]\n")
    
    queries = [
        "What is Docker?",
        "Explain Kubernetes.",
        "What are microservices?"
    ]
    
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    results = []
    for i, query in enumerate(queries, 1):
        console.print(f"\n[cyan]Processing query {i}/{len(queries)}...[/cyan]")
        result = coordinator.run(
            user_query=query,
            max_iterations=2,
            verbose=False  # Suppress detailed output for batch
        )
        results.append({
            'query': query,
            'response': result['final_response'],
            'iterations': result['iterations']
        })
        console.print(f"[green]✓ Query {i} completed in {result['iterations']} iterations[/green]")
    
    # Summary table
    table = Table(title="Batch Processing Results")
    table.add_column("Query", style="cyan", width=30)
    table.add_column("Iterations", style="green")
    table.add_column("Preview", style="white", width=50)
    
    for r in results:
        preview = r['response'][:100] + "..." if len(r['response']) > 100 else r['response']
        table.add_row(r['query'], str(r['iterations']), preview)
    
    console.print("\n")
    console.print(table)
    return results

def example_8_history_tracking():
    """Example 8: Tracking conversation history"""
    console.print("\n[bold cyan]Example 8: History Tracking[/bold cyan]\n")
    
    client = OllamaClient()
    coordinator = DualAgentCoordinator(client)
    
    result = coordinator.run(
        user_query="Explain the concept of recursion with an example.",
        max_iterations=3,
        verbose=False
    )
    
    # Display iteration history
    console.print("\n[bold]Iteration History:[/bold]\n")
    for entry in result['history']:
        console.print(f"[cyan]--- Iteration {entry['iteration']} ---[/cyan]")
        console.print(f"[green]Generator Output:[/green]\n{entry['generator_output'][:200]}...\n")
        if entry['critic_feedback']:
            console.print(f"[yellow]Critic Feedback:[/yellow]\n{entry['critic_feedback'][:200]}...\n")
    
    return result

def run_all_examples():
    """Run all examples in sequence"""
    examples = [
        ("Basic Query", example_1_basic_query),
        ("Technical Question", example_2_technical_question),
        ("Creative Task", example_3_creative_task),
        ("Code Generation", example_4_code_generation),
        ("Comparative Analysis", example_5_comparison_analysis),
        ("Quick Response", example_6_minimal_iterations),
        ("Batch Processing", example_7_batch_processing),
        ("History Tracking", example_8_history_tracking)
    ]
    
    console.print("\n[bold magenta]Dual-Agent System - Example Demonstrations[/bold magenta]\n")
    console.print("Select an example to run:\n")
    
    for i, (name, _) in enumerate(examples, 1):
        console.print(f"  {i}. {name}")
    console.print(f"  {len(examples) + 1}. Run all examples")
    
    choice = console.input("\n[bold cyan]Your choice: [/bold cyan]")
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(examples):
            name, func = examples[choice_num - 1]
            console.print(f"\n[bold]Running: {name}[/bold]")
            func()
        elif choice_num == len(examples) + 1:
            for name, func in examples:
                console.print(f"\n[bold magenta]{'='*70}[/bold magenta]")
                console.print(f"[bold]Running: {name}[/bold]")
                console.print(f"[bold magenta]{'='*70}[/bold magenta]")
                func()
                console.input("\n[dim]Press Enter to continue...[/dim]")
        else:
            console.print("[red]Invalid choice![/red]")
    except ValueError:
        console.print("[red]Invalid input![/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")

if __name__ == "__main__":
    run_all_examples()
