#pragma once

#include <iostream>
#include <string>
#include <mutex>
#include <memory>

namespace Patterns {

/*
 * SINGLETON PATTERN
 * 
 * 🎯 PROBLEM: Need exactly one instance of a class with global access point
 * 
 * 💡 SOLUTION: Ensure class has only one instance and provide global access to it
 * 
 * 🌍 REAL-WORLD EXAMPLES:
 *    - Database connection pools
 *    - Logging systems
 *    - Configuration managers
 *    - Cache managers
 * 
 * ⚠️ CAUTIONS:
 *    - Can be anti-pattern if overused
 *    - Makes unit testing difficult
 *    - Hidden dependencies
 *    - Thread-safety concerns
 */

// Thread-safe Singleton using Meyer's Singleton (C++11)
class ConfigurationManager {
private:
    std::string appName_;
    std::string version_;
    bool debugMode_;
    mutable std::mutex mutex_;

    // Private constructor
    ConfigurationManager() 
        : appName_("MyApp"), version_("1.0.0"), debugMode_(false) {
        std::cout << "🔧 ConfigurationManager initialized\n";
    }

    // Delete copy constructor and assignment operator
    ConfigurationManager(const ConfigurationManager&) = delete;
    ConfigurationManager& operator=(const ConfigurationManager&) = delete;

public:
    // Thread-safe singleton instance (C++11 guarantees thread-safe initialization)
    static ConfigurationManager& getInstance() {
        static ConfigurationManager instance;
        return instance;
    }

    void setAppName(const std::string& name) {
        std::lock_guard<std::mutex> lock(mutex_);
        appName_ = name;
    }

    std::string getAppName() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return appName_;
    }

    void setVersion(const std::string& version) {
        std::lock_guard<std::mutex> lock(mutex_);
        version_ = version;
    }

    std::string getVersion() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return version_;
    }

    void setDebugMode(bool debug) {
        std::lock_guard<std::mutex> lock(mutex_);
        debugMode_ = debug;
    }

    bool isDebugMode() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return debugMode_;
    }

    void displayConfig() const {
        std::lock_guard<std::mutex> lock(mutex_);
        std::cout << "⚙️  Configuration:\n";
        std::cout << "   App Name: " << appName_ << "\n";
        std::cout << "   Version: " << version_ << "\n";
        std::cout << "   Debug Mode: " << (debugMode_ ? "ON" : "OFF") << "\n";
    }
};

void demoSingleton() {
    std::cout << "=== SINGLETON PATTERN DEMO ===\n\n";
    
    std::cout << "📝 Accessing singleton instance (first time):\n";
    auto& config1 = ConfigurationManager::getInstance();
    config1.displayConfig();
    
    std::cout << "\n📝 Modifying configuration:\n";
    config1.setAppName("Design Patterns Demo");
    config1.setVersion("2.0.0");
    config1.setDebugMode(true);
    
    std::cout << "\n📝 Accessing singleton instance (second time):\n";
    auto& config2 = ConfigurationManager::getInstance();
    config2.displayConfig();
    
    std::cout << "\n✅ Both references point to the same instance!\n";
    std::cout << "   Address of config1: " << &config1 << "\n";
    std::cout << "   Address of config2: " << &config2 << "\n";
    
    std::cout << "\n💡 INTERVIEW INSIGHTS:\n";
    std::cout << "   • Meyer's Singleton (C++11) is thread-safe by default\n";
    std::cout << "   • Static local variable ensures single instance\n";
    std::cout << "   • Lazy initialization - created on first use\n";
    std::cout << "   • Use mutex for thread-safe member access\n";
    std::cout << "   • Consider dependency injection as alternative\n\n";
    
    std::cout << "⚠️  CAUTIONS:\n";
    std::cout << "   • Can become anti-pattern if overused\n";
    std::cout << "   • Makes unit testing harder (global state)\n";
    std::cout << "   • Hidden dependencies between classes\n";
    std::cout << "   • Consider alternatives: DI, static methods\n";
}

} // namespace Patterns
