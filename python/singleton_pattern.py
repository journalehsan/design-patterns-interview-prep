'''
🚀 SINGLETON PATTERN - INTERVIEW FOCUSED 🚀

The Singleton Pattern ensures a class has only one instance and provides
global access to that instance. It's one of the most controversial patterns
due to its potential for misuse.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to ensure only one instance of a class exists?"
2. "What are the problems with Singleton pattern?"
3. "How to implement thread-safe Singleton?"
4. "When should you use Singleton vs Dependency Injection?"

💡 KEY INTERVIEW POINTS:
- Thread safety considerations
- Lazy vs eager initialization
- Singleton anti-patterns
- Alternative approaches (Dependency Injection)
'''

import threading
from typing import Optional, Dict, Any
from datetime import datetime
import time

# ============================================================================
# BASIC SINGLETON IMPLEMENTATIONS
# ============================================================================

class BasicSingleton:
    """Basic Singleton implementation (NOT thread-safe)"""
    
    _instance: Optional['BasicSingleton'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.value = 0
            self.created_at = datetime.now()
            self._initialized = True
            print("🏗️ BasicSingleton instance created")
    
    def increment(self):
        """Increment value"""
        self.value += 1
        return self.value
    
    def get_info(self) -> Dict[str, Any]:
        """Get singleton info"""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "instance_id": id(self)
        }

class ThreadSafeSingleton:
    """Thread-safe Singleton using double-checked locking"""
    
    _instance: Optional['ThreadSafeSingleton'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.value = 0
            self.created_at = datetime.now()
            self._initialized = True
            print("🔒 ThreadSafeSingleton instance created")
    
    def increment(self):
        """Thread-safe increment"""
        with self._lock:
            self.value += 1
            return self.value
    
    def get_info(self) -> Dict[str, Any]:
        """Get singleton info"""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "instance_id": id(self)
        }

class EagerSingleton:
    """Eager initialization Singleton (thread-safe)"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = 0
            cls._instance.created_at = datetime.now()
            print("⚡ EagerSingleton instance created")
        return cls._instance
    
    def increment(self):
        """Increment value"""
        self.value += 1
        return self.value
    
    def get_info(self) -> Dict[str, Any]:
        """Get singleton info"""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "instance_id": id(self)
        }

# ============================================================================
# REAL-WORLD SINGLETON EXAMPLES
# ============================================================================

class DatabaseConnection:
    """Database connection singleton"""
    
    _instance: Optional['DatabaseConnection'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "postgresql://localhost:5432/mydb"
            self.is_connected = False
            self.connection_count = 0
            self.created_at = datetime.now()
            self._initialized = True
            print("🗄️ DatabaseConnection singleton created")
    
    def connect(self) -> bool:
        """Connect to database"""
        if not self.is_connected:
            print(f"🔌 Connecting to database: {self.connection_string}")
            time.sleep(0.1)  # Simulate connection time
            self.is_connected = True
            self.connection_count += 1
            return True
        return True
    
    def disconnect(self):
        """Disconnect from database"""
        if self.is_connected:
            print("🔌 Disconnecting from database")
            self.is_connected = False
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute database query"""
        if not self.is_connected:
            raise RuntimeError("Database not connected")
        
        print(f"📊 Executing query: {query}")
        time.sleep(0.05)  # Simulate query execution
        return {
            "query": query,
            "rows_affected": 1,
            "execution_time": 0.05,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information"""
        return {
            "connection_string": self.connection_string,
            "is_connected": self.is_connected,
            "connection_count": self.connection_count,
            "created_at": self.created_at.isoformat(),
            "instance_id": id(self)
        }

class Logger:
    """Logger singleton"""
    
    _instance: Optional['Logger'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.log_level = "INFO"
            self.log_file = "application.log"
            self.logs: list = []
            self.created_at = datetime.now()
            self._initialized = True
            print("📝 Logger singleton created")
    
    def set_log_level(self, level: str):
        """Set log level"""
        self.log_level = level
        print(f"📝 Log level set to: {level}")
    
    def log(self, level: str, message: str):
        """Log a message"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}"
        
        self.logs.append(log_entry)
        print(f"📝 {log_entry}")
        
        # In real implementation, would write to file
        # with open(self.log_file, 'a') as f:
        #     f.write(log_entry + '\n')
    
    def info(self, message: str):
        """Log info message"""
        self.log("INFO", message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.log("WARNING", message)
    
    def error(self, message: str):
        """Log error message"""
        self.log("ERROR", message)
    
    def get_log_count(self) -> int:
        """Get total log count"""
        return len(self.logs)
    
    def get_logs(self) -> list:
        """Get all logs"""
        return self.logs.copy()

class ConfigurationManager:
    """Configuration manager singleton"""
    
    _instance: Optional['ConfigurationManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.config: Dict[str, Any] = {
                "app_name": "Design Patterns Demo",
                "version": "1.0.0",
                "debug": False,
                "database_url": "postgresql://localhost:5432/mydb",
                "max_connections": 100,
                "timeout": 30
            }
            self.created_at = datetime.now()
            self._initialized = True
            print("⚙️ ConfigurationManager singleton created")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        print(f"⚙️ Configuration updated: {key} = {value}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self.config.copy()
    
    def reload(self):
        """Reload configuration (simulate)"""
        print("⚙️ Reloading configuration...")
        time.sleep(0.1)  # Simulate reload time
        print("⚙️ Configuration reloaded")

# ============================================================================
# SINGLETON WITH METACLASS
# ============================================================================

class SingletonMeta(type):
    """Metaclass for Singleton pattern"""
    
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MetaclassSingleton(metaclass=SingletonMeta):
    """Singleton using metaclass"""
    
    def __init__(self):
        self.value = 0
        self.created_at = datetime.now()
        print("🎭 MetaclassSingleton instance created")
    
    def increment(self):
        """Increment value"""
        self.value += 1
        return self.value
    
    def get_info(self) -> Dict[str, Any]:
        """Get singleton info"""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "instance_id": id(self)
        }

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_singleton_interview():
    """
    🎯 INTERVIEW DEMO: Singleton Pattern
    Demonstrates various Singleton implementations and their trade-offs
    """
    print("\n" + "="*60)
    print("🚀 SINGLETON PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to ensure only one instance of a class exists?")
    print("2. What are the problems with Singleton pattern?")
    print("3. How to implement thread-safe Singleton?")
    print("4. When should you use Singleton vs Dependency Injection?")
    
    # ========================================================================
    # BASIC SINGLETON DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🏗️ BASIC SINGLETON DEMO")
    print("="*50)
    
    print("\n🔍 Testing basic singleton:")
    
    # Create multiple instances
    singleton1 = BasicSingleton()
    singleton2 = BasicSingleton()
    singleton3 = BasicSingleton()
    
    # Test if they're the same instance
    print(f"   singleton1 id: {id(singleton1)}")
    print(f"   singleton2 id: {id(singleton2)}")
    print(f"   singleton3 id: {id(singleton3)}")
    print(f"   Are they the same? {singleton1 is singleton2 is singleton3}")
    
    # Test shared state
    singleton1.increment()
    singleton2.increment()
    singleton3.increment()
    
    print(f"   Value after increments: {singleton1.value}")
    print(f"   Info: {singleton1.get_info()}")
    
    # ========================================================================
    # THREAD-SAFE SINGLETON DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🔒 THREAD-SAFE SINGLETON DEMO")
    print("="*50)
    
    print("\n🧵 Testing thread-safe singleton:")
    
    def worker_thread(thread_id: int):
        """Worker thread function"""
        singleton = ThreadSafeSingleton()
        for _ in range(5):
            value = singleton.increment()
            print(f"   Thread {thread_id}: value = {value}")
            time.sleep(0.01)
    
    # Create and start threads
    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker_thread, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for threads to complete
    for thread in threads:
        thread.join()
    
    # Check final state
    final_singleton = ThreadSafeSingleton()
    print(f"   Final value: {final_singleton.value}")
    print(f"   Final info: {final_singleton.get_info()}")
    
    # ========================================================================
    # REAL-WORLD SINGLETON EXAMPLES
    # ========================================================================
    print("\n" + "="*50)
    print("🌍 REAL-WORLD SINGLETON EXAMPLES")
    print("="*50)
    
    # Database Connection Demo
    print("\n🗄️ Database Connection Singleton:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"   Same instance? {db1 is db2}")
    print(f"   Connection info: {db1.get_connection_info()}")
    
    db1.connect()
    result = db1.execute_query("SELECT * FROM users")
    print(f"   Query result: {result}")
    
    # Logger Demo
    print("\n📝 Logger Singleton:")
    logger1 = Logger()
    logger2 = Logger()
    
    print(f"   Same instance? {logger1 is logger2}")
    
    logger1.info("Application started")
    logger2.warning("Low memory warning")
    logger1.error("Database connection failed")
    
    print(f"   Total logs: {logger1.get_log_count()}")
    
    # Configuration Manager Demo
    print("\n⚙️ Configuration Manager Singleton:")
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    
    print(f"   Same instance? {config1 is config2}")
    print(f"   App name: {config1.get('app_name')}")
    print(f"   Debug mode: {config1.get('debug')}")
    
    config1.set('debug', True)
    print(f"   Debug mode after change: {config2.get('debug')}")
    
    # ========================================================================
    # METACLASS SINGLETON DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🎭 METACLASS SINGLETON DEMO")
    print("="*50)
    
    print("\n🔍 Testing metaclass singleton:")
    
    meta1 = MetaclassSingleton()
    meta2 = MetaclassSingleton()
    
    print(f"   Same instance? {meta1 is meta2}")
    print(f"   Info: {meta1.get_info()}")
    
    # ========================================================================
    # SINGLETON PROBLEMS AND ALTERNATIVES
    # ========================================================================
    print("\n" + "="*50)
    print("⚠️ SINGLETON PROBLEMS AND ALTERNATIVES")
    print("="*50)
    
    print("\n❌ Common Problems with Singleton:")
    print("   1. 🧪 Testing - Hard to mock and test")
    print("   2. 🔗 Coupling - Creates tight coupling")
    print("   3. 🧵 Threading - Can cause threading issues")
    print("   4. 🔄 State - Global state can be problematic")
    print("   5. 🏗️ Inheritance - Difficult to extend")
    print("   6. 🔧 Configuration - Hard to configure")
    
    print("\n✅ Better Alternatives:")
    print("   1. 💉 Dependency Injection - Pass dependencies explicitly")
    print("   2. 🏭 Factory Pattern - Use factories for object creation")
    print("   3. 📦 Service Locator - Locate services when needed")
    print("   4. 🎯 Context Objects - Pass context through call chain")
    print("   5. 🔧 Configuration Objects - Use configuration classes")
    
    print("\n🎯 When Singleton Might Be Acceptable:")
    print("   1. 🗄️ Database connections (with connection pooling)")
    print("   2. 📝 Logging systems")
    print("   3. ⚙️ Configuration managers")
    print("   4. 🎨 UI managers (in desktop apps)")
    print("   5. 🔧 Hardware interfaces")
    
    # ========================================================================
    # THREADING ISSUES DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🧵 THREADING ISSUES DEMO")
    print("="*50)
    
    print("\n⚠️ Demonstrating threading issues with basic singleton:")
    
    def unsafe_worker(thread_id: int):
        """Unsafe worker thread"""
        singleton = BasicSingleton()
        for _ in range(3):
            value = singleton.increment()
            print(f"   Unsafe Thread {thread_id}: value = {value}")
            time.sleep(0.01)
    
    # Create threads for unsafe singleton
    unsafe_threads = []
    for i in range(2):
        thread = threading.Thread(target=unsafe_worker, args=(i,))
        unsafe_threads.append(thread)
        thread.start()
    
    # Wait for threads
    for thread in unsafe_threads:
        thread.join()
    
    print(f"   Final unsafe value: {BasicSingleton().value}")
    
    # ========================================================================
    # SINGLETON BEST PRACTICES
    # ========================================================================
    print("\n" + "="*50)
    print("💡 SINGLETON BEST PRACTICES")
    print("="*50)
    
    print("\n🎯 If You Must Use Singleton:")
    print("   1. 🔒 Make it thread-safe")
    print("   2. 🧪 Design for testability")
    print("   3. 📝 Document the global state")
    print("   4. 🔧 Make it configurable")
    print("   5. 🚫 Avoid mutable global state")
    print("   6. 🎯 Use lazy initialization")
    print("   7. 🔄 Consider lifecycle management")
    
    print("\n🏗️ Implementation Guidelines:")
    print("   1. Use double-checked locking for thread safety")
    print("   2. Consider using metaclass for cleaner code")
    print("   3. Implement proper initialization logic")
    print("   4. Handle inheritance carefully")
    print("   5. Consider using dependency injection instead")

if __name__ == "__main__":
    demo_singleton_interview()
