// Pattern module declarations
pub mod builder;
pub mod factory;
pub mod singleton;
pub mod observer;
pub mod strategy;
pub mod command;
pub mod decorator;
pub mod adapter;
pub mod facade;
pub mod template_method;
pub mod proxy;
pub mod visitor;
pub mod memento;
pub mod chain_of_responsibility;
pub mod state;

// Re-export demo functions
pub use builder::demo_builder;
pub use factory::demo_factory;
pub use singleton::demo_singleton;
pub use observer::demo_observer;
pub use strategy::demo_strategy;
pub use command::demo_command;
pub use decorator::demo_decorator;
pub use adapter::demo_adapter;
pub use facade::demo_facade;
pub use template_method::demo_template_method;
pub use proxy::demo_proxy;
pub use visitor::demo_visitor;
pub use memento::demo_memento;
pub use chain_of_responsibility::demo_chain_of_responsibility;
pub use state::demo_state;
