'''
🚀 ADAPTER PATTERN - INTERVIEW FOCUSED 🚀

The Adapter Design Pattern allows incompatible interfaces to work together.
It acts as a bridge between two incompatible interfaces by wrapping an
existing class with a new interface.

🎯 COMMON INTERVIEW QUESTIONS:
1. "How to integrate with a legacy system you can't modify?"
2. "What if you need two-way adaptation?"
3. "How to handle incompatible interfaces?"
4. "How to handle data transformation between systems?"

💡 KEY INTERVIEW POINTS:
- Bidirectional adaptation
- Data format transformation
- Legacy system integration
- Interface compatibility
- Real-world integration scenarios
'''

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# ============================================================================
# LEGACY SYSTEM SIMULATION (Interview scenario: integrating with old systems)
# ============================================================================

class LegacyDatabase:
    """Simulates an old database system with different interface"""
    def __init__(self):
        self._data = {
            'users': [
                {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'created': '2023-01-15'},
                {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'created': '2023-02-20'}
            ]
        }
    
    def fetch_user_data_legacy_format(self, user_id: int) -> str:
        """Returns data in old colon-separated format"""
        for user in self._data['users']:
            if user['id'] == user_id:
                return f"ID:{user['id']}:NAME:{user['name']}:EMAIL:{user['email']}:CREATED:{user['created']}"
        return "USER_NOT_FOUND"
    
    def save_user_data_legacy_format(self, data: str) -> bool:
        """Saves data in old colon-separated format"""
        try:
            parts = data.split(':')
            if len(parts) >= 8:  # ID:1:NAME:John:EMAIL:john@example.com:CREATED:2023-01-15
                user_data = {
                    'id': int(parts[1]),
                    'name': parts[3],
                    'email': parts[5],
                    'created': parts[7]
                }
                # Update existing user or add new one
                for i, user in enumerate(self._data['users']):
                    if user['id'] == user_data['id']:
                        self._data['users'][i] = user_data
                        return True
                self._data['users'].append(user_data)
                return True
        except (ValueError, IndexError):
            pass
        return False

class ModernAPI:
    """Simulates a modern REST API with JSON interface"""
    def __init__(self):
        self._data = {
            'users': [
                {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'created_at': '2023-01-15T00:00:00Z'},
                {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'created_at': '2023-02-20T00:00:00Z'}
            ]
        }
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Returns user data as JSON dictionary"""
        for user in self._data['users']:
            if user['id'] == user_id:
                return {
                    'success': True,
                    'data': user,
                    'timestamp': datetime.now().isoformat()
                }
        return {
            'success': False,
            'error': 'User not found',
            'timestamp': datetime.now().isoformat()
        }
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates user and returns JSON response"""
        try:
            new_user = {
                'id': max([u['id'] for u in self._data['users']]) + 1,
                'name': user_data.get('name', ''),
                'email': user_data.get('email', ''),
                'created_at': datetime.now().isoformat() + 'Z'
            }
            self._data['users'].append(new_user)
            return {
                'success': True,
                'data': new_user,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# ============================================================================
# ADAPTER INTERFACES
# ============================================================================

class UserService(ABC):
    """Modern user service interface"""
    @abstractmethod
    def get_user(self, user_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

# ============================================================================
# BIDIRECTIONAL ADAPTER (Interview focus: two-way adaptation)
# ============================================================================

class LegacyToModernAdapter(UserService):
    """
    Adapter that makes Legacy Database compatible with Modern UserService interface
    Interview question: How to adapt legacy system to modern interface?
    """
    def __init__(self, legacy_db: LegacyDatabase):
        self._legacy_db = legacy_db
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Convert legacy format to modern JSON format"""
        legacy_data = self._legacy_db.fetch_user_data_legacy_format(user_id)
        
        if legacy_data == "USER_NOT_FOUND":
            return {
                'success': False,
                'error': 'User not found',
                'timestamp': datetime.now().isoformat()
            }
        
        # Parse legacy colon-separated format
        parts = legacy_data.split(':')
        if len(parts) >= 8:
            user_data = {
                'id': int(parts[1]),
                'name': parts[3],
                'email': parts[5],
                'created_at': parts[7] + 'T00:00:00Z'  # Convert to ISO format
            }
            return {
                'success': True,
                'data': user_data,
                'timestamp': datetime.now().isoformat()
            }
        
        return {
            'success': False,
            'error': 'Invalid data format',
            'timestamp': datetime.now().isoformat()
        }
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert modern JSON format to legacy format and save"""
        # Convert modern format to legacy format
        legacy_format = f"ID:0:NAME:{user_data.get('name', '')}:EMAIL:{user_data.get('email', '')}:CREATED:{datetime.now().strftime('%Y-%m-%d')}"
        
        success = self._legacy_db.save_user_data_legacy_format(legacy_format)
        
        if success:
            return {
                'success': True,
                'data': user_data,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'success': False,
                'error': 'Failed to save user',
                'timestamp': datetime.now().isoformat()
            }

class ModernToLegacyAdapter:
    """
    Adapter that makes Modern API compatible with Legacy Database interface
    Interview question: How to adapt modern system to legacy interface?
    """
    def __init__(self, modern_api: ModernAPI):
        self._modern_api = modern_api
    
    def fetch_user_data_legacy_format(self, user_id: int) -> str:
        """Convert modern JSON format to legacy colon-separated format"""
        response = self._modern_api.get_user(user_id)
        
        if not response['success']:
            return "USER_NOT_FOUND"
        
        user_data = response['data']
        # Convert ISO timestamp to simple date
        created_date = user_data['created_at'][:10]  # Extract YYYY-MM-DD
        
        return f"ID:{user_data['id']}:NAME:{user_data['name']}:EMAIL:{user_data['email']}:CREATED:{created_date}"
    
    def save_user_data_legacy_format(self, data: str) -> bool:
        """Convert legacy format to modern JSON and save"""
        try:
            parts = data.split(':')
            if len(parts) >= 8:
                user_data = {
                    'name': parts[3],
                    'email': parts[5]
                }
                response = self._modern_api.create_user(user_data)
                return response['success']
        except (ValueError, IndexError):
            pass
        return False

# ============================================================================
# UNIVERSAL ADAPTER (Interview focus: handling multiple formats)
# ============================================================================

class UniversalDataAdapter:
    """
    Universal adapter that can handle multiple data formats
    Interview question: How to handle different data formats in one adapter?
    """
    def __init__(self):
        self._format_handlers = {
            'json': self._handle_json,
            'xml': self._handle_xml,
            'csv': self._handle_csv,
            'legacy': self._handle_legacy
        }
    
    def convert_data(self, data: str, from_format: str, to_format: str) -> str:
        """Convert data between different formats"""
        if from_format not in self._format_handlers:
            raise ValueError(f"Unsupported source format: {from_format}")
        
        if to_format not in self._format_handlers:
            raise ValueError(f"Unsupported target format: {to_format}")
        
        # Parse from source format
        parsed_data = self._format_handlers[from_format](data)
        
        # Convert to target format
        return self._format_handlers[to_format](parsed_data, reverse=True)
    
    def _handle_json(self, data: Union[str, Dict], reverse: bool = False) -> Union[Dict, str]:
        if reverse:
            return json.dumps(data, indent=2)
        return json.loads(data)
    
    def _handle_xml(self, data: Union[str, Dict], reverse: bool = False) -> Union[Dict, str]:
        if reverse:
            root = ET.Element("user")
            for key, value in data.items():
                child = ET.SubElement(root, key)
                child.text = str(value)
            return ET.tostring(root, encoding='unicode')
        else:
            root = ET.fromstring(data)
            return {child.tag: child.text for child in root}
    
    def _handle_csv(self, data: Union[str, Dict], reverse: bool = False) -> Union[Dict, str]:
        if reverse:
            return f"id,name,email\n{data['id']},{data['name']},{data['email']}"
        else:
            lines = data.strip().split('\n')
            headers = lines[0].split(',')
            values = lines[1].split(',')
            return dict(zip(headers, values))
    
    def _handle_legacy(self, data: Union[str, Dict], reverse: bool = False) -> Union[Dict, str]:
        if reverse:
            return f"ID:{data['id']}:NAME:{data['name']}:EMAIL:{data['email']}"
        else:
            parts = data.split(':')
            return {
                'id': int(parts[1]),
                'name': parts[3],
                'email': parts[5]
            }

# ============================================================================
# CLIENT CODE
# ============================================================================

class UserServiceClient:
    """Client that works with UserService interface"""
    def __init__(self, user_service: UserService):
        self._user_service = user_service
    
    def display_user(self, user_id: int):
        """Display user information"""
        response = self._user_service.get_user(user_id)
        
        if response['success']:
            user = response['data']
            print(f"👤 User ID: {user['id']}")
            print(f"   Name: {user['name']}")
            print(f"   Email: {user['email']}")
            print(f"   Created: {user['created_at']}")
        else:
            print(f"❌ Error: {response['error']}")
    
    def create_user(self, name: str, email: str):
        """Create a new user"""
        user_data = {'name': name, 'email': email}
        response = self._user_service.create_user(user_data)
        
        if response['success']:
            print(f"✅ User created successfully: {response['data']['name']}")
        else:
            print(f"❌ Failed to create user: {response['error']}")

def demo_adapter_interview():
    """
    🎯 INTERVIEW DEMO: Adapter Pattern
    Demonstrates legacy integration and bidirectional adaptation
    """
    print("\n" + "="*60)
    print("🚀 ADAPTER PATTERN - INTERVIEW DEMO")
    print("="*60)
    
    print("\n💡 Common interview questions:")
    print("1. How to integrate with a legacy system you can't modify?")
    print("2. What if you need two-way adaptation?")
    print("3. How to handle different data formats?")
    print("4. How to make incompatible interfaces work together?")
    
    # ========================================================================
    # LEGACY TO MODERN ADAPTER DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🔄 LEGACY TO MODERN ADAPTER DEMO")
    print("="*50)
    
    # Create systems
    legacy_db = LegacyDatabase()
    modern_api = ModernAPI()
    
    # Create adapter
    legacy_adapter = LegacyToModernAdapter(legacy_db)
    
    # Use adapter with modern client
    client = UserServiceClient(legacy_adapter)
    
    print("\n📖 Reading users from legacy system via adapter:")
    client.display_user(1)
    client.display_user(2)
    client.display_user(999)  # Non-existent user
    
    print("\n✏️ Creating user in legacy system via adapter:")
    client.create_user("Bob Wilson", "bob@example.com")
    
    # ========================================================================
    # MODERN TO LEGACY ADAPTER DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🔄 MODERN TO LEGACY ADAPTER DEMO")
    print("="*50)
    
    # Create reverse adapter
    modern_adapter = ModernToLegacyAdapter(modern_api)
    
    print("\n📖 Reading users from modern system in legacy format:")
    print(f"User 1: {modern_adapter.fetch_user_data_legacy_format(1)}")
    print(f"User 2: {modern_adapter.fetch_user_data_legacy_format(2)}")
    print(f"User 999: {modern_adapter.fetch_user_data_legacy_format(999)}")
    
    print("\n✏️ Creating user in modern system via legacy format:")
    legacy_data = "ID:0:NAME:Alice Johnson:EMAIL:alice@example.com:CREATED:2023-12-01"
    success = modern_adapter.save_user_data_legacy_format(legacy_data)
    print(f"Success: {success}")
    
    # ========================================================================
    # UNIVERSAL DATA ADAPTER DEMO
    # ========================================================================
    print("\n" + "="*50)
    print("🌐 UNIVERSAL DATA ADAPTER DEMO")
    print("="*50)
    
    universal_adapter = UniversalDataAdapter()
    
    # Sample data in different formats
    json_data = '{"id": 1, "name": "John Doe", "email": "john@example.com"}'
    xml_data = '<user><id>1</id><name>John Doe</name><email>john@example.com</email></user>'
    csv_data = 'id,name,email\n1,John Doe,john@example.com'
    legacy_data = 'ID:1:NAME:John Doe:EMAIL:john@example.com'
    
    print("\n🔄 Converting between different formats:")
    
    # JSON to XML
    xml_result = universal_adapter.convert_data(json_data, 'json', 'xml')
    print(f"JSON → XML:\n{xml_result}")
    
    # XML to CSV
    csv_result = universal_adapter.convert_data(xml_data, 'xml', 'csv')
    print(f"\nXML → CSV:\n{csv_result}")
    
    # CSV to Legacy
    legacy_result = universal_adapter.convert_data(csv_data, 'csv', 'legacy')
    print(f"\nCSV → Legacy:\n{legacy_result}")
    
    # Legacy to JSON
    json_result = universal_adapter.convert_data(legacy_data, 'legacy', 'json')
    print(f"\nLegacy → JSON:\n{json_result}")

if __name__ == "__main__":
    demo_adapter_interview()

