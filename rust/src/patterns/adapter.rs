// Adapter Pattern Demo

// Legacy system
pub struct OldPrinter {
    text: String,
}

impl OldPrinter {
    pub fn new(text: &str) -> Self {
        OldPrinter {
            text: text.to_string(),
        }
    }
    
    pub fn print_old_format(&self) -> String {
        format!("OLD: {}", self.text)
    }
}

// New interface
pub trait ModernPrinter {
    fn print(&self) -> String;
}

// Adapter
pub struct PrinterAdapter {
    old_printer: OldPrinter,
}

impl PrinterAdapter {
    pub fn new(text: &str) -> Self {
        PrinterAdapter {
            old_printer: OldPrinter::new(text),
        }
    }
}

impl ModernPrinter for PrinterAdapter {
    fn print(&self) -> String {
        self.old_printer.print_old_format().replace("OLD: ", "")
    }
}

// Modern implementation
pub struct ModernPrinterImpl {
    text: String,
}

impl ModernPrinterImpl {
    pub fn new(text: &str) -> Self {
        ModernPrinterImpl {
            text: text.to_string(),
        }
    }
}

impl ModernPrinter for ModernPrinterImpl {
    fn print(&self) -> String {
        format!("MODERN: {}", self.text)
    }
}

pub fn demo_adapter() {
    println!("🔌 ADAPTER PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern makes incompatible interfaces work together.");
    println!("Rust Benefit: Type safety for interface conversion.");
    
    println!("\n📝 Example 1: Adapter for legacy system");
    let adapter = PrinterAdapter::new("Hello from legacy system!");
    println!("{}", adapter.print());
    
    println!("\n📝 Example 2: Modern implementation");
    let modern_printer = ModernPrinterImpl::new("Hello from modern system!");
    println!("{}", modern_printer.print());
    
    println!("\n📝 Example 3: Using both through trait");
    let printers: Vec<Box<dyn ModernPrinter>> = vec![
        Box::new(PrinterAdapter::new("Adapted legacy printer")),
        Box::new(ModernPrinterImpl::new("Modern printer")),
    ];
    
    for printer in printers {
        println!("{}", printer.print());
    }
    
    println!("\n💡 Interview Points:");
    println!("   • Make incompatible interfaces work together");
    println!("   • Reuse existing code");
    println!("   • Integrate with legacy systems");
    println!("   • Type-safe interface conversion");
}
