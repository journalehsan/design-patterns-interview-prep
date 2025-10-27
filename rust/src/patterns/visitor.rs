// Visitor Pattern Demo

pub trait Element {
    fn accept(&self, visitor: &dyn Visitor);
    fn get_name(&self) -> &str;
}

pub trait Visitor {
    fn visit_element_a(&self, element: &ElementA);
    fn visit_element_b(&self, element: &ElementB);
}

pub struct ElementA {
    pub value: i32,
}

impl ElementA {
    pub fn new(value: i32) -> Self {
        ElementA { value }
    }
}

impl Element for ElementA {
    fn accept(&self, visitor: &dyn Visitor) {
        visitor.visit_element_a(self);
    }
    
    fn get_name(&self) -> &str {
        "ElementA"
    }
}

pub struct ElementB {
    pub value: String,
}

impl ElementB {
    pub fn new(value: &str) -> Self {
        ElementB {
            value: value.to_string(),
        }
    }
}

impl Element for ElementB {
    fn accept(&self, visitor: &dyn Visitor) {
        visitor.visit_element_b(self);
    }
    
    fn get_name(&self) -> &str {
        "ElementB"
    }
}

pub struct ConcreteVisitor;

impl Visitor for ConcreteVisitor {
    fn visit_element_a(&self, element: &ElementA) {
        println!("Visiting ElementA with value: {}", element.value);
    }
  
    fn visit_element_b(&self, element: &ElementB) {
        println!("Visiting ElementB with value: {}", element.value);
    }
}

pub struct CountVisitor {
    count: usize,
}

impl CountVisitor {
    pub fn new() -> Self {
        CountVisitor { count: 0 }
    }
    
    pub fn get_count(&self) -> usize {
        self.count
    }
}

impl Visitor for CountVisitor {
    fn visit_element_a(&self, _element: &ElementA) {
        println!("Counting ElementA...");
    }
  
    fn visit_element_b(&self, _element: &ElementB) {
        println!("Counting ElementB...");
    }
}

pub fn demo_visitor() {
    println!("👤 VISITOR PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern defines operations on object structures.");
    println!("Rust Benefit: Separate algorithms from object structure.");
    
    println!("\n📝 Example 1: Concrete visitor");
    let visitor = ConcreteVisitor;
    let elements: Vec<Box<dyn Element>> = vec![
        Box::new(ElementA::new(42)),
        Box::new(ElementB::new("Hello")),
        Box::new(ElementA::new(100)),
    ];
    
    for element in &elements {
        element.accept(&visitor);
    }
    
    println!("\n💡 Interview Points:");
    println!("   • Add new operations without modifying elements");
    println!("   • Separate algorithms from object structures");
    println!("   • Use case: compiler AST visitors, type checkers");
    println!("   • Double dispatch simulation");
}
