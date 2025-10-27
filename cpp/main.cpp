/*
 * 🚀 DESIGN PATTERNS INTERVIEW PREP - C++ EDITION 🚀
 * 
 * This is the main entry point for the Design Patterns Interview Preparation system.
 * It provides an interactive menu to explore different design patterns with
 * interview-focused examples and explanations.
 * 
 * 🎯 FEATURES:
 * - Interactive pattern selection
 * - Interview-focused demos
 * - Real-world examples with modern C++ features
 * - Common interview questions
 * - Performance considerations
 * - Exception safety and RAII
 * 
 * 💡 USAGE:
 *     mkdir build && cd build
 *     cmake ..
 *     make
 *     ./design_patterns_cpp
 * 
 * 📚 PATTERNS INCLUDED:
 * 1. Builder Pattern - Complex Object Construction
 * 2. Factory Pattern - Object Creation
 * 3. Singleton Pattern - Single Instance Management
 * 4. Observer Pattern - Event System & Notifications
 * 5. Strategy Pattern - Algorithm Selection
 * 6. Command Pattern - Undo/Redo & Transactions
 * 7. Decorator Pattern - Dynamic Behavior
 * 8. Adapter Pattern - Legacy Integration
 * 9. Facade Pattern - Simplified Interface
 * 10. Template Method Pattern - Algorithm Skeleton
 * 11. Proxy Pattern - Lazy Loading
 * 12. Visitor Pattern - Operations on Structures
 * 13. Memento Pattern - State Restoration
 * 14. Chain of Responsibility - Request Handling
 * 15. State Pattern - Behavior Based on State
 */

#include <iostream>
#include <string>
#include <vector>
#include <limits>

// Include all pattern headers
#include "patterns/builder.hpp"
#include "patterns/factory.hpp"
#include "patterns/singleton.hpp"
#include "patterns/observer.hpp"
#include "patterns/strategy.hpp"
#include "patterns/command.hpp"
#include "patterns/decorator.hpp"
#include "patterns/adapter.hpp"
#include "patterns/facade.hpp"
#include "patterns/template_method.hpp"
#include "patterns/proxy.hpp"
#include "patterns/visitor.hpp"
#include "patterns/memento.hpp"
#include "patterns/chain_of_responsibility.hpp"
#include "patterns/state.hpp"

class DesignPatternsMenu {
private:
    void displayHeader() const {
        std::cout << "\n" << std::string(80, '=') << "\n";
        std::cout << "🚀 DESIGN PATTERNS INTERVIEW PREP - C++ EDITION 🚀\n";
        std::cout << std::string(80, '=') << "\n";
        std::cout << "Master the most common design patterns in C++!\n";
        std::cout << "Each pattern includes real-world examples and modern C++ features.\n";
        std::cout << std::string(80, '=') << "\n";
    }

    void displayMenu() const {
        std::cout << "\n📚 AVAILABLE PATTERNS:\n";
        std::cout << std::string(50, '-') << "\n";
        std::cout << "1.  Builder Pattern - Complex Object Construction\n";
        std::cout << "2.  Factory Pattern - Object Creation\n";
        std::cout << "3.  Singleton Pattern - Single Instance Management\n";
        std::cout << "4.  Observer Pattern - Event System & Notifications\n";
        std::cout << "5.  Strategy Pattern - Algorithm Selection\n";
        std::cout << "6.  Command Pattern - Undo/Redo & Transactions\n";
        std::cout << "7.  Decorator Pattern - Dynamic Behavior\n";
        std::cout << "8.  Adapter Pattern - Legacy Integration\n";
        std::cout << "9.  Facade Pattern - Simplified Interface\n";
        std::cout << "10. Template Method Pattern - Algorithm Skeleton\n";
        std::cout << "11. Proxy Pattern - Lazy Loading\n";
        std::cout << "12. Visitor Pattern - Operations on Structures\n";
        std::cout << "13. Memento Pattern - State Restoration\n";
        std::cout << "14. Chain of Responsibility - Request Handling\n";
        std::cout << "15. State Pattern - Behavior Based on State\n";
        std::cout << "16. 📖 Interview Tips & Common Questions\n";
        std::cout << "17. 🚪 Exit\n";
        std::cout << std::string(50, '-') << "\n";
    }

    void displayInterviewTips() const {
        std::cout << "\n" << std::string(60, '=') << "\n";
        std::cout << "📖 INTERVIEW TIPS & STRATEGIES\n";
        std::cout << std::string(60, '=') << "\n";
        
        std::cout << "\n💡 Key Interview Tips:\n";
        std::vector<std::string> tips = {
            "🎯 Always explain the problem the pattern solves",
            "💡 Provide real-world examples from your experience",
            "🔧 Show how to implement the pattern step by step",
            "⚠️ Discuss trade-offs and when NOT to use the pattern",
            "🚀 Mention performance implications and alternatives",
            "🧪 Be ready to handle edge cases and error scenarios"
        };
        for (const auto& tip : tips) {
            std::cout << "   " << tip << "\n";
        }
        
        std::cout << "\n🔄 Common Follow-up Questions:\n";
        std::vector<std::string> questions = {
            "How would you test this pattern?",
            "What are the performance implications?",
            "How does this compare to [other pattern]?",
            "What if you need to handle [specific edge case]?",
            "How would you implement this in a distributed system?",
            "What are the memory implications?"
        };
        for (size_t i = 0; i < questions.size(); ++i) {
            std::cout << "   " << (i + 1) << ". " << questions[i] << "\n";
        }
        
        std::cout << "\n" << std::string(60, '=') << "\n";
    }

    void runPatternDemo(int choice) {
        std::cout << "\n🚀 Running demo...\n\n";
        
        switch(choice) {
            case 1:
                Patterns::demoBuilder();
                break;
            case 2:
                Patterns::demoFactory();
                break;
            case 3:
                Patterns::demoSingleton();
                break;
            case 4:
                Patterns::demoObserver();
                break;
            case 5:
                Patterns::demoStrategy();
                break;
            case 6:
                Patterns::demoCommand();
                break;
            case 7:
                Patterns::demoDecorator();
                break;
            case 8:
                Patterns::demoAdapter();
                break;
            case 9:
                Patterns::demoFacade();
                break;
            case 10:
                Patterns::demoTemplateMethod();
                break;
            case 11:
                Patterns::demoProxy();
                break;
            case 12:
                Patterns::demoVisitor();
                break;
            case 13:
                Patterns::demoMemento();
                break;
            case 14:
                Patterns::demoChainOfResponsibility();
                break;
            case 15:
                Patterns::demoState();
                break;
            default:
                std::cout << "❌ Invalid pattern selection!\n";
                return;
        }
        
        std::cout << "\n" << std::string(60, '=') << "\n";
        std::cout << "✅ Demo completed successfully!\n";
    }

    void clearInputBuffer() {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    void waitForEnter() {
        std::cout << "\nPress Enter to continue...";
        clearInputBuffer();
        std::cin.get();
    }

public:
    void run() {
        int choice;
        std::string continueChoice;
        
        while (true) {
            displayHeader();
            displayMenu();
            
            std::cout << "\n🎯 Choose a pattern to explore (1-17): ";
            
            if (!(std::cin >> choice)) {
                std::cout << "❌ Invalid input! Please enter a number between 1-17.\n";
                clearInputBuffer();
                waitForEnter();
                continue;
            }
            
            if (choice == 16) {
                displayInterviewTips();
                waitForEnter();
            }
            else if (choice == 17) {
                std::cout << "\n🎉 Thanks for using Design Patterns Interview Prep (C++ Edition)!\n";
                std::cout << "Good luck with your interviews! 🚀\n";
                break;
            }
            else if (choice >= 1 && choice <= 15) {
                runPatternDemo(choice);
                
                std::cout << "\n🔄 Would you like to explore another pattern? (y/n): ";
                std::cin >> continueChoice;
                
                if (continueChoice != "y" && continueChoice != "Y" && 
                    continueChoice != "yes" && continueChoice != "Yes") {
                    std::cout << "\n🎉 Thanks for using Design Patterns Interview Prep (C++ Edition)!\n";
                    std::cout << "Good luck with your interviews! 🚀\n";
                    break;
                }
            }
            else {
                std::cout << "❌ Invalid choice! Please select 1-17.\n";
                waitForEnter();
            }
        }
    }
};

int main() {
    try {
        DesignPatternsMenu menu;
        menu.run();
        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "❌ Fatal error: " << e.what() << "\n";
        return 1;
    }
}
