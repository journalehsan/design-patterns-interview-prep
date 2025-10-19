#!/usr/bin/env python3
'''
🚀 QUICK DEMO - Design Patterns Interview Prep 🚀

This script provides a quick demonstration of all design patterns
without the interactive menu. Perfect for seeing all patterns in action
at once or for automated testing.

Usage:
    python quick_demo.py
'''

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_all_demos():
    """Run all pattern demos in sequence"""
    print("🚀 DESIGN PATTERNS QUICK DEMO")
    print("="*60)
    print("Running all pattern demos in sequence...")
    print("="*60)
    
    demos = [
        ("Observer Pattern", "observer_pattern", "demo_observer_interview"),
        ("Strategy Pattern", "strategy_patttern", "demo_strategy_interview"),
        ("Adapter Pattern", "adapter_pattern", "demo_adapter_interview"),
        ("Decorator Pattern", "decorator_pattern", "demo_decorator_interview"),
        ("Command Pattern", "command_pattern", "demo_command_interview"),
        ("Memento Pattern", "memento_pattern", "demo_memento_interview"),
        ("Visitor Pattern", "visitor_pattern", "demo_visitor_interview"),
        ("Template Method Pattern", "template_method_pattern", "demo_template_method_interview"),
        ("Composite Pattern", "composite_pattern", "demo_composite_interview"),
        ("Builder Pattern", "builder_pattern", "demo_builder_interview"),
        ("Factory Patterns", "factory_patterns", "demo_factory_interview"),
        ("Singleton Pattern", "singleton_pattern", "demo_singleton_interview")
    ]
    
    for i, (name, module_name, demo_func_name) in enumerate(demos, 1):
        try:
            print(f"\n{'='*20} {i}/12: {name} {'='*20}")
            module = __import__(module_name)
            demo_func = getattr(module, demo_func_name)
            demo_func()
            print(f"✅ {name} demo completed successfully!")
        except Exception as e:
            print(f"❌ Error running {name} demo: {e}")
    
    print("\n" + "="*60)
    print("🎉 All demos completed!")
    print("💡 For interactive exploration, run: python main.py")
    print("="*60)

if __name__ == "__main__":
    run_all_demos()
