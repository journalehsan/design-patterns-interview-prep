// Singleton Pattern Demo
use std::sync::{Mutex, Once, Arc};
use std::collections::VecDeque;
use std::time::SystemTime;

#[derive(Debug)]
pub struct LogEntry {
    timestamp: SystemTime,
    level: LogLevel,
    message: String,
}

#[derive(Debug, Clone, Copy)]
pub enum LogLevel {
    Info,
    Warning,
    Error,
    Debug,
}

impl std::fmt::Display for LogLevel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LogLevel::Info => write!(f, "INFO"),
            LogLevel::Warning => write!(f, "WARN"),
            LogLevel::Error => write!(f, "ERROR"),
            LogLevel::Debug => write!(f, "DEBUG"),
        }
    }
}

pub struct Logger {
    logs: VecDeque<LogEntry>,
    max_logs: usize,
}

impl Logger {
    pub fn get_instance() -> Arc<Mutex<Logger>> {
        static INIT: Once = Once::new();
        static mut INSTANCE: Option<Arc<Mutex<Logger>>> = None;
        
        unsafe {
            INIT.call_once(|| {
                INSTANCE = Some(Arc::new(Mutex::new(Logger {
                    logs: VecDeque::new(),
                    max_logs: 1000,
                })));
            });
            INSTANCE.as_ref().unwrap().clone()
        }
    }
    
    pub fn log(&mut self, level: LogLevel, message: &str) {
        let entry = LogEntry {
            timestamp: SystemTime::now(),
            level,
            message: message.to_string(),
        };
        
        self.logs.push_back(entry);
        
        while self.logs.len() > self.max_logs {
            self.logs.pop_front();
        }
        
        println!("[{}] {}", level, message);
    }
    
    pub fn info(&mut self, message: &str) {
        self.log(LogLevel::Info, message);
    }
    
    pub fn warning(&mut self, message: &str) {
        self.log(LogLevel::Warning, message);
    }
    
    pub fn error(&mut self, message: &str) {
        self.log(LogLevel::Error, message);
    }
    
    pub fn debug(&mut self, message: &str) {
        self.log(LogLevel::Debug, message);
    }
    
    pub fn get_recent_logs(&self, count: usize) -> Vec<&LogEntry> {
        self.logs.iter().rev().take(count).collect()
    }
}

pub fn demo_singleton() {
    println!("🔒 SINGLETON PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern ensures only one instance exists.");
    println!("Rust Benefit: Arc<Mutex<T>> for thread safety.");
    
    println!("\n📝 Example 1: Thread-safe logging");
    let logger = Logger::get_instance();
    
    {
        let mut logger = logger.lock().unwrap();
        logger.info("Application started");
        logger.warning("This is a warning message");
        logger.error("An error occurred");
        logger.debug("Debug information");
    }
    
    println!("\n📝 Example 2: Getting singleton multiple times");
    let logger1 = Logger::get_instance();
    let logger2 = Logger::get_instance();
    
    // Both should be the same instance
    {
        logger1.lock().unwrap().info("Log from instance 1");
        logger2.lock().unwrap().info("Log from instance 2");
    }
    
    println!("\n💡 Interview Points:");
    println!("   • Thread safety with Arc<Mutex<T>>");
    println!("   • Static initialization with Once");
    println!("   • No null pointer dereferences");
    println!("   • Compile-time guarantees");
}
