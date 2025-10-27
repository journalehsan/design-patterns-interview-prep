// Proxy Pattern Demo

pub trait Image {
    fn display(&self);
}

pub struct RealImage {
    filename: String,
    loaded: bool,
}

impl RealImage {
    pub fn new(filename: &str) -> Self {
        println!("Loading image: {}", filename);
        RealImage {
            filename: filename.to_string(),
            loaded: false,
        }
    }
  
    fn load_from_disk(&self) {
        println!("Loading {} from disk (expensive operation)", self.filename);
    }
}

impl Image for RealImage {
    fn display(&self) {
        if !self.loaded {
            println!("First time access - loading image");
        }
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
        println!("Creating image proxy: {}", filename);
        ImageProxy {
            real_image: None,
            filename: filename.to_string(),
        }
    }
}

impl Image for ImageProxy {
    fn display(&self) {
        if self.real_image.is_none() {
            println!("Lazy loading initiated");
        }
        
        // Lazy loading happens here
        let real_image = RealImage::new(&self.filename);
        real_image.display();
    }
}

pub fn demo_proxy() {
    println!("🎭 PROXY PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern provides a placeholder for another object.");
    println!("Rust Benefit: Lazy initialization and access control.");
    
    println!("\n📝 Example 1: Lazy loading with proxy");
    println!("Note: Image is NOT loaded until display is called");
    let proxy = ImageProxy::new("huge_image.jpg");
    
    println!("\nNow accessing the image through proxy:");
    proxy.display();
    
    println!("\n📝 Example 2: Direct access (no proxy)");
    let direct_image = RealImage::new("direct.jpg");
    direct_image.display();
    
    println!("\n💡 Interview Points:");
    println!("   • Lazy initialization");
    println!("   • Virtual proxy for expensive objects");
    println!("   • Access control");
    println!("   • Reduce memory usage");
}
