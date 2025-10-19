'''
🚀 VISITOR PATTERN - INTERVIEW FOCUSED 🚀

The Visitor Pattern represents an operation to be performed on elements of an
object structure. It lets you define new operations without changing the classes
of the elements on which it operates.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to add new operations to existing classes without modifying them?"
2. "How to implement type-safe operations on heterogeneous object collections?"
3. "How to separate algorithms from object structure?"
4. "How to implement double dispatch in single-dispatch languages?"

💡 KEY INTERVIEW POINTS:
- Double dispatch mechanism
- Type-safe operations on object hierarchies
- Separation of algorithms from structure
- Extensibility without modification
'''

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
import json
from datetime import datetime

# ============================================================================
# ELEMENT INTERFACE AND CONCRETE ELEMENTS
# ============================================================================

class DocumentElement(ABC):
    """Abstract base class for document elements"""
    @abstractmethod
    def accept(self, visitor: 'DocumentVisitor'):
        """Accept a visitor"""
        pass
    
    @abstractmethod
    def get_content(self) -> str:
        """Get element content"""
        pass

class TextElement(DocumentElement):
    """Text element in document"""
    def __init__(self, text: str, font_size: int = 12, is_bold: bool = False):
        self.text = text
        self.font_size = font_size
        self.is_bold = is_bold
    
    def accept(self, visitor: 'DocumentVisitor'):
        visitor.visit_text(self)
    
    def get_content(self) -> str:
        return self.text
    
    def get_word_count(self) -> int:
        return len(self.text.split())
    
    def get_character_count(self) -> int:
        return len(self.text)

class ImageElement(DocumentElement):
    """Image element in document"""
    def __init__(self, filename: str, width: int, height: int, alt_text: str = ""):
        self.filename = filename
        self.width = width
        self.height = height
        self.alt_text = alt_text
    
    def accept(self, visitor: 'DocumentVisitor'):
        visitor.visit_image(self)
    
    def get_content(self) -> str:
        return f"Image: {self.filename}"
    
    def get_file_size(self) -> int:
        # Simulate file size calculation
        return self.width * self.height * 3  # RGB bytes
    
    def get_aspect_ratio(self) -> float:
        return self.width / self.height if self.height > 0 else 0

class TableElement(DocumentElement):
    """Table element in document"""
    def __init__(self, rows: int, cols: int, data: List[List[str]] = None):
        self.rows = rows
        self.cols = cols
        self.data = data or [["" for _ in range(cols)] for _ in range(rows)]
    
    def accept(self, visitor: 'DocumentVisitor'):
        visitor.visit_table(self)
    
    def get_content(self) -> str:
        return f"Table: {self.rows}x{self.cols}"
    
    def get_cell_count(self) -> int:
        return self.rows * self.cols
    
    def get_non_empty_cells(self) -> int:
        return sum(1 for row in self.data for cell in row if cell.strip())
    
    def set_cell(self, row: int, col: int, value: str):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = value

class LinkElement(DocumentElement):
    """Link element in document"""
    def __init__(self, text: str, url: str, is_external: bool = False):
        self.text = text
        self.url = url
        self.is_external = is_external
    
    def accept(self, visitor: 'DocumentVisitor'):
        visitor.visit_link(self)
    
    def get_content(self) -> str:
        return f"Link: {self.text} -> {self.url}"
    
    def is_valid_url(self) -> bool:
        return self.url.startswith(('http://', 'https://', 'mailto:', '/'))

# ============================================================================
# VISITOR INTERFACE AND CONCRETE VISITORS
# ============================================================================

class DocumentVisitor(ABC):
    """Abstract visitor interface"""
    @abstractmethod
    def visit_text(self, element: TextElement):
        pass
    
    @abstractmethod
    def visit_image(self, element: ImageElement):
        pass
    
    @abstractmethod
    def visit_table(self, element: TableElement):
        pass
    
    @abstractmethod
    def visit_link(self, element: LinkElement):
        pass

class WordCountVisitor(DocumentVisitor):
    """Visitor that counts words in document"""
    def __init__(self):
        self.total_words = 0
        self.text_elements = 0
        self.images = 0
        self.tables = 0
        self.links = 0
    
    def visit_text(self, element: TextElement):
        self.text_elements += 1
        self.total_words += element.get_word_count()
        print(f"📝 Text element: '{element.text[:30]}...' - {element.get_word_count()} words")
    
    def visit_image(self, element: ImageElement):
        self.images += 1
        print(f"🖼️ Image: {element.filename} - {element.get_file_size()} bytes")
    
    def visit_table(self, element: TableElement):
        self.tables += 1
        # Count words in table cells
        table_words = 0
        for row in element.data:
            for cell in row:
                table_words += len(cell.split())
        self.total_words += table_words
        print(f"📊 Table: {element.rows}x{element.cols} - {table_words} words in cells")
    
    def visit_link(self, element: LinkElement):
        self.links += 1
        self.total_words += element.get_word_count()
        print(f"🔗 Link: '{element.text}' -> {element.url}")
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            'total_words': self.total_words,
            'text_elements': self.text_elements,
            'images': self.images,
            'tables': self.tables,
            'links': self.links
        }

class ExportVisitor(DocumentVisitor):
    """Visitor that exports document to different formats"""
    def __init__(self, format_type: str = "json"):
        self.format_type = format_type
        self.export_data = {
            'document': {
                'elements': [],
                'metadata': {
                    'export_time': datetime.now().isoformat(),
                    'format': format_type
                }
            }
        }
    
    def visit_text(self, element: TextElement):
        element_data = {
            'type': 'text',
            'content': element.text,
            'font_size': element.font_size,
            'is_bold': element.is_bold,
            'word_count': element.get_word_count(),
            'character_count': element.get_character_count()
        }
        self.export_data['document']['elements'].append(element_data)
        print(f"📤 Exported text: '{element.text[:20]}...'")
    
    def visit_image(self, element: ImageElement):
        element_data = {
            'type': 'image',
            'filename': element.filename,
            'width': element.width,
            'height': element.height,
            'alt_text': element.alt_text,
            'file_size': element.get_file_size(),
            'aspect_ratio': element.get_aspect_ratio()
        }
        self.export_data['document']['elements'].append(element_data)
        print(f"📤 Exported image: {element.filename}")
    
    def visit_table(self, element: TableElement):
        element_data = {
            'type': 'table',
            'rows': element.rows,
            'cols': element.cols,
            'data': element.data,
            'cell_count': element.get_cell_count(),
            'non_empty_cells': element.get_non_empty_cells()
        }
        self.export_data['document']['elements'].append(element_data)
        print(f"📤 Exported table: {element.rows}x{element.cols}")
    
    def visit_link(self, element: LinkElement):
        element_data = {
            'type': 'link',
            'text': element.text,
            'url': element.url,
            'is_external': element.is_external,
            'is_valid': element.is_valid_url()
        }
        self.export_data['document']['elements'].append(element_data)
        print(f"📤 Exported link: {element.text} -> {element.url}")
    
    def get_export(self) -> str:
        """Get exported data in specified format"""
        if self.format_type == "json":
            return json.dumps(self.export_data, indent=2)
        elif self.format_type == "html":
            return self._export_to_html()
        elif self.format_type == "markdown":
            return self._export_to_markdown()
        else:
            return str(self.export_data)
    
    def _export_to_html(self) -> str:
        """Export to HTML format"""
        html = "<!DOCTYPE html>\n<html>\n<head><title>Document Export</title></head>\n<body>\n"
        
        for element in self.export_data['document']['elements']:
            if element['type'] == 'text':
                style = f"font-size: {element['font_size']}px;"
                if element['is_bold']:
                    style += " font-weight: bold;"
                html += f"<p style='{style}'>{element['content']}</p>\n"
            elif element['type'] == 'image':
                html += f"<img src='{element['filename']}' width='{element['width']}' height='{element['height']}' alt='{element['alt_text']}'>\n"
            elif element['type'] == 'table':
                html += "<table border='1'>\n"
                for row in element['data']:
                    html += "<tr>"
                    for cell in row:
                        html += f"<td>{cell}</td>"
                    html += "</tr>\n"
                html += "</table>\n"
            elif element['type'] == 'link':
                html += f"<a href='{element['url']}'>{element['text']}</a>\n"
        
        html += "</body>\n</html>"
        return html
    
    def _export_to_markdown(self) -> str:
        """Export to Markdown format"""
        markdown = "# Document Export\n\n"
        
        for element in self.export_data['document']['elements']:
            if element['type'] == 'text':
                if element['is_bold']:
                    markdown += f"**{element['content']}**\n\n"
                else:
                    markdown += f"{element['content']}\n\n"
            elif element['type'] == 'image':
                markdown += f"![{element['alt_text']}]({element['filename']})\n\n"
            elif element['type'] == 'table':
                markdown += "| " + " | ".join([f"Col {i+1}" for i in range(element['cols'])]) + " |\n"
                markdown += "| " + " | ".join(["---" for _ in range(element['cols'])]) + " |\n"
                for row in element['data']:
                    markdown += "| " + " | ".join(row) + " |\n"
                markdown += "\n"
            elif element['type'] == 'link':
                markdown += f"[{element['text']}]({element['url']})\n\n"
        
        return markdown

class ValidationVisitor(DocumentVisitor):
    """Visitor that validates document elements"""
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.valid_elements = 0
    
    def visit_text(self, element: TextElement):
        self.valid_elements += 1
        
        if not element.text.strip():
            self.warnings.append(f"Empty text element found")
        
        if element.font_size < 8 or element.font_size > 72:
            self.warnings.append(f"Text element has unusual font size: {element.font_size}")
        
        if len(element.text) > 1000:
            self.warnings.append(f"Text element is very long: {len(element.text)} characters")
        
        print(f"✅ Validated text element: {len(element.text)} characters")
    
    def visit_image(self, element: ImageElement):
        self.valid_elements += 1
        
        if not element.filename:
            self.errors.append("Image element missing filename")
            return
        
        if element.width <= 0 or element.height <= 0:
            self.errors.append(f"Image has invalid dimensions: {element.width}x{element.height}")
        
        if not element.alt_text:
            self.warnings.append(f"Image '{element.filename}' missing alt text")
        
        if element.get_file_size() > 10 * 1024 * 1024:  # 10MB
            self.warnings.append(f"Image '{element.filename}' is very large: {element.get_file_size()} bytes")
        
        print(f"✅ Validated image: {element.filename} ({element.width}x{element.height})")
    
    def visit_table(self, element: TableElement):
        self.valid_elements += 1
        
        if element.rows <= 0 or element.cols <= 0:
            self.errors.append(f"Table has invalid dimensions: {element.rows}x{element.cols}")
            return
        
        if element.get_non_empty_cells() == 0:
            self.warnings.append("Table is completely empty")
        
        # Check for inconsistent row lengths
        for i, row in enumerate(element.data):
            if len(row) != element.cols:
                self.errors.append(f"Table row {i} has {len(row)} cells, expected {element.cols}")
        
        print(f"✅ Validated table: {element.rows}x{element.cols} with {element.get_non_empty_cells()} filled cells")
    
    def visit_link(self, element: LinkElement):
        self.valid_elements += 1
        
        if not element.text.strip():
            self.errors.append("Link element missing text")
        
        if not element.url.strip():
            self.errors.append("Link element missing URL")
        elif not element.is_valid_url():
            self.warnings.append(f"Link has potentially invalid URL: {element.url}")
        
        if element.is_external and not element.url.startswith(('http://', 'https://')):
            self.warnings.append(f"External link should use http/https: {element.url}")
        
        print(f"✅ Validated link: '{element.text}' -> {element.url}")
    
    def get_validation_report(self) -> Dict[str, Any]:
        return {
            'valid_elements': self.valid_elements,
            'errors': self.errors,
            'warnings': self.warnings,
            'is_valid': len(self.errors) == 0,
            'has_warnings': len(self.warnings) > 0
        }

# ============================================================================
# DOCUMENT STRUCTURE
# ============================================================================

class Document:
    """Document containing various elements"""
    def __init__(self, title: str):
        self.title = title
        self.elements: List[DocumentElement] = []
    
    def add_element(self, element: DocumentElement):
        """Add element to document"""
        self.elements.append(element)
        print(f"📄 Added {element.__class__.__name__} to document")
    
    def accept_visitor(self, visitor: DocumentVisitor):
        """Accept a visitor to process all elements"""
        print(f"\n🔍 Processing document '{self.title}' with {visitor.__class__.__name__}")
        for element in self.elements:
            element.accept(visitor)
        print("✅ Document processing completed")

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_visitor_interview():
    """
    🎯 INTERVIEW DEMO: Visitor Pattern
    Demonstrates operations on heterogeneous object structures
    """
    print("\n" + "="*60)
    print("🚀 VISITOR PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to add new operations to existing classes without modifying them?")
    print("2. How to implement type-safe operations on heterogeneous collections?")
    print("3. How to separate algorithms from object structure?")
    print("4. How to implement double dispatch in single-dispatch languages?")
    
    # ========================================================================
    # DOCUMENT CREATION DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📄 DOCUMENT CREATION DEMO")
    print("="*50)
    
    # Create a document with various elements
    doc = Document("Design Patterns Interview Guide")
    
    # Add text elements
    doc.add_element(TextElement("Design Patterns Interview Prep", font_size=18, is_bold=True))
    doc.add_element(TextElement("This guide covers essential design patterns for technical interviews."))
    doc.add_element(TextElement("Each pattern includes real-world examples and common interview questions."))
    
    # Add image element
    doc.add_element(ImageElement("patterns-diagram.png", 800, 600, "Design patterns overview"))
    
    # Add table element
    table = TableElement(3, 3)
    table.set_cell(0, 0, "Pattern")
    table.set_cell(0, 1, "Type")
    table.set_cell(0, 2, "Use Case")
    table.set_cell(1, 0, "Observer")
    table.set_cell(1, 1, "Behavioral")
    table.set_cell(1, 2, "Event handling")
    table.set_cell(2, 0, "Strategy")
    table.set_cell(2, 1, "Behavioral")
    table.set_cell(2, 2, "Algorithm selection")
    doc.add_element(table)
    
    # Add link elements
    doc.add_element(LinkElement("Gang of Four Book", "https://en.wikipedia.org/wiki/Design_Patterns", True))
    doc.add_element(LinkElement("Local Examples", "/examples", False))
    
    print(f"\n📊 Document created with {len(doc.elements)} elements")
    
    # ========================================================================
    # WORD COUNT VISITOR DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📊 WORD COUNT VISITOR DEMO")
    print("="*50)
    
    word_visitor = WordCountVisitor()
    doc.accept_visitor(word_visitor)
    
    summary = word_visitor.get_summary()
    print(f"\n📈 Word Count Summary:")
    print(f"   Total words: {summary['total_words']}")
    print(f"   Text elements: {summary['text_elements']}")
    print(f"   Images: {summary['images']}")
    print(f"   Tables: {summary['tables']}")
    print(f"   Links: {summary['links']}")
    
    # ========================================================================
    # EXPORT VISITOR DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📤 EXPORT VISITOR DEMO")
    print("="*50)
    
    # JSON Export
    print("\n🔄 Exporting to JSON format:")
    json_visitor = ExportVisitor("json")
    doc.accept_visitor(json_visitor)
    json_export = json_visitor.get_export()
    print(f"📄 JSON Export (first 200 chars):\n{json_export[:200]}...")
    
    # HTML Export
    print("\n🔄 Exporting to HTML format:")
    html_visitor = ExportVisitor("html")
    doc.accept_visitor(html_visitor)
    html_export = html_visitor.get_export()
    print(f"📄 HTML Export (first 300 chars):\n{html_export[:300]}...")
    
    # Markdown Export
    print("\n🔄 Exporting to Markdown format:")
    md_visitor = ExportVisitor("markdown")
    doc.accept_visitor(md_visitor)
    md_export = md_visitor.get_export()
    print(f"📄 Markdown Export:\n{md_export}")
    
    # ========================================================================
    # VALIDATION VISITOR DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("✅ VALIDATION VISITOR DEMO")
    print("="*50)
    
    # Create a document with some issues for validation
    test_doc = Document("Test Document with Issues")
    
    # Add problematic elements
    test_doc.add_element(TextElement(""))  # Empty text
    test_doc.add_element(TextElement("A" * 1500))  # Very long text
    test_doc.add_element(ImageElement("", 0, 0))  # Invalid image
    test_doc.add_element(ImageElement("large-image.jpg", 4000, 3000))  # Large image
    test_doc.add_element(LinkElement("", "invalid-url"))  # Empty link text
    test_doc.add_element(LinkElement("Valid Link", "https://example.com"))  # Valid link
    
    print("\n🔍 Validating document with issues:")
    validation_visitor = ValidationVisitor()
    test_doc.accept_visitor(validation_visitor)
    
    report = validation_visitor.get_validation_report()
    print(f"\n📋 Validation Report:")
    print(f"   Valid elements: {report['valid_elements']}")
    print(f"   Errors: {len(report['errors'])}")
    print(f"   Warnings: {len(report['warnings'])}")
    print(f"   Document is valid: {report['is_valid']}")
    print(f"   Has warnings: {report['has_warnings']}")
    
    if report['errors']:
        print(f"\n❌ Errors:")
        for error in report['errors']:
            print(f"   - {error}")
    
    if report['warnings']:
        print(f"\n⚠️ Warnings:")
        for warning in report['warnings']:
            print(f"   - {warning}")
    
    # ========================================================================
    # VISITOR PATTERN BENEFITS DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("💡 VISITOR PATTERN BENEFITS")
    print("="*50)
    
    print("\n🎯 Key Benefits:")
    print("   1. ✅ Open/Closed Principle - Open for extension, closed for modification")
    print("   2. ✅ Single Responsibility - Each visitor handles one type of operation")
    print("   3. ✅ Type Safety - Compile-time type checking for operations")
    print("   4. ✅ Extensibility - Easy to add new operations without changing existing code")
    print("   5. ✅ Separation of Concerns - Algorithms separated from object structure")
    
    print("\n🔄 Double Dispatch Mechanism:")
    print("   1. Client calls element.accept(visitor)")
    print("   2. Element calls visitor.visit_element_type(self)")
    print("   3. Visitor performs operation on specific element type")
    print("   4. This enables type-safe operations on heterogeneous collections")
    
    print("\n⚠️ Trade-offs:")
    print("   - Adds complexity to the codebase")
    print("   - Requires modifying element classes to add accept() method")
    print("   - Can make the code harder to understand for beginners")
    print("   - May not be suitable for simple, homogeneous collections")

if __name__ == "__main__":
    demo_visitor_interview()
