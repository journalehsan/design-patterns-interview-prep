'''
🚀 STRATEGY PATTERN - INTERVIEW FOCUSED 🚀

The Strategy Pattern is a behavioral design pattern that enables
selecting an algorithm's behavior at runtime.
It defines a family of algorithms, encapsulates each one,
and makes them interchangeable. This allows the algorithm 
to vary independently from clients that use it.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to make validation rules configurable?"
2. "When would you use Strategy vs Template Method?"
3. "How to dynamically change algorithms at runtime?"
4. "How to combine multiple strategies?"

💡 KEY INTERVIEW POINTS:
- Real-world validation scenarios
- Multiple strategy combinations (AND/OR logic)
- Dynamic strategy switching
- Strategy vs Factory pattern comparison
- Performance considerations
'''

from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
import re
import time

# ============================================================================
# VALIDATION STRATEGIES (Real-world interview scenario)
# ============================================================================

class ValidationStrategy(ABC):
    """Abstract validation strategy interface"""
    @abstractmethod
    def validate(self, data: str) -> bool:
        pass
    
    @abstractmethod
    def get_error_message(self) -> str:
        pass

class EmailValidation(ValidationStrategy):
    """Email validation strategy"""
    def __init__(self):
        self.error_message = "Invalid email format"
        self.pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def validate(self, data: str) -> bool:
        return bool(re.match(self.pattern, data))
    
    def get_error_message(self) -> str:
        return self.error_message

class PhoneValidation(ValidationStrategy):
    """Phone number validation strategy"""
    def __init__(self):
        self.error_message = "Invalid phone number format"
    
    def validate(self, data: str) -> bool:
        # Remove common phone number characters
        cleaned = re.sub(r'[+\-\s\(\)]', '', data)
        # Check if it's all digits and reasonable length
        return cleaned.isdigit() and 7 <= len(cleaned) <= 15
    
    def get_error_message(self) -> str:
        return self.error_message

class CreditCardValidation(ValidationStrategy):
    """Credit card validation using Luhn algorithm"""
    def __init__(self):
        self.error_message = "Invalid credit card number"
    
    def validate(self, data: str) -> bool:
        # Remove spaces and non-digits
        digits = re.sub(r'\D', '', data)
        
        if len(digits) < 13 or len(digits) > 19:
            return False
        
        # Luhn algorithm
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            digit = int(digit)
            if i % 2 == 1:  # Every second digit from right
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        
        return checksum % 10 == 0
    
    def get_error_message(self) -> str:
        return self.error_message

class PasswordValidation(ValidationStrategy):
    """Password strength validation"""
    def __init__(self, min_length: int = 8):
        self.min_length = min_length
        self.error_message = f"Password must be at least {min_length} characters with uppercase, lowercase, digit, and special character"
    
    def validate(self, data: str) -> bool:
        if len(data) < self.min_length:
            return False
        
        has_upper = any(c.isupper() for c in data)
        has_lower = any(c.islower() for c in data)
        has_digit = any(c.isdigit() for c in data)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in data)
        
        return has_upper and has_lower and has_digit and has_special
    
    def get_error_message(self) -> str:
        return self.error_message

# ============================================================================
# MULTI-STRATEGY VALIDATOR (Interview focus: combining strategies)
# ============================================================================

class Validator:
    """
    Enhanced validator that can combine multiple strategies
    Interview question: How to combine multiple validation strategies?
    """
    def __init__(self):
        self._strategies: List[ValidationStrategy] = []
        self._validation_mode = "ALL"  # "ALL" or "ANY"
    
    def add_strategy(self, strategy: ValidationStrategy):
        """Add a validation strategy"""
        self._strategies.append(strategy)
        print(f"✅ Added strategy: {strategy.__class__.__name__}")
    
    def set_validation_mode(self, mode: str):
        """Set validation mode: 'ALL' (AND logic) or 'ANY' (OR logic)"""
        if mode.upper() in ["ALL", "ANY"]:
            self._validation_mode = mode.upper()
            print(f"🔄 Validation mode set to: {self._validation_mode}")
        else:
            raise ValueError("Mode must be 'ALL' or 'ANY'")
    
    def validate(self, data: str) -> Dict[str, Any]:
        """
        Validate data using all strategies
        Returns detailed validation results
        """
        if not self._strategies:
            return {
                'valid': True,
                'message': 'No validation strategies configured',
                'details': []
            }
        
        results = []
        for strategy in self._strategies:
            is_valid = strategy.validate(data)
            results.append({
                'strategy': strategy.__class__.__name__,
                'valid': is_valid,
                'error': strategy.get_error_message() if not is_valid else None
            })
        
        # Determine overall validity based on mode
        if self._validation_mode == "ALL":
            overall_valid = all(r['valid'] for r in results)
        else:  # ANY
            overall_valid = any(r['valid'] for r in results)
        
        return {
            'valid': overall_valid,
            'mode': self._validation_mode,
            'details': results,
            'message': self._get_validation_message(results, overall_valid)
        }
    
    def _get_validation_message(self, results: List[Dict], valid: bool) -> str:
        """Generate human-readable validation message"""
        if valid:
            if self._validation_mode == "ALL":
                return "✅ All validations passed"
            else:
                return "✅ At least one validation passed"
        else:
            if self._validation_mode == "ALL":
                failed = [r['strategy'] for r in results if not r['valid']]
                return f"❌ Failed validations: {', '.join(failed)}"
            else:
                return "❌ All validations failed"

# ============================================================================
# SORTING STRATEGIES (Classic example with enhancements)
# ============================================================================

class SortingStrategy(ABC):
    """Abstract sorting strategy"""
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class BubbleSortStrategy(SortingStrategy):
    """Bubble sort implementation"""
    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def get_name(self) -> str:
        return "Bubble Sort"

class QuickSortStrategy(SortingStrategy):
    """Quick sort implementation"""
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data.copy()
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        return self.sort(left) + middle + self.sort(right)
    
    def get_name(self) -> str:
        return "Quick Sort"

class MergeSortStrategy(SortingStrategy):
    """Merge sort implementation"""
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data.copy()
        
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def get_name(self) -> str:
        return "Merge Sort"

class SortingContext:
    """Context for sorting strategies with performance measurement"""
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy):
        self._strategy = strategy
        print(f"🔄 Sorting strategy changed to: {strategy.get_name()}")
    
    def sort_with_timing(self, data: List[int]) -> Dict[str, Any]:
        """Sort data and measure performance"""
        start_time = time.time()
        result = self._strategy.sort(data)
        end_time = time.time()
        
        return {
            'sorted_data': result,
            'strategy': self._strategy.get_name(),
            'execution_time': end_time - start_time,
            'data_size': len(data)
        }

def demo_strategy_interview():
    """
    🎯 INTERVIEW DEMO: Strategy Pattern
    Demonstrates real-world validation and sorting scenarios
    """
    print("\n" + "="*60)
    print("🚀 STRATEGY PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to make validation rules configurable?")
    print("2. How to combine multiple strategies?")
    print("3. When to use Strategy vs Factory pattern?")
    print("4. How to measure strategy performance?")
    
    # ========================================================================
    # VALIDATION STRATEGIES DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📋 VALIDATION STRATEGIES DEMO")
    print("="*50)
    
    validator = Validator()
    
    # Add validation strategies
    validator.add_strategy(EmailValidation())
    validator.add_strategy(PhoneValidation())
    validator.add_strategy(PasswordValidation(min_length=8))
    
    # Test data
    test_cases = [
        "user@example.com",
        "+1-555-123-4567",
        "Password123!",
        "invalid-email",
        "123",  # Too short for phone
        "weak"  # Weak password
    ]
    
    print("\n🔍 Testing with ALL validation mode (all must pass):")
    validator.set_validation_mode("ALL")
    
    for test_data in test_cases:
        result = validator.validate(test_data)
        print(f"\n📝 Testing: '{test_data}'")
        print(f"   Result: {result['message']}")
        for detail in result['details']:
            status = "✅" if detail['valid'] else "❌"
            print(f"   {status} {detail['strategy']}: {detail['error'] or 'Valid'}")
    
    print("\n🔍 Testing with ANY validation mode (any can pass):")
    validator.set_validation_mode("ANY")
    
    for test_data in test_cases:
        result = validator.validate(test_data)
        print(f"\n📝 Testing: '{test_data}'")
        print(f"   Result: {result['message']}")
    
    # ========================================================================
    # SORTING STRATEGIES DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🔢 SORTING STRATEGIES DEMO")
    print("="*50)
    
    # Test data
    test_data = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30]
    print(f"📊 Original data: {test_data}")
    
    # Create sorting strategies
    strategies = [
        BubbleSortStrategy(),
        QuickSortStrategy(),
        MergeSortStrategy()
    ]
    
    context = SortingContext(strategies[0])
    
    print("\n🏃‍♂️ Performance comparison:")
    for strategy in strategies:
        context.set_strategy(strategy)
        result = context.sort_with_timing(test_data)
        print(f"   {result['strategy']}: {result['execution_time']*1000:.2f}ms")
        print(f"   Result: {result['sorted_data']}")
    
    # ========================================================================
    # CREDIT CARD VALIDATION DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("💳 CREDIT CARD VALIDATION DEMO")
    print("="*50)
    
    cc_validator = Validator()
    cc_validator.add_strategy(CreditCardValidation())
    
    test_cards = [
        "4111111111111111",  # Valid Visa
        "5500000000000004",  # Valid Mastercard
        "1234567890123456",  # Invalid
        "4532 1234 5678 9012",  # Valid with spaces
        "4532-1234-5678-9012"   # Valid with dashes
    ]
    
    for card in test_cards:
        result = cc_validator.validate(card)
        status = "✅ Valid" if result['valid'] else "❌ Invalid"
        print(f"   Card {card[:8]}...: {status}")

if __name__ == "__main__":
    demo_strategy_interview()


