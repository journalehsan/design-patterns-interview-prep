#pragma once

#include <iostream>
#include <string>
#include <memory>
#include <vector>
#include <sstream>

namespace Patterns {

/*
 * BUILDER PATTERN
 * 
 * 🎯 PROBLEM: Creating complex objects with many optional parameters
 * 
 * 💡 SOLUTION: Separate object construction from representation using a builder
 * 
 * 🌍 REAL-WORLD EXAMPLES:
 *    - StringBuilder in Java/C#
 *    - HTTP request builders
 *    - SQL query builders
 *    - Configuration builders
 * 
 * ⚡ KEY BENEFITS:
 *    - Fluent interface for object construction
 *    - Step-by-step object creation with validation
 *    - Different representations from same building process
 *    - More readable than telescoping constructors
 */

// Product: Complex object to build
class HttpRequest {
private:
    std::string method_;
    std::string url_;
    std::string body_;
    std::vector<std::pair<std::string, std::string>> headers_;
    int timeout_;

public:
    HttpRequest() : method_("GET"), timeout_(30) {}

    void setMethod(const std::string& method) { method_ = method; }
    void setUrl(const std::string& url) { url_ = url; }
    void setBody(const std::string& body) { body_ = body; }
    void addHeader(const std::string& key, const std::string& value) {
        headers_.push_back({key, value});
    }
    void setTimeout(int timeout) { timeout_ = timeout; }

    std::string toString() const {
        std::ostringstream oss;
        oss << "HTTP Request:\n";
        oss << "  Method: " << method_ << "\n";
        oss << "  URL: " << url_ << "\n";
        oss << "  Timeout: " << timeout_ << "s\n";
        oss << "  Headers:\n";
        for (const auto& header : headers_) {
            oss << "    " << header.first << ": " << header.second << "\n";
        }
        if (!body_.empty()) {
            oss << "  Body: " << body_ << "\n";
        }
        return oss.str();
    }
};

// Builder: Constructs HttpRequest objects
class HttpRequestBuilder {
private:
    std::unique_ptr<HttpRequest> request_;

public:
    HttpRequestBuilder() : request_(std::make_unique<HttpRequest>()) {}

    HttpRequestBuilder& method(const std::string& method) {
        request_->setMethod(method);
        return *this;
    }

    HttpRequestBuilder& url(const std::string& url) {
        request_->setUrl(url);
        return *this;
    }

    HttpRequestBuilder& body(const std::string& body) {
        request_->setBody(body);
        return *this;
    }

    HttpRequestBuilder& header(const std::string& key, const std::string& value) {
        request_->addHeader(key, value);
        return *this;
    }

    HttpRequestBuilder& timeout(int timeout) {
        request_->setTimeout(timeout);
        return *this;
    }

    std::unique_ptr<HttpRequest> build() {
        return std::move(request_);
    }
};

void demoBuilder() {
    std::cout << "=== BUILDER PATTERN DEMO ===\n\n";
    
    std::cout << "📝 Building a complex HTTP request with fluent interface:\n\n";
    
    // Build a POST request
    auto request1 = HttpRequestBuilder()
        .method("POST")
        .url("https://api.example.com/users")
        .header("Content-Type", "application/json")
        .header("Authorization", "Bearer token123")
        .body(R"({"name":"John","email":"john@example.com"})")
        .timeout(60)
        .build();
    
    std::cout << request1->toString() << "\n";
    
    std::cout << "✅ Built complex object with fluent interface!\n\n";
    
    // Build a GET request
    std::cout << "📝 Building a simple GET request:\n\n";
    
    auto request2 = HttpRequestBuilder()
        .method("GET")
        .url("https://api.example.com/users/123")
        .header("Accept", "application/json")
        .build();
    
    std::cout << request2->toString() << "\n";
    
    std::cout << "💡 INTERVIEW INSIGHTS:\n";
    std::cout << "   • Builder pattern provides fluent, readable API\n";
    std::cout << "   • Separates construction logic from representation\n";
    std::cout << "   • Allows step-by-step validation during build\n";
    std::cout << "   • Better than telescoping constructors\n";
    std::cout << "   • Can create different representations from same builder\n\n";
    
    std::cout << "🎯 WHEN TO USE:\n";
    std::cout << "   • Object has many optional parameters\n";
    std::cout << "   • Need to construct objects step-by-step\n";
    std::cout << "   • Want to enforce immutability after construction\n";
    std::cout << "   • Complex validation required during construction\n";
}

} // namespace Patterns
