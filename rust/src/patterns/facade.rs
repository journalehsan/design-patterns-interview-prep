// Facade Pattern Demo

pub struct CPU {
    pub name: String,
}

impl CPU {
    pub fn start(&self) { 
        println!("CPU {} started", self.name); 
    }
    
    pub fn execute(&self) { 
        println!("CPU executing instructions"); 
    }
    
    pub fn stop(&self) { 
        println!("CPU stopped"); 
    }
}

pub struct Memory {
    pub size: u32,
}

impl Memory {
    pub fn load(&self) { 
        println!("Loading {}MB memory", self.size); 
    }
    
    pub fn unload(&self) { 
        println!("Unloading memory"); 
    }
}

pub struct HardDrive {
    pub capacity: u32,
}

impl HardDrive {
    pub fn read(&self) {
        println!("Reading from {}GB hard drive", self.capacity);
    }
    
    pub fn write(&self) {
        println!("Writing to {}GB hard drive", self.capacity);
    }
}

pub struct ComputerFacade {
    cpu: CPU,
    memory: Memory,
    hard_drive: HardDrive,
}

impl ComputerFacade {
    pub fn new() -> Self {
        ComputerFacade {
            cpu: CPU { name: "Intel i7".to_string() },
            memory: Memory { size: 8192 },
            hard_drive: HardDrive { capacity: 500 },
        }
    }
  
    pub fn start_computer(&self) {
        println!("Starting computer...");
        self.cpu.start();
        self.memory.load();
        self.hard_drive.read();
        self.cpu.execute();
        println!("Computer ready!\n");
    }
  
    pub fn shutdown_computer(&self) {
        println!("Shutting down computer...");
        self.cpu.stop();
        self.memory.unload();
        self.hard_drive.write();
        println!("Computer shut down.\n");
    }
}

pub fn demo_facade() {
    println!("🏛️  FACADE PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern provides a simplified interface to complex subsystems.");
    println!("Rust Benefit: Clean API hiding implementation complexity.");
    
    println!("\n📝 Example 1: Simplified computer operations");
    let computer = ComputerFacade::new();
    
    computer.start_computer();
    computer.shutdown_computer();
    
    println!("\n📝 Example 2: Direct access (without facade)");
    println!("Using components directly:");
    let cpu = CPU { name: "AMD Ryzen".to_string() };
    let memory = Memory { size: 16384 };
    let hard_drive = HardDrive { capacity: 1000 };
    
    println!("Low-level operations:");
    cpu.start();
    memory.load();
    hard_drive.read();
    
    println!("\n💡 Interview Points:");
    println!("   • Simplify complex subsystem interfaces");
    println!("   • Provide a unified API");
    println!("   • Hide implementation details");
    println!("   • Reduce coupling between client and subsystem");
}
