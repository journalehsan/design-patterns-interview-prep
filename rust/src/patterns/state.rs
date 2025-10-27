// State Pattern Demo

pub enum State {
    Idle,
    Active,
    Processing,
}

pub struct Context {
    state: State,
}

impl Context {
    pub fn new() -> Self {
        Context {
            state: State::Idle,
        }
    }
  
    pub fn set_state(&mut self, state: State) {
        self.state = state;
    }
  
    pub fn request(&mut self) -> String {
        match self.state {
            State::Idle => {
                println!("Current state: Idle");
                println!("Transitioning to Active...");
                self.set_state(State::Active);
                "Idle → Active".to_string()
            }
            State::Active => {
                println!("Current state: Active");
                println!("Transitioning to Processing...");
                self.set_state(State::Processing);
                "Active → Processing".to_string()
            }
            State::Processing => {
                println!("Current state: Processing");
                println!("Transitioning back to Idle...");
                self.set_state(State::Idle);
                "Processing → Idle".to_string()
            }
        }
    }
}

pub fn demo_state() {
    println!("🔄 STATE PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern allows object behavior to change with state.");
    println!("Rust Benefit: State machine with type safety.");
    
    println!("\n📝 Example 1: Simple state machine");
    let mut context = Context::new();
    
    println!("\nRequest 1:");
    println!("{}", context.request());
    
    println!("\nRequest 2:");
    println!("{}", context.request());
    
    println!("\nRequest 3:");
    println!("{}", context.request());
    
    println!("\nRequest 4:");
    println!("{}", context.request());
    
    println!("\n💡 Interview Points:");
    println!("   • Behavior depends on internal state");
    println!("   • Encapsulate state transitions");
    println!("   • Avoid large if/else chains");
    println!("   • Use case: game entities, workflow engines");
}
