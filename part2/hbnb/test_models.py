#!/usr/bin/env python3
"""
Test script for HBnB Business Logic Models

This script tests the core business logic classes (User, Place, Review, Amenity)
and their relationships according to the requirements.
"""

import sys
import traceback
from datetime import datetime


def test_user_creation():
    """Test User class creation and validation."""
    print("Testing User Class Creation...")
    
    try:
        from app.models.user import User
        
        # Test valid user creation
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        assert user.first_name == "John"
        assert user.last_name == "Doe"  
        assert user.email == "john.doe@example.com"
        assert user.is_admin is False  # Default value
        assert hasattr(user, 'id')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')
        
        # Test admin user
        admin = User(first_name="Admin", last_name="User", email="admin@example.com", is_admin=True)
        assert admin.is_admin is True
        
        print("✅ User creation test passed!")
        
        # Test user validation
        try:
            User("", "Doe", "john@example.com")
            assert False, "Should have raised ValueError for empty first name"
        except ValueError:
            pass
        
        try:
            User("John", "Doe", "invalid-email")
            assert False, "Should have raised ValueError for invalid email"
        except ValueError:
            pass
        
        print("✅ User validation test passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ User test failed: {e}")
        traceback.print_exc()
        return False


def test_amenity_creation():
    """Test Amenity class creation and validation."""
    print("\nTesting Amenity Class Creation...")
    
    try:
        from app.models.amenity import Amenity
        
        # Test valid amenity creation
        amenity = Amenity(name="Wi-Fi")
        assert amenity.name == "Wi-Fi"
        assert hasattr(amenity, 'id')
        assert hasattr(amenity, 'created_at')
        assert hasattr(amenity, 'updated_at')
        
        print("✅ Amenity creation test passed!")
        
        # Test amenity validation
        try:
            Amenity("")
            assert False, "Should have raised ValueError for empty name"
        except ValueError:
            pass
        
        try:
            Amenity("A" * 51)  # Too long
            assert False, "Should have raised ValueError for name too long"
        except ValueError:
            pass
        
        print("✅ Amenity validation test passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Amenity test failed: {e}")
        traceback.print_exc()
        return False


def test_place_creation():
    """Test Place class creation and relationships."""
    print("\nTesting Place Class Creation and Relationships...")
    
    try:
        from app.models.user import User
        from app.models.place import Place
        from app.models.amenity import Amenity
        
        # Create a user (owner)
        owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        
        # Create a place
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )
        
        assert place.title == "Cozy Apartment"
        assert place.description == "A nice place to stay"
        assert place.price == 100.0
        assert place.latitude == 37.7749
        assert place.longitude == -122.4194
        assert place.owner == owner
        assert len(place.reviews) == 0
        assert len(place.amenities) == 0
        
        print("✅ Place creation test passed!")
        
        # Test adding amenities
        wifi = Amenity("Wi-Fi")
        parking = Amenity("Parking")
        
        place.add_amenity(wifi)
        place.add_amenity(parking)
        
        assert len(place.amenities) == 2
        assert wifi in place.amenities
        assert parking in place.amenities
        
        print("✅ Place-Amenity relationship test passed!")
        
        # Test place validation
        try:
            Place("", "desc", 100, 37.7749, -122.4194, owner)
            assert False, "Should have raised ValueError for empty title"
        except ValueError:
            pass
        
        try:
            Place("Title", "desc", -100, 37.7749, -122.4194, owner)
            assert False, "Should have raised ValueError for negative price"
        except ValueError:
            pass
        
        try:
            Place("Title", "desc", 100, 95.0, -122.4194, owner)
            assert False, "Should have raised ValueError for invalid latitude"
        except ValueError:
            pass
        
        print("✅ Place validation test passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Place test failed: {e}")
        traceback.print_exc()
        return False


def test_review_creation():
    """Test Review class creation and business logic."""
    print("\nTesting Review Class Creation and Business Logic...")
    
    try:
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        
        # Create users
        owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        reviewer = User(first_name="Bob", last_name="Johnson", email="bob.johnson@example.com")
        
        # Create a place
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )
        
        # Create a review
        review = Review(
            text="Great stay!",
            rating=5,
            place=place,
            user=reviewer
        )
        
        assert review.text == "Great stay!"
        assert review.rating == 5
        assert review.place == place
        assert review.user == reviewer
        
        # Add review to place
        place.add_review(review)
        assert len(place.reviews) == 1
        assert place.reviews[0] == review
        
        print("✅ Review creation and relationship test passed!")
        
        # Test business logic: owner cannot review own place
        try:
            owner_review = Review(
                text="My own place is great!",
                rating=5,
                place=place,
                user=owner  # Owner trying to review own place
            )
            assert False, "Should have raised ValueError for owner reviewing own place"
        except ValueError as e:
            assert "cannot review their own places" in str(e)
        
        print("✅ Review business logic validation test passed!")
        
        # Test review validation
        try:
            Review("", 5, place, reviewer)
            assert False, "Should have raised ValueError for empty text"
        except ValueError:
            pass
        
        try:
            Review("Great!", 6, place, reviewer)
            assert False, "Should have raised ValueError for rating > 5"
        except ValueError:
            pass
        
        try:
            Review("Great!", 0, place, reviewer)
            assert False, "Should have raised ValueError for rating < 1"
        except ValueError:
            pass
        
        print("✅ Review validation test passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Review test failed: {e}")
        traceback.print_exc()
        return False


def test_model_updates():
    """Test model update functionality."""
    print("\nTesting Model Update Functionality...")
    
    try:
        from app.models.user import User
        from app.models.place import Place
        from app.models.amenity import Amenity
        
        # Test user update
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        original_updated_at = user.updated_at
        
        user.update({
            'first_name': 'Johnny',
            'last_name': 'Smith'
        })
        
        assert user.first_name == 'Johnny'
        assert user.last_name == 'Smith'
        assert user.updated_at > original_updated_at
        
        # Test amenity update
        amenity = Amenity("Wi-Fi")
        amenity.update({'name': 'High-Speed Wi-Fi'})
        assert amenity.name == 'High-Speed Wi-Fi'
        
        # Test place update
        place = Place("Title", "Desc", 100.0, 37.7749, -122.4194, user)
        place.update({
            'title': 'New Title',
            'price': 150.0
        })
        assert place.title == 'New Title'
        assert place.price == 150.0
        
        print("✅ Model update test passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Model update test failed: {e}")
        traceback.print_exc()
        return False


def test_model_serialization():
    """Test model to_dict functionality."""
    print("\nTesting Model Serialization...")
    
    try:
        from app.models.user import User
        from app.models.amenity import Amenity
        
        # Test user serialization
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        user_dict = user.to_dict()
        
        assert 'id' in user_dict
        assert user_dict['first_name'] == 'John'
        assert user_dict['last_name'] == 'Doe'
        assert user_dict['email'] == 'john@example.com'
        assert 'created_at' in user_dict
        assert 'updated_at' in user_dict
        
        # Test amenity serialization
        amenity = Amenity("Wi-Fi")
        amenity_dict = amenity.to_dict()
        
        assert 'id' in amenity_dict
        assert amenity_dict['name'] == 'Wi-Fi'
        assert 'created_at' in amenity_dict
        assert 'updated_at' in amenity_dict
        
        print("✅ Model serialization test passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Model serialization test failed: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all model tests."""
    print("=" * 60)
    print("🧪 HBnB BUSINESS LOGIC MODELS TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_user_creation,
        test_amenity_creation,
        test_place_creation,
        test_review_creation,
        test_model_updates,
        test_model_serialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your business logic models are working correctly.")
        print("\n✅ Ready for next steps:")
        print("   1. Implement the Persistence Layer (Repository Pattern)")
        print("   2. Create the Facade Service Layer")
        print("   3. Build the API endpoints")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. Please fix the issues above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
