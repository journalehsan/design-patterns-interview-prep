'''
🚀 BUILDER PATTERN - INTERVIEW FOCUSED 🚀

The Builder Pattern separates the construction of a complex object from its
representation, allowing the same construction process to create different
representations.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to create complex objects with many optional parameters?"
2. "How to build objects step by step with validation?"
3. "How to create different representations of the same object?"
4. "How to make object construction more readable and maintainable?"

💡 KEY INTERVIEW POINTS:
- Step-by-step object construction
- Fluent interface design
- Parameter validation
- Different object representations
'''

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# ============================================================================
# COMPUTER BUILDER EXAMPLE
# ============================================================================

class Computer:
    """Product class - Complex computer object"""
    
    def __init__(self):
        self.cpu = ""
        self.memory = 0
        self.storage = 0
        self.graphics_card = ""
        self.motherboard = ""
        self.power_supply = ""
        self.case = ""
        self.cooling_system = ""
        self.operating_system = ""
        self.accessories: List[str] = []
        self.price = 0.0
        self.warranty_years = 1
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get computer specifications"""
        return {
            "cpu": self.cpu,
            "memory_gb": self.memory,
            "storage_gb": self.storage,
            "graphics_card": self.graphics_card,
            "motherboard": self.motherboard,
            "power_supply": self.power_supply,
            "case": self.case,
            "cooling_system": self.cooling_system,
            "operating_system": self.operating_system,
            "accessories": self.accessories,
            "price": self.price,
            "warranty_years": self.warranty_years
        }
    
    def display_specs(self) -> str:
        """Display computer specifications"""
        specs = self.get_specifications()
        result = "🖥️ Computer Specifications:\n"
        result += f"   CPU: {specs['cpu']}\n"
        result += f"   Memory: {specs['memory_gb']} GB\n"
        result += f"   Storage: {specs['storage_gb']} GB\n"
        result += f"   Graphics: {specs['graphics_card']}\n"
        result += f"   Motherboard: {specs['motherboard']}\n"
        result += f"   Power Supply: {specs['power_supply']}\n"
        result += f"   Case: {specs['case']}\n"
        result += f"   Cooling: {specs['cooling_system']}\n"
        result += f"   OS: {specs['operating_system']}\n"
        result += f"   Accessories: {', '.join(specs['accessories']) if specs['accessories'] else 'None'}\n"
        result += f"   Price: ${specs['price']:,.2f}\n"
        result += f"   Warranty: {specs['warranty_years']} years"
        return result

class ComputerBuilder(ABC):
    """Abstract builder interface"""
    
    def __init__(self):
        self.computer = Computer()
        self.reset()
    
    def reset(self):
        """Reset builder to initial state"""
        self.computer = Computer()
        return self
    
    @abstractmethod
    def set_cpu(self, cpu: str):
        """Set CPU"""
        pass
    
    @abstractmethod
    def set_memory(self, memory_gb: int):
        """Set memory"""
        pass
    
    @abstractmethod
    def set_storage(self, storage_gb: int):
        """Set storage"""
        pass
    
    @abstractmethod
    def set_graphics_card(self, graphics_card: str):
        """Set graphics card"""
        pass
    
    def set_motherboard(self, motherboard: str):
        """Set motherboard (optional)"""
        self.computer.motherboard = motherboard
        return self
    
    def set_power_supply(self, power_supply: str):
        """Set power supply (optional)"""
        self.computer.power_supply = power_supply
        return self
    
    def set_case(self, case: str):
        """Set case (optional)"""
        self.computer.case = case
        return self
    
    def set_cooling_system(self, cooling: str):
        """Set cooling system (optional)"""
        self.computer.cooling_system = cooling
        return self
    
    def set_operating_system(self, os: str):
        """Set operating system (optional)"""
        self.computer.operating_system = os
        return self
    
    def add_accessory(self, accessory: str):
        """Add accessory"""
        self.computer.accessories.append(accessory)
        return self
    
    def set_warranty(self, years: int):
        """Set warranty period"""
        self.computer.warranty_years = years
        return self
    
    def calculate_price(self):
        """Calculate total price based on components"""
        # Base price calculation logic
        base_price = 500  # Base system price
        
        # CPU pricing
        cpu_prices = {
            "Intel i3": 150, "Intel i5": 250, "Intel i7": 400, "Intel i9": 600,
            "AMD Ryzen 3": 120, "AMD Ryzen 5": 200, "AMD Ryzen 7": 350, "AMD Ryzen 9": 500
        }
        base_price += cpu_prices.get(self.computer.cpu, 200)
        
        # Memory pricing
        base_price += self.computer.memory * 10  # $10 per GB
        
        # Storage pricing
        base_price += self.computer.storage * 0.1  # $0.10 per GB
        
        # Graphics card pricing
        gpu_prices = {
            "Integrated": 0, "GTX 1660": 200, "RTX 3060": 400, "RTX 3070": 600,
            "RTX 3080": 800, "RTX 4090": 1200
        }
        base_price += gpu_prices.get(self.computer.graphics_card, 300)
        
        # Accessories pricing
        accessory_prices = {
            "Keyboard": 50, "Mouse": 30, "Monitor": 200, "Webcam": 80,
            "Speakers": 60, "Headset": 100
        }
        for accessory in self.computer.accessories:
            base_price += accessory_prices.get(accessory, 25)
        
        self.computer.price = base_price
        return self
    
    def build(self) -> Computer:
        """Build and return the computer"""
        if not self._validate_build():
            raise ValueError("Invalid computer configuration")
        
        self.calculate_price()
        return self.computer
    
    def _validate_build(self) -> bool:
        """Validate the computer configuration"""
        if not self.computer.cpu:
            print("❌ CPU is required")
            return False
        
        if self.computer.memory <= 0:
            print("❌ Memory must be greater than 0")
            return False
        
        if self.computer.storage <= 0:
            print("❌ Storage must be greater than 0")
            return False
        
        if not self.computer.graphics_card:
            print("❌ Graphics card is required")
            return False
        
        return True

class GamingComputerBuilder(ComputerBuilder):
    """Concrete builder for gaming computers"""
    
    def set_cpu(self, cpu: str):
        """Set CPU for gaming (high-performance)"""
        gaming_cpus = ["Intel i7", "Intel i9", "AMD Ryzen 7", "AMD Ryzen 9"]
        if cpu not in gaming_cpus:
            print(f"⚠️ Warning: {cpu} may not be optimal for gaming")
        self.computer.cpu = cpu
        return self
    
    def set_memory(self, memory_gb: int):
        """Set memory for gaming (minimum 16GB)"""
        if memory_gb < 16:
            print(f"⚠️ Warning: {memory_gb}GB may not be sufficient for gaming")
        self.computer.memory = memory_gb
        return self
    
    def set_storage(self, storage_gb: int):
        """Set storage for gaming (minimum 500GB)"""
        if storage_gb < 500:
            print(f"⚠️ Warning: {storage_gb}GB may not be sufficient for games")
        self.computer.storage = storage_gb
        return self
    
    def set_graphics_card(self, graphics_card: str):
        """Set graphics card for gaming (dedicated GPU required)"""
        if graphics_card == "Integrated":
            print("❌ Gaming computers require dedicated graphics cards")
            return self
        
        gaming_gpus = ["GTX 1660", "RTX 3060", "RTX 3070", "RTX 3080", "RTX 4090"]
        if graphics_card not in gaming_gpus:
            print(f"⚠️ Warning: {graphics_card} may not be optimal for gaming")
        
        self.computer.graphics_card = graphics_card
        return self

class OfficeComputerBuilder(ComputerBuilder):
    """Concrete builder for office computers"""
    
    def set_cpu(self, cpu: str):
        """Set CPU for office work (efficient)"""
        office_cpus = ["Intel i3", "Intel i5", "AMD Ryzen 3", "AMD Ryzen 5"]
        if cpu not in office_cpus:
            print(f"⚠️ Warning: {cpu} may be overkill for office work")
        self.computer.cpu = cpu
        return self
    
    def set_memory(self, memory_gb: int):
        """Set memory for office work (8GB minimum)"""
        if memory_gb < 8:
            print(f"⚠️ Warning: {memory_gb}GB may not be sufficient for office work")
        self.computer.memory = memory_gb
        return self
    
    def set_storage(self, storage_gb: int):
        """Set storage for office work (250GB minimum)"""
        if storage_gb < 250:
            print(f"⚠️ Warning: {storage_gb}GB may not be sufficient for office work")
        self.computer.storage = storage_gb
        return self
    
    def set_graphics_card(self, graphics_card: str):
        """Set graphics card for office work (integrated OK)"""
        self.computer.graphics_card = graphics_card
        return self

class ComputerDirector:
    """Director class that orchestrates the building process"""
    
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_budget_gaming_pc(self) -> Computer:
        """Build a budget gaming PC"""
        return (self.builder.reset()
                .set_cpu("AMD Ryzen 5")
                .set_memory(16)
                .set_storage(500)
                .set_graphics_card("RTX 3060")
                .set_motherboard("B450 Gaming")
                .set_power_supply("600W 80+ Bronze")
                .set_case("Mid Tower ATX")
                .set_cooling_system("Air Cooling")
                .set_operating_system("Windows 11")
                .add_accessory("Keyboard")
                .add_accessory("Mouse")
                .set_warranty(2)
                .build())
    
    def build_high_end_gaming_pc(self) -> Computer:
        """Build a high-end gaming PC"""
        return (self.builder.reset()
                .set_cpu("Intel i9")
                .set_memory(32)
                .set_storage(1000)
                .set_graphics_card("RTX 4090")
                .set_motherboard("Z790 Gaming")
                .set_power_supply("850W 80+ Gold")
                .set_case("Full Tower ATX")
                .set_cooling_system("Liquid Cooling")
                .set_operating_system("Windows 11 Pro")
                .add_accessory("Mechanical Keyboard")
                .add_accessory("Gaming Mouse")
                .add_accessory("Gaming Monitor")
                .add_accessory("Gaming Headset")
                .set_warranty(3)
                .build())
    
    def build_office_workstation(self) -> Computer:
        """Build an office workstation"""
        return (self.builder.reset()
                .set_cpu("Intel i5")
                .set_memory(16)
                .set_storage(500)
                .set_graphics_card("Integrated")
                .set_motherboard("H470 Business")
                .set_power_supply("400W 80+ Bronze")
                .set_case("Mini Tower")
                .set_cooling_system("Stock Cooling")
                .set_operating_system("Windows 11 Pro")
                .add_accessory("Keyboard")
                .add_accessory("Mouse")
                .add_accessory("Monitor")
                .set_warranty(3)
                .build())

# ============================================================================
# SQL QUERY BUILDER EXAMPLE
# ============================================================================

class SQLQuery:
    """Product class - SQL Query object"""
    
    def __init__(self):
        self.query_type = ""
        self.table = ""
        self.columns: List[str] = []
        self.where_conditions: List[str] = []
        self.join_clauses: List[str] = []
        self.group_by: List[str] = []
        self.having_conditions: List[str] = []
        self.order_by: List[str] = []
        self.limit_value: Optional[int] = None
        self.offset_value: Optional[int] = None
    
    def to_string(self) -> str:
        """Convert query to SQL string"""
        query_parts = []
        
        # SELECT clause
        if self.query_type.upper() == "SELECT":
            columns = ", ".join(self.columns) if self.columns else "*"
            query_parts.append(f"SELECT {columns}")
        
        # FROM clause
        if self.table:
            query_parts.append(f"FROM {self.table}")
        
        # JOIN clauses
        for join in self.join_clauses:
            query_parts.append(join)
        
        # WHERE clause
        if self.where_conditions:
            where_clause = " AND ".join(self.where_conditions)
            query_parts.append(f"WHERE {where_clause}")
        
        # GROUP BY clause
        if self.group_by:
            group_clause = ", ".join(self.group_by)
            query_parts.append(f"GROUP BY {group_clause}")
        
        # HAVING clause
        if self.having_conditions:
            having_clause = " AND ".join(self.having_conditions)
            query_parts.append(f"HAVING {having_clause}")
        
        # ORDER BY clause
        if self.order_by:
            order_clause = ", ".join(self.order_by)
            query_parts.append(f"ORDER BY {order_clause}")
        
        # LIMIT clause
        if self.limit_value is not None:
            query_parts.append(f"LIMIT {self.limit_value}")
        
        # OFFSET clause
        if self.offset_value is not None:
            query_parts.append(f"OFFSET {self.offset_value}")
        
        return " ".join(query_parts)

class SQLQueryBuilder:
    """Builder for SQL queries"""
    
    def __init__(self):
        self.query = SQLQuery()
        self.reset()
    
    def reset(self):
        """Reset builder"""
        self.query = SQLQuery()
        return self
    
    def select(self, *columns: str):
        """Add SELECT clause"""
        self.query.query_type = "SELECT"
        self.query.columns.extend(columns)
        return self
    
    def from_table(self, table: str):
        """Add FROM clause"""
        self.query.table = table
        return self
    
    def where(self, condition: str):
        """Add WHERE condition"""
        self.query.where_conditions.append(condition)
        return self
    
    def join(self, table: str, condition: str, join_type: str = "INNER"):
        """Add JOIN clause"""
        join_clause = f"{join_type} JOIN {table} ON {condition}"
        self.query.join_clauses.append(join_clause)
        return self
    
    def group_by(self, *columns: str):
        """Add GROUP BY clause"""
        self.query.group_by.extend(columns)
        return self
    
    def having(self, condition: str):
        """Add HAVING condition"""
        self.query.having_conditions.append(condition)
        return self
    
    def order_by(self, *columns: str):
        """Add ORDER BY clause"""
        self.query.order_by.extend(columns)
        return self
    
    def limit(self, count: int):
        """Add LIMIT clause"""
        self.query.limit_value = count
        return self
    
    def offset(self, count: int):
        """Add OFFSET clause"""
        self.query.offset_value = count
        return self
    
    def build(self) -> SQLQuery:
        """Build and return the query"""
        if not self._validate_query():
            raise ValueError("Invalid SQL query")
        return self.query
    
    def _validate_query(self) -> bool:
        """Validate the query"""
        if not self.query.query_type:
            print("❌ Query type is required")
            return False
        
        if not self.query.table:
            print("❌ Table is required")
            return False
        
        return True

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_builder_interview():
    """
    🎯 INTERVIEW DEMO: Builder Pattern
    Demonstrates step-by-step object construction
    """
    print("\n" + "="*60)
    print("🚀 BUILDER PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to create complex objects with many optional parameters?")
    print("2. How to build objects step by step with validation?")
    print("3. How to create different representations of the same object?")
    print("4. How to make object construction more readable and maintainable?")
    
    # ========================================================================
    # COMPUTER BUILDER DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🖥️ COMPUTER BUILDER DEMO")
    print("="*50)
    
    # Create builders
    gaming_builder = GamingComputerBuilder()
    office_builder = OfficeComputerBuilder()
    
    # Create director
    director = ComputerDirector(gaming_builder)
    
    # Build different computer configurations
    print("\n🎮 Building budget gaming PC:")
    budget_gaming_pc = director.build_budget_gaming_pc()
    print(budget_gaming_pc.display_specs())
    
    print("\n🎮 Building high-end gaming PC:")
    high_end_gaming_pc = director.build_high_end_gaming_pc()
    print(high_end_gaming_pc.display_specs())
    
    # Build office workstation
    print("\n💼 Building office workstation:")
    director.builder = office_builder
    office_workstation = director.build_office_workstation()
    print(office_workstation.display_specs())
    
    # Custom build example
    print("\n🔧 Custom build example:")
    custom_pc = (gaming_builder.reset()
                .set_cpu("AMD Ryzen 7")
                .set_memory(32)
                .set_storage(1000)
                .set_graphics_card("RTX 3070")
                .set_motherboard("X570 Gaming")
                .set_power_supply("750W 80+ Gold")
                .set_case("Full Tower")
                .set_cooling_system("Liquid Cooling")
                .set_operating_system("Windows 11 Pro")
                .add_accessory("Mechanical Keyboard")
                .add_accessory("Gaming Mouse")
                .add_accessory("Monitor")
                .set_warranty(3)
                .build())
    print(custom_pc.display_specs())
    
    # ========================================================================
    # SQL QUERY BUILDER DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🗄️ SQL QUERY BUILDER DEMO")
    print("="*50)
    
    # Create query builder
    query_builder = SQLQueryBuilder()
    
    # Build different queries
    print("\n📊 Building simple SELECT query:")
    simple_query = (query_builder.reset()
                   .select("id", "name", "email")
                   .from_table("users")
                   .where("age > 18")
                   .order_by("name")
                   .limit(10)
                   .build())
    print(f"SQL: {simple_query.to_string()}")
    
    print("\n📊 Building complex query with JOINs:")
    complex_query = (query_builder.reset()
                     .select("u.name", "u.email", "COUNT(o.id) as order_count", "SUM(o.total) as total_spent")
                     .from_table("users u")
                     .join("orders o", "u.id = o.user_id", "LEFT")
                     .where("u.created_at >= '2023-01-01'")
                     .group_by("u.id", "u.name", "u.email")
                     .having("COUNT(o.id) > 5")
                     .order_by("total_spent DESC")
                     .limit(20)
                     .build())
    print(f"SQL: {complex_query.to_string()}")
    
    print("\n📊 Building pagination query:")
    pagination_query = (query_builder.reset()
                       .select("*")
                       .from_table("products")
                       .where("category = 'electronics'")
                       .order_by("price ASC")
                       .limit(10)
                       .offset(20)
                       .build())
    print(f"SQL: {pagination_query.to_string()}")
    
    # ========================================================================
    # BUILDER PATTERN BENEFITS DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("💡 BUILDER PATTERN BENEFITS")
    print("="*50)
    
    print("\n🎯 Key Benefits:")
    print("   1. ✅ Readable Code - Fluent interface makes code self-documenting")
    print("   2. ✅ Flexibility - Easy to add/remove optional parameters")
    print("   3. ✅ Validation - Can validate object state during construction")
    print("   4. ✅ Immutability - Can make objects immutable after construction")
    print("   5. ✅ Different Representations - Same builder can create different objects")
    
    print("\n🔧 Builder Components:")
    print("   1. 🏗️ Builder - Interface for building objects")
    print("   2. 🎯 Concrete Builder - Implements building steps")
    print("   3. 📦 Product - The complex object being built")
    print("   4. 🎭 Director - Orchestrates the building process (optional)")
    
    print("\n📚 Real-World Examples:")
    print("   - StringBuilder in Java/C#")
    print("   - Query builders (SQL, MongoDB)")
    print("   - Configuration builders")
    print("   - HTTP request builders")
    print("   - Test data builders")
    print("   - UI component builders")
    
    print("\n⚠️ Trade-offs:")
    print("   - Adds complexity to the codebase")
    print("   - Requires more classes and interfaces")
    print("   - May be overkill for simple objects")
    print("   - Can lead to verbose code for simple cases")
    
    # ========================================================================
    # ERROR HANDLING DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("⚠️ ERROR HANDLING DEMO")
    print("="*50)
    
    print("\n🧪 Testing validation scenarios:")
    
    # Test invalid computer build
    print("\nTesting invalid computer configuration:")
    try:
        invalid_pc = (gaming_builder.reset()
                     .set_cpu("Intel i3")  # Not optimal for gaming
                     .set_memory(4)  # Too little memory
                     .set_storage(100)  # Too little storage
                     .set_graphics_card("Integrated")  # Not suitable for gaming
                     .build())
    except ValueError as e:
        print(f"❌ Build failed as expected: {e}")
    
    # Test invalid SQL query
    print("\nTesting invalid SQL query:")
    try:
        invalid_query = (query_builder.reset()
                        .select("name")
                        # Missing FROM clause
                        .build())
    except ValueError as e:
        print(f"❌ Query build failed as expected: {e}")

if __name__ == "__main__":
    demo_builder_interview()
