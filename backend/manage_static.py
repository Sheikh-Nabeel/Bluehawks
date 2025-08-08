#!/usr/bin/env python
"""
Static file management script for Bluehawks Security Services
Handles static file collection and organization for frontend/backend structure
"""

import os
import sys
import shutil
from pathlib import Path

def setup_static_files():
    """Setup static files for the frontend/backend structure"""
    
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent
    frontend_static = project_root / 'frontend' / 'static'
    backend_static = Path(__file__).resolve().parent / 'static'
    staticfiles_dir = Path(__file__).resolve().parent / 'staticfiles'
    
    print("🔄 Setting up static files for frontend/backend structure...")
    
    # Check if frontend static directory exists
    if not frontend_static.exists():
        print(f"❌ Frontend static directory not found: {frontend_static}")
        return False
    
    # Create backend static directory if it doesn't exist
    backend_static.mkdir(exist_ok=True)
    
    # Create staticfiles directory if it doesn't exist
    staticfiles_dir.mkdir(exist_ok=True)
    
    print(f"✅ Frontend static directory: {frontend_static}")
    print(f"✅ Backend static directory: {backend_static}")
    print(f"✅ Static files directory: {staticfiles_dir}")
    
    return True

def collect_static_files():
    """Collect static files using Django's collectstatic command"""
    
    print("\n📦 Collecting static files...")
    
    # Change to backend directory
    backend_dir = Path(__file__).resolve().parent
    os.chdir(backend_dir)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluehawks.settings')
    
    try:
        import django
        django.setup()
        
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("✅ Static files collected successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")
        return False

def verify_static_structure():
    """Verify the static file structure is correct"""
    
    project_root = Path(__file__).resolve().parent.parent
    frontend_static = project_root / 'frontend' / 'static'
    backend_static = Path(__file__).resolve().parent / 'static'
    staticfiles_dir = Path(__file__).resolve().parent / 'staticfiles'
    
    print("\n🔍 Verifying static file structure...")
    
    # Check frontend static files
    if frontend_static.exists():
        print(f"✅ Frontend static files: {frontend_static}")
        for item in frontend_static.iterdir():
            if item.is_dir():
                print(f"   📁 {item.name}/")
            else:
                print(f"   📄 {item.name}")
    else:
        print(f"❌ Frontend static directory missing: {frontend_static}")
    
    # Check backend static files
    if backend_static.exists():
        print(f"✅ Backend static files: {backend_static}")
        for item in backend_static.iterdir():
            if item.is_dir():
                print(f"   📁 {item.name}/")
            else:
                print(f"   📄 {item.name}")
    else:
        print(f"❌ Backend static directory missing: {backend_static}")
    
    # Check collected static files
    if staticfiles_dir.exists():
        print(f"✅ Collected static files: {staticfiles_dir}")
        for item in staticfiles_dir.iterdir():
            if item.is_dir():
                print(f"   📁 {item.name}/")
            else:
                print(f"   📄 {item.name}")
    else:
        print(f"❌ Static files directory missing: {staticfiles_dir}")

def main():
    """Main function to manage static files"""
    
    print("🚀 Bluehawks Static File Manager")
    print("=" * 40)
    
    # Setup static files
    if not setup_static_files():
        return
    
    # Collect static files
    if not collect_static_files():
        return
    
    # Verify structure
    verify_static_structure()
    
    print("\n🎉 Static file management completed!")
    print("\n📋 Summary:")
    print("   • Frontend static files: frontend/static/")
    print("   • Backend static files: backend/static/")
    print("   • Collected static files: backend/staticfiles/")
    print("   • Django serves from: frontend/static/ and backend/static/ (development)")
    print("   • Web server serves from: backend/staticfiles/ (production)")

if __name__ == "__main__":
    main()
