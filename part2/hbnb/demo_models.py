#!/usr/bin/env python3
"""
HBnB Business Logic Models Demonstration

This script demonstrates the core business logic models and their
relationships in action.
"""

def main():
    print("🏨 HBnB Business Logic Models Demonstration")
    print("=" * 50)
    
    # Import all models
    from app.models import User, Place, Review, Amenity
    
    print("\n1. Creating Users...")
    # Create users
    alice = User(
        first_name="Alice", 
        last_name="Johnson", 
        email="alice.johnson@example.com",
        is_admin=False
    )
    
    bob = User(
        first_name="Bob", 
        last_name="Smith", 
        email="bob.smith@example.com"
    )
    
    admin = User(
        first_name="Admin", 
        last_name="User", 
        email="admin@hbnb.com",
        is_admin=True
    )
    
    print(f"✅ Created user: {alice}")
    print(f"✅ Created user: {bob}")
    print(f"✅ Created admin: {admin}")
    
    print("\n2. Creating Amenities...")
    # Create amenities
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Free Parking")
    pool = Amenity(name="Swimming Pool")
    gym = Amenity(name="Fitness Center")
    
    amenities = [wifi, parking, pool, gym]
    for amenity in amenities:
        print(f"✅ Created amenity: {amenity}")
    
    print("\n3. Creating Places...")
    # Create places
    downtown_apt = Place(
        title="Downtown Luxury Apartment",
        description="A beautiful apartment in the heart of the city with stunning views",
        price=150.00,
        latitude=37.7749,
        longitude=-122.4194,
        owner=alice
    )
    
    beach_house = Place(
        title="Cozy Beach House",
        description="Perfect getaway by the ocean with private beach access",
        price=250.00,
        latitude=36.7783,
        longitude=-119.4179,
        owner=alice
    )
    
    print(f"✅ Created place: {downtown_apt}")
    print(f"✅ Created place: {beach_house}")
    
    print("\n4. Adding Amenities to Places...")
    # Add amenities to places
    downtown_apt.add_amenity(wifi)
    downtown_apt.add_amenity(gym)
    
    beach_house.add_amenity(wifi)
    beach_house.add_amenity(parking)
    beach_house.add_amenity(pool)
    
    print(f"✅ Downtown apartment has {len(downtown_apt.amenities)} amenities")
    print(f"✅ Beach house has {len(beach_house.amenities)} amenities")
    
    print("\n5. Creating Reviews...")
    # Create reviews (Bob reviews Alice's places)
    review1 = Review(
        text="Amazing place! The view was spectacular and everything was clean.",
        rating=5,
        place=downtown_apt,
        user=bob
    )
    
    review2 = Review(
        text="Great location but could use better WiFi in the bedroom.",
        rating=4,
        place=downtown_apt,
        user=bob
    )
    
    review3 = Review(
        text="Perfect beach getaway! Loved the private beach access.",
        rating=5,
        place=beach_house,
        user=bob
    )
    
    # Add reviews to places
    downtown_apt.add_review(review1)
    downtown_apt.add_review(review2)
    beach_house.add_review(review3)
    
    print(f"✅ Created review: {review1}")
    print(f"✅ Created review: {review2}")
    print(f"✅ Created review: {review3}")
    
    print("\n6. Demonstrating Business Logic...")
    # Try to create an invalid review (owner reviewing own place)
    try:
        invalid_review = Review(
            text="My place is amazing!",
            rating=5,
            place=downtown_apt,
            user=alice  # Alice trying to review her own place
        )
    except ValueError as e:
        print(f"✅ Business logic validation works: {e}")
    
    print("\n7. Data Summary...")
    print(f"📊 Users created: 3")
    print(f"📊 Places created: 2")
    print(f"📊 Reviews created: 3")
    print(f"📊 Amenities created: 4")
    
    print(f"\n🏠 Downtown Apartment:")
    print(f"   - Owner: {downtown_apt.owner.first_name} {downtown_apt.owner.last_name}")
    print(f"   - Price: ${downtown_apt.price}/night")
    print(f"   - Reviews: {len(downtown_apt.reviews)}")
    print(f"   - Amenities: {[a.name for a in downtown_apt.amenities]}")
    
    print(f"\n🏖️ Beach House:")
    print(f"   - Owner: {beach_house.owner.first_name} {beach_house.owner.last_name}")
    print(f"   - Price: ${beach_house.price}/night")
    print(f"   - Reviews: {len(beach_house.reviews)}")
    print(f"   - Amenities: {[a.name for a in beach_house.amenities]}")
    
    print("\n8. Testing Model Updates...")
    # Test updating models
    print(f"📝 Updating Alice's last name...")
    alice.update({'last_name': 'Johnson-Smith'})
    print(f"✅ Updated: {alice}")
    
    print(f"📝 Updating downtown apartment price...")
    downtown_apt.update({'price': 175.00})
    print(f"✅ Updated price to ${downtown_apt.price}/night")
    
    print("\n🎉 All models working correctly!")
    print("✅ Ready for Persistence Layer implementation")
    print("✅ Ready for Facade Service Layer implementation")
    print("✅ Ready for API endpoint implementation")


if __name__ == "__main__":
    main()
