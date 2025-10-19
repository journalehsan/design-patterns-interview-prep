#!/usr/bin/env python3
'''
🚀 DESIGN PATTERNS INTERVIEW PREP - MAIN MENU 🚀

This is the main entry point for the Design Patterns Interview Preparation system.
It provides an interactive menu to explore different design patterns with
interview-focused examples and explanations.

🎯 FEATURES:
- Interactive pattern selection
- Interview-focused demos
- Real-world examples
- Common interview questions
- Performance considerations
- Error handling scenarios

💡 USAGE:
    python main.py

📚 PATTERNS INCLUDED:
1. Observer Pattern - Event System & Notifications
2. Strategy Pattern - Validation & Algorithm Selection
3. Adapter Pattern - Legacy Integration & Data Transformation
4. Decorator Pattern - Middleware & Cross-cutting Concerns
5. Command Pattern - Undo/Redo & Transaction Management
'''

import sys
import os
from typing import Dict, Callable, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import pattern demos
try:
    from observer_pattern import demo_observer_interview
    from strategy_patttern import demo_strategy_interview
    from adapter_pattern import demo_adapter_interview
    from decorator_pattern import demo_decorator_interview
    from command_pattern import demo_command_interview
    from memento_pattern import demo_memento_interview
    from visitor_pattern import demo_visitor_interview
    from template_method_pattern import demo_template_method_interview
    from composite_pattern import demo_composite_interview
    from builder_pattern import demo_builder_interview
    from factory_patterns import demo_factory_interview
    from singleton_pattern import demo_singleton_interview
except ImportError as e:
    print(f"❌ Error importing pattern modules: {e}")
    print("Make sure all pattern files are in the same directory as main.py")
    sys.exit(1)

class DesignPatternsMenu:
    """Main menu system for design patterns interview prep"""
    
    def __init__(self):
        self.patterns = {
            '1': {
                'name': 'Observer Pattern - Event System & Notifications',
                'description': 'One-to-many dependency between objects. When one object changes state, all dependents are notified.',
                'demo': demo_observer_interview,
                'interview_questions': [
                    'How would you design a notification system?',
                    'What if an observer takes too long to process?',
                    'How to prevent memory leaks with observers?',
                    'How to handle failing observers gracefully?'
                ],
                'real_world_examples': [
                    'Event-driven architectures',
                    'Model-View-Controller (MVC)',
                    'Publish-Subscribe systems',
                    'Notification systems'
                ]
            },
            '2': {
                'name': 'Strategy Pattern - Validation & Algorithm Selection',
                'description': 'Define a family of algorithms, encapsulate each one, and make them interchangeable.',
                'demo': demo_strategy_interview,
                'interview_questions': [
                    'How to make validation rules configurable?',
                    'When would you use Strategy vs Template Method?',
                    'How to dynamically change algorithms at runtime?',
                    'How to combine multiple strategies?'
                ],
                'real_world_examples': [
                    'Payment processing systems',
                    'Data validation frameworks',
                    'Sorting algorithms',
                    'Compression algorithms'
                ]
            },
            '3': {
                'name': 'Adapter Pattern - Legacy Integration & Data Transformation',
                'description': 'Allows incompatible interfaces to work together by wrapping existing classes.',
                'demo': demo_adapter_interview,
                'interview_questions': [
                    'How to integrate with a legacy system you can\'t modify?',
                    'What if you need two-way adaptation?',
                    'How to handle incompatible interfaces?',
                    'How to handle data transformation between systems?'
                ],
                'real_world_examples': [
                    'Legacy system integration',
                    'Third-party API wrappers',
                    'Data format converters',
                    'Database adapters'
                ]
            },
            '4': {
                'name': 'Decorator Pattern - Middleware & Cross-cutting Concerns',
                'description': 'Add behavior to objects dynamically without altering their structure.',
                'demo': demo_decorator_interview,
                'interview_questions': [
                    'How to add logging/caching without modifying existing code?',
                    'What\'s the difference between Decorator and Proxy?',
                    'How to manage decorator order?',
                    'How to implement middleware functionality?'
                ],
                'real_world_examples': [
                    'Web middleware (logging, authentication)',
                    'Caching layers',
                    'Input validation',
                    'Performance monitoring'
                ]
            },
            '5': {
                'name': 'Command Pattern - Undo/Redo & Transaction Management',
                'description': 'Encapsulate requests as objects, allowing parameterization, queuing, and undo operations.',
                'demo': demo_command_interview,
                'interview_questions': [
                    'How to implement undo/redo in a text editor?',
                    'What about transactional operations?',
                    'How to handle command queuing?',
                    'How to implement macro commands?'
                ],
                'real_world_examples': [
                    'Text editors with undo/redo',
                    'Database transactions',
                    'GUI button actions',
                    'Remote procedure calls'
                ]
            },
            '6': {
                'name': 'Memento Pattern - State Restoration & Checkpoints',
                'description': 'Capture and externalize an object\'s internal state for later restoration.',
                'demo': demo_memento_interview,
                'interview_questions': [
                    'How to implement save/restore functionality in a game?',
                    'How to implement undo/redo with state snapshots?',
                    'How to handle version control for object states?',
                    'How to implement checkpoint/rollback systems?'
                ],
                'real_world_examples': [
                    'Game save systems',
                    'Document editors with undo/redo',
                    'Database transactions',
                    'Configuration management'
                ]
            },
            '7': {
                'name': 'Visitor Pattern - Operations on Object Structures',
                'description': 'Define operations on object structures without changing the classes.',
                'demo': demo_visitor_interview,
                'interview_questions': [
                    'How to add new operations to existing classes without modifying them?',
                    'How to implement type-safe operations on heterogeneous collections?',
                    'How to separate algorithms from object structure?',
                    'How to implement double dispatch in single-dispatch languages?'
                ],
                'real_world_examples': [
                    'Document processing systems',
                    'Compiler AST visitors',
                    'File system operations',
                    'GUI component rendering'
                ]
            },
            '8': {
                'name': 'Template Method Pattern - Algorithm Skeletons',
                'description': 'Define algorithm skeleton with customizable steps in subclasses.',
                'demo': demo_template_method_interview,
                'interview_questions': [
                    'How to define a common algorithm structure with customizable steps?',
                    'How to avoid code duplication in similar algorithms?',
                    'How to enforce a specific order of operations?',
                    'How to implement the Hollywood Principle?'
                ],
                'real_world_examples': [
                    'Framework lifecycle methods',
                    'Build systems (Maven, Gradle)',
                    'Data processing pipelines',
                    'Game engine update loops'
                ]
            },
            '9': {
                'name': 'Composite Pattern - Tree Structures & Hierarchies',
                'description': 'Compose objects into tree structures to represent part-whole hierarchies.',
                'demo': demo_composite_interview,
                'interview_questions': [
                    'How to represent hierarchical structures like file systems?',
                    'How to implement tree operations uniformly on leaves and composites?',
                    'How to build complex UI component hierarchies?',
                    'How to implement organizational structures or menu systems?'
                ],
                'real_world_examples': [
                    'File system structures',
                    'GUI component hierarchies',
                    'Organizational charts',
                    'Menu systems'
                ]
            },
            '10': {
                'name': 'Builder Pattern - Complex Object Construction',
                'description': 'Separate object construction from representation for flexible building.',
                'demo': demo_builder_interview,
                'interview_questions': [
                    'How to create complex objects with many optional parameters?',
                    'How to build objects step by step with validation?',
                    'How to create different representations of the same object?',
                    'How to make object construction more readable and maintainable?'
                ],
                'real_world_examples': [
                    'StringBuilder in Java/C#',
                    'Query builders (SQL, MongoDB)',
                    'Configuration builders',
                    'HTTP request builders'
                ]
            },
            '11': {
                'name': 'Factory Patterns - Object Creation (Simple, Method, Abstract)',
                'description': 'Create objects without specifying their exact classes.',
                'demo': demo_factory_interview,
                'interview_questions': [
                    'How to create objects without knowing their exact classes?',
                    'What\'s the difference between Simple Factory, Factory Method, and Abstract Factory?',
                    'How to add new product types without modifying existing code?',
                    'How to create families of related objects?'
                ],
                'real_world_examples': [
                    'Payment processor factories',
                    'Document creator factories',
                    'UI theme factories',
                    'Database provider factories'
                ]
            },
            '12': {
                'name': 'Singleton Pattern - Single Instance Management',
                'description': 'Ensure a class has only one instance with global access.',
                'demo': demo_singleton_interview,
                'interview_questions': [
                    'How to ensure only one instance of a class exists?',
                    'What are the problems with Singleton pattern?',
                    'How to implement thread-safe Singleton?',
                    'When should you use Singleton vs Dependency Injection?'
                ],
                'real_world_examples': [
                    'Database connection managers',
                    'Logging systems',
                    'Configuration managers',
                    'UI managers (desktop apps)'
                ]
            }
        }
        
        self.help_info = {
            'interview_tips': [
                '🎯 Always explain the problem the pattern solves',
                '💡 Provide real-world examples from your experience',
                '🔧 Show how to implement the pattern step by step',
                '⚠️ Discuss trade-offs and when NOT to use the pattern',
                '🚀 Mention performance implications and alternatives',
                '🧪 Be ready to handle edge cases and error scenarios'
            ],
            'common_follow_ups': [
                'How would you test this pattern?',
                'What are the performance implications?',
                'How does this compare to [other pattern]?',
                'What if you need to handle [specific edge case]?',
                'How would you implement this in a distributed system?',
                'What are the memory implications?'
            ]
        }
    
    def display_header(self):
        """Display the main header"""
        print("\n" + "="*80)
        print("🚀 DESIGN PATTERNS INTERVIEW PREP 🚀")
        print("="*80)
        print("Master the most common design patterns asked in technical interviews!")
        print("Each pattern includes real-world examples, edge cases, and interview scenarios.")
        print("="*80)
    
    def display_menu(self):
        """Display the main menu"""
        print("\n📚 AVAILABLE PATTERNS:")
        print("-" * 50)
        
        for key, pattern in self.patterns.items():
            print(f"{key}. {pattern['name']}")
            print(f"   {pattern['description']}")
            print()
        
        print("13. 📖 Interview Tips & Common Questions")
        print("14. 🎯 Quick Pattern Comparison")
        print("15. 🚪 Exit")
        print("-" * 50)
    
    def display_pattern_info(self, pattern_key: str):
        """Display detailed information about a pattern"""
        if pattern_key not in self.patterns:
            print("❌ Invalid pattern selection!")
            return
        
        pattern = self.patterns[pattern_key]
        
        print("\n" + "="*60)
        print(f"📖 {pattern['name']}")
        print("="*60)
        print(f"📝 Description: {pattern['description']}")
        
        print(f"\n🎯 Common Interview Questions:")
        for i, question in enumerate(pattern['interview_questions'], 1):
            print(f"   {i}. {question}")
        
        print(f"\n🌍 Real-World Examples:")
        for i, example in enumerate(pattern['real_world_examples'], 1):
            print(f"   {i}. {example}")
        
        print("\n" + "="*60)
    
    def display_interview_tips(self):
        """Display interview tips and common questions"""
        print("\n" + "="*60)
        print("📖 INTERVIEW TIPS & STRATEGIES")
        print("="*60)
        
        print("\n💡 Key Interview Tips:")
        for tip in self.help_info['interview_tips']:
            print(f"   {tip}")
        
        print(f"\n🔄 Common Follow-up Questions:")
        for i, question in enumerate(self.help_info['common_follow_ups'], 1):
            print(f"   {i}. {question}")
        
        print(f"\n🎯 Pattern Selection Strategy:")
        print("   1. Start with the problem you're trying to solve")
        print("   2. Explain why this pattern is the best choice")
        print("   3. Show a simple implementation")
        print("   4. Discuss edge cases and error handling")
        print("   5. Mention alternatives and trade-offs")
        
        print("\n" + "="*60)
    
    def display_pattern_comparison(self):
        """Display a quick comparison of patterns"""
        print("\n" + "="*80)
        print("🎯 QUICK PATTERN COMPARISON")
        print("="*80)
        
        comparison = {
            'Observer': 'Event handling, notifications, MVC',
            'Strategy': 'Algorithm selection, validation, payment processing',
            'Adapter': 'Legacy integration, interface compatibility',
            'Decorator': 'Adding features, middleware, cross-cutting concerns',
            'Command': 'Undo/redo, queuing, macro operations'
        }
        
        print("\n📊 When to Use Each Pattern:")
        print("-" * 50)
        for pattern, use_case in comparison.items():
            print(f"🔹 {pattern:12} → {use_case}")
        
        print(f"\n🤔 Pattern Selection Guide:")
        print("   • Need notifications? → Observer")
        print("   • Multiple algorithms? → Strategy")
        print("   • Incompatible interfaces? → Adapter")
        print("   • Add features dynamically? → Decorator")
        print("   • Need undo/redo? → Command")
        
        print("\n" + "="*80)
    
    def run_pattern_demo(self, pattern_key: str):
        """Run the demo for a selected pattern"""
        if pattern_key not in self.patterns:
            print("❌ Invalid pattern selection!")
            return
        
        pattern = self.patterns[pattern_key]
        
        print(f"\n🚀 Running demo for: {pattern['name']}")
        print("="*60)
        
        try:
            # Run the demo
            pattern['demo']()
            
            print("\n" + "="*60)
            print("✅ Demo completed successfully!")
            
            # Ask if user wants to see pattern info
            response = input("\n📖 Would you like to see pattern details? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                self.display_pattern_info(pattern_key)
        
        except Exception as e:
            print(f"\n❌ Error running demo: {e}")
            print("Please check that all pattern files are present and correct.")
    
    def run(self):
        """Main menu loop"""
        while True:
            try:
                self.display_header()
                self.display_menu()
                
                choice = input("\n🎯 Choose a pattern to explore (1-15): ").strip()
                
                if choice == '13':
                    self.display_interview_tips()
                elif choice == '14':
                    self.display_pattern_comparison()
                elif choice == '15':
                    print("\n🎉 Thanks for using Design Patterns Interview Prep!")
                    print("Good luck with your interviews! 🚀")
                    break
                elif choice in self.patterns:
                    self.run_pattern_demo(choice)
                else:
                    print("❌ Invalid choice! Please select 1-15.")
                
                # Ask if user wants to continue
                if choice in self.patterns:
                    continue_choice = input("\n🔄 Would you like to explore another pattern? (y/n): ").strip().lower()
                    if continue_choice not in ['y', 'yes']:
                        print("\n🎉 Thanks for using Design Patterns Interview Prep!")
                        print("Good luck with your interviews! 🚀")
                        break
                
                # Clear screen for better UX (optional)
                if choice in ['13', '14']:
                    input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using Design Patterns Interview Prep!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("Please try again or contact support.")

def main():
    """Main entry point"""
    try:
        menu = DesignPatternsMenu()
        menu.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
