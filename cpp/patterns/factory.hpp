#pragma once

#include <iostream>
#include <string>
#include <memory>
#include <map>

namespace Patterns {

/*
 * FACTORY PATTERN
 * 
 * 🎯 PROBLEM: Creating objects without specifying exact classes
 * 
 * 💡 SOLUTION: Define interface for creating objects, let subclasses decide which class to instantiate
 * 
 * 🌍 REAL-WORLD EXAMPLES:
 *    - Payment processor factories
 *    - Document creator factories
 *    - Database connection factories
 *    - UI theme factories
 * 
 * ⚡ KEY BENEFITS:
 *    - Decouples client code from concrete classes
 *    - Promotes loose coupling
 *    - Makes code more maintainable and testable
 *    - Follows Open/Closed Principle
 */

// Product interface
class PaymentProcessor {
public:
    virtual ~PaymentProcessor() = default;
    virtual void processPayment(double amount) = 0;
    virtual std::string getProcessorName() const = 0;
};

// Concrete Products
class CreditCardProcessor : public PaymentProcessor {
public:
    void processPayment(double amount) override {
        std::cout << "💳 Processing credit card payment: $" << amount << "\n";
        std::cout << "   • Validating card number...\n";
        std::cout << "   • Checking credit limit...\n";
        std::cout << "   • Processing transaction...\n";
        std::cout << "   ✅ Payment successful!\n";
    }

    std::string getProcessorName() const override {
        return "Credit Card Processor";
    }
};

class PayPalProcessor : public PaymentProcessor {
public:
    void processPayment(double amount) override {
        std::cout << "💰 Processing PayPal payment: $" << amount << "\n";
        std::cout << "   • Redirecting to PayPal...\n";
        std::cout << "   • Authenticating user...\n";
        std::cout << "   • Processing transaction...\n";
        std::cout << "   ✅ Payment successful!\n";
    }

    std::string getProcessorName() const override {
        return "PayPal Processor";
    }
};

class BitcoinProcessor : public PaymentProcessor {
public:
    void processPayment(double amount) override {
        std::cout << "₿ Processing Bitcoin payment: $" << amount << "\n";
        std::cout << "   • Converting to BTC...\n";
        std::cout << "   • Broadcasting transaction...\n";
        std::cout << "   • Waiting for confirmations...\n";
        std::cout << "   ✅ Payment successful!\n";
    }

    std::string getProcessorName() const override {
        return "Bitcoin Processor";
    }
};

// Factory Method Pattern
class PaymentProcessorFactory {
public:
    static std::unique_ptr<PaymentProcessor> createProcessor(const std::string& type) {
        if (type == "credit_card") {
            return std::make_unique<CreditCardProcessor>();
        } else if (type == "paypal") {
            return std::make_unique<PayPalProcessor>();
        } else if (type == "bitcoin") {
            return std::make_unique<BitcoinProcessor>();
        }
        throw std::invalid_argument("Unknown payment processor type: " + type);
    }

    static std::vector<std::string> getAvailableProcessors() {
        return {"credit_card", "paypal", "bitcoin"};
    }
};

void demoFactory() {
    std::cout << "=== FACTORY PATTERN DEMO ===\n\n";
    
    std::cout << "💼 Payment Processing System\n\n";
    
    // Create different payment processors using factory
    std::vector<std::string> paymentMethods = {"credit_card", "paypal", "bitcoin"};
    double amount = 99.99;
    
    for (const auto& method : paymentMethods) {
        std::cout << "Creating processor for: " << method << "\n";
        auto processor = PaymentProcessorFactory::createProcessor(method);
        std::cout << "Processor created: " << processor->getProcessorName() << "\n\n";
        processor->processPayment(amount);
        std::cout << "\n" << std::string(50, '-') << "\n\n";
    }
    
    std::cout << "💡 INTERVIEW INSIGHTS:\n";
    std::cout << "   • Factory encapsulates object creation logic\n";
    std::cout << "   • Client doesn't need to know concrete classes\n";
    std::cout << "   • Easy to add new product types without modifying client\n";
    std::cout << "   • Promotes loose coupling and testability\n";
    std::cout << "   • Can use abstract factory for families of related objects\n\n";
    
    std::cout << "🎯 WHEN TO USE:\n";
    std::cout << "   • Don't know exact types ahead of time\n";
    std::cout << "   • Want to provide library/framework extension points\n";
    std::cout << "   • Need to delegate instantiation to subclasses\n";
    std::cout << "   • Want to manage/control object creation process\n";
}

} // namespace Patterns
