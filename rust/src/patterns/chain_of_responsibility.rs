// Chain of Responsibility Pattern Demo

pub trait Handler {
    fn set_next(&mut self, next: Box<dyn Handler>);
    fn handle(&self, request: &Request) -> Option<String>;
}

pub struct Request {
    pub amount: u32,
    pub description: String,
}

impl Request {
    pub fn new(amount: u32, description: &str) -> Self {
        Request {
            amount,
            description: description.to_string(),
        }
    }
}

pub struct ManagerHandler {
    next: Option<Box<dyn Handler>>,
}

impl ManagerHandler {
    pub fn new() -> Self {
        ManagerHandler { next: None }
    }
}

impl Handler for ManagerHandler {
    fn set_next(&mut self, next: Box<dyn Handler>) {
        self.next = Some(next);
    }
  
    fn handle(&self, request: &Request) -> Option<String> {
        if request.amount <= 1000 {
            Some(format!("✅ Manager approved: {}", request.description))
        } else {
            self.next.as_ref()?.handle(request)
        }
    }
}

pub struct DirectorHandler {
    next: Option<Box<dyn Handler>>,
}

impl DirectorHandler {
    pub fn new() -> Self {
        DirectorHandler { next: None }
    }
}

impl Handler for DirectorHandler {
    fn set_next(&mut self, next: Box<dyn Handler>) {
        self.next = Some(next);
    }
  
    fn handle(&self, request: &Request) -> Option<String> {
        if request.amount <= 10000 {
            Some(format!("✅ Director approved: {}", request.description))
        } else {
            self.next.as_ref()?.handle(request)
        }
    }
}

pub struct CEOHandler;

impl CEOHandler {
    pub fn new() -> Self {
        CEOHandler
    }
}

impl Handler for CEOHandler {
    fn set_next(&mut self, _next: Box<dyn Handler>) {
        // CEO is the last in chain
    }
  
    fn handle(&self, request: &Request) -> Option<String> {
        if request.amount <= 100000 {
            Some(format!("✅ CEO approved: {}", request.description))
        } else {
            Some(format!("❌ Request rejected: amount too large"))
        }
    }
}

pub fn demo_chain_of_responsibility() {
    println!("🔗 CHAIN OF RESPONSIBILITY DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern passes requests along a chain of handlers.");
    println!("Rust Benefit: Dynamic dispatch with trait objects.");
    
    println!("\n📝 Example 1: Approval chain");
    
    let mut manager = ManagerHandler::new();
    let director = DirectorHandler::new();
    let _ceo = CEOHandler::new();
    
    manager.set_next(Box::new(director));
    
    // This will need to be implemented differently due to ownership
    let requests = vec![
        Request::new(500, "Office supplies"),
        Request::new(5000, "Equipment upgrade"),
        Request::new(50000, "Infrastructure project"),
        Request::new(200000, "Acquisition"),
    ];
    
    println!("Processing requests through approval chain:");
    for request in &requests {
        println!("\nRequest: {} - ${}", request.description, request.amount);
        if let Some(result) = manager.handle(request) {
            println!("Result: {}", result);
        }
    }
    
    println!("\n💡 Interview Points:");
    println!("   • Avoid coupling sender and receiver");
    println!("   • Chain processing requests");
    println!("   • Multiple handlers process request");
    println!("   • Use case: middleware, filters, validators");
}
