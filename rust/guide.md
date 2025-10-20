# **Rust Design Patterns Guide - 15 Essential Patterns**

A comprehensive guide to implementing classic design patterns in Rust, with focus on Rust's unique features like ownership, borrowing, and lifetimes.

## **Table of Contents**
1. [Introduction](#introduction)
2. [Creational Patterns](#creational-patterns)
3. [Structural Patterns](#structural-patterns)
4. [Behavioral Patterns](#behavioral-patterns)
5. [Rust-Specific Considerations](#rust-specific-considerations)
6. [Performance Analysis](#performance-analysis)
7. [Anti-patterns](#anti-patterns)

## **Introduction**

Design patterns are proven solutions to common programming problems. In Rust, these patterns must be adapted to work with the language's unique features:

- **Ownership System**: Ensures memory safety without garbage collection
- **Borrowing**: Allows multiple references with compile-time guarantees
- **Lifetimes**: Tracks how long references are valid
- **Trait System**: Provides polymorphism and code reuse
- **Zero-cost Abstractions**: High-level patterns with no runtime overhead

---

## **Creational Patterns**

Creational patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

### **1. Builder Pattern**

The Builder pattern provides a flexible solution to construct complex objects step by step. In Rust, it's commonly used with the `Result` type for validation.

```rust
#[derive(Debug, Clone)]
pub struct DatabaseConfig {
    pub host: String,
    pub port: u16,
    pub username: String,
    pub password: String,
    pub ssl: bool,
    pub connection_timeout: u64,
}

pub struct DatabaseConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    username: Option<String>,
    password: Option<String>,
    ssl: bool,
    connection_timeout: Option<u64>,
}

impl DatabaseConfigBuilder {
    pub fn new() -> Self {
        DatabaseConfigBuilder {
            host: None,
            port: None,
            username: None,
            password: None,
            ssl: false,
            connection_timeout: None,
        }
    }
    
    pub fn host(mut self, host: &str) -> Self {
        self.host = Some(host.to_string());
        self
    }
    
    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }
    
    pub fn username(mut self, username: &str) -> Self {
        self.username = Some(username.to_string());
        self
    }
    
    pub fn password(mut self, password: &str) -> Self {
        self.password = Some(password.to_string());
        self
    }
    
    pub fn ssl(mut self, ssl: bool) -> Self {
        self.ssl = ssl;
        self
    }
    
    pub fn connection_timeout(mut self, timeout: u64) -> Self {
        self.connection_timeout = Some(timeout);
        self
    }
    
    pub fn build(self) -> Result<DatabaseConfig, String> {
        let host = self.host.ok_or("Host is required")?;
        let port = self.port.ok_or("Port is required")?;
        let username = self.username.ok_or("Username is required")?;
        let password = self.password.ok_or("Password is required")?;
        let connection_timeout = self.connection_timeout.unwrap_or(30);
        
        Ok(DatabaseConfig {
            host,
            port,
            username,
            password,
            ssl: self.ssl,
            connection_timeout,
        })
    }
}

// Usage example
fn main() {
    let config = DatabaseConfigBuilder::new()
        .host("localhost")
        .port(5432)
        .username("admin")
        .password("secret")
        .ssl(true)
        .connection_timeout(60)
        .build()
        .expect("Failed to build database config");
    
    println!("Database config: {:?}", config);
}
```

**Rust Benefits:**
- **Compile-time safety**: Missing required fields cause compilation errors
- **Method chaining**: Fluent interface with owned `self`
- **Error handling**: Uses `Result` for validation failures
- **Zero-cost abstractions**: No runtime overhead

### **2. Factory Pattern**

The Factory pattern creates objects without specifying their exact class. In Rust, this is implemented using traits and trait objects.

```rust
pub trait Animal {
    fn make_sound(&self);
    fn get_species(&self) -> String;
    fn get_weight(&self) -> f32;
}

#[derive(Debug)]
pub struct Dog {
    name: String,
    weight: f32,
}

impl Dog {
    pub fn new(name: &str, weight: f32) -> Self {
        Dog {
            name: name.to_string(),
            weight,
        }
    }
}

impl Animal for Dog {
    fn make_sound(&self) {
        println!("{} says: Woof!", self.name);
    }
    
    fn get_species(&self) -> String {
        "Canis lupus familiaris".to_string()
    }
    
    fn get_weight(&self) -> f32 {
        self.weight
    }
}

#[derive(Debug)]
pub struct Cat {
    name: String,
    weight: f32,
}

impl Cat {
    pub fn new(name: &str, weight: f32) -> Self {
        Cat {
            name: name.to_string(),
            weight,
        }
    }
}

impl Animal for Cat {
    fn make_sound(&self) {
        println!("{} says: Meow!", self.name);
    }
    
    fn get_species(&self) -> String {
        "Felis catus".to_string()
    }
    
    fn get_weight(&self) -> f32 {
        self.weight
    }
}

#[derive(Debug, Clone, Copy)]
pub enum AnimalType {
    Dog,
    Cat,
    Bird,
}

pub struct AnimalFactory;

impl AnimalFactory {
    pub fn create_animal(animal_type: AnimalType, name: &str, weight: f32) -> Result<Box<dyn Animal>, String> {
        match animal_type {
            AnimalType::Dog => {
                if weight < 1.0 || weight > 100.0 {
                    return Err("Dog weight must be between 1.0 and 100.0 kg".to_string());
                }
                Ok(Box::new(Dog::new(name, weight)))
            },
            AnimalType::Cat => {
                if weight < 0.5 || weight > 20.0 {
                    return Err("Cat weight must be between 0.5 and 20.0 kg".to_string());
                }
                Ok(Box::new(Cat::new(name, weight)))
            },
            AnimalType::Bird => {
                Err("Bird implementation not yet available".to_string())
            }
        }
    }
    
    // Alternative factory method with default parameters
    pub fn create_dog(name: &str) -> Box<dyn Animal> {
        Box::new(Dog::new(name, 25.0)) // Average dog weight
    }
    
    pub fn create_cat(name: &str) -> Box<dyn Animal> {
        Box::new(Cat::new(name, 4.5)) // Average cat weight
    }
}

// Usage example
fn main() {
    let animals: Vec<Box<dyn Animal>> = vec![
        AnimalFactory::create_animal(AnimalType::Dog, "Buddy", 30.0).unwrap(),
        AnimalFactory::create_animal(AnimalType::Cat, "Whiskers", 5.0).unwrap(),
        AnimalFactory::create_dog("Max"),
        AnimalFactory::create_cat("Luna"),
    ];
    
    for animal in animals {
        animal.make_sound();
        println!("Species: {}", animal.get_species());
        println!("Weight: {:.1} kg\n", animal.get_weight());
    }
}
```

**Rust Benefits:**
- **Trait objects**: Dynamic dispatch with `dyn Animal`
- **Type safety**: Enum-based factory selection
- **Error handling**: `Result` type for validation
- **Memory safety**: Box for heap allocation

### **3. Singleton Pattern**

The Singleton pattern ensures a class has only one instance. In Rust, this is implemented using `std::sync::Once` and `Arc<Mutex<T>>` for thread safety.

```rust
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
        
        // Add new log entry
        self.logs.push_back(entry);
        
        // Remove old logs if we exceed max_logs
        while self.logs.len() > self.max_logs {
            self.logs.pop_front();
        }
        
        // Print to console (in real implementation, this would be configurable)
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
    
    pub fn clear_logs(&mut self) {
        self.logs.clear();
    }
    
    pub fn set_max_logs(&mut self, max_logs: usize) {
        self.max_logs = max_logs;
    }
}

// Usage example
fn main() {
    let logger = Logger::get_instance();
    
    // Thread-safe logging
    {
        let mut logger = logger.lock().unwrap();
        logger.info("Application started");
        logger.warning("This is a warning message");
        logger.error("An error occurred");
        logger.debug("Debug information");
    }
    
    // Get recent logs
    {
        let logger = logger.lock().unwrap();
        let recent_logs = logger.get_recent_logs(2);
        println!("\nRecent logs:");
        for log in recent_logs {
            println!("  {:?}", log);
        }
    }
}
```

**Rust Benefits:**
- **Thread safety**: `Arc<Mutex<T>>` for concurrent access
- **Memory safety**: No null pointer dereferences
- **Zero-cost abstractions**: Minimal runtime overhead
- **Compile-time guarantees**: Impossible to create multiple instances accidentally

**Alternative: Lazy Static Pattern**
```rust
use lazy_static::lazy_static;

lazy_static! {
    static ref LOGGER: Arc<Mutex<Logger>> = Arc::new(Mutex::new(Logger {
        logs: VecDeque::new(),
        max_logs: 1000,
    }));
}
```

---

## **Structural Patterns**

Structural patterns deal with object composition and relationships between entities.

### **4. Observer Pattern**

The Observer pattern defines a one-to-many dependency between objects. In Rust, this is implemented using `Rc<RefCell<T>>` for shared ownership and interior mutability.

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct NewsEvent {
    pub id: u32,
    pub title: String,
    pub content: String,
    pub category: String,
}

pub trait Observer {
    fn update(&self, event: &NewsEvent);
    fn get_name(&self) -> &str;
}

pub struct NewsSubject {
    observers: Vec<Weak<RefCell<dyn Observer>>>,
    events: Vec<NewsEvent>,
    next_id: u32,
}

impl NewsSubject {
    pub fn new() -> Self {
        NewsSubject {
            observers: Vec::new(),
            events: Vec::new(),
            next_id: 1,
        }
    }
    
    pub fn attach(&mut self, observer: Rc<RefCell<dyn Observer>>) {
        self.observers.push(Rc::downgrade(&observer));
        println!("Observer '{}' attached", observer.borrow().get_name());
    }
    
    pub fn detach(&mut self, observer_name: &str) {
        self.observers.retain(|weak_observer| {
            if let Some(observer) = weak_observer.upgrade() {
                observer.borrow().get_name() != observer_name
            } else {
                false // Remove dropped observers
            }
        });
    }
    
    pub fn notify(&self, event: &NewsEvent) {
        println!("Notifying {} observers about: {}", self.observers.len(), event.title);
        
        for weak_observer in &self.observers {
            if let Some(observer) = weak_observer.upgrade() {
                observer.borrow().update(event);
            }
        }
    }
    
    pub fn publish_news(&mut self, title: &str, content: &str, category: &str) {
        let event = NewsEvent {
            id: self.next_id,
            title: title.to_string(),
            content: content.to_string(),
            category: category.to_string(),
        };
        
        self.next_id += 1;
        self.events.push(event.clone());
        self.notify(&event);
    }
    
    pub fn get_events(&self) -> &Vec<NewsEvent> {
        &self.events
    }
}

// Concrete Observer implementations
pub struct EmailNotifier {
    name: String,
    email: String,
    categories: Vec<String>,
}

impl EmailNotifier {
    pub fn new(name: &str, email: &str, categories: Vec<String>) -> Self {
        EmailNotifier {
            name: name.to_string(),
            email: email.to_string(),
            categories,
        }
    }
}

impl Observer for EmailNotifier {
    fn update(&self, event: &NewsEvent) {
        if self.categories.is_empty() || self.categories.contains(&event.category) {
            println!("📧 Email sent to {} ({}) about: {}", 
                     self.email, self.name, event.title);
        }
    }
    
    fn get_name(&self) -> &str {
        &self.name
    }
}

pub struct SMSSender {
    name: String,
    phone: String,
    priority_categories: Vec<String>,
}

impl SMSSender {
    pub fn new(name: &str, phone: &str, priority_categories: Vec<String>) -> Self {
        SMSSender {
            name: name.to_string(),
            phone: phone.to_string(),
            priority_categories,
        }
    }
}

impl Observer for SMSSender {
    fn update(&self, event: &NewsEvent) {
        if self.priority_categories.contains(&event.category) {
            println!("📱 SMS sent to {} ({}) about: {}", 
                     self.phone, self.name, event.title);
        }
    }
    
    fn get_name(&self) -> &str {
        &self.name
    }
}

// Usage example
fn main() {
    let mut news_subject = NewsSubject::new();
    
    // Create observers
    let email_notifier = Rc::new(RefCell::new(EmailNotifier::new(
        "Tech News Subscriber",
        "user@example.com",
        vec!["Technology".to_string(), "Science".to_string()]
    )));
    
    let sms_sender = Rc::new(RefCell::new(SMSSender::new(
        "Emergency Alert System",
        "+1234567890",
        vec!["Breaking".to_string(), "Emergency".to_string()]
    )));
    
    // Attach observers
    news_subject.attach(email_notifier.clone());
    news_subject.attach(sms_sender.clone());
    
    // Publish news events
    news_subject.publish_news(
        "New AI Breakthrough",
        "Scientists develop new AI model...",
        "Technology"
    );
    
    news_subject.publish_news(
        "Breaking: Earthquake Alert",
        "Earthquake detected in region...",
        "Breaking"
    );
    
    news_subject.publish_news(
        "Weather Update",
        "Sunny weather expected...",
        "Weather"
    );
    
    // Detach an observer
    news_subject.detach("Tech News Subscriber");
    
    news_subject.publish_news(
        "Another Tech Update",
        "More technology news...",
        "Technology"
    );
}
```

**Rust Benefits:**
- **Memory safety**: `Weak` references prevent reference cycles
- **Interior mutability**: `RefCell` allows runtime borrow checking
- **Shared ownership**: `Rc` enables multiple observers
- **Type safety**: Trait objects with compile-time guarantees

### **5. Strategy Pattern**

```rust
pub trait PaymentStrategy {
    fn pay(&self, amount: f64) -> String;
}

pub struct CreditCardPayment;
pub struct PayPalPayment;
pub struct BitcoinPayment;

impl PaymentStrategy for CreditCardPayment {
    fn pay(&self, amount: f64) -> String {
        format!("Paid ${:.2} using Credit Card", amount)
    }
}

pub struct PaymentProcessor {
    strategy: Box<dyn PaymentStrategy>,
}

impl PaymentProcessor {
    pub fn new(strategy: Box<dyn PaymentStrategy>) -> Self {
        PaymentProcessor { strategy }
    }
  
    pub fn process_payment(&self, amount: f64) -> String {
        self.strategy.pay(amount)
    }
}
```

### **6. Command Pattern**

```rust
pub trait Command {
    fn execute(&self);
    fn undo(&self);
}

pub struct Light {
    is_on: bool,
}

impl Light {
    pub fn new() -> Self { Light { is_on: false } }
    pub fn turn_on(&mut self) { self.is_on = true; }
    pub fn turn_off(&mut self) { self.is_on = false; }
}

pub struct TurnOnCommand {
    light: Rc<RefCell<Light>>,
}

impl Command for TurnOnCommand {
    fn execute(&self) {
        self.light.borrow_mut().turn_on();
    }
  
    fn undo(&self) {
        self.light.borrow_mut().turn_off();
    }
}

pub struct RemoteControl {
    command: Option<Box<dyn Command>>,
}

impl RemoteControl {
    pub fn set_command(&mut self, command: Box<dyn Command>) {
        self.command = Some(command);
    }
  
    pub fn press_button(&self) {
        if let Some(command) = &self.command {
            command.execute();
        }
    }
}
```

### **7. Decorator Pattern**

```rust
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
```

### **8. Adapter Pattern**

```rust
// Legacy system
pub struct OldPrinter {
    text: String,
}

impl OldPrinter {
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
            old_printer: OldPrinter { text: text.to_string() },
        }
    }
}

impl ModernPrinter for PrinterAdapter {
    fn print(&self) -> String {
        self.old_printer.print_old_format().replace("OLD: ", "")
    }
}
```

### **9. Facade Pattern**

```rust
pub struct CPU {
    pub name: String,
}

impl CPU {
    pub fn start(&self) { println!("CPU {} started", self.name); }
    pub fn execute(&self) { println!("CPU executing instructions"); }
    pub fn stop(&self) { println!("CPU stopped"); }
}

pub struct Memory {
    pub size: u32,
}

impl Memory {
    pub fn load(&self) { println!("Loading {}MB memory", self.size); }
    pub fn unload(&self) { println!("Unloading memory"); }
}

pub struct ComputerFacade {
    cpu: CPU,
    memory: Memory,
}

impl ComputerFacade {
    pub fn new() -> Self {
        ComputerFacade {
            cpu: CPU { name: "Intel i7".to_string() },
            memory: Memory { size: 8192 },
        }
    }
  
    pub fn start_computer(&self) {
        println!("Starting computer...");
        self.cpu.start();
        self.memory.load();
        self.cpu.execute();
    }
  
    pub fn shutdown_computer(&self) {
        println!("Shutting down computer...");
        self.cpu.stop();
        self.memory.unload();
    }
}
```

### **10. Template Method Pattern**

```rust
pub trait DataProcessor {
    fn process(&self) {
        self.load_data();
        self.validate_data();
        self.transform_data();
        self.save_data();
    }
  
    fn load_data(&self);
    fn validate_data(&self);
    fn transform_data(&self);
    fn save_data(&self);
}

pub struct CSVProcessor;

impl DataProcessor for CSVProcessor {
    fn load_data(&self) {
        println!("Loading CSV data...");
    }
  
    fn validate_data(&self) {
        println!("Validating CSV format...");
    }
  
    fn transform_data(&self) {
        println!("Transforming CSV data...");
    }
  
    fn save_data(&self) {
        println!("Saving processed CSV data...");
    }
}
```

### **11. State Pattern**

```rust
pub trait State {
    fn handle(&self, context: &mut Context);
}

pub struct Context {
    state: Box<dyn State>,
}

impl Context {
    pub fn new() -> Self {
        Context {
            state: Box::new(IdleState),
        }
    }
  
    pub fn set_state(&mut self, state: Box<dyn State>) {
        self.state = state;
    }
  
    pub fn request(&mut self) {
        self.state.handle(self);
    }
}

pub struct IdleState;

impl State for IdleState {
    fn handle(&self, context: &mut Context) {
        println!("Idle state - transitioning to Active");
        context.set_state(Box::new(ActiveState));
    }
}

pub struct ActiveState;

impl State for ActiveState {
    fn handle(&self, context: &mut Context) {
        println!("Active state - transitioning to Idle");
        context.set_state(Box::new(IdleState));
    }
}
```

### **12. Proxy Pattern**

```rust
pub trait Image {
    fn display(&self);
}

pub struct RealImage {
    filename: String,
}

impl RealImage {
    pub fn new(filename: &str) -> Self {
        println!("Loading image: {}", filename);
        RealImage {
            filename: filename.to_string(),
        }
    }
  
    fn load_from_disk(&self) {
        println!("Loading {} from disk", self.filename);
    }
}

impl Image for RealImage {
    fn display(&self) {
        self.load_from_disk();
        println!("Displaying {}", self.filename);
    }
}

pub struct ImageProxy {
    real_image: Option<RealImage>,
    filename: String,
}

impl ImageProxy {
    pub fn new(filename: &str) -> Self {
        ImageProxy {
            real_image: None,
            filename: filename.to_string(),
        }
    }
}

impl Image for ImageProxy {
    fn display(&self) {
        if self.real_image.is_none() {
            // Lazy loading
            let real_image = RealImage::new(&self.filename);
            real_image.display();
        }
    }
}
```

### **13. Chain of Responsibility Pattern**

```rust
pub trait Handler {
    fn set_next(&mut self, next: Box<dyn Handler>);
    fn handle(&self, request: &Request) -> Option<String>;
}

pub struct Request {
    pub amount: u32,
}

pub struct ManagerHandler {
    next: Option<Box<dyn Handler>>,
}

impl Handler for ManagerHandler {
    fn set_next(&mut self, next: Box<dyn Handler>) {
        self.next = Some(next);
    }
  
    fn handle(&self, request: &Request) -> Option<String> {
        if request.amount <= 1000 {
            Some("Manager approved".to_string())
        } else {
            self.next.as_ref()?.handle(request)
        }
    }
}

pub struct DirectorHandler {
    next: Option<Box<dyn Handler>>,
}

impl Handler for DirectorHandler {
    fn set_next(&mut self, next: Box<dyn Handler>) {
        self.next = Some(next);
    }
  
    fn handle(&self, request: &Request) -> Option<String> {
        if request.amount <= 10000 {
            Some("Director approved".to_string())
        } else {
            self.next.as_ref()?.handle(request)
        }
    }
}
```

### **14. Visitor Pattern**

```rust
pub trait Element {
    fn accept(&self, visitor: &dyn Visitor);
}

pub trait Visitor {
    fn visit_element_a(&self, element: &ElementA);
    fn visit_element_b(&self, element: &ElementB);
}

pub struct ElementA {
    pub value: i32,
}

impl Element for ElementA {
    fn accept(&self, visitor: &dyn Visitor) {
        visitor.visit_element_a(self);
    }
}

pub struct ElementB {
    pub value: String,
}

impl Element for ElementB {
    fn accept(&self, visitor: &dyn Visitor) {
        visitor.visit_element_b(self);
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
```

### **15. Memento Pattern**

```rust
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
        self.mementos.push(memento);
    }
  
    pub fn get_memento(&self, index: usize) -> Option<&Memento> {
        self.mementos.get(index)
    }
}
```

---

## **Rust-Specific Considerations**

### **Ownership and Borrowing in Design Patterns**

Rust's ownership system inherits unique challenges and benefits when implementing design patterns:

#### **Memory Management**
```rust
// ✅ Good: Using owned data
pub struct Config {
    data: String, // Owned string
}

// ✅ Good: Using references with lifetimes
pub fn process_config<'a>(config: &'a Config) -> &'a str {
    &config.data
}

// ❌ Avoid: Unnecessary cloning
pub fn bad_example(config: Config) -> String {
    config.data.clone() // Expensive clone
}
```

#### **Interior Mutability Patterns**
```rust
use std::cell::{RefCell, Cell};
use std::rc::Rc;

// For single-threaded scenarios
pub struct StateManager {
    state: RefCell<u32>,
    counter: Cell<u32>,
}

// For multi-threaded scenarios
use std::sync::{Arc, Mutex};
pub struct ThreadSafeState {
    state: Arc<Mutex<u32>>,
}
```

#### **Trait Objects vs Generics**
```rust
// ✅ Use generics for compile-time polymorphism
pub fn process<T: Processor>(processor: T) {
    processor.process();
}

// ✅ Use trait objects for runtime polymorphism
pub fn process_dynamic(processors: Vec<Box<dyn Processor>>) {
    for processor in processors {
        processor.process();
    }
}
```

### **Common Rust Idioms in Design Patterns**

#### **Builder Pattern with Validation**
```rust
pub struct DatabaseBuilder {
    config: DatabaseConfig,
}

impl DatabaseBuilder {
    pub fn validate(&self) -> Result<(), String> {
        if self.config.host.is_empty() {
            return Err("Host cannot be empty".to_string());
        }
        if self.config.port == 0 {
            return Err("Port must be greater than 0".to_string());
        }
        Ok(())
    }
}
```

#### **Error Handling in Factories**
```rust
pub enum CreationError {
    InvalidParameters(String),
    ResourceUnavailable,
    ConfigurationError(String),
}

impl std::fmt::Display for CreationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CreationError::InvalidParameters(msg) => write!(f, "Invalid parameters: {}", msg),
            CreationError::ResourceUnavailable => write!(f, "Resource unavailable"),
            CreationError::ConfigurationError(msg) => write!(f, "Configuration error: {}", msg),
        }
    }
}
```

---

## **Performance Analysis**

### **Benchmarking Design Patterns in Rust**

#### **Memory Usage Comparison**
```rust
// Builder Pattern: Zero-cost abstraction
pub fn build_config() -> DatabaseConfig {
    DatabaseConfigBuilder::new()
        .host("localhost")
        .port(5432)
        .build()
        .unwrap()
}

// Direct construction: Same memory footprint
pub fn direct_config() -> DatabaseConfig {
    DatabaseConfig {
        host: "localhost".to_string(),
        port: 5432,
        // ...
    }
}
```

#### **Runtime Performance**
- **Trait Objects**: ~10% overhead due to dynamic dispatch
- **Generics**: Zero runtime cost (monomorphization)
- **Arc/Mutex**: Minimal overhead for thread safety
- **Rc/RefCell**: Very low overhead for single-threaded scenarios

#### **When to Use Each Pattern**

| Pattern | Use Case | Performance Impact | Memory Safety |
|---------|----------|-------------------|---------------|
| Builder | Complex object construction | Zero cost | ✅ Safe |
| Factory | Runtime type selection | Low (trait objects) | ✅ Safe |
| Singleton | Global state management | Low (Arc/Mutex) | ✅ Safe |
| Observer | Event-driven systems | Low (Rc/Weak) | ✅ Safe |
| Strategy | Algorithm selection | Zero (generics) | ✅ Safe |

---

## **Anti-patterns in Rust**

### **What to Avoid**

#### **1. Unnecessary Cloning**
```rust
// ❌ Bad: Unnecessary clones
pub fn process_strings_bad(strings: Vec<String>) -> Vec<String> {
    strings.iter()
        .map(|s| s.clone()) // Expensive clone
        .collect()
}

// ✅ Good: Use references
pub fn process_strings_good(strings: &[String]) -> Vec<String> {
    strings.iter()
        .map(|s| s.to_uppercase()) // Transform without clone
        .collect()
}
```

#### **2. Overusing `unwrap()`**
```rust
// ❌ Bad: Panic-prone code
pub fn bad_config() -> DatabaseConfig {
    DatabaseConfigBuilder::new()
        .build()
        .unwrap() // Can panic!
}

// ✅ Good: Proper error handling
pub fn good_config() -> Result<DatabaseConfig, String> {
    DatabaseConfigBuilder::new()
        .host("localhost")
        .port(5432)
        .build() // Returns Result
}
```

#### **3. Ignoring Lifetimes**
```rust
// ❌ Bad: Missing lifetime parameters
pub fn bad_reference(data: &str) -> &str {
    &data // Compiler error!
}

// ✅ Good: Explicit lifetimes
pub fn good_reference<'a>(data: &'a str) -> &'a str {
    data
}
```

#### **4. Overusing `Arc<Mutex<T>>`**
```rust
// ❌ Bad: Unnecessary synchronization
pub struct OverSynchronized {
    data: Arc<Mutex<String>>, // Single-threaded app
}

// ✅ Good: Use appropriate synchronization
pub struct ProperlySynchronized {
    data: RefCell<String>, // Single-threaded
}

pub struct ThreadSafe {
    data: Arc<Mutex<String>>, // Multi-threaded
}
```

### **Best Practices**

1. **Prefer borrowing over ownership** when possible
2. **Use `Result` types** for error handling instead of panics
3. **Choose the right synchronization primitive** for your use case
4. **Profile before optimizing** - measure actual performance
5. **Use `cargo clippy`** to catch common anti-patterns

---

## **Real-World Applications**

### **File Manager Project Patterns**

#### **Command Pattern for File Operations**
```rust
pub trait FileCommand {
    fn execute(&self) -> Result<(), FileError>;
    fn undo(&self) -> Result<(), FileError>;
}

pub struct MoveFileCommand {
    source: PathBuf,
    destination: PathBuf,
}

impl FileCommand for MoveFileCommand {
    fn execute(&self) -> Result<(), FileError> {
        std::fs::rename(&self.source, &self.destination)
            .map_err(FileError::IoError)
    }
    
    fn undo(&self) -> Result<(), FileError> {
        std::fs::rename(&self.destination, &self.source)
            .map_err(FileError::IoError)
    }
}
```

#### **Observer Pattern for File System Events**
```rust
pub trait FileSystemObserver {
    fn on_file_created(&self, path: &Path);
    fn on_file_deleted(&self, path: &Path);
    fn on_file_modified(&self, path: &Path);
}

pub struct FileSystemWatcher {
    observers: Vec<Weak<RefCell<dyn FileSystemObserver>>>,
}

impl FileSystemWatcher {
    pub fn watch_directory(&self, path: &Path) {
        // Implementation using notify crate
    }
}
```

---

## **Conclusion**

Rust's design patterns provide powerful abstractions while maintaining memory safety and performance. The key is to:

1. **Understand Rust's ownership system** and how it affects pattern implementation
2. **Choose appropriate patterns** based on your specific use case
3. **Use the type system** to catch errors at compile time
4. **Profile and measure** performance before optimizing
5. **Follow Rust idioms** and best practices

This guide provides a solid foundation for implementing design patterns in Rust while leveraging the language's unique strengths! 🦀

---

## **Additional Resources**

- [Rust Book](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
