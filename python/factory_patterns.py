'''
🚀 FACTORY PATTERNS - INTERVIEW FOCUSED 🚀

Factory Patterns provide an interface for creating objects without specifying
their exact classes. This includes Simple Factory, Factory Method, and Abstract Factory.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to create objects without knowing their exact classes?"
2. "What's the difference between Simple Factory, Factory Method, and Abstract Factory?"
3. "How to add new product types without modifying existing code?"
4. "How to create families of related objects?"

💡 KEY INTERVIEW POINTS:
- Object creation without tight coupling
- Extensibility and maintainability
- Factory hierarchy and product families
- Configuration-driven object creation
'''

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
import json

# ============================================================================
# SIMPLE FACTORY PATTERN
# ============================================================================

class PaymentMethod(Enum):
    """Payment method types"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CRYPTOCURRENCY = "cryptocurrency"

class PaymentProcessor(ABC):
    """Abstract payment processor"""
    
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.transaction_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        """Process a payment"""
        pass
    
    @abstractmethod
    def get_processor_name(self) -> str:
        """Get processor name"""
        pass
    
    def add_transaction(self, transaction: Dict[str, Any]):
        """Add transaction to history"""
        self.transaction_history.append(transaction)

class CreditCardProcessor(PaymentProcessor):
    """Credit card payment processor"""
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        print(f"💳 Processing credit card payment: ${amount} {currency}")
        
        # Simulate processing
        transaction = {
            "id": f"CC_{len(self.transaction_history) + 1}",
            "amount": amount,
            "currency": currency,
            "method": "credit_card",
            "status": "completed",
            "processor": self.get_processor_name()
        }
        
        self.add_transaction(transaction)
        return transaction
    
    def get_processor_name(self) -> str:
        return "CreditCardProcessor"

class PayPalProcessor(PaymentProcessor):
    """PayPal payment processor"""
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        print(f"🅿️ Processing PayPal payment: ${amount} {currency}")
        
        # Simulate processing
        transaction = {
            "id": f"PP_{len(self.transaction_history) + 1}",
            "amount": amount,
            "currency": currency,
            "method": "paypal",
            "status": "completed",
            "processor": self.get_processor_name()
        }
        
        self.add_transaction(transaction)
        return transaction
    
    def get_processor_name(self) -> str:
        return "PayPalProcessor"

class CryptocurrencyProcessor(PaymentProcessor):
    """Cryptocurrency payment processor"""
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict[str, Any]:
        print(f"₿ Processing cryptocurrency payment: ${amount} {currency}")
        
        # Simulate processing
        transaction = {
            "id": f"CRYPTO_{len(self.transaction_history) + 1}",
            "amount": amount,
            "currency": currency,
            "method": "cryptocurrency",
            "status": "completed",
            "processor": self.get_processor_name()
        }
        
        self.add_transaction(transaction)
        return transaction
    
    def get_processor_name(self) -> str:
        return "CryptocurrencyProcessor"

class PaymentProcessorFactory:
    """Simple Factory for creating payment processors"""
    
    @staticmethod
    def create_processor(payment_method: PaymentMethod, account_id: str) -> PaymentProcessor:
        """Create payment processor based on method"""
        processors = {
            PaymentMethod.CREDIT_CARD: CreditCardProcessor,
            PaymentMethod.DEBIT_CARD: CreditCardProcessor,  # Same as credit card
            PaymentMethod.PAYPAL: PayPalProcessor,
            PaymentMethod.CRYPTOCURRENCY: CryptocurrencyProcessor,
        }
        
        processor_class = processors.get(payment_method)
        if not processor_class:
            raise ValueError(f"Unsupported payment method: {payment_method}")
        
        return processor_class(account_id)

# ============================================================================
# FACTORY METHOD PATTERN
# ============================================================================

class Document(ABC):
    """Abstract document class"""
    
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.created_at = None
        self.modified_at = None
    
    @abstractmethod
    def save(self, filename: str) -> bool:
        """Save document"""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Get file extension"""
        pass
    
    @abstractmethod
    def get_mime_type(self) -> str:
        """Get MIME type"""
        pass

class PDFDocument(Document):
    """PDF document"""
    
    def save(self, filename: str) -> bool:
        print(f"📄 Saving PDF document: {filename}")
        # Simulate PDF saving
        return True
    
    def get_file_extension(self) -> str:
        return ".pdf"
    
    def get_mime_type(self) -> str:
        return "application/pdf"

class WordDocument(Document):
    """Word document"""
    
    def save(self, filename: str) -> bool:
        print(f"📝 Saving Word document: {filename}")
        # Simulate Word document saving
        return True
    
    def get_file_extension(self) -> str:
        return ".docx"
    
    def get_mime_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

class TextDocument(Document):
    """Plain text document"""
    
    def save(self, filename: str) -> bool:
        print(f"📄 Saving text document: {filename}")
        # Simulate text file saving
        return True
    
    def get_file_extension(self) -> str:
        return ".txt"
    
    def get_mime_type(self) -> str:
        return "text/plain"

class DocumentCreator(ABC):
    """Abstract document creator (Factory Method)"""
    
    @abstractmethod
    def create_document(self, title: str, content: str) -> Document:
        """Create a document"""
        pass
    
    def create_and_save_document(self, title: str, content: str, filename: str) -> bool:
        """Create document and save it"""
        document = self.create_document(title, content)
        return document.save(filename)

class PDFDocumentCreator(DocumentCreator):
    """PDF document creator"""
    
    def create_document(self, title: str, content: str) -> Document:
        return PDFDocument(title, content)

class WordDocumentCreator(DocumentCreator):
    """Word document creator"""
    
    def create_document(self, title: str, content: str) -> Document:
        return WordDocument(title, content)

class TextDocumentCreator(DocumentCreator):
    """Text document creator"""
    
    def create_document(self, title: str, content: str) -> Document:
        return TextDocument(title, content)

# ============================================================================
# ABSTRACT FACTORY PATTERN
# ============================================================================

class UITheme(Enum):
    """UI theme types"""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"

class Button(ABC):
    """Abstract button component"""
    
    def __init__(self, text: str):
        self.text = text
    
    @abstractmethod
    def render(self) -> str:
        """Render button"""
        pass
    
    @abstractmethod
    def get_theme(self) -> str:
        """Get button theme"""
        pass

class LightButton(Button):
    """Light theme button"""
    
    def render(self) -> str:
        return f"🔘 Light Button: {self.text}"
    
    def get_theme(self) -> str:
        return "light"

class DarkButton(Button):
    """Dark theme button"""
    
    def render(self) -> str:
        return f"⚫ Dark Button: {self.text}"
    
    def get_theme(self) -> str:
        return "dark"

class HighContrastButton(Button):
    """High contrast theme button"""
    
    def render(self) -> str:
        return f"🔳 High Contrast Button: {self.text}"
    
    def get_theme(self) -> str:
        return "high_contrast"

class TextField(ABC):
    """Abstract text field component"""
    
    def __init__(self, placeholder: str):
        self.placeholder = placeholder
        self.value = ""
    
    @abstractmethod
    def render(self) -> str:
        """Render text field"""
        pass
    
    @abstractmethod
    def get_theme(self) -> str:
        """Get text field theme"""
        pass
    
    def set_value(self, value: str):
        """Set field value"""
        self.value = value

class LightTextField(TextField):
    """Light theme text field"""
    
    def render(self) -> str:
        return f"📝 Light Text Field: {self.placeholder} = '{self.value}'"
    
    def get_theme(self) -> str:
        return "light"

class DarkTextField(TextField):
    """Dark theme text field"""
    
    def render(self) -> str:
        return f"📄 Dark Text Field: {self.placeholder} = '{self.value}'"
    
    def get_theme(self) -> str:
        return "dark"

class HighContrastTextField(TextField):
    """High contrast theme text field"""
    
    def render(self) -> str:
        return f"📋 High Contrast Text Field: {self.placeholder} = '{self.value}'"
    
    def get_theme(self) -> str:
        return "high_contrast"

class UIFactory(ABC):
    """Abstract UI factory"""
    
    @abstractmethod
    def create_button(self, text: str) -> Button:
        """Create button"""
        pass
    
    @abstractmethod
    def create_text_field(self, placeholder: str) -> TextField:
        """Create text field"""
        pass
    
    @abstractmethod
    def get_theme_name(self) -> str:
        """Get theme name"""
        pass

class LightThemeFactory(UIFactory):
    """Light theme factory"""
    
    def create_button(self, text: str) -> Button:
        return LightButton(text)
    
    def create_text_field(self, placeholder: str) -> TextField:
        return LightTextField(placeholder)
    
    def get_theme_name(self) -> str:
        return "Light Theme"

class DarkThemeFactory(UIFactory):
    """Dark theme factory"""
    
    def create_button(self, text: str) -> Button:
        return DarkButton(text)
    
    def create_text_field(self, placeholder: str) -> TextField:
        return DarkTextField(placeholder)
    
    def get_theme_name(self) -> str:
        return "Dark Theme"

class HighContrastThemeFactory(UIFactory):
    """High contrast theme factory"""
    
    def create_button(self, text: str) -> Button:
        return HighContrastButton(text)
    
    def create_text_field(self, placeholder: str) -> TextField:
        return HighContrastTextField(placeholder)
    
    def get_theme_name(self) -> str:
        return "High Contrast Theme"

class UIFactoryProvider:
    """Factory provider for UI themes"""
    
    @staticmethod
    def get_factory(theme: UITheme) -> UIFactory:
        """Get UI factory for theme"""
        factories = {
            UITheme.LIGHT: LightThemeFactory,
            UITheme.DARK: DarkThemeFactory,
            UITheme.HIGH_CONTRAST: HighContrastThemeFactory,
        }
        
        factory_class = factories.get(theme)
        if not factory_class:
            raise ValueError(f"Unsupported theme: {theme}")
        
        return factory_class()

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_factory_interview():
    """
    🎯 INTERVIEW DEMO: Factory Patterns
    Demonstrates Simple Factory, Factory Method, and Abstract Factory
    """
    print("\n" + "="*60)
    print("🚀 FACTORY PATTERNS - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to create objects without knowing their exact classes?")
    print("2. What's the difference between Simple Factory, Factory Method, and Abstract Factory?")
    print("3. How to add new product types without modifying existing code?")
    print("4. How to create families of related objects?")
    
    # ========================================================================
    # SIMPLE FACTORY DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🏭 SIMPLE FACTORY PATTERN DEMO")
    print("="*50)
    
    print("\n💳 Processing payments with Simple Factory:")
    
    # Process different payment methods
    payment_methods = [
        (PaymentMethod.CREDIT_CARD, "user123"),
        (PaymentMethod.PAYPAL, "user456"),
        (PaymentMethod.CRYPTOCURRENCY, "user789")
    ]
    
    for method, account_id in payment_methods:
        try:
            processor = PaymentProcessorFactory.create_processor(method, account_id)
            result = processor.process_payment(100.0, "USD")
            print(f"✅ Payment successful: {result['id']} via {result['processor']}")
        except ValueError as e:
            print(f"❌ Payment failed: {e}")
    
    # ========================================================================
    # FACTORY METHOD DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🏭 FACTORY METHOD PATTERN DEMO")
    print("="*50)
    
    print("\n📄 Creating documents with Factory Method:")
    
    # Create different document types
    creators = [
        (PDFDocumentCreator(), "Report", "This is a PDF report content", "report.pdf"),
        (WordDocumentCreator(), "Letter", "This is a Word document content", "letter.docx"),
        (TextDocumentCreator(), "Notes", "This is plain text content", "notes.txt")
    ]
    
    for creator, title, content, filename in creators:
        try:
            success = creator.create_and_save_document(title, content, filename)
            if success:
                document = creator.create_document(title, content)
                print(f"✅ Document created: {filename} ({document.get_mime_type()})")
        except Exception as e:
            print(f"❌ Document creation failed: {e}")
    
    # ========================================================================
    # ABSTRACT FACTORY DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🏭 ABSTRACT FACTORY PATTERN DEMO")
    print("="*50)
    
    print("\n🎨 Creating UI components with Abstract Factory:")
    
    # Create UI components for different themes
    themes = [UITheme.LIGHT, UITheme.DARK, UITheme.HIGH_CONTRAST]
    
    for theme in themes:
        print(f"\n🎨 Creating {theme.value} theme components:")
        
        try:
            factory = UIFactoryProvider.get_factory(theme)
            
            # Create components
            button = factory.create_button("Submit")
            text_field = factory.create_text_field("Enter your name")
            text_field.set_value("John Doe")
            
            # Render components
            print(f"   {button.render()}")
            print(f"   {text_field.render()}")
            print(f"   Theme: {factory.get_theme_name()}")
            
        except ValueError as e:
            print(f"❌ Theme creation failed: {e}")
    
    # ========================================================================
    # FACTORY PATTERNS COMPARISON
    # ========================================================================
    print("\n" + "="*50)
    print("📊 FACTORY PATTERNS COMPARISON")
    print("="*50)
    
    print("\n🔍 Pattern Comparison:")
    print("┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("│ Pattern         │ Complexity      │ Flexibility     │ Use Case        │")
    print("├─────────────────┼─────────────────┼─────────────────┼─────────────────┤")
    print("│ Simple Factory  │ Low             │ Low             │ Single product  │")
    print("│ Factory Method  │ Medium          │ High            │ Product family  │")
    print("│ Abstract Factory│ High            │ Very High       │ Product families│")
    print("└─────────────────┴─────────────────┴─────────────────┴─────────────────┘")
    
    print("\n🎯 When to Use Each Pattern:")
    print("   1. 🏭 Simple Factory:")
    print("      - Single product type with multiple implementations")
    print("      - Simple object creation logic")
    print("      - Configuration-driven creation")
    print("      - Example: Payment processors, database connections")
    
    print("\n   2. 🏭 Factory Method:")
    print("      - Product family with common interface")
    print("      - Need to defer instantiation to subclasses")
    print("      - Framework/library design")
    print("      - Example: Document creators, logger factories")
    
    print("\n   3. 🏭 Abstract Factory:")
    print("      - Multiple related product families")
    print("      - Need to ensure products work together")
    print("      - Platform-specific implementations")
    print("      - Example: UI themes, database providers")
    
    # ========================================================================
    # EXTENSIBILITY DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🔧 EXTENSIBILITY DEMO")
    print("="*50)
    
    print("\n💡 Adding new payment method (Simple Factory):")
    print("   1. Create new processor class")
    print("   2. Add to factory mapping")
    print("   3. No changes to existing code")
    
    print("\n💡 Adding new document type (Factory Method):")
    print("   1. Create new document class")
    print("   2. Create new document creator")
    print("   3. No changes to existing code")
    
    print("\n💡 Adding new UI theme (Abstract Factory):")
    print("   1. Create new component classes")
    print("   2. Create new theme factory")
    print("   3. Add to factory provider")
    print("   4. No changes to existing code")
    
    # ========================================================================
    # REAL-WORLD EXAMPLES
    # ========================================================================
    print("\n" + "="*50)
    print("🌍 REAL-WORLD EXAMPLES")
    print("="*50)
    
    print("\n📚 Common Factory Pattern Examples:")
    print("   🏭 Simple Factory:")
    print("      - java.util.Calendar.getInstance()")
    print("      - Spring BeanFactory")
    print("      - Database connection factories")
    
    print("\n   🏭 Factory Method:")
    print("      - java.util.Collections.unmodifiableList()")
    print("      - React.createElement()")
    print("      - Logger factories (Log4j, SLF4J)")
    
    print("\n   🏭 Abstract Factory:")
    print("      - javax.xml.parsers.DocumentBuilderFactory")
    print("      - GUI toolkit factories (Swing, JavaFX)")
    print("      - Database provider factories")
    
    # ========================================================================
    # ERROR HANDLING DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("⚠️ ERROR HANDLING DEMO")
    print("="*50)
    
    print("\n🧪 Testing error scenarios:")
    
    # Test unsupported payment method
    print("\nTesting unsupported payment method:")
    try:
        # This would fail if we had an unsupported method
        processor = PaymentProcessorFactory.create_processor(PaymentMethod.BANK_TRANSFER, "user123")
    except ValueError as e:
        print(f"❌ Expected error: {e}")
    
    # Test unsupported UI theme
    print("\nTesting unsupported UI theme:")
    try:
        # This would fail if we had an unsupported theme
        factory = UIFactoryProvider.get_factory(UITheme.LIGHT)  # This should work
        print("✅ Light theme factory created successfully")
    except ValueError as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    demo_factory_interview()
