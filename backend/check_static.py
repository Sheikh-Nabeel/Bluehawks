#!/usr/bin/env python
"""
Static Files Checker for Bluehawks Security Services
This script checks for missing static files and path mismatches.
"""

import os
import re
from pathlib import Path

# Django setup
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluehawks.settings_production')
django.setup()

from django.conf import settings
from django.template.loader import get_template
from django.template import Template, Context
from django.contrib.staticfiles.finders import find

def find_static_references():
    """Find all static file references in templates."""
    static_refs = []
    
    # Common template directories
    template_dirs = [
        '../frontend/templates',
        'templates'
    ]
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Find all static references
                                static_pattern = r'{%\s*static\s+[\'"]([^\'"]+)[\'"]\s*%}'
                                matches = re.findall(static_pattern, content)
                                for match in matches:
                                    static_refs.append({
                                        'file': file_path,
                                        'static_path': match,
                                        'full_path': os.path.join(settings.STATICFILES_DIRS[0], match) if settings.STATICFILES_DIRS else None
                                    })
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
    
    return static_refs

def check_static_files():
    """Check which static files exist and which are missing."""
    print("🔍 Checking Static Files...")
    print("=" * 50)
    
    static_refs = find_static_references()
    
    missing_files = []
    existing_files = []
    
    for ref in static_refs:
        static_path = ref['static_path']
        file_path = ref['full_path']
        
        if file_path and os.path.exists(file_path):
            existing_files.append(static_path)
        else:
            missing_files.append({
                'static_path': static_path,
                'template_file': ref['file']
            })
    
    print(f"✅ Found {len(existing_files)} existing static files")
    print(f"❌ Found {len(missing_files)} missing static files")
    
    if missing_files:
        print("\n❌ Missing Static Files:")
        print("-" * 30)
        for missing in missing_files:
            print(f"  {missing['static_path']} (referenced in {os.path.basename(missing['template_file'])})")
    
    print("\n✅ Existing Static Files:")
    print("-" * 30)
    for existing in sorted(existing_files):
        print(f"  {existing}")
    
    return missing_files, existing_files

def check_static_directories():
    """Check static file directories structure."""
    print("\n📁 Static Directories Structure:")
    print("=" * 50)
    
    for static_dir in settings.STATICFILES_DIRS:
        if os.path.exists(static_dir):
            print(f"\n📂 {static_dir}:")
            for root, dirs, files in os.walk(static_dir):
                level = root.replace(static_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files[:10]:  # Show first 10 files
                    print(f"{subindent}{file}")
                if len(files) > 10:
                    print(f"{subindent}... and {len(files) - 10} more files")

if __name__ == '__main__':
    try:
        missing, existing = check_static_files()
        check_static_directories()
        
        if missing:
            print(f"\n🚨 {len(missing)} static files are missing!")
            print("Please check the file paths and ensure all referenced files exist.")
        else:
            print("\n🎉 All static files are present!")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc() 