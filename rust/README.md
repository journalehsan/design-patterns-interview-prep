# 🦀 Design Patterns in Rust

A comprehensive implementation of design patterns in Rust, featuring an interactive menu system to explore each pattern with real-world examples and Rust-specific benefits.

## 🚀 Features

- **15 Essential Design Patterns** - From creational to behavioral patterns
- **Interactive Menu** - Easy navigation through pattern demos
- **Rust-Specific Features** - Demonstrates ownership, borrowing, lifetimes
- **Real-World Examples** - Practical implementations
- **Interview Focus** - Common interview scenarios and solutions

## 📚 Included Patterns

### Creational Patterns
1. **Builder Pattern** - Complex object construction with validation
2. **Factory Pattern** - Object creation without exact class specification
3. **Singleton Pattern** - Single instance management with thread safety

### Structural Patterns
4. **Observer Pattern** - Event system and notifications
5. **Strategy Pattern** - Algorithm selection and encapsulation
6. **Command Pattern** - Undo/redo and transaction management
7. **Decorator Pattern** - Dynamic behavior addition
8. **Adapter Pattern** - Legacy integration and compatibility
9. **Facade Pattern** - Simplified interface to complex systems
10. **Proxy Pattern** - Lazy loading and access control
11. **Visitor Pattern** - Operations on object structures

### Behavioral Patterns
12. **Template Method** - Algorithm skeletons
13. **Memento Pattern** - State restoration and checkpoints
14. **Chain of Responsibility** - Request handling chain
15. **State Pattern** - Behavior based on state

## 🎯 Usage

### Building the Project

```bash
cd rust
cargo build --release
```

### Running the Interactive Menu

```bash
cargo run
```

or with the release binary:

```bash
cargo run --release
```

or directly:

```bash
./target/release/design_patterns_rust
```

### Menu Navigation

```
🚀 DESIGN PATTERNS INTERVIEW PREP - RUST EDITION 🚀
================================================================================
Master the most common design patterns in Rust!
Each pattern includes real-world examples and Rust-specific features.
================================================================================

📚 AVAILABLE PATTERNS:
--------------------------------------------------
1.  Builder Pattern - Complex Object Construction
2.  Factory Pattern - Object Creation
3.  Singleton Pattern - Single Instance Management
4.  Observer Pattern - Event System & Notifications
5.  Strategy Pattern - Algorithm Selection
6.  Command Pattern - Undo/Redo & Transactions
7.  Decorator Pattern - Dynamic Behavior
8.  Adapter Pattern - Legacy Integration
9.  Facade Pattern - Simplified Interface
10. Template Method Pattern - Algorithm Skeleton
11. Proxy Pattern - Lazy Loading
12. Visitor Pattern - Operations on Structures
13. Memento Pattern - State Restoration
14. Chain of Responsibility - Request Handling
15. State Pattern - Behavior Based on State
16. 📖 Interview Tips & Common Questions
17. 🚪 Exit
--------------------------------------------------

🎯 Choose a pattern to explore (1-17):
```

## 🏗️ Project Structure

```
rust/
├── Cargo.toml          # Rust project configuration
├── src/
│   ├── main.rs         # Main menu system
│   └── patterns/
│       ├── mod.rs      # Module declarations
│       ├── builder.rs
│       ├── factory.rs
│       ├── singleton.rs
│       ├── observer.rs
│       ├── strategy.rs
│       ├── command.rs
│       ├── decorator.rs
│       ├── adapter.rs
│       ├── facade.rs
│       ├── template_method.rs
│       ├── proxy.rs
│       ├── visitor.rs
│       ├── memento.rs
│       ├── chain_of_responsibility.rs
│       └── state.rs
└── README.md           # This file
```

## 🎓 Learning Resources

### Key Rust Concepts Demonstrated

1. **Ownership & Borrowing** - How patterns adapt to Rust's memory model
2. **Trait Objects** - Dynamic dispatch with `dyn Trait`
3. **Smart Pointers** - `Rc<RefCell<T>>` and `Arc<Mutex<T>>`
4. **Zero-Cost Abstractions** - No runtime overhead
5. **Type Safety** - Compile-time guarantees

### Interview Tips

Each pattern demo includes:
- Real-world use cases
- Rust-specific benefits
- Implementation examples
- Common pitfalls
- Performance considerations

## 🔍 Example: Observer Pattern

```rust
pub fn demo_observer() {
    println!("👀 OBSERVER PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern defines one-to-many dependency between objects.");
    println!("Rust Benefit: Rc<RefCell<T>> for shared ownership.");
    
    // Creates observers, attaches them, and demonstrates notifications
    // ...
}
```

## 🧪 Testing

To run the project:

```bash
cargo run
```

Each pattern can be selected from the interactive menu to see:
- Pattern explanation
- Rust-specific implementation details
- Working code examples
- Interview points

## 📖 Documentation

For detailed explanations of each pattern, see:

- `guide.md` - Comprehensive guide with code examples
- Inline comments in each pattern file
- Demo function documentation

## 🦀 Why Rust for Design Patterns?

Rust's unique features make design patterns:

1. **Safer** - Memory safety without garbage collection
2. **Faster** - Zero-cost abstractions
3. **More Expressive** - Ownership and borrowing enable new patterns
4. **Compile-Time Verified** - Errors caught at compile time

## 📝 Examples

### Builder Pattern
```rust
let config = DatabaseConfigBuilder::new()
    .host("localhost")
    .port(5432)
    .username("admin")
    .password("secret")
    .ssl(true)
    .build()?;
```

### Observer Pattern
```rust
let email_notifier = Rc::new(RefCell::new(EmailNotifier::new(
    "Tech News Subscriber",
    "user@example.com",
    vec!["Technology".to_string()]
)));

news_subject.attach(email_notifier);
```

### Command Pattern
```rust
let light = Rc::new(RefCell::new(Light::new()));
let mut remote = RemoteControl::new();
remote.add_command(Box::new(TurnOnCommand::new(light)));
remote.execute_all();
```

## 🤝 Contributing

Contributions are welcome! Please see the main project's CONTRIBUTING.md file.

## 📄 License

This project is licensed under the same license as the main project - see the main LICENSE file.

## 🙏 Acknowledgments

- Based on the Gang of Four Design Patterns book
- Rust Design Patterns community
- All contributors to Rust language development

---

**Happy Coding in Rust! 🦀✨**
