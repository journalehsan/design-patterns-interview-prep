// Strategy Pattern Demo

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

impl PaymentStrategy for PayPalPayment {
    fn pay(&self, amount: f64) -> String {
        format!("Paid ${:.2} using PayPal", amount)
    }
}

impl PaymentStrategy for BitcoinPayment {
    fn pay(&self, amount: f64) -> String {
        format!("Paid ${:.2} using Bitcoin", amount)
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

pub fn demo_strategy() {
    println!("🎯 STRATEGY PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern makes algorithms interchangeable.");
    println!("Rust Benefit: Trait objects for runtime algorithm selection.");
    
    println!("\n📝 Example 1: Different payment methods");
    
    let credit_processor = PaymentProcessor::new(Box::new(CreditCardPayment));
    println!("{}", credit_processor.process_payment(100.0));
    
    let paypal_processor = PaymentProcessor::new(Box::new(PayPalPayment));
    println!("{}", paypal_processor.process_payment(50.0));
    
    let bitcoin_processor = PaymentProcessor::new(Box::new(BitcoinPayment));
    println!("{}", bitcoin_processor.process_payment(75.5));
    
    println!("\n💡 Interview Points:");
    println!("   • Encapsulate algorithms in separate types");
    println!("   • Runtime selection using trait objects");
    println!("   • Easy to add new strategies");
    println!("   • Open/Closed Principle compliance");
}
