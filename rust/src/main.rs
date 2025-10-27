use std::io;
mod patterns;

use patterns::{
    demo_builder, demo_factory, demo_singleton, demo_observer, 
    demo_strategy, demo_command, demo_decorator, demo_adapter,
    demo_facade, demo_template_method, demo_proxy, demo_visitor,
    demo_memento, demo_chain_of_responsibility, demo_state
};

fn main() {
    let menu = DesignPatternsMenu::new();
    menu.run();
}

struct DesignPatternsMenu;

impl DesignPatternsMenu {
    fn new() -> Self {
        DesignPatternsMenu
    }

    fn display_header(&self) {
        println!("\n{}", "=".repeat(80));
        println!("🚀 DESIGN PATTERNS INTERVIEW PREP - RUST EDITION 🚀");
        println!("{}", "=".repeat(80));
        println!("Master the most common design patterns in Rust!");
        println!("Each pattern includes real-world examples and Rust-specific features.");
        println!("{}", "=".repeat(80));
    }

    fn display_menu(&self) {
        println!("\n📚 AVAILABLE PATTERNS:");
        println!("{}", "-".repeat(50));
        println!("1.  Builder Pattern - Complex Object Construction");
        println!("2.  Factory Pattern - Object Creation");
        println!("3.  Singleton Pattern - Single Instance Management");
        println!("4.  Observer Pattern - Event System & Notifications");
        println!("5.  Strategy Pattern - Algorithm Selection");
        println!("6.  Command Pattern - Undo/Redo & Transactions");
        println!("7.  Decorator Pattern - Dynamic Behavior");
        println!("8.  Adapter Pattern - Legacy Integration");
        println!("9.  Facade Pattern - Simplified Interface");
        println!("10. Template Method Pattern - Algorithm Skeleton");
        println!("11. Proxy Pattern - Lazy Loading");
        println!("12. Visitor Pattern - Operations on Structures");
        println!("13. Memento Pattern - State Restoration");
        println!("14. Chain of Responsibility - Request Handling");
        println!("15. State Pattern - Behavior Based on State");
        println!("16. 📖 Interview Tips & Common Questions");
        println!("17. 🚪 Exit");
        println!("{}", "-".repeat(50));
    }

    fn display_interview_tips(&self) {
        println!("\n{}", "=".repeat(60));
        println!("📖 INTERVIEW TIPS & STRATEGIES");
        println!("{}", "=".repeat(60));
        
        println!("\n💡 Key Interview Tips:");
        let tips = vec![
            "🎯 Always explain the problem the pattern solves",
            "💡 Provide real-world examples from your experience",
            "🔧 Show how to implement the pattern step by step",
            "⚠️ Discuss trade-offs and when NOT to use the pattern",
            "🚀 Mention performance implications and alternatives",
            "🧪 Be ready to handle edge cases and error scenarios"
        ];
        for tip in tips {
            println!("   {}", tip);
        }
        
        println!("\n🔄 Common Follow-up Questions:");
        let questions = vec![
            "How would you test this pattern?",
            "What are the performance implications?",
            "How does this compare to [other pattern]?",
            "What if you need to handle [specific edge case]?",
            "How would you implement this in a distributed system?",
            "What are the memory implications?"
        ];
        for (i, question) in questions.iter().enumerate() {
            println!("   {}. {}", i + 1, question);
        }
        
        println!("\n{}", "=".repeat(60));
    }

    fn run_pattern_demo(&self, pattern_key: &str) {
        println!("\n🚀 Running demo...\n");
        
        match pattern_key {
            "1" => demo_builder(),
            "2" => demo_factory(),
            "3" => demo_singleton(),
            "4" => demo_observer(),
            "5" => demo_strategy(),
            "6" => demo_command(),
            "7" => demo_decorator(),
            "8" => demo_adapter(),
            "9" => demo_facade(),
            "10" => demo_template_method(),
            "11" => demo_proxy(),
            "12" => demo_visitor(),
            "13" => demo_memento(),
            "14" => demo_chain_of_responsibility(),
            "15" => demo_state(),
            _ => println!("❌ Invalid pattern selection!"),
        }
        
        println!("\n{}", "=".repeat(60));
        println!("✅ Demo completed successfully!");
    }

    fn run(&self) {
        loop {
            self.display_header();
            self.display_menu();
            
            print!("\n🎯 Choose a pattern to explore (1-17): ");
            io::Write::flush(&mut io::stdout()).expect("Failed to flush stdout");
            
            let mut choice = String::new();
            io::stdin().read_line(&mut choice).expect("Failed to read line");
            let choice = choice.trim();
            
            match choice {
                "16" => {
                    self.display_interview_tips();
                    println!("\nPress Enter to continue...");
                    let mut buffer = String::new();
                    io::stdin().read_line(&mut buffer).unwrap();
                }
                "17" => {
                    println!("\n🎉 Thanks for using Design Patterns Interview Prep (Rust Edition)!");
                    println!("Good luck with your interviews! 🚀");
                    break;
                }
                pattern if pattern >= "1" && pattern <= "15" => {
                    self.run_pattern_demo(pattern);
                    
                    print!("\n🔄 Would you like to explore another pattern? (y/n): ");
                    io::Write::flush(&mut io::stdout()).expect("Failed to flush stdout");
                    
                    let mut continue_choice = String::new();
                    io::stdin().read_line(&mut continue_choice).expect("Failed to read line");
                    
                    if continue_choice.trim().to_lowercase() != "y" && 
                       continue_choice.trim().to_lowercase() != "yes" {
                        println!("\n🎉 Thanks for using Design Patterns Interview Prep (Rust Edition)!");
                        println!("Good luck with your interviews! 🚀");
                        break;
                    }
                }
                _ => {
                    println!("❌ Invalid choice! Please select 1-17.");
                    println!("\nPress Enter to continue...");
                    let mut buffer = String::new();
                    io::stdin().read_line(&mut buffer).unwrap();
                }
            }
        }
    }
}
