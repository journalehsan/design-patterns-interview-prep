// Template Method Pattern Demo

pub trait DataProcessor {
    fn process(&self) {
        println!("📊 Data Processing Pipeline");
        println!("{}", "=".repeat(40));
        self.load_data();
        self.validate_data();
        self.transform_data();
        self.save_data();
        println!("{}", "=".repeat(40));
        println!("✅ Processing complete!");
    }
  
    fn load_data(&self);
    fn validate_data(&self);
    fn transform_data(&self);
    fn save_data(&self);
}

pub struct CSVProcessor;

impl DataProcessor for CSVProcessor {
    fn load_data(&self) {
        println!("📁 Loading CSV data...");
    }
  
    fn validate_data(&self) {
        println!("✓ Validating CSV format...");
    }
  
    fn transform_data(&self) {
        println!("🔄 Transforming CSV data...");
    }
  
    fn save_data(&self) {
        println!("💾 Saving processed CSV data...");
    }
}

pub struct JSONProcessor;

impl DataProcessor for JSONProcessor {
    fn load_data(&self) {
        println!("📁 Loading JSON data...");
    }
  
    fn validate_data(&self) {
        println!("✓ Validating JSON format...");
    }
  
    fn transform_data(&self) {
        println!("🔄 Transforming JSON data...");
    }
  
    fn save_data(&self) {
        println!("💾 Saving processed JSON data...");
    }
}

pub fn demo_template_method() {
    println!("📋 TEMPLATE METHOD PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern defines algorithm skeleton with customizable steps.");
    println!("Rust Benefit: Trait default implementations.");
    
    println!("\n📝 Example 1: CSV processing");
    let csv_processor = CSVProcessor;
    csv_processor.process();
    
    println!("\n📝 Example 2: JSON processing");
    let json_processor = JSONProcessor;
    json_processor.process();
    
    println!("\n💡 Interview Points:");
    println!("   • Define algorithm structure in base trait");
    println!("   • Subclasses provide specific implementations");
    println!("   • Reduce code duplication");
    println!("   • Hollywood Principle (Don't call us, we'll call you)");
}
