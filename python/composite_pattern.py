'''
🚀 COMPOSITE PATTERN - INTERVIEW FOCUSED 🚀

The Composite Pattern composes objects into tree structures to represent
part-whole hierarchies. It lets clients treat individual objects and
compositions uniformly.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to represent hierarchical structures like file systems?"
2. "How to implement tree operations uniformly on leaves and composites?"
3. "How to build complex UI component hierarchies?"
4. "How to implement organizational structures or menu systems?"

💡 KEY INTERVIEW POINTS:
- Uniform treatment of individual and composite objects
- Tree structure representation
- Recursive operations
- Part-whole hierarchies
'''

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import os

# ============================================================================
# FILE SYSTEM COMPOSITE
# ============================================================================

class FileSystemComponent(ABC):
    """Abstract base class for file system components"""
    
    def __init__(self, name: str):
        self.name = name
        self.parent: Optional['FileSystemComponent'] = None
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
    
    @abstractmethod
    def get_size(self) -> int:
        """Get component size in bytes"""
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """Get component type"""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Display component with indentation"""
        pass
    
    def get_path(self) -> str:
        """Get full path of component"""
        if self.parent:
            return os.path.join(self.parent.get_path(), self.name)
        return self.name
    
    def get_depth(self) -> int:
        """Get depth in hierarchy"""
        if self.parent:
            return self.parent.get_depth() + 1
        return 0

class File(FileSystemComponent):
    """Leaf class representing a file"""
    
    def __init__(self, name: str, size: int, content: str = ""):
        super().__init__(name)
        self.size = size
        self.content = content
        self.extension = os.path.splitext(name)[1]
    
    def get_size(self) -> int:
        return self.size
    
    def get_type(self) -> str:
        return "file"
    
    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}📄 {self.name} ({self.size} bytes)"
    
    def read_content(self) -> str:
        """Read file content"""
        return self.content
    
    def write_content(self, content: str):
        """Write content to file"""
        self.content = content
        self.size = len(content.encode('utf-8'))
        self.modified_at = datetime.now()
        print(f"✏️ Updated file: {self.name}")

class Directory(FileSystemComponent):
    """Composite class representing a directory"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[FileSystemComponent] = []
    
    def get_size(self) -> int:
        """Calculate total size of directory and all children"""
        total_size = 0
        for child in self.children:
            total_size += child.get_size()
        return total_size
    
    def get_type(self) -> str:
        return "directory"
    
    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        result = f"{prefix}📁 {self.name}/ ({len(self.children)} items, {self.get_size()} bytes)\n"
        
        for child in self.children:
            result += child.display(indent + 1) + "\n"
        
        return result.rstrip()
    
    def add(self, component: FileSystemComponent) -> bool:
        """Add child component"""
        if component not in self.children:
            component.parent = self
            self.children.append(component)
            self.modified_at = datetime.now()
            print(f"➕ Added {component.get_type()}: {component.name}")
            return True
        return False
    
    def remove(self, component: FileSystemComponent) -> bool:
        """Remove child component"""
        if component in self.children:
            component.parent = None
            self.children.remove(component)
            self.modified_at = datetime.now()
            print(f"➖ Removed {component.get_type()}: {component.name}")
            return True
        return False
    
    def find(self, name: str) -> Optional[FileSystemComponent]:
        """Find component by name (recursive search)"""
        for child in self.children:
            if child.name == name:
                return child
            if isinstance(child, Directory):
                found = child.find(name)
                if found:
                    return found
        return None
    
    def get_file_count(self) -> int:
        """Get total number of files in directory tree"""
        count = 0
        for child in self.children:
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.get_file_count()
        return count
    
    def get_directory_count(self) -> int:
        """Get total number of directories in directory tree"""
        count = 1  # Count self
        for child in self.children:
            if isinstance(child, Directory):
                count += child.get_directory_count()
        return count

# ============================================================================
# UI COMPONENT COMPOSITE
# ============================================================================

class UIComponent(ABC):
    """Abstract base class for UI components"""
    
    def __init__(self, name: str, x: int = 0, y: int = 0, width: int = 100, height: int = 50):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.parent: Optional['UIComponent'] = None
        self.children: List['UIComponent'] = []
    
    @abstractmethod
    def render(self) -> str:
        """Render component"""
        pass
    
    @abstractmethod
    def get_component_type(self) -> str:
        """Get component type"""
        pass
    
    def add_child(self, child: 'UIComponent'):
        """Add child component"""
        child.parent = self
        self.children.append(child)
        print(f"➕ Added {child.get_component_type()}: {child.name}")
    
    def remove_child(self, child: 'UIComponent'):
        """Remove child component"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            print(f"➖ Removed {child.get_component_type()}: {child.name}")
    
    def get_absolute_position(self) -> tuple:
        """Get absolute position considering parent positions"""
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            return (parent_x + self.x, parent_y + self.y)
        return (self.x, self.y)
    
    def is_point_inside(self, x: int, y: int) -> bool:
        """Check if point is inside component bounds"""
        abs_x, abs_y = self.get_absolute_position()
        return (abs_x <= x <= abs_x + self.width and 
                abs_y <= y <= abs_y + self.height)

class Button(UIComponent):
    """Leaf component - Button"""
    
    def __init__(self, name: str, text: str, x: int = 0, y: int = 0, width: int = 100, height: int = 30):
        super().__init__(name, x, y, width, height)
        self.text = text
        self.enabled = True
    
    def render(self) -> str:
        if not self.visible:
            return ""
        
        abs_x, abs_y = self.get_absolute_position()
        status = "enabled" if self.enabled else "disabled"
        return f"🔘 Button '{self.text}' at ({abs_x}, {abs_y}) [{self.width}x{self.height}] - {status}"
    
    def get_component_type(self) -> str:
        return "button"
    
    def click(self):
        """Handle button click"""
        if self.enabled and self.visible:
            print(f"🖱️ Button '{self.text}' clicked!")

class Label(UIComponent):
    """Leaf component - Label"""
    
    def __init__(self, name: str, text: str, x: int = 0, y: int = 0, width: int = 100, height: int = 20):
        super().__init__(name, x, y, width, height)
        self.text = text
        self.font_size = 12
        self.color = "black"
    
    def render(self) -> str:
        if not self.visible:
            return ""
        
        abs_x, abs_y = self.get_absolute_position()
        return f"🏷️ Label '{self.text}' at ({abs_x}, {abs_y}) [{self.width}x{self.height}] - {self.color}"
    
    def get_component_type(self) -> str:
        return "label"

class Panel(UIComponent):
    """Composite component - Panel"""
    
    def __init__(self, name: str, x: int = 0, y: int = 0, width: int = 200, height: int = 150):
        super().__init__(name, x, y, width, height)
        self.background_color = "white"
        self.border_width = 1
    
    def render(self) -> str:
        if not self.visible:
            return ""
        
        abs_x, abs_y = self.get_absolute_position()
        result = f"📦 Panel '{self.name}' at ({abs_x}, {abs_y}) [{self.width}x{self.height}] - {self.background_color}\n"
        
        for child in self.children:
            child_render = child.render()
            if child_render:
                result += "  " + child_render + "\n"
        
        return result.rstrip()
    
    def get_component_type(self) -> str:
        return "panel"
    
    def get_total_components(self) -> int:
        """Get total number of components in panel tree"""
        count = 1  # Count self
        for child in self.children:
            if isinstance(child, Panel):
                count += child.get_total_components()
            else:
                count += 1
        return count

# ============================================================================
# ORGANIZATIONAL STRUCTURE COMPOSITE
# ============================================================================

class Employee(ABC):
    """Abstract base class for employees"""
    
    def __init__(self, name: str, position: str, salary: float):
        self.name = name
        self.position = position
        self.salary = salary
        self.department = ""
        self.hire_date = datetime.now()
    
    @abstractmethod
    def get_total_salary(self) -> float:
        """Get total salary (including subordinates)"""
        pass
    
    @abstractmethod
    def get_employee_count(self) -> int:
        """Get total number of employees (including subordinates)"""
        pass
    
    @abstractmethod
    def display_hierarchy(self, indent: int = 0) -> str:
        """Display organizational hierarchy"""
        pass
    
    def get_info(self) -> str:
        """Get employee information"""
        return f"{self.name} - {self.position} (${self.salary:,.2f})"

class IndividualEmployee(Employee):
    """Leaf class - Individual employee"""
    
    def get_total_salary(self) -> float:
        return self.salary
    
    def get_employee_count(self) -> int:
        return 1
    
    def display_hierarchy(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}👤 {self.get_info()}"

class Manager(Employee):
    """Composite class - Manager with subordinates"""
    
    def __init__(self, name: str, position: str, salary: float):
        super().__init__(name, position, salary)
        self.subordinates: List[Employee] = []
    
    def add_subordinate(self, employee: Employee):
        """Add subordinate"""
        employee.department = self.department
        self.subordinates.append(employee)
        print(f"➕ {self.name} now manages {employee.name}")
    
    def remove_subordinate(self, employee: Employee):
        """Remove subordinate"""
        if employee in self.subordinates:
            self.subordinates.remove(employee)
            print(f"➖ {self.name} no longer manages {employee.name}")
    
    def get_total_salary(self) -> float:
        """Get total salary including all subordinates"""
        total = self.salary
        for subordinate in self.subordinates:
            total += subordinate.get_total_salary()
        return total
    
    def get_employee_count(self) -> int:
        """Get total employee count including subordinates"""
        count = 1  # Count self
        for subordinate in self.subordinates:
            count += subordinate.get_employee_count()
        return count
    
    def display_hierarchy(self, indent: int = 0) -> str:
        """Display organizational hierarchy"""
        prefix = "  " * indent
        result = f"{prefix}👔 {self.get_info()} (Team: {self.get_employee_count()} people)\n"
        
        for subordinate in self.subordinates:
            result += subordinate.display_hierarchy(indent + 1) + "\n"
        
        return result.rstrip()
    
    def find_employee(self, name: str) -> Optional[Employee]:
        """Find employee by name in hierarchy"""
        if self.name == name:
            return self
        
        for subordinate in self.subordinates:
            if subordinate.name == name:
                return subordinate
            if isinstance(subordinate, Manager):
                found = subordinate.find_employee(name)
                if found:
                    return found
        
        return None

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_composite_interview():
    """
    🎯 INTERVIEW DEMO: Composite Pattern
    Demonstrates hierarchical structures and uniform operations
    """
    print("\n" + "="*60)
    print("🚀 COMPOSITE PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to represent hierarchical structures like file systems?")
    print("2. How to implement tree operations uniformly on leaves and composites?")
    print("3. How to build complex UI component hierarchies?")
    print("4. How to implement organizational structures or menu systems?")
    
    # ========================================================================
    # FILE SYSTEM COMPOSITE DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📁 FILE SYSTEM COMPOSITE DEMO")
    print("="*50)
    
    # Create file system structure
    root = Directory("project")
    
    # Create subdirectories
    src_dir = Directory("src")
    docs_dir = Directory("docs")
    tests_dir = Directory("tests")
    
    # Create files
    main_file = File("main.py", 1024, "print('Hello World')")
    config_file = File("config.json", 512, '{"debug": true}')
    readme_file = File("README.md", 2048, "# Project Documentation")
    test_file = File("test_main.py", 1536, "import unittest")
    
    # Build hierarchy
    root.add(src_dir)
    root.add(docs_dir)
    root.add(tests_dir)
    
    src_dir.add(main_file)
    src_dir.add(config_file)
    docs_dir.add(readme_file)
    tests_dir.add(test_file)
    
    print(f"\n📊 File System Statistics:")
    print(f"   Total size: {root.get_size()} bytes")
    print(f"   Files: {root.get_file_count()}")
    print(f"   Directories: {root.get_directory_count()}")
    
    print(f"\n📁 File System Structure:")
    print(root.display())
    
    # Test search functionality
    print(f"\n🔍 Searching for 'main.py':")
    found = root.find("main.py")
    if found:
        print(f"   Found: {found.get_path()}")
        print(f"   Type: {found.get_type()}")
        print(f"   Size: {found.get_size()} bytes")
    
    # ========================================================================
    # UI COMPONENT COMPOSITE DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🖥️ UI COMPONENT COMPOSITE DEMO")
    print("="*50)
    
    # Create UI hierarchy
    main_panel = Panel("MainPanel", 0, 0, 400, 300)
    
    # Create header panel
    header_panel = Panel("HeaderPanel", 10, 10, 380, 60)
    title_label = Label("TitleLabel", "Design Patterns Demo", 10, 10, 200, 30)
    close_button = Button("CloseButton", "Close", 300, 20, 80, 30)
    
    # Create content panel
    content_panel = Panel("ContentPanel", 10, 80, 380, 200)
    name_label = Label("NameLabel", "Name:", 10, 10, 50, 20)
    name_input = Button("NameInput", "Enter name...", 70, 5, 200, 30)
    submit_button = Button("SubmitButton", "Submit", 280, 5, 80, 30)
    
    # Build UI hierarchy
    main_panel.add_child(header_panel)
    main_panel.add_child(content_panel)
    
    header_panel.add_child(title_label)
    header_panel.add_child(close_button)
    
    content_panel.add_child(name_label)
    content_panel.add_child(name_input)
    content_panel.add_child(submit_button)
    
    print(f"\n🖥️ UI Component Hierarchy:")
    print(main_panel.render())
    
    print(f"\n📊 UI Statistics:")
    print(f"   Total components: {main_panel.get_total_components()}")
    
    # Test component interaction
    print(f"\n🖱️ Testing component interactions:")
    submit_button.click()
    close_button.click()
    
    # ========================================================================
    # ORGANIZATIONAL STRUCTURE DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🏢 ORGANIZATIONAL STRUCTURE DEMO")
    print("="*50)
    
    # Create organizational hierarchy
    ceo = Manager("Alice Johnson", "CEO", 200000)
    ceo.department = "Executive"
    
    # CTO and team
    cto = Manager("Bob Smith", "CTO", 150000)
    cto.department = "Engineering"
    
    senior_dev1 = IndividualEmployee("Charlie Brown", "Senior Developer", 120000)
    senior_dev2 = IndividualEmployee("Diana Prince", "Senior Developer", 125000)
    junior_dev = IndividualEmployee("Eve Wilson", "Junior Developer", 80000)
    
    # Marketing team
    marketing_director = Manager("Frank Miller", "Marketing Director", 130000)
    marketing_director.department = "Marketing"
    
    marketing_specialist1 = IndividualEmployee("Grace Lee", "Marketing Specialist", 70000)
    marketing_specialist2 = IndividualEmployee("Henry Davis", "Marketing Specialist", 75000)
    
    # Build hierarchy
    ceo.add_subordinate(cto)
    ceo.add_subordinate(marketing_director)
    
    cto.add_subordinate(senior_dev1)
    cto.add_subordinate(senior_dev2)
    cto.add_subordinate(junior_dev)
    
    marketing_director.add_subordinate(marketing_specialist1)
    marketing_director.add_subordinate(marketing_specialist2)
    
    print(f"\n🏢 Organizational Hierarchy:")
    print(ceo.display_hierarchy())
    
    print(f"\n📊 Organization Statistics:")
    print(f"   Total employees: {ceo.get_employee_count()}")
    print(f"   Total salary budget: ${ceo.get_total_salary():,.2f}")
    print(f"   Average salary: ${ceo.get_total_salary() / ceo.get_employee_count():,.2f}")
    
    # Test employee search
    print(f"\n🔍 Searching for 'Diana Prince':")
    found_employee = ceo.find_employee("Diana Prince")
    if found_employee:
        print(f"   Found: {found_employee.get_info()}")
    
    # ========================================================================
    # COMPOSITE PATTERN BENEFITS DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("💡 COMPOSITE PATTERN BENEFITS")
    print("="*50)
    
    print("\n🎯 Key Benefits:")
    print("   1. ✅ Uniform Treatment - Same interface for leaves and composites")
    print("   2. ✅ Tree Structures - Natural representation of hierarchies")
    print("   3. ✅ Recursive Operations - Easy to implement tree traversals")
    print("   4. ✅ Flexibility - Easy to add new component types")
    print("   5. ✅ Transparency - Clients don't need to know if they're working with leaves or composites")
    
    print("\n🔧 Component Types:")
    print("   1. 🍃 Leaf - Individual objects (File, Button, IndividualEmployee)")
    print("   2. 🌳 Composite - Containers with children (Directory, Panel, Manager)")
    print("   3. 🔗 Component - Common interface for both leaves and composites")
    
    print("\n📚 Real-World Examples:")
    print("   - File system structures")
    print("   - GUI component hierarchies")
    print("   - Organizational charts")
    print("   - Menu systems")
    print("   - Document structures (HTML, XML)")
    print("   - Game object hierarchies")
    
    print("\n⚠️ Trade-offs:")
    print("   - Can make the design overly general")
    print("   - May be difficult to restrict components of a composite")
    print("   - Can make it harder to add new operations")
    print("   - May violate Single Responsibility Principle")

if __name__ == "__main__":
    demo_composite_interview()
