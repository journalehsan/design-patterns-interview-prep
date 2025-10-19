'''
🚀 OBSERVER PATTERN - INTERVIEW FOCUSED 🚀

The Observer Pattern is a behavioral design pattern that defines a one-to-many dependency between objects,
so that when one object changes state, all its dependents are notified and updated automatically.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How would you design a notification system?"
2. "What if an observer takes too long to process?"
3. "How to prevent memory leaks with observers?"
4. "How to handle failing observers gracefully?"

💡 KEY INTERVIEW POINTS:
- Error handling in observer notifications
- State management with property setters
- Preventing duplicate observers
- Context passing with notifications
- Memory leak prevention
'''

from abc import ABC, abstractmethod
from typing import List, Any, Dict
import time

class Observer(ABC):
    """Abstract Observer interface"""
    @abstractmethod
    def update(self, observable, *args, **kwargs):
        pass

class Observable:
    """
    Enhanced Observable with interview-focused features:
    - Error handling for failing observers
    - State management with property setters
    - Duplicate prevention
    - Context passing
    """
    def __init__(self):
        self._observers: List[Observer] = []
        self._state = None
        self._name = self.__class__.__name__

    def add_observer(self, observer: Observer) -> bool:
        """
        Add observer with duplicate prevention
        Returns True if added, False if already exists
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[{self._name}] Observer {observer.__class__.__name__} added")
            return True
        print(f"[{self._name}] Observer {observer.__class__.__name__} already exists")
        return False

    def remove_observer(self, observer: Observer) -> bool:
        """
        Remove observer safely
        Returns True if removed, False if not found
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[{self._name}] Observer {observer.__class__.__name__} removed")
            return True
        print(f"[{self._name}] Observer {observer.__class__.__name__} not found")
        return False

    def notify_observers(self, *args, **kwargs):
        """
        Notify all observers with error handling
        Uses copy of observers list to allow removal during iteration
        """
        if not self._observers:
            print(f"[{self._name}] No observers to notify")
            return

        print(f"[{self._name}] Notifying {len(self._observers)} observers...")
        
        # Create copy to allow removal during iteration
        observers_copy = self._observers[:]
        
        for observer in observers_copy:
            try:
                observer.update(self, *args, **kwargs)
            except Exception as e:
                print(f"[{self._name}] ❌ Observer {observer.__class__.__name__} failed: {e}")
                # Remove failing observer to prevent future failures
                if observer in self._observers:
                    self._observers.remove(observer)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        """State setter that automatically notifies observers of changes"""
        old_value = self._state
        self._state = value
        
        if old_value != value:
            print(f"[{self._name}] State changed: {old_value} → {value}")
            self.notify_observers(
                old_value=old_value, 
                new_value=value,
                timestamp=time.time()
            )

    def get_observer_count(self) -> int:
        return len(self._observers)

# Concrete Observers with different behaviors
class LoggerObserver(Observer):
    """Observer that logs all state changes"""
    def __init__(self, name: str = "Logger"):
        self.name = name
        self.log_count = 0

    def update(self, observable, *args, **kwargs):
        self.log_count += 1
        old_val = kwargs.get('old_value', 'None')
        new_val = kwargs.get('new_value', 'None')
        timestamp = kwargs.get('timestamp', time.time())
        
        print(f"📝 [{self.name}] Log #{self.log_count}: {observable._name} changed from '{old_val}' to '{new_val}' at {timestamp}")

class CacheObserver(Observer):
    """Observer that maintains a cache of state changes"""
    def __init__(self, name: str = "Cache"):
        self.name = name
        self.cache: Dict[str, Any] = {}
        self.history: List[Dict] = []

    def update(self, observable, *args, **kwargs):
        old_val = kwargs.get('old_value')
        new_val = kwargs.get('new_value')
        
        # Update cache
        self.cache['last_updated'] = new_val
        self.cache['update_count'] = self.cache.get('update_count', 0) + 1
        
        # Maintain history
        self.history.append({
            'observable': observable._name,
            'old_value': old_val,
            'new_value': new_val,
            'timestamp': kwargs.get('timestamp', time.time())
        })
        
        print(f"💾 [{self.name}] Cache updated: {self.cache}")
        print(f"📚 [{self.name}] History entries: {len(self.history)}")

class FailingObserver(Observer):
    """Observer that always fails - for testing error handling"""
    def __init__(self, name: str = "Failing"):
        self.name = name
        self.failure_count = 0

    def update(self, observable, *args, **kwargs):
        self.failure_count += 1
        raise Exception(f"💥 [{self.name}] Intentional failure #{self.failure_count}")

class SlowObserver(Observer):
    """Observer that takes time to process - for testing performance"""
    def __init__(self, name: str = "Slow", delay: float = 0.5):
        self.name = name
        self.delay = delay
        self.process_count = 0

    def update(self, observable, *args, **kwargs):
        self.process_count += 1
        print(f"⏳ [{self.name}] Processing update #{self.process_count} (will take {self.delay}s)...")
        time.sleep(self.delay)
        print(f"✅ [{self.name}] Finished processing update #{self.process_count}")

def demo_observer_interview():
    """
    🎯 INTERVIEW DEMO: Observer Pattern
    Demonstrates common interview scenarios and edge cases
    """
    print("\n" + "="*60)
    print("🚀 OBSERVER PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to prevent duplicate observers?")
    print("2. How to handle failing observers?")
    print("3. How to pass context with notifications?")
    print("4. How to prevent memory leaks?")
    
    # Create observable system
    system = Observable()
    
    # Create different types of observers
    logger = LoggerObserver("SystemLogger")
    cache = CacheObserver("SystemCache")
    slow_processor = SlowObserver("SlowProcessor", 0.2)
    
    print(f"\n📊 Initial state: {system.get_observer_count()} observers")
    
    # Test duplicate prevention
    print("\n🔍 Testing duplicate prevention:")
    system.add_observer(logger)
    system.add_observer(logger)  # Should be prevented
    system.add_observer(cache)
    system.add_observer(slow_processor)
    
    print(f"📊 After adding observers: {system.get_observer_count()} observers")
    
    # Test state changes with automatic notifications
    print("\n🔄 Testing state changes:")
    system.state = "INITIALIZED"
    system.state = "RUNNING"
    system.state = "PROCESSING"
    
    # Test with failing observer
    print("\n💥 Testing error handling:")
    failing_observer = FailingObserver("TestFailing")
    system.add_observer(failing_observer)
    system.state = "FAILING_STATE"  # This should handle the failure gracefully
    
    print(f"📊 After failure: {system.get_observer_count()} observers (failing one should be removed)")
    
    # Test observer removal
    print("\n🗑️ Testing observer removal:")
    system.remove_observer(slow_processor)
    system.state = "FINAL_STATE"
    
    print(f"📊 Final state: {system.get_observer_count()} observers")
    
    # Show cache and history
    print(f"\n📚 Cache observer history: {len(cache.history)} entries")
    print(f"📝 Logger observer logs: {logger.log_count} entries")

if __name__ == "__main__":
    demo_observer_interview()

