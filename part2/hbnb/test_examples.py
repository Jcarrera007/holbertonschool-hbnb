#!/usr/bin/env python3
"""
Individual test examples for the HBnB Business Logic Models.

These are simple test examples as mentioned in the requirements
to validate that the classes are functioning as expected.
"""

def test_user_creation():
    """Test User creation as shown in requirements."""
    from app.models.user import User

    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")


def test_place_creation():
    """Test Place creation with relationships as shown in requirements."""
    from app.models.place import Place
    from app.models.user import User
    from app.models.review import Review

    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Adding a review
    reviewer = User(first_name="Bob", last_name="Johnson", email="bob.johnson@example.com")
    review = Review(text="Great stay!", rating=5, place=place, user=reviewer)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")


def test_amenity_creation():
    """Test Amenity creation as shown in requirements."""
    from app.models.amenity import Amenity

    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")


if __name__ == "__main__":
    print("Running individual test examples...")
    test_user_creation()
    test_place_creation()
    test_amenity_creation()
    print("All individual tests passed!")
