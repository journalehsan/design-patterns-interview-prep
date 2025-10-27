// Command Pattern Demo
use std::cell::RefCell;
use std::rc::Rc;

pub trait Command {
    fn execute(&self);
    fn undo(&self);
    fn name(&self) -> &str;
}

pub struct Light {
    is_on: bool,
}

impl Light {
    pub fn new() -> Self { 
        Light { is_on: false } 
    }
    
    pub fn turn_on(&mut self) { 
        self.is_on = true;
        println!("Light is now ON");
    }
    
    pub fn turn_off(&mut self) { 
        self.is_on = false;
        println!("Light is now OFF");
    }
}

pub struct TurnOnCommand {
    light: Rc<RefCell<Light>>,
}

impl TurnOnCommand {
    pub fn new(light: Rc<RefCell<Light>>) -> Self {
        TurnOnCommand { light }
    }
}

impl Command for TurnOnCommand {
    fn execute(&self) {
        self.light.borrow_mut().turn_on();
    }
  
    fn undo(&self) {
        self.light.borrow_mut().turn_off();
    }
    
    fn name(&self) -> &str {
        "Turn On"
    }
}

pub struct TurnOffCommand {
    light: Rc<RefCell<Light>>,
}

impl TurnOffCommand {
    pub fn new(light: Rc<RefCell<Light>>) -> Self {
        TurnOffCommand { light }
    }
}

impl Command for TurnOffCommand {
    fn execute(&self) {
        self.light.borrow_mut().turn_off();
    }
  
    fn undo(&self) {
        self.light.borrow_mut().turn_on();
    }
    
    fn name(&self) -> &str {
        "Turn Off"
    }
}

pub struct RemoteControl {
    commands: Vec<Box<dyn Command>>,
}

impl RemoteControl {
    pub fn new() -> Self {
        RemoteControl {
            commands: Vec::new(),
        }
    }
  
    pub fn add_command(&mut self, command: Box<dyn Command>) {
        println!("Added command: {}", command.name());
        self.commands.push(command);
    }
  
    pub fn execute_all(&self) {
        for command in &self.commands {
            command.execute();
        }
    }
    
    pub fn undo_all(&self) {
        for command in self.commands.iter().rev() {
            command.undo();
        }
    }
}

pub fn demo_command() {
    println!("📝 COMMAND PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern encapsulates requests as objects.");
    println!("Rust Benefit: Rc<RefCell<T>> for undo/redo functionality.");
    
    println!("\n📝 Example 1: Undo/Redo operations");
    let light = Rc::new(RefCell::new(Light::new()));
    
    let mut remote = RemoteControl::new();
    remote.add_command(Box::new(TurnOnCommand::new(light.clone())));
    remote.add_command(Box::new(TurnOffCommand::new(light.clone())));
    
    println!("\nExecuting all commands:");
    remote.execute_all();
    
    println!("\nUndoing all commands:");
    remote.undo_all();
    
    println!("\n💡 Interview Points:");
    println!("   • Encapsulate requests as objects");
    println!("   • Parameterize clients with different requests");
    println!("   • Undo/redo support");
    println!("   • Queue and log operations");
}
