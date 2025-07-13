from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the Repository pattern."""
    
    def __init__(self, db_session, model_class):
        """
        Initialize the repository with database session and model class.
        
        Args:
            db_session: SQLAlchemy database session
            model_class: SQLAlchemy model class
        """
        self.db = db_session
        self.model = model_class

    def add(self, obj):
        """Add an object to the database."""
        self.db.session.add(obj)
        self.db.session.commit()
        return obj

    def get(self, obj_id):
        """Get an object by ID."""
        return self.db.session.get(self.model, obj_id)

    def get_all(self):
        """Get all objects of this type."""
        return self.db.session.query(self.model).all()

    def update(self, obj_id, data):
        """Update an object with new data."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object by ID."""
        obj = self.get(obj_id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute value."""
        return self.db.session.query(self.model).filter(
            getattr(self.model, attr_name) == attr_value
        ).first()