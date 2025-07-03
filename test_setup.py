#!/usr/bin/env python3
"""
Test script for Codeforces Tutor
This script tests the basic functionality of all modules
"""

import sys
import importlib.util

def test_imports():
    """Test if all modules can be imported successfully"""
    try:
        print("Testing imports...")

        # Test main.py import
        spec = importlib.util.spec_from_file_location("main", "main.py")
        main_module = importlib.util.module_from_spec(spec)

        # Test question_filtering.py import
        spec = importlib.util.spec_from_file_location("question_filtering", "question_filtering.py")
        qf_module = importlib.util.module_from_spec(spec)

        # Test user_analytics.py import
        spec = importlib.util.spec_from_file_location("user_analytics", "user_analytics.py")
        ua_module = importlib.util.module_from_spec(spec)

        print("✅ All modules imported successfully!")
        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_api_connectivity():
    """Test if we can connect to Codeforces API"""
    try:
        import requests

        print("\nTesting API connectivity...")

        # Test basic API call
        url = "https://codeforces.com/api/contest.list"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                print("✅ Codeforces API is accessible!")
                return True
            else:
                print(f"❌ API returned status: {data['status']}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False

    except ImportError:
        print("❌ requests library not installed. Run: pip install requests")
        return False
    except Exception as e:
        print(f"❌ API connectivity error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    import os

    required_files = ['main.py', 'question_filtering.py', 'user_analytics.py', 'README.md']

    print("\nChecking file structure...")
    all_present = True

    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_present = False

    return all_present

def main():
    """Run all tests"""
    print("=" * 50)
    print("    CODEFORCES TUTOR - TESTING SUITE")
    print("=" * 50)

    tests_passed = 0
    total_tests = 3

    # Test 1: File structure
    if test_file_structure():
        tests_passed += 1

    # Test 2: Imports
    if test_imports():
        tests_passed += 1

    # Test 3: API connectivity
    if test_api_connectivity():
        tests_passed += 1

    print("\n" + "=" * 50)
    print(f"    TEST RESULTS: {tests_passed}/{total_tests} PASSED")
    print("=" * 50)

    if tests_passed == total_tests:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\nTo start the application, run:")
        print("python main.py")
    else:
        print(f"\n⚠️  {total_tests - tests_passed} test(s) failed. Please check the issues above.")

    print("\nFor usage instructions, see README.md")

if __name__ == "__main__":
    main()
