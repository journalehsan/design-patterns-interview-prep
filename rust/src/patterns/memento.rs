// Memento Pattern Demo

pub struct Memento {
    state: String,
}

impl Memento {
    pub fn new(state: &str) -> Self {
        Memento {
            state: state.to_string(),
        }
    }
  
    pub fn get_state(&self) -> &str {
        &self.state
    }
}

pub struct Originator {
    state: String,
}

impl Originator {
    pub fn new(state: &str) -> Self {
        Originator {
            state: state.to_string(),
        }
    }
  
    pub fn set_state(&mut self, state: &str) {
        self.state = state.to_string();
    }
  
    pub fn get_state(&self) -> &str {
        &self.state
    }
  
    pub fn create_memento(&self) -> Memento {
        Memento::new(&self.state)
    }
  
    pub fn restore_from_memento(&mut self, memento: &Memento) {
        self.state = memento.get_state().to_string();
    }
}

pub struct Caretaker {
    mementos: Vec<Memento>,
}

impl Caretaker {
    pub fn new() -> Self {
        Caretaker {
            mementos: Vec::new(),
        }
    }
  
    pub fn add_memento(&mut self, memento: Memento) {
        println!("📸 Save point created");
        self.mementos.push(memento);
    }
  
    pub fn get_memento(&self, index: usize) -> Option<&Memento> {
        self.mementos.get(index)
    }
    
    pub fn get_save_count(&self) -> usize {
        self.mementos.len()
    }
}

pub fn demo_memento() {
    println!("💾 MEMENTO PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern captures and restores object state.");
    println!("Rust Benefit: Safe state management with immutability.");
    
    println!("\n📝 Example 1: Game save/restore system");
    let mut game_state = Originator::new("Level 1 - Village");
    let mut caretaker = Caretaker::new();
    
    println!("Initial state: {}", game_state.get_state());
    
    // Save checkpoint 1
    caretaker.add_memento(game_state.create_memento());
    
    game_state.set_state("Level 2 - Forest");
    println!("New state: {}", game_state.get_state());
    
    // Save checkpoint 2
    caretaker.add_memento(game_state.create_memento());
    
    game_state.set_state("Level 3 - Castle");
    println!("New state: {}", game_state.get_state());
    
    println!("\nRestoring from checkpoint 1:");
    if let Some(memento) = caretaker.get_memento(0) {
        game_state.restore_from_memento(memento);
        println!("Restored state: {}", game_state.get_state());
    }
    
    println!("\n💡 Interview Points:");
    println!("   • Capture object state without violating encapsulation");
    println!("   • Undo/redo functionality");
    println!("   • Game save systems");
    println!("   • Transaction rollback");
}
