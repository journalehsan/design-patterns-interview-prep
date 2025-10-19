'''
🚀 COMMAND PATTERN - INTERVIEW FOCUSED 🚀

The Command Pattern encapsulates a request as an object, allowing you to
parameterize clients with different requests, queue or log requests, and
support undoable operations.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to implement undo/redo in a text editor?"
2. "What about transactional operations?"
3. "How to handle command queuing?"
4. "How to implement macro commands (command sequences)?"

💡 KEY INTERVIEW POINTS:
- Undo/Redo functionality
- Command queuing and batching
- Macro commands
- Transaction support
- Command history management
'''

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

# ============================================================================
# RECEIVER CLASSES (Objects that perform the actual work)
# ============================================================================

class Document:
    """Document that can be edited"""
    def __init__(self, name: str = "Untitled"):
        self.name = name
        self.content = ""
        self.cursor_position = 0
        self.history = []
    
    def insert_text(self, text: str, position: int) -> bool:
        """Insert text at specified position"""
        if position < 0 or position > len(self.content):
            return False
        
        self.content = self.content[:position] + text + self.content[position:]
        self.cursor_position = position + len(text)
        self.history.append(f"Inserted '{text}' at position {position}")
        return True
    
    def delete_text(self, position: int, length: int) -> str:
        """Delete text starting at position"""
        if position < 0 or position >= len(self.content) or length <= 0:
            return ""
        
        end_pos = min(position + length, len(self.content))
        deleted_text = self.content[position:end_pos]
        self.content = self.content[:position] + self.content[end_pos:]
        self.cursor_position = position
        self.history.append(f"Deleted '{deleted_text}' from position {position}")
        return deleted_text
    
    def replace_text(self, old_text: str, new_text: str) -> bool:
        """Replace all occurrences of old_text with new_text"""
        if old_text not in self.content:
            return False
        
        self.content = self.content.replace(old_text, new_text)
        self.history.append(f"Replaced '{old_text}' with '{new_text}'")
        return True
    
    def get_content(self) -> str:
        return self.content
    
    def get_cursor_position(self) -> int:
        return self.cursor_position
    
    def set_cursor_position(self, position: int) -> bool:
        if 0 <= position <= len(self.content):
            self.cursor_position = position
            return True
        return False

class Calculator:
    """Calculator that can perform operations"""
    def __init__(self):
        self.value = 0.0
        self.history = []
    
    def add(self, number: float) -> float:
        """Add a number to current value"""
        old_value = self.value
        self.value += number
        self.history.append(f"Added {number} to {old_value} = {self.value}")
        return self.value
    
    def subtract(self, number: float) -> float:
        """Subtract a number from current value"""
        old_value = self.value
        self.value -= number
        self.history.append(f"Subtracted {number} from {old_value} = {self.value}")
        return self.value
    
    def multiply(self, number: float) -> float:
        """Multiply current value by a number"""
        old_value = self.value
        self.value *= number
        self.history.append(f"Multiplied {old_value} by {number} = {self.value}")
        return self.value
    
    def divide(self, number: float) -> float:
        """Divide current value by a number"""
        if number == 0:
            raise ValueError("Cannot divide by zero")
        
        old_value = self.value
        self.value /= number
        self.history.append(f"Divided {old_value} by {number} = {self.value}")
        return self.value
    
    def get_value(self) -> float:
        return self.value
    
    def set_value(self, value: float):
        self.value = value

# ============================================================================
# COMMAND INTERFACE AND CONCRETE COMMANDS
# ============================================================================

class Command(ABC):
    """Abstract command interface"""
    @abstractmethod
    def execute(self) -> bool:
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """Undo the command"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get command description"""
        pass

# ============================================================================
# DOCUMENT COMMANDS
# ============================================================================

class InsertTextCommand(Command):
    """Command to insert text into document"""
    def __init__(self, document: Document, text: str, position: int):
        self.document = document
        self.text = text
        self.position = position
        self.executed = False
    
    def execute(self) -> bool:
        if self.executed:
            return False
        
        success = self.document.insert_text(self.text, self.position)
        if success:
            self.executed = True
        return success
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        
        # Delete the text we inserted
        deleted = self.document.delete_text(self.position, len(self.text))
        if deleted == self.text:
            self.executed = False
            return True
        return False
    
    def get_description(self) -> str:
        return f"Insert '{self.text}' at position {self.position}"

class DeleteTextCommand(Command):
    """Command to delete text from document"""
    def __init__(self, document: Document, position: int, length: int):
        self.document = document
        self.position = position
        self.length = length
        self.deleted_text = ""
        self.executed = False
    
    def execute(self) -> bool:
        if self.executed:
            return False
        
        self.deleted_text = self.document.delete_text(self.position, self.length)
        if self.deleted_text:
            self.executed = True
            return True
        return False
    
    def undo(self) -> bool:
        if not self.executed or not self.deleted_text:
            return False
        
        # Re-insert the deleted text
        success = self.document.insert_text(self.deleted_text, self.position)
        if success:
            self.executed = False
        return success
    
    def get_description(self) -> str:
        return f"Delete {self.length} characters from position {self.position}"

class ReplaceTextCommand(Command):
    """Command to replace text in document"""
    def __init__(self, document: Document, old_text: str, new_text: str):
        self.document = document
        self.old_text = old_text
        self.new_text = new_text
        self.executed = False
    
    def execute(self) -> bool:
        if self.executed:
            return False
        
        success = self.document.replace_text(self.old_text, self.new_text)
        if success:
            self.executed = True
        return success
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        
        # Replace back to original text
        success = self.document.replace_text(self.new_text, self.old_text)
        if success:
            self.executed = False
        return success
    
    def get_description(self) -> str:
        return f"Replace '{self.old_text}' with '{self.new_text}'"

# ============================================================================
# CALCULATOR COMMANDS
# ============================================================================

class CalculatorCommand(Command):
    """Base class for calculator commands"""
    def __init__(self, calculator: Calculator, number: float):
        self.calculator = calculator
        self.number = number
        self.previous_value = 0.0
        self.executed = False

class AddCommand(CalculatorCommand):
    """Command to add a number"""
    def execute(self) -> bool:
        if self.executed:
            return False
        
        self.previous_value = self.calculator.get_value()
        self.calculator.add(self.number)
        self.executed = True
        return True
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        
        self.calculator.set_value(self.previous_value)
        self.executed = False
        return True
    
    def get_description(self) -> str:
        return f"Add {self.number}"

class SubtractCommand(CalculatorCommand):
    """Command to subtract a number"""
    def execute(self) -> bool:
        if self.executed:
            return False
        
        self.previous_value = self.calculator.get_value()
        self.calculator.subtract(self.number)
        self.executed = True
        return True
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        
        self.calculator.set_value(self.previous_value)
        self.executed = False
        return True
    
    def get_description(self) -> str:
        return f"Subtract {self.number}"

class MultiplyCommand(CalculatorCommand):
    """Command to multiply by a number"""
    def execute(self) -> bool:
        if self.executed:
            return False
        
        self.previous_value = self.calculator.get_value()
        self.calculator.multiply(self.number)
        self.executed = True
        return True
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        
        self.calculator.set_value(self.previous_value)
        self.executed = False
        return True
    
    def get_description(self) -> str:
        return f"Multiply by {self.number}"

# ============================================================================
# MACRO COMMAND (Command sequences)
# ============================================================================

class MacroCommand(Command):
    """Command that executes multiple commands as a group"""
    def __init__(self, commands: List[Command], description: str = "Macro Command"):
        self.commands = commands
        self.description = description
        self.executed = False
    
    def execute(self) -> bool:
        if self.executed:
            return False
        
        print(f"🎬 Executing macro: {self.description}")
        for i, command in enumerate(self.commands):
            if not command.execute():
                # If any command fails, undo all previously executed commands
                print(f"❌ Command {i+1} failed, undoing previous commands...")
                for j in range(i-1, -1, -1):
                    self.commands[j].undo()
                return False
        
        self.executed = True
        print(f"✅ Macro completed successfully")
        return True
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        
        print(f"🔄 Undoing macro: {self.description}")
        # Undo commands in reverse order
        for command in reversed(self.commands):
            command.undo()
        
        self.executed = False
        print(f"✅ Macro undone successfully")
        return True
    
    def get_description(self) -> str:
        return f"{self.description} ({len(self.commands)} commands)"

# ============================================================================
# COMMAND MANAGER (Invoker)
# ============================================================================

class CommandManager:
    """Manages command execution, undo/redo, and history"""
    def __init__(self):
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []
        self.command_history: List[Dict[str, Any]] = []
        self.max_history = 100
    
    def execute_command(self, command: Command) -> bool:
        """Execute a command and add it to history"""
        print(f"▶️  Executing: {command.get_description()}")
        
        success = command.execute()
        if success:
            self.undo_stack.append(command)
            self.redo_stack.clear()  # Clear redo stack when new command executed
            
            # Add to history
            self.command_history.append({
                'command': command,
                'description': command.get_description(),
                'timestamp': datetime.now(),
                'type': 'execute'
            })
            
            # Limit history size
            if len(self.command_history) > self.max_history:
                self.command_history.pop(0)
            
            print(f"✅ Command executed successfully")
        else:
            print(f"❌ Command execution failed")
        
        return success
    
    def undo(self) -> bool:
        """Undo the last executed command"""
        if not self.undo_stack:
            print("⚠️  Nothing to undo")
            return False
        
        command = self.undo_stack.pop()
        print(f"↩️  Undoing: {command.get_description()}")
        
        success = command.undo()
        if success:
            self.redo_stack.append(command)
            
            # Add to history
            self.command_history.append({
                'command': command,
                'description': f"UNDO: {command.get_description()}",
                'timestamp': datetime.now(),
                'type': 'undo'
            })
            
            print(f"✅ Command undone successfully")
        else:
            print(f"❌ Command undo failed")
            # Put command back on undo stack if undo failed
            self.undo_stack.append(command)
        
        return success
    
    def redo(self) -> bool:
        """Redo the last undone command"""
        if not self.redo_stack:
            print("⚠️  Nothing to redo")
            return False
        
        command = self.redo_stack.pop()
        print(f"↪️  Redoing: {command.get_description()}")
        
        success = command.execute()
        if success:
            self.undo_stack.append(command)
            
            # Add to history
            self.command_history.append({
                'command': command,
                'description': f"REDO: {command.get_description()}",
                'timestamp': datetime.now(),
                'type': 'redo'
            })
            
            print(f"✅ Command redone successfully")
        else:
            print(f"❌ Command redo failed")
            # Put command back on redo stack if redo failed
            self.redo_stack.append(command)
        
        return success
    
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return len(self.redo_stack) > 0
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get command history"""
        return self.command_history.copy()
    
    def clear_history(self):
        """Clear all history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.command_history.clear()
        print("🗑️  Command history cleared")
    
    def print_status(self):
        """Print current status"""
        print(f"\n📊 Command Manager Status:")
        print(f"   Undo stack: {len(self.undo_stack)} commands")
        print(f"   Redo stack: {len(self.redo_stack)} commands")
        print(f"   History: {len(self.command_history)} entries")
        print(f"   Can undo: {self.can_undo()}")
        print(f"   Can redo: {self.can_redo()}")

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_command_interview():
    """
    🎯 INTERVIEW DEMO: Command Pattern
    Demonstrates undo/redo, macro commands, and command queuing
    """
    print("\n" + "="*60)
    print("🚀 COMMAND PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to implement undo/redo in a text editor?")
    print("2. What about transactional operations?")
    print("3. How to handle command queuing?")
    print("4. How to implement macro commands?")
    
    # ========================================================================
    # DOCUMENT EDITOR DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📝 DOCUMENT EDITOR DEMO")
    print("="*50)
    
    # Create document and command manager
    doc = Document("Interview Demo")
    manager = CommandManager()
    
    print(f"\n📄 Created document: '{doc.name}'")
    print(f"Initial content: '{doc.get_content()}'")
    
    # Execute some commands
    print("\n✏️  Executing commands:")
    manager.execute_command(InsertTextCommand(doc, "Hello", 0))
    manager.execute_command(InsertTextCommand(doc, " World", 5))
    manager.execute_command(InsertTextCommand(doc, "!", 11))
    
    print(f"Content after inserts: '{doc.get_content()}'")
    
    # Test undo operations
    print("\n↩️  Testing undo operations:")
    manager.undo()  # Undo "!"
    print(f"After undoing '!': '{doc.get_content()}'")
    
    manager.undo()  # Undo " World"
    print(f"After undoing ' World': '{doc.get_content()}'")
    
    # Test redo operations
    print("\n↪️  Testing redo operations:")
    manager.redo()  # Redo " World"
    print(f"After redoing ' World': '{doc.get_content()}'")
    
    manager.redo()  # Redo "!"
    print(f"After redoing '!': '{doc.get_content()}'")
    
    # Test replace command
    print("\n🔄 Testing replace command:")
    manager.execute_command(ReplaceTextCommand(doc, "Hello", "Hi"))
    print(f"After replacing 'Hello' with 'Hi': '{doc.get_content()}'")
    
    manager.undo()
    print(f"After undoing replace: '{doc.get_content()}'")
    
    # ========================================================================
    # CALCULATOR DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🧮 CALCULATOR DEMO")
    print("="*50)
    
    calc = Calculator()
    calc_manager = CommandManager()
    
    print(f"\n🔢 Initial calculator value: {calc.get_value()}")
    
    # Execute calculator commands
    print("\n➕ Executing calculator commands:")
    calc_manager.execute_command(AddCommand(calc, 10))
    print(f"After adding 10: {calc.get_value()}")
    
    calc_manager.execute_command(MultiplyCommand(calc, 2))
    print(f"After multiplying by 2: {calc.get_value()}")
    
    calc_manager.execute_command(SubtractCommand(calc, 5))
    print(f"After subtracting 5: {calc.get_value()}")
    
    # Test undo/redo
    print("\n↩️  Testing calculator undo:")
    calc_manager.undo()
    print(f"After undoing subtract 5: {calc.get_value()}")
    
    calc_manager.undo()
    print(f"After undoing multiply by 2: {calc.get_value()}")
    
    print("\n↪️  Testing calculator redo:")
    calc_manager.redo()
    print(f"After redoing multiply by 2: {calc.get_value()}")
    
    # ========================================================================
    # MACRO COMMAND DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🎬 MACRO COMMAND DEMO")
    print("="*50)
    
    # Create a macro that formats a document
    doc2 = Document("Macro Demo")
    macro_manager = CommandManager()
    
    # Create macro commands
    format_commands = [
        InsertTextCommand(doc2, "# Title\n", 0),
        InsertTextCommand(doc2, "## Subtitle\n", 8),
        InsertTextCommand(doc2, "This is a formatted document.\n", 21),
        InsertTextCommand(doc2, "**Bold text** and *italic text*.\n", 52)
    ]
    
    format_macro = MacroCommand(format_commands, "Format Document")
    
    print(f"\n📄 Initial document content: '{doc2.get_content()}'")
    
    # Execute macro
    print("\n🎬 Executing format macro:")
    macro_manager.execute_command(format_macro)
    print(f"Document after macro: '{doc2.get_content()}'")
    
    # Undo macro
    print("\n↩️  Undoing macro:")
    macro_manager.undo()
    print(f"Document after undoing macro: '{doc2.get_content()}'")
    
    # ========================================================================
    # COMMAND HISTORY DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📚 COMMAND HISTORY DEMO")
    print("="*50)
    
    # Show command history
    print("\n📋 Command history:")
    history = manager.get_history()
    for i, entry in enumerate(history[-10:], 1):  # Show last 10 commands
        timestamp = entry['timestamp'].strftime("%H:%M:%S")
        print(f"   {i}. [{timestamp}] {entry['description']}")
    
    # Show status
    manager.print_status()
    
    # ========================================================================
    # ERROR HANDLING DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("⚠️  ERROR HANDLING DEMO")
    print("="*50)
    
    # Test invalid operations
    print("\n🧪 Testing error handling:")
    
    # Try to undo when nothing to undo
    print("\nTesting undo with empty stack:")
    empty_manager = CommandManager()
    empty_manager.undo()
    
    # Try to redo when nothing to redo
    print("\nTesting redo with empty stack:")
    empty_manager.redo()
    
    # Test invalid document operations
    print("\nTesting invalid document operations:")
    invalid_doc = Document("Error Test")
    error_manager = CommandManager()
    
    # Try to insert at invalid position
    invalid_cmd = InsertTextCommand(invalid_doc, "test", -1)
    error_manager.execute_command(invalid_cmd)
    
    # Try to delete from invalid position
    invalid_doc.insert_text("Hello", 0)
    invalid_delete = DeleteTextCommand(invalid_doc, 10, 5)  # Beyond content length
    error_manager.execute_command(invalid_delete)

if __name__ == "__main__":
    demo_command_interview()
