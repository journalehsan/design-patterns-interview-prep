// Builder Pattern Demo

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

pub fn demo_builder() {
    println!("🏗️  BUILDER PATTERN DEMO");
    println!("{}", "=".repeat(60));
    println!("\nThis pattern constructs complex objects step by step.");
    println!("Rust Benefit: Compile-time safety with method chaining.");
    
    println!("\n📝 Example 1: Building a valid database configuration");
    let config = DatabaseConfigBuilder::new()
        .host("localhost")
        .port(5432)
        .username("admin")
        .password("secret")
        .ssl(true)
        .connection_timeout(60)
        .build()
        .expect("Failed to build database config");
    
    println!("✅ Configuration built: {:?}", config);
    
    println!("\n📝 Example 2: Building with missing required fields");
    let result = DatabaseConfigBuilder::new()
        .host("localhost")
        .port(5432)
        .build();
    
    match result {
        Ok(_) => println!("✅ Config built successfully"),
        Err(e) => println!("❌ Error: {}", e),
    }
    
    println!("\n📝 Example 3: Builder with default values");
    let config = DatabaseConfigBuilder::new()
        .host("production.example.com")
        .port(3306)
        .username("dbuser")
        .password("secure123")
        .ssl(false)
        .build()
        .unwrap();
    
    println!("✅ Configuration with defaults: {:?}", config);
    
    println!("\n💡 Interview Points:");
    println!("   • Method chaining with owned self");
    println!("   • Validation using Result type");
    println!("   • Optional fields with Default values");
    println!("   • No runtime overhead (zero-cost abstraction)");
}
