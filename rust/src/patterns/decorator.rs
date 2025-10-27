// Decorator Pattern Demo

pub trait Coffee {
    fn cost(&self) -> f64;
    fn description(&self) -> String;
}

pub struct SimpleCoffee;

impl Coffee for SimpleCoffee {
    fn cost(&self) -> f64 { 2.0 }
    fn description(&self) -> String { "Simple coffee".to_string() }
}

pub struct MilkDecorator {
    coffee: Box<dyn Coffee>,
}

impl MilkDecorator {
    pub fn new(coffee: Box<dyn Coffee>) -> Self {
        MilkDecorator { coffee }
    }
}

impl Coffee for MilkDecorator {
    fn cost(&self) -> f64 {
        self.coffee.cost() + 0.5
    }
  
    fn description(&self) -> String {
        format!("{}, milk", self.coffee.description())
    }
}

pub struct SugarDecorator {
    coffee: Box<dyn Coffee>,
}

impl SugarDecorator {
    pub fn new(coffee: Box<dyn Coffee>) -> Self {
        SugarDecorator { coffee }
    }
}

impl Coffee for SugarDecorator {
    fn cost(&self) -> f64 {
        self.coffee.cost() + 0.2
    }
  
    fn description(&self) -> String {
        format!("{}, sugar", self.coffee.description())
    }
}

pub fn demo_decorator() {
    println!("🎨 DECORATOR PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern adds behavior to objects dynamically.");
    println!("Rust Benefit: Trait objects for composition.");
    
    println!("\n📝 Example 1: Building coffee with decorators");
    
    let simple_coffee = Box::new(SimpleCoffee);
    println!("{} - ${:.2}", simple_coffee.description(), simple_coffee.cost());
    
    let coffee_with_milk = MilkDecorator::new(simple_coffee);
    println!("{} - ${:.2}", coffee_with_milk.description(), coffee_with_milk.cost());
    
    println!("\n📝 Example 2: Multiple decorators");
    let simple = Box::new(SimpleCoffee);
    let with_milk = MilkDecorator::new(simple);
    let with_sugar = SugarDecorator::new(Box::new(with_milk));
    
    println!("{} - ${:.2}", with_sugar.description(), with_sugar.cost());
    
    println!("\n💡 Interview Points:");
    println!("   • Add behavior without modifying existing code");
    println!("   • Compose objects dynamically");
    println!("   • Open/Closed Principle");
    println!("   • Alternative to subclassing");
}
