// Observer Pattern Demo
use std::cell::RefCell;
use std::rc::{Rc, Weak};

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
                false
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
}

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

pub fn demo_observer() {
    println!("👀 OBSERVER PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern defines one-to-many dependency between objects.");
    println!("Rust Benefit: Rc<RefCell<T>> for shared ownership.");
    
    println!("\n📝 Example 1: News notification system");
    let mut news_subject = NewsSubject::new();
    
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
    
    news_subject.attach(email_notifier.clone());
    news_subject.attach(sms_sender.clone());
    
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
    
    println!("\n📝 Example 2: Detaching observer");
    news_subject.detach("Tech News Subscriber");
    
    news_subject.publish_news(
        "Another Tech Update",
        "More technology news...",
        "Technology"
    );
    
    println!("\n💡 Interview Points:");
    println!("   • Weak references prevent memory leaks");
    println!("   • Interior mutability with RefCell");
    println!("   • Shared ownership with Rc");
    println!("   • Type safety with trait objects");
}
