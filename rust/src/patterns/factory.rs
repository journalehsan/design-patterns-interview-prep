// Factory Pattern Demo

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
    
    pub fn create_dog(name: &str) -> Box<dyn Animal> {
        Box::new(Dog::new(name, 25.0)) // Average dog weight
    }
    
    pub fn create_cat(name: &str) -> Box<dyn Animal> {
        Box::new(Cat::new(name, 4.5)) // Average cat weight
    }
}

pub fn demo_factory() {
    println!("🏭 FACTORY PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern creates objects without specifying exact classes.");
    println!("Rust Benefit: Trait objects for dynamic dispatch.");
    
    println!("\n📝 Example 1: Creating animals with factory");
    let animals: Vec<Box<dyn Animal>> = vec![
        AnimalFactory::create_animal(AnimalType::Dog, "Buddy", 30.0).unwrap(),
        AnimalFactory::create_animal(AnimalType::Cat, "Whiskers", 5.0).unwrap(),
        AnimalFactory::create_dog("Max"),
        AnimalFactory::create_cat("Luna"),
    ];
    
    for animal in animals {
        animal.make_sound();
        println!("   Species: {}", animal.get_species());
        println!("   Weight: {:.1} kg\n", animal.get_weight());
    }
    
    println!("\n📝 Example 2: Error handling with invalid parameters");
    match AnimalFactory::create_animal(AnimalType::Dog, "Tiny", 0.5) {
        Ok(_) => println!("✅ Animal created"),
        Err(e) => println!("❌ Error: {}", e),
    }
    
    println!("\n💡 Interview Points:");
    println!("   • Trait objects for runtime polymorphism");
    println!("   • Enum-based factory selection");
    println!("   • Error handling with Result type");
    println!("   • Memory safety with Box");
}
