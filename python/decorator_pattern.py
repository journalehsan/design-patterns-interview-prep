'''
🚀 DECORATOR PATTERN - INTERVIEW FOCUSED 🚀

The Decorator Pattern allows behavior to be added to objects dynamically
without altering their structure. It provides a flexible alternative to
subclassing for extending functionality.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to add logging/caching to existing code without modifying it?"
2. "What's the difference between Decorator and Proxy?"
3. "How to manage decorator order?"
4. "How to implement middleware functionality?"

💡 KEY INTERVIEW POINTS:
- Dynamic behavior addition
- Decorator composition and ordering
- Middleware implementation
- Caching and logging decorators
- Performance monitoring
'''

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable
import time
import functools
import json
from datetime import datetime

# ============================================================================
# CORE SERVICE INTERFACE
# ============================================================================

class DataService(ABC):
    """Abstract data service interface"""
    @abstractmethod
    def get_data(self, query: str) -> str:
        pass
    
    @abstractmethod
    def save_data(self, data: str) -> bool:
        pass

class RealDataService(DataService):
    """Real data service that simulates database operations"""
    def __init__(self):
        self._data_store = {
            'users': ['John Doe', 'Jane Smith', 'Bob Wilson'],
            'products': ['Laptop', 'Mouse', 'Keyboard'],
            'orders': ['Order-001', 'Order-002', 'Order-003']
        }
        self._operation_count = 0
    
    def get_data(self, query: str) -> str:
        """Simulate database query with delay"""
        self._operation_count += 1
        time.sleep(0.1)  # Simulate database latency
        
        if query in self._data_store:
            return f"Found {len(self._data_store[query])} {query}: {self._data_store[query]}"
        else:
            return f"No data found for query: {query}"
    
    def save_data(self, data: str) -> bool:
        """Simulate data saving"""
        self._operation_count += 1
        time.sleep(0.05)  # Simulate save latency
        print(f"💾 Saved data: {data}")
        return True

# ============================================================================
# DECORATOR BASE CLASS
# ============================================================================

class DataServiceDecorator(DataService):
    """Base decorator class that maintains the same interface"""
    def __init__(self, data_service: DataService):
        self._data_service = data_service
    
    def get_data(self, query: str) -> str:
        return self._data_service.get_data(query)
    
    def save_data(self, data: str) -> bool:
        return self._data_service.save_data(data)

# ============================================================================
# CONCRETE DECORATORS
# ============================================================================

class LoggingDecorator(DataServiceDecorator):
    """Decorator that adds logging functionality"""
    def __init__(self, data_service: DataService, logger_name: str = "DataService"):
        super().__init__(data_service)
        self.logger_name = logger_name
        self.log_count = 0
    
    def get_data(self, query: str) -> str:
        start_time = time.time()
        self.log_count += 1
        
        print(f"📝 [{self.logger_name}] Log #{self.log_count}: GET request for '{query}'")
        
        try:
            result = super().get_data(query)
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            
            print(f"📝 [{self.logger_name}] Log #{self.log_count}: GET completed in {duration:.2f}ms")
            return result
        except Exception as e:
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            print(f"📝 [{self.logger_name}] Log #{self.log_count}: GET failed after {duration:.2f}ms - {e}")
            raise
    
    def save_data(self, data: str) -> bool:
        start_time = time.time()
        self.log_count += 1
        
        print(f"📝 [{self.logger_name}] Log #{self.log_count}: SAVE request for '{data[:50]}...'")
        
        try:
            result = super().save_data(data)
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            
            print(f"📝 [{self.logger_name}] Log #{self.log_count}: SAVE completed in {duration:.2f}ms")
            return result
        except Exception as e:
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            print(f"📝 [{self.logger_name}] Log #{self.log_count}: SAVE failed after {duration:.2f}ms - {e}")
            raise

class CachingDecorator(DataServiceDecorator):
    """Decorator that adds caching functionality"""
    def __init__(self, data_service: DataService, cache_size: int = 100):
        super().__init__(data_service)
        self._cache: Dict[str, str] = {}
        self._cache_size = cache_size
        self._cache_hits = 0
        self._cache_misses = 0
    
    def get_data(self, query: str) -> str:
        # Check cache first
        if query in self._cache:
            self._cache_hits += 1
            print(f"💾 [CACHE HIT] Query: '{query}' (Hit rate: {self._get_hit_rate():.1f}%)")
            return self._cache[query]
        
        # Cache miss - get from service
        self._cache_misses += 1
        print(f"💾 [CACHE MISS] Query: '{query}' (Hit rate: {self._get_hit_rate():.1f}%)")
        
        result = super().get_data(query)
        
        # Add to cache (with size limit)
        if len(self._cache) >= self._cache_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[query] = result
        return result
    
    def _get_hit_rate(self) -> float:
        total = self._cache_hits + self._cache_misses
        return (self._cache_hits / total * 100) if total > 0 else 0.0
    
    def clear_cache(self):
        """Clear the cache"""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
        print("💾 [CACHE] Cache cleared")

class ValidationDecorator(DataServiceDecorator):
    """Decorator that adds input validation"""
    def __init__(self, data_service: DataService):
        super().__init__(data_service)
        self.validation_errors = 0
    
    def get_data(self, query: str) -> str:
        if not self._validate_query(query):
            self.validation_errors += 1
            raise ValueError(f"Invalid query: '{query}'")
        
        return super().get_data(query)
    
    def save_data(self, data: str) -> bool:
        if not self._validate_data(data):
            self.validation_errors += 1
            raise ValueError(f"Invalid data: '{data[:50]}...'")
        
        return super().save_data(data)
    
    def _validate_query(self, query: str) -> bool:
        """Validate query parameters"""
        if not query or len(query.strip()) == 0:
            return False
        if len(query) > 100:
            return False
        if any(char in query for char in ['<', '>', '&', '"', "'"]):
            return False  # Basic XSS prevention
        return True
    
    def _validate_data(self, data: str) -> bool:
        """Validate data before saving"""
        if not data or len(data.strip()) == 0:
            return False
        if len(data) > 1000:
            return False
        return True

class RetryDecorator(DataServiceDecorator):
    """Decorator that adds retry functionality"""
    def __init__(self, data_service: DataService, max_retries: int = 3, delay: float = 0.1):
        super().__init__(data_service)
        self.max_retries = max_retries
        self.delay = delay
        self.retry_count = 0
    
    def get_data(self, query: str) -> str:
        for attempt in range(self.max_retries + 1):
            try:
                return super().get_data(query)
            except Exception as e:
                if attempt < self.max_retries:
                    self.retry_count += 1
                    print(f"🔄 [RETRY] Attempt {attempt + 1} failed: {e}. Retrying in {self.delay}s...")
                    time.sleep(self.delay)
                else:
                    print(f"🔄 [RETRY] All {self.max_retries + 1} attempts failed")
                    raise
    
    def save_data(self, data: str) -> bool:
        for attempt in range(self.max_retries + 1):
            try:
                return super().save_data(data)
            except Exception as e:
                if attempt < self.max_retries:
                    self.retry_count += 1
                    print(f"🔄 [RETRY] Attempt {attempt + 1} failed: {e}. Retrying in {self.delay}s...")
                    time.sleep(self.delay)
                else:
                    print(f"🔄 [RETRY] All {self.max_retries + 1} attempts failed")
                    raise

class MetricsDecorator(DataServiceDecorator):
    """Decorator that collects performance metrics"""
    def __init__(self, data_service: DataService):
        super().__init__(data_service)
        self.metrics = {
            'get_requests': 0,
            'save_requests': 0,
            'total_get_time': 0.0,
            'total_save_time': 0.0,
            'errors': 0
        }
    
    def get_data(self, query: str) -> str:
        start_time = time.time()
        self.metrics['get_requests'] += 1
        
        try:
            result = super().get_data(query)
            end_time = time.time()
            self.metrics['total_get_time'] += (end_time - start_time)
            return result
        except Exception as e:
            self.metrics['errors'] += 1
            raise
    
    def save_data(self, data: str) -> bool:
        start_time = time.time()
        self.metrics['save_requests'] += 1
        
        try:
            result = super().save_data(data)
            end_time = time.time()
            self.metrics['total_save_time'] += (end_time - start_time)
            return result
        except Exception as e:
            self.metrics['errors'] += 1
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        metrics = self.metrics.copy()
        
        if metrics['get_requests'] > 0:
            metrics['avg_get_time'] = metrics['total_get_time'] / metrics['get_requests']
        else:
            metrics['avg_get_time'] = 0.0
        
        if metrics['save_requests'] > 0:
            metrics['avg_save_time'] = metrics['total_save_time'] / metrics['save_requests']
        else:
            metrics['avg_save_time'] = 0.0
        
        return metrics
    
    def print_metrics(self):
        """Print performance metrics"""
        metrics = self.get_metrics()
        print("\n📊 PERFORMANCE METRICS:")
        print(f"   GET requests: {metrics['get_requests']}")
        print(f"   SAVE requests: {metrics['save_requests']}")
        print(f"   Average GET time: {metrics['avg_get_time']*1000:.2f}ms")
        print(f"   Average SAVE time: {metrics['avg_save_time']*1000:.2f}ms")
        print(f"   Total errors: {metrics['errors']}")

# ============================================================================
# FUNCTIONAL DECORATORS (Python decorator functions)
# ============================================================================

def timing_decorator(func: Callable) -> Callable:
    """Function decorator that measures execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️  Function '{func.__name__}' executed in {(end_time - start_time)*1000:.2f}ms")
        return result
    return wrapper

def retry_decorator(max_retries: int = 3, delay: float = 0.1):
    """Function decorator that adds retry functionality"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries:
                        print(f"🔄 Retry {attempt + 1}/{max_retries} for {func.__name__}: {e}")
                        time.sleep(delay)
                    else:
                        raise
            return None
        return wrapper
    return decorator

def cache_decorator(cache_size: int = 100):
    """Function decorator that adds caching"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            cache_key = str(args) + str(sorted(kwargs.items()))
            
            if cache_key in cache:
                print(f"💾 Cache hit for {func.__name__}")
                return cache[cache_key]
            
            print(f"💾 Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            
            # Add to cache with size limit
            if len(cache) >= cache_size:
                # Remove oldest entry
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            cache[cache_key] = result
            return result
        
        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

@timing_decorator
@retry_decorator(max_retries=2, delay=0.05)
@cache_decorator(cache_size=5)
def expensive_calculation(n: int) -> int:
    """Simulate an expensive calculation"""
    time.sleep(0.1)  # Simulate work
    return n * n * n

def demo_decorator_interview():
    """
    🎯 INTERVIEW DEMO: Decorator Pattern
    Demonstrates class-based and function-based decorators
    """
    print("\n" + "="*60)
    print("🚀 DECORATOR PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to add logging/caching without modifying existing code?")
    print("2. What's the difference between Decorator and Proxy?")
    print("3. How to manage decorator order?")
    print("4. How to implement middleware functionality?")
    
    # ========================================================================
    # CLASS-BASED DECORATORS DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🏗️ CLASS-BASED DECORATORS DEMO")
    print("="*50)
    
    # Create base service
    base_service = RealDataService()
    
    # Build decorated service with multiple decorators
    print("\n🔧 Building decorated service with multiple decorators:")
    service = base_service
    service = MetricsDecorator(service)
    service = LoggingDecorator(service, "MainService")
    service = CachingDecorator(service, cache_size=3)
    service = ValidationDecorator(service)
    service = RetryDecorator(service, max_retries=2, delay=0.05)
    
    print("✅ Service built with decorators: Metrics → Logging → Caching → Validation → Retry")
    
    # Test the decorated service
    print("\n🧪 Testing decorated service:")
    
    # Test successful operations
    print("\n📖 Testing GET operations:")
    service.get_data("users")
    service.get_data("products")
    service.get_data("users")  # Should hit cache
    
    print("\n💾 Testing SAVE operations:")
    service.save_data("New user: Alice Johnson")
    service.save_data("New product: Monitor")
    
    # Test validation
    print("\n🛡️ Testing validation:")
    try:
        service.get_data("")  # Should fail validation
    except ValueError as e:
        print(f"   Validation caught: {e}")
    
    try:
        service.get_data("invalid" * 20)  # Should fail validation
    except ValueError as e:
        print(f"   Validation caught: {e}")
    
    # Show metrics
    if isinstance(service, MetricsDecorator):
        service.print_metrics()
    
    # Show cache statistics
    if isinstance(service, CachingDecorator):
        print(f"\n💾 Cache statistics:")
        print(f"   Cache hits: {service._cache_hits}")
        print(f"   Cache misses: {service._cache_misses}")
        print(f"   Hit rate: {service._get_hit_rate():.1f}%")
    
    # ========================================================================
    # FUNCTION-BASED DECORATORS DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🔧 FUNCTION-BASED DECORATORS DEMO")
    print("="*50)
    
    print("\n🧮 Testing decorated function:")
    
    # Test the decorated function
    print("First call (cache miss):")
    result1 = expensive_calculation(5)
    print(f"Result: {result1}")
    
    print("\nSecond call (cache hit):")
    result2 = expensive_calculation(5)
    print(f"Result: {result2}")
    
    print("\nThird call with different input (cache miss):")
    result3 = expensive_calculation(3)
    print(f"Result: {result3}")
    
    # ========================================================================
    # DECORATOR ORDER DEMONSTRATION
    # ========================================================================
    print("\n" + "="*50)
    print("📋 DECORATOR ORDER DEMONSTRATION")
    print("="*50)
    
    print("\n💡 Decorator order matters! The order of execution is:")
    print("   1. Retry (outermost) - handles failures")
    print("   2. Validation - validates input")
    print("   3. Caching - checks cache first")
    print("   4. Logging - logs operations")
    print("   5. Metrics - collects performance data")
    print("   6. Base Service (innermost) - actual work")
    
    print("\n🔄 If we change the order, behavior changes:")
    
    # Different order: Validation first, then caching
    service2 = RealDataService()
    service2 = ValidationDecorator(service2)
    service2 = CachingDecorator(service2, cache_size=2)
    service2 = LoggingDecorator(service2, "OrderedService")
    
    print("\nTesting with different decorator order:")
    service2.get_data("users")
    service2.get_data("users")  # Should hit cache (validation already passed)

if __name__ == "__main__":
    demo_decorator_interview()
