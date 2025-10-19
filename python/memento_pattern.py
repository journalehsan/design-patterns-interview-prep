'''
🚀 MEMENTO PATTERN - INTERVIEW FOCUSED 🚀

The Memento Pattern captures and externalizes an object's internal state
so that the object can be restored to this state later without violating encapsulation.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to implement save/restore functionality in a game?"
2. "How to implement undo/redo with state snapshots?"
3. "How to handle version control for object states?"
4. "How to implement checkpoint/rollback systems?"

💡 KEY INTERVIEW POINTS:
- State capture without breaking encapsulation
- Caretaker management of mementos
- Memory management for large states
- Version control and state history
'''

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import copy

# ============================================================================
# ORIGINATOR CLASSES (Objects whose state needs to be saved)
# ============================================================================

class GameCharacter:
    """Game character that can save and restore its state"""
    def __init__(self, name: str):
        self.name = name
        self.level = 1
        self.health = 100
        self.mana = 50
        self.experience = 0
        self.position = {"x": 0, "y": 0}
        self.inventory = []
        self.skills = []
        self._state_version = 1
    
    def level_up(self):
        """Level up the character"""
        self.level += 1
        self.health = min(100, self.health + 20)
        self.mana = min(100, self.mana + 15)
        self._state_version += 1
        print(f"🎉 {self.name} leveled up to level {self.level}!")
    
    def take_damage(self, damage: int):
        """Take damage"""
        self.health = max(0, self.health - damage)
        self._state_version += 1
        print(f"💔 {self.name} took {damage} damage. Health: {self.health}")
    
    def gain_experience(self, exp: int):
        """Gain experience points"""
        self.experience += exp
        self._state_version += 1
        print(f"⭐ {self.name} gained {exp} experience. Total: {self.experience}")
    
    def move_to(self, x: int, y: int):
        """Move character to new position"""
        self.position = {"x": x, "y": y}
        self._state_version += 1
        print(f"🚶 {self.name} moved to position ({x}, {y})")
    
    def add_item(self, item: str):
        """Add item to inventory"""
        self.inventory.append(item)
        self._state_version += 1
        print(f"🎒 {self.name} picked up: {item}")
    
    def learn_skill(self, skill: str):
        """Learn a new skill"""
        if skill not in self.skills:
            self.skills.append(skill)
            self._state_version += 1
            print(f"🧠 {self.name} learned skill: {skill}")
    
    def get_state_info(self) -> str:
        """Get current state information"""
        return (f"Character: {self.name} | Level: {self.level} | "
                f"Health: {self.health} | Mana: {self.mana} | "
                f"Exp: {self.experience} | Position: {self.position} | "
                f"Inventory: {len(self.inventory)} items | "
                f"Skills: {len(self.skills)} skills | "
                f"Version: {self._state_version}")
    
    def create_memento(self) -> 'CharacterMemento':
        """Create a memento of current state"""
        return CharacterMemento(
            level=self.level,
            health=self.health,
            mana=self.mana,
            experience=self.experience,
            position=copy.deepcopy(self.position),
            inventory=copy.deepcopy(self.inventory),
            skills=copy.deepcopy(self.skills),
            version=self._state_version,
            timestamp=datetime.now()
        )
    
    def restore_from_memento(self, memento: 'CharacterMemento'):
        """Restore state from memento"""
        self.level = memento.level
        self.health = memento.health
        self.mana = memento.mana
        self.experience = memento.experience
        self.position = copy.deepcopy(memento.position)
        self.inventory = copy.deepcopy(memento.inventory)
        self.skills = copy.deepcopy(memento.skills)
        self._state_version = memento.version
        print(f"🔄 {self.name} restored to version {memento.version} from {memento.timestamp}")

class DocumentEditor:
    """Document editor that can save and restore states"""
    def __init__(self, filename: str):
        self.filename = filename
        self.content = ""
        self.cursor_position = 0
        self.selection_start = 0
        self.selection_end = 0
        self.font_size = 12
        self.font_family = "Arial"
        self.is_bold = False
        self.is_italic = False
        self._change_count = 0
    
    def insert_text(self, text: str):
        """Insert text at cursor position"""
        self.content = (self.content[:self.cursor_position] + 
                       text + 
                       self.content[self.cursor_position:])
        self.cursor_position += len(text)
        self._change_count += 1
        print(f"📝 Inserted '{text}' at position {self.cursor_position - len(text)}")
    
    def delete_text(self, length: int):
        """Delete text before cursor"""
        if length > 0 and self.cursor_position >= length:
            deleted = self.content[self.cursor_position - length:self.cursor_position]
            self.content = (self.content[:self.cursor_position - length] + 
                           self.content[self.cursor_position:])
            self.cursor_position -= length
            self._change_count += 1
            print(f"🗑️ Deleted '{deleted}'")
    
    def set_formatting(self, bold: bool = None, italic: bool = None, 
                      font_size: int = None, font_family: str = None):
        """Set text formatting"""
        if bold is not None:
            self.is_bold = bold
        if italic is not None:
            self.is_italic = italic
        if font_size is not None:
            self.font_size = font_size
        if font_family is not None:
            self.font_family = font_family
        self._change_count += 1
        print(f"🎨 Formatting updated: Bold={self.is_bold}, Italic={self.is_italic}, "
              f"Size={self.font_size}, Font={self.font_family}")
    
    def get_state_info(self) -> str:
        """Get current state information"""
        return (f"Document: {self.filename} | Content: {len(self.content)} chars | "
                f"Cursor: {self.cursor_position} | Changes: {self._change_count} | "
                f"Format: {self.font_family} {self.font_size}pt "
                f"{'Bold' if self.is_bold else ''} {'Italic' if self.is_italic else ''}")
    
    def create_memento(self) -> 'DocumentMemento':
        """Create a memento of current state"""
        return DocumentMemento(
            content=self.content,
            cursor_position=self.cursor_position,
            selection_start=self.selection_start,
            selection_end=self.selection_end,
            font_size=self.font_size,
            font_family=self.font_family,
            is_bold=self.is_bold,
            is_italic=self.is_italic,
            change_count=self._change_count,
            timestamp=datetime.now()
        )
    
    def restore_from_memento(self, memento: 'DocumentMemento'):
        """Restore state from memento"""
        self.content = memento.content
        self.cursor_position = memento.cursor_position
        self.selection_start = memento.selection_start
        self.selection_end = memento.selection_end
        self.font_size = memento.font_size
        self.font_family = memento.font_family
        self.is_bold = memento.is_bold
        self.is_italic = memento.is_italic
        self._change_count = memento.change_count
        print(f"🔄 Document restored to change #{memento.change_count} from {memento.timestamp}")

# ============================================================================
# MEMENTO CLASSES (State snapshots)
# ============================================================================

class CharacterMemento:
    """Memento for character state"""
    def __init__(self, level: int, health: int, mana: int, experience: int,
                 position: Dict[str, int], inventory: List[str], skills: List[str],
                 version: int, timestamp: datetime):
        self.level = level
        self.health = health
        self.mana = mana
        self.experience = experience
        self.position = position
        self.inventory = inventory
        self.skills = skills
        self.version = version
        self.timestamp = timestamp
    
    def get_description(self) -> str:
        """Get memento description"""
        return (f"Version {self.version} | Level {self.level} | "
                f"Health {self.health} | Mana {self.mana} | "
                f"Exp {self.experience} | Items {len(self.inventory)} | "
                f"Skills {len(self.skills)} | {self.timestamp.strftime('%H:%M:%S')}")

class DocumentMemento:
    """Memento for document state"""
    def __init__(self, content: str, cursor_position: int, selection_start: int,
                 selection_end: int, font_size: int, font_family: str,
                 is_bold: bool, is_italic: bool, change_count: int, timestamp: datetime):
        self.content = content
        self.cursor_position = cursor_position
        self.selection_start = selection_start
        self.selection_end = selection_end
        self.font_size = font_size
        self.font_family = font_family
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.change_count = change_count
        self.timestamp = timestamp
    
    def get_description(self) -> str:
        """Get memento description"""
        return (f"Change #{self.change_count} | {len(self.content)} chars | "
                f"Cursor {self.cursor_position} | {self.font_family} {self.font_size}pt | "
                f"{self.timestamp.strftime('%H:%M:%S')}")

# ============================================================================
# CARETAKER CLASSES (Manage mementos)
# ============================================================================

class GameSaveManager:
    """Manages game saves and checkpoints"""
    def __init__(self, max_saves: int = 10):
        self.saves: List[CharacterMemento] = []
        self.checkpoints: List[CharacterMemento] = []
        self.max_saves = max_saves
        self.current_save_index = -1
    
    def save_game(self, character: GameCharacter) -> bool:
        """Save current game state"""
        memento = character.create_memento()
        self.saves.append(memento)
        
        # Limit number of saves
        if len(self.saves) > self.max_saves:
            self.saves.pop(0)
        
        self.current_save_index = len(self.saves) - 1
        print(f"💾 Game saved: {memento.get_description()}")
        return True
    
    def load_game(self, character: GameCharacter, save_index: int = -1) -> bool:
        """Load game from save"""
        if not self.saves:
            print("❌ No saves available!")
            return False
        
        if save_index == -1:
            save_index = self.current_save_index
        
        if 0 <= save_index < len(self.saves):
            memento = self.saves[save_index]
            character.restore_from_memento(memento)
            self.current_save_index = save_index
            return True
        else:
            print(f"❌ Invalid save index: {save_index}")
            return False
    
    def create_checkpoint(self, character: GameCharacter):
        """Create a checkpoint (temporary save)"""
        memento = character.create_memento()
        self.checkpoints.append(memento)
        print(f"📍 Checkpoint created: {memento.get_description()}")
    
    def restore_checkpoint(self, character: GameCharacter) -> bool:
        """Restore from last checkpoint"""
        if not self.checkpoints:
            print("❌ No checkpoints available!")
            return False
        
        memento = self.checkpoints[-1]
        character.restore_from_memento(memento)
        print(f"📍 Restored from checkpoint: {memento.get_description()}")
        return True
    
    def list_saves(self):
        """List all available saves"""
        if not self.saves:
            print("📋 No saves available")
            return
        
        print("📋 Available saves:")
        for i, save in enumerate(self.saves):
            marker = " 👈" if i == self.current_save_index else ""
            print(f"   {i}: {save.get_description()}{marker}")
    
    def delete_save(self, save_index: int) -> bool:
        """Delete a save"""
        if 0 <= save_index < len(self.saves):
            deleted_save = self.saves.pop(save_index)
            print(f"🗑️ Deleted save: {deleted_save.get_description()}")
            
            # Adjust current save index
            if self.current_save_index >= len(self.saves):
                self.current_save_index = len(self.saves) - 1
            
            return True
        else:
            print(f"❌ Invalid save index: {save_index}")
            return False

class DocumentHistoryManager:
    """Manages document history and undo/redo"""
    def __init__(self, max_history: int = 50):
        self.history: List[DocumentMemento] = []
        self.current_index = -1
        self.max_history = max_history
    
    def save_state(self, document: DocumentEditor) -> bool:
        """Save current document state"""
        memento = document.create_memento()
        
        # Remove any history after current index (for redo)
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        self.history.append(memento)
        self.current_index = len(self.history) - 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index -= 1
        
        print(f"📝 State saved: {memento.get_description()}")
        return True
    
    def undo(self, document: DocumentEditor) -> bool:
        """Undo last change"""
        if self.current_index > 0:
            self.current_index -= 1
            memento = self.history[self.current_index]
            document.restore_from_memento(memento)
            print(f"↩️ Undo: {memento.get_description()}")
            return True
        else:
            print("❌ Nothing to undo!")
            return False
    
    def redo(self, document: DocumentEditor) -> bool:
        """Redo last undone change"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            memento = self.history[self.current_index]
            document.restore_from_memento(memento)
            print(f"↪️ Redo: {memento.get_description()}")
            return True
        else:
            print("❌ Nothing to redo!")
            return False
    
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return self.current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return self.current_index < len(self.history) - 1
    
    def get_history_info(self) -> str:
        """Get history information"""
        return (f"History: {len(self.history)} states | "
                f"Current: {self.current_index + 1} | "
                f"Can undo: {self.can_undo()} | "
                f"Can redo: {self.can_redo()}")

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_memento_interview():
    """
    🎯 INTERVIEW DEMO: Memento Pattern
    Demonstrates state capture and restoration scenarios
    """
    print("\n" + "="*60)
    print("🚀 MEMENTO PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to implement save/restore functionality in a game?")
    print("2. How to implement undo/redo with state snapshots?")
    print("3. How to handle version control for object states?")
    print("4. How to implement checkpoint/rollback systems?")
    
    # ========================================================================
    # GAME CHARACTER SAVE SYSTEM DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🎮 GAME CHARACTER SAVE SYSTEM DEMO")
    print("="*50)
    
    # Create character and save manager
    hero = GameCharacter("DragonSlayer")
    save_manager = GameSaveManager(max_saves=5)
    
    print(f"\n👤 Created character: {hero.get_state_info()}")
    
    # Play the game and create saves
    print("\n🎮 Playing the game...")
    hero.gain_experience(100)
    hero.add_item("Sword")
    hero.learn_skill("Fireball")
    hero.move_to(10, 5)
    
    print(f"\n📊 After some gameplay: {hero.get_state_info()}")
    
    # Save game
    save_manager.save_game(hero)
    
    # Continue playing
    print("\n🎮 Continuing gameplay...")
    hero.level_up()
    hero.take_damage(30)
    hero.add_item("Shield")
    hero.learn_skill("Heal")
    hero.move_to(15, 8)
    
    print(f"\n📊 After more gameplay: {hero.get_state_info()}")
    
    # Create checkpoint
    save_manager.create_checkpoint(hero)
    
    # More gameplay
    print("\n🎮 More gameplay...")
    hero.gain_experience(200)
    hero.take_damage(50)
    
    print(f"\n📊 After dangerous encounter: {hero.get_state_info()}")
    
    # Show available saves
    save_manager.list_saves()
    
    # Restore from checkpoint
    print("\n📍 Restoring from checkpoint...")
    save_manager.restore_checkpoint(hero)
    print(f"📊 After checkpoint restore: {hero.get_state_info()}")
    
    # Load previous save
    print("\n💾 Loading previous save...")
    save_manager.load_game(hero, 0)
    print(f"📊 After loading save: {hero.get_state_info()}")
    
    # ========================================================================
    # DOCUMENT EDITOR HISTORY DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📝 DOCUMENT EDITOR HISTORY DEMO")
    print("="*50)
    
    # Create document and history manager
    doc = DocumentEditor("Interview Notes")
    history_manager = DocumentHistoryManager(max_history=10)
    
    print(f"\n📄 Created document: {doc.get_state_info()}")
    
    # Edit document with history tracking
    print("\n✏️ Editing document...")
    
    # Initial state
    history_manager.save_state(doc)
    doc.insert_text("Design Patterns Interview Prep")
    history_manager.save_state(doc)
    
    doc.insert_text("\n\n1. Observer Pattern")
    history_manager.save_state(doc)
    
    doc.insert_text("\n   - Event-driven architecture")
    history_manager.save_state(doc)
    
    doc.set_formatting(bold=True, font_size=14)
    history_manager.save_state(doc)
    
    doc.insert_text("\n\n2. Strategy Pattern")
    history_manager.save_state(doc)
    
    print(f"\n📊 After editing: {doc.get_state_info()}")
    print(f"📋 History: {history_manager.get_history_info()}")
    
    # Test undo/redo
    print("\n↩️ Testing undo operations:")
    history_manager.undo(doc)
    print(f"After undo: {doc.get_state_info()}")
    
    history_manager.undo(doc)
    print(f"After another undo: {doc.get_state_info()}")
    
    print("\n↪️ Testing redo operations:")
    history_manager.redo(doc)
    print(f"After redo: {doc.get_state_info()}")
    
    history_manager.redo(doc)
    print(f"After another redo: {doc.get_state_info()}")
    
    # ========================================================================
    # MEMORY MANAGEMENT DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🧠 MEMORY MANAGEMENT DEMO")
    print("="*50)
    
    print("\n💡 Memory management considerations:")
    print("   - Limit number of saved states")
    print("   - Use deep copy for complex objects")
    print("   - Implement state compression for large objects")
    print("   - Consider lazy loading for large mementos")
    
    # Show memory usage simulation
    print(f"\n📊 Current save manager state:")
    print(f"   Saves: {len(save_manager.saves)}")
    print(f"   Checkpoints: {len(save_manager.checkpoints)}")
    print(f"   Max saves: {save_manager.max_saves}")
    
    print(f"\n📊 Current history manager state:")
    print(f"   History entries: {len(history_manager.history)}")
    print(f"   Max history: {history_manager.max_history}")
    print(f"   Current index: {history_manager.current_index}")
    
    # ========================================================================
    # ERROR HANDLING DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("⚠️ ERROR HANDLING DEMO")
    print("="*50)
    
    print("\n🧪 Testing error scenarios:")
    
    # Test loading invalid save
    print("\nTesting invalid save loading:")
    save_manager.load_game(hero, 999)  # Invalid index
    
    # Test undo when nothing to undo
    print("\nTesting undo with no history:")
    empty_history = DocumentHistoryManager()
    empty_doc = DocumentEditor("Empty")
    empty_history.undo(empty_doc)
    
    # Test redo when nothing to redo
    print("\nTesting redo with no history:")
    empty_history.redo(empty_doc)

if __name__ == "__main__":
    demo_memento_interview()
