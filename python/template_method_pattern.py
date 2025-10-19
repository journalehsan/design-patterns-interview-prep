'''
🚀 TEMPLATE METHOD PATTERN - INTERVIEW FOCUSED 🚀

The Template Method Pattern defines the skeleton of an algorithm in a method,
deferring some steps to subclasses. It lets subclasses redefine certain steps
of an algorithm without changing the algorithm's structure.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to define a common algorithm structure with customizable steps?"
2. "How to avoid code duplication in similar algorithms?"
3. "How to enforce a specific order of operations?"
4. "How to implement the Hollywood Principle (Don't call us, we'll call you)?"

💡 KEY INTERVIEW POINTS:
- Algorithm skeleton with customizable steps
- Code reuse and DRY principle
- Hook methods and abstract methods
- Framework design patterns
'''

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
import json
from datetime import datetime

# ============================================================================
# DATA PROCESSING TEMPLATE
# ============================================================================

class DataProcessor(ABC):
    """Abstract base class for data processing algorithms"""
    
    def process_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Template method that defines the algorithm structure.
        This method cannot be overridden by subclasses.
        """
        print("🔄 Starting data processing pipeline...")
        
        # Step 1: Validate input data
        if not self._validate_input(data):
            return {"success": False, "error": "Invalid input data"}
        
        # Step 2: Preprocess data
        processed_data = self._preprocess_data(data)
        
        # Step 3: Transform data (abstract method - must be implemented)
        transformed_data = self._transform_data(processed_data)
        
        # Step 4: Post-process data (hook method - can be overridden)
        final_data = self._postprocess_data(transformed_data)
        
        # Step 5: Generate report
        report = self._generate_report(final_data)
        
        print("✅ Data processing pipeline completed!")
        return {
            "success": True,
            "data": final_data,
            "report": report,
            "timestamp": datetime.now().isoformat()
        }
    
    def _validate_input(self, data: List[Dict[str, Any]]) -> bool:
        """Validate input data - can be overridden"""
        if not data:
            print("❌ No data provided")
            return False
        
        if not isinstance(data, list):
            print("❌ Data must be a list")
            return False
        
        print(f"✅ Input validation passed: {len(data)} records")
        return True
    
    def _preprocess_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Preprocess data - can be overridden"""
        print("🔧 Preprocessing data...")
        
        # Remove empty records
        filtered_data = [record for record in data if record]
        
        # Add processing metadata
        for i, record in enumerate(filtered_data):
            record['_processing_id'] = i + 1
            record['_processed_at'] = datetime.now().isoformat()
        
        print(f"✅ Preprocessing completed: {len(filtered_data)} records")
        return filtered_data
    
    @abstractmethod
    def _transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform data - must be implemented by subclasses"""
        pass
    
    def _postprocess_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Post-process data - hook method, can be overridden"""
        print("🔧 Post-processing data...")
        return data
    
    def _generate_report(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate processing report - can be overridden"""
        return {
            "total_records": len(data),
            "processing_time": datetime.now().isoformat(),
            "processor_type": self.__class__.__name__
        }

class UserDataProcessor(DataProcessor):
    """Process user data with specific transformations"""
    
    def _validate_input(self, data: List[Dict[str, Any]]) -> bool:
        """Override validation for user data"""
        if not super()._validate_input(data):
            return False
        
        # Check for required user fields
        required_fields = ['id', 'name', 'email']
        for i, record in enumerate(data):
            for field in required_fields:
                if field not in record:
                    print(f"❌ Record {i} missing required field: {field}")
                    return False
        
        print("✅ User data validation passed")
        return True
    
    def _transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform user data"""
        print("🔄 Transforming user data...")
        
        transformed_data = []
        for record in data:
            # Normalize email
            email = record['email'].lower().strip()
            
            # Capitalize name
            name = record['name'].title()
            
            # Generate user code
            user_code = f"USR_{record['id']:04d}"
            
            transformed_record = {
                'id': record['id'],
                'name': name,
                'email': email,
                'user_code': user_code,
                'status': 'active',
                '_processing_id': record.get('_processing_id'),
                '_processed_at': record.get('_processed_at')
            }
            transformed_data.append(transformed_record)
        
        print(f"✅ User data transformation completed: {len(transformed_data)} users")
        return transformed_data
    
    def _postprocess_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Post-process user data"""
        print("🔧 Post-processing user data...")
        
        # Sort by user code
        data.sort(key=lambda x: x['user_code'])
        
        # Add summary statistics
        for record in data:
            record['_summary'] = {
                'name_length': len(record['name']),
                'email_domain': record['email'].split('@')[1] if '@' in record['email'] else 'unknown'
            }
        
        return data

class ProductDataProcessor(DataProcessor):
    """Process product data with specific transformations"""
    
    def _transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform product data"""
        print("🔄 Transforming product data...")
        
        transformed_data = []
        for record in data:
            # Calculate price with tax
            base_price = float(record.get('price', 0))
            tax_rate = 0.08  # 8% tax
            price_with_tax = base_price * (1 + tax_rate)
            
            # Generate product code
            category = record.get('category', 'general').upper()[:3]
            product_code = f"{category}_{record['id']:04d}"
            
            # Determine availability
            stock = int(record.get('stock', 0))
            availability = 'in_stock' if stock > 0 else 'out_of_stock'
            
            transformed_record = {
                'id': record['id'],
                'name': record['name'],
                'category': record.get('category', 'general'),
                'base_price': base_price,
                'price_with_tax': round(price_with_tax, 2),
                'stock': stock,
                'availability': availability,
                'product_code': product_code,
                '_processing_id': record.get('_processing_id'),
                '_processed_at': record.get('_processed_at')
            }
            transformed_data.append(transformed_record)
        
        print(f"✅ Product data transformation completed: {len(transformed_data)} products")
        return transformed_data
    
    def _generate_report(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate product-specific report"""
        base_report = super()._generate_report(data)
        
        # Add product-specific statistics
        total_value = sum(record['base_price'] for record in data)
        in_stock_count = sum(1 for record in data if record['availability'] == 'in_stock')
        categories = set(record['category'] for record in data)
        
        base_report.update({
            'total_inventory_value': total_value,
            'in_stock_products': in_stock_count,
            'out_of_stock_products': len(data) - in_stock_count,
            'categories': list(categories),
            'category_count': len(categories)
        })
        
        return base_report

# ============================================================================
# BUILD SYSTEM TEMPLATE
# ============================================================================

class BuildSystem(ABC):
    """Abstract build system with template method"""
    
    def build_project(self, project_name: str) -> Dict[str, Any]:
        """Template method for building a project"""
        print(f"🏗️ Starting build process for: {project_name}")
        
        # Step 1: Clean previous build
        self._clean_build_directory()
        
        # Step 2: Install dependencies
        if not self._install_dependencies():
            return {"success": False, "error": "Failed to install dependencies"}
        
        # Step 3: Compile source code
        if not self._compile_source():
            return {"success": False, "error": "Compilation failed"}
        
        # Step 4: Run tests
        test_results = self._run_tests()
        
        # Step 5: Package application
        package_path = self._package_application()
        
        # Step 6: Deploy (optional hook)
        deploy_result = self._deploy_application(package_path)
        
        print("✅ Build process completed!")
        return {
            "success": True,
            "project": project_name,
            "package_path": package_path,
            "test_results": test_results,
            "deploy_result": deploy_result,
            "build_time": datetime.now().isoformat()
        }
    
    def _clean_build_directory(self):
        """Clean build directory - can be overridden"""
        print("🧹 Cleaning build directory...")
        time.sleep(0.1)  # Simulate cleaning
        print("✅ Build directory cleaned")
    
    @abstractmethod
    def _install_dependencies(self) -> bool:
        """Install dependencies - must be implemented"""
        pass
    
    @abstractmethod
    def _compile_source(self) -> bool:
        """Compile source code - must be implemented"""
        pass
    
    def _run_tests(self) -> Dict[str, Any]:
        """Run tests - hook method, can be overridden"""
        print("🧪 Running tests...")
        time.sleep(0.2)  # Simulate test execution
        return {
            "total_tests": 25,
            "passed": 23,
            "failed": 2,
            "coverage": 87.5
        }
    
    @abstractmethod
    def _package_application(self) -> str:
        """Package application - must be implemented"""
        pass
    
    def _deploy_application(self, package_path: str) -> Optional[Dict[str, Any]]:
        """Deploy application - hook method, can be overridden"""
        print("🚀 Deploying application...")
        time.sleep(0.1)  # Simulate deployment
        return {
            "deployed": True,
            "package_path": package_path,
            "deployment_time": datetime.now().isoformat()
        }

class PythonBuildSystem(BuildSystem):
    """Python-specific build system"""
    
    def _install_dependencies(self) -> bool:
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")
        time.sleep(0.3)  # Simulate pip install
        print("✅ Python dependencies installed")
        return True
    
    def _compile_source(self) -> bool:
        """Compile Python source (bytecode compilation)"""
        print("🐍 Compiling Python source to bytecode...")
        time.sleep(0.2)  # Simulate compilation
        print("✅ Python source compiled")
        return True
    
    def _package_application(self) -> str:
        """Package Python application"""
        print("📦 Packaging Python application...")
        time.sleep(0.2)  # Simulate packaging
        package_path = "dist/python_app.tar.gz"
        print(f"✅ Python application packaged: {package_path}")
        return package_path
    
    def _deploy_application(self, package_path: str) -> Optional[Dict[str, Any]]:
        """Deploy Python application to server"""
        print("🐍 Deploying Python application to server...")
        time.sleep(0.3)  # Simulate deployment
        return {
            "deployed": True,
            "package_path": package_path,
            "server": "python-server-01",
            "deployment_time": datetime.now().isoformat()
        }

class JavaBuildSystem(BuildSystem):
    """Java-specific build system"""
    
    def _install_dependencies(self) -> bool:
        """Install Java dependencies using Maven"""
        print("☕ Installing Java dependencies with Maven...")
        time.sleep(0.4)  # Simulate Maven download
        print("✅ Java dependencies installed")
        return True
    
    def _compile_source(self) -> bool:
        """Compile Java source code"""
        print("☕ Compiling Java source code...")
        time.sleep(0.3)  # Simulate javac compilation
        print("✅ Java source compiled")
        return True
    
    def _run_tests(self) -> Dict[str, Any]:
        """Run Java tests with JUnit"""
        print("🧪 Running Java tests with JUnit...")
        time.sleep(0.3)  # Simulate test execution
        return {
            "total_tests": 45,
            "passed": 44,
            "failed": 1,
            "coverage": 92.3
        }
    
    def _package_application(self) -> str:
        """Package Java application as JAR"""
        print("☕ Packaging Java application as JAR...")
        time.sleep(0.2)  # Simulate JAR creation
        package_path = "target/java_app.jar"
        print(f"✅ Java application packaged: {package_path}")
        return package_path

# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_template_method_interview():
    """
    🎯 INTERVIEW DEMO: Template Method Pattern
    Demonstrates algorithm skeletons with customizable steps
    """
    print("\n" + "="*60)
    print("🚀 TEMPLATE METHOD PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to define a common algorithm structure with customizable steps?")
    print("2. How to avoid code duplication in similar algorithms?")
    print("3. How to enforce a specific order of operations?")
    print("4. How to implement the Hollywood Principle?")
    
    # ========================================================================
    # DATA PROCESSING DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("📊 DATA PROCESSING TEMPLATE DEMO")
    print("="*50)
    
    # Sample user data
    user_data = [
        {"id": 1, "name": "john doe", "email": "JOHN@EXAMPLE.COM"},
        {"id": 2, "name": "jane smith", "email": "jane.smith@test.org"},
        {"id": 3, "name": "bob wilson", "email": "BOB.WILSON@company.com"},
        {"id": 4, "name": "alice brown", "email": "alice@university.edu"}
    ]
    
    # Sample product data
    product_data = [
        {"id": 101, "name": "Laptop", "category": "electronics", "price": 999.99, "stock": 5},
        {"id": 102, "name": "Mouse", "category": "electronics", "price": 29.99, "stock": 0},
        {"id": 103, "name": "Book", "category": "education", "price": 19.99, "stock": 15},
        {"id": 104, "name": "Pen", "category": "office", "price": 2.99, "stock": 50}
    ]
    
    # Process user data
    print("\n👥 Processing user data:")
    user_processor = UserDataProcessor()
    user_result = user_processor.process_data(user_data)
    
    if user_result["success"]:
        print(f"✅ User processing successful!")
        print(f"📊 Processed {len(user_result['data'])} users")
        print(f"📋 Report: {user_result['report']}")
        
        # Show sample processed data
        print("\n📄 Sample processed user data:")
        for user in user_result['data'][:2]:
            print(f"   {user['user_code']}: {user['name']} ({user['email']})")
    
    # Process product data
    print("\n🛍️ Processing product data:")
    product_processor = ProductDataProcessor()
    product_result = product_processor.process_data(product_data)
    
    if product_result["success"]:
        print(f"✅ Product processing successful!")
        print(f"📊 Processed {len(product_result['data'])} products")
        print(f"📋 Report: {product_result['report']}")
        
        # Show sample processed data
        print("\n📄 Sample processed product data:")
        for product in product_result['data'][:2]:
            print(f"   {product['product_code']}: {product['name']} - ${product['price_with_tax']}")
    
    # ========================================================================
    # BUILD SYSTEM DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🏗️ BUILD SYSTEM TEMPLATE DEMO")
    print("="*50)
    
    # Python build
    print("\n🐍 Building Python project:")
    python_builder = PythonBuildSystem()
    python_result = python_builder.build_project("python-web-app")
    
    if python_result["success"]:
        print(f"✅ Python build successful!")
        print(f"📦 Package: {python_result['package_path']}")
        print(f"🧪 Tests: {python_result['test_results']}")
        print(f"🚀 Deploy: {python_result['deploy_result']}")
    
    # Java build
    print("\n☕ Building Java project:")
    java_builder = JavaBuildSystem()
    java_result = java_builder.build_project("java-enterprise-app")
    
    if java_result["success"]:
        print(f"✅ Java build successful!")
        print(f"📦 Package: {java_result['package_path']}")
        print(f"🧪 Tests: {java_result['test_results']}")
        print(f"🚀 Deploy: {java_result['deploy_result']}")
    
    # ========================================================================
    # TEMPLATE METHOD BENEFITS DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("💡 TEMPLATE METHOD BENEFITS")
    print("="*50)
    
    print("\n🎯 Key Benefits:")
    print("   1. ✅ Code Reuse - Common algorithm structure shared across classes")
    print("   2. ✅ Consistency - Enforces same algorithm flow for all implementations")
    print("   3. ✅ Flexibility - Allows customization of specific steps")
    print("   4. ✅ Maintainability - Changes to algorithm structure affect all subclasses")
    print("   5. ✅ Hollywood Principle - Framework controls the flow, not the client")
    
    print("\n🔧 Method Types in Template Method:")
    print("   1. 📋 Template Method - Defines algorithm skeleton (final method)")
    print("   2. 🔧 Abstract Methods - Must be implemented by subclasses")
    print("   3. 🪝 Hook Methods - Can be overridden by subclasses (optional)")
    print("   4. 🔒 Concrete Methods - Cannot be overridden (final)")
    
    print("\n📚 Real-World Examples:")
    print("   - Framework lifecycle methods (Spring, React)")
    print("   - Build systems (Maven, Gradle)")
    print("   - Data processing pipelines")
    print("   - Game engine update loops")
    print("   - Web framework request/response cycles")
    
    print("\n⚠️ Trade-offs:")
    print("   - Can lead to deep inheritance hierarchies")
    print("   - May violate Liskov Substitution Principle if not designed carefully")
    print("   - Can be harder to understand than simple inheritance")
    print("   - Template method must be stable (hard to change once published)")
    
    # ========================================================================
    # ERROR HANDLING DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("⚠️ ERROR HANDLING DEMO")
    print("="*50)
    
    print("\n🧪 Testing error scenarios:")
    
    # Test with invalid data
    print("\nTesting with invalid user data:")
    invalid_user_data = [
        {"id": 1, "name": "John"},  # Missing email
        {"id": 2, "email": "jane@example.com"}  # Missing name
    ]
    
    user_processor = UserDataProcessor()
    invalid_result = user_processor.process_data(invalid_user_data)
    
    if not invalid_result["success"]:
        print(f"❌ Processing failed as expected: {invalid_result['error']}")
    
    # Test with empty data
    print("\nTesting with empty data:")
    empty_result = user_processor.process_data([])
    
    if not empty_result["success"]:
        print(f"❌ Processing failed as expected: {empty_result['error']}")

if __name__ == "__main__":
    demo_template_method_interview()
