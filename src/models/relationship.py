from .timeline_component import TimelineComponent

class Relationship:
    STANDARD_TYPES = {
        "CAUSE_EFFECT", "CONTEMPORANEOUS", "PRECEDES", 
        "FOLLOWS", "INCLUDES", "EXCLUDES"
    }

    def __init__(self, id: str, from_component: TimelineComponent, 
                 to_component: TimelineComponent, relationship_type: str):
        self.id = id
        self.from_component = from_component
        self.to_component = to_component
        self._type = None
        self.type = relationship_type  # Using the setter

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        # Clean up the value
        clean_value = value.upper().replace("-", "_")
        
        # If it's a standard type, validate it
        if clean_value in self.STANDARD_TYPES:
            self._type = clean_value
        else:
            # For custom types, store the original value (not uppercased)
            self._type = value

    def validate_relationship(self):
        # Only validate INCLUDES relationship type
        if self.type == "INCLUDES":
            if not isinstance(self.from_component, Period):
                raise ValueError("'INCLUDES' relationship requires a Period as the 'from' component")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "from": self.from_component.id,
            "to": self.to_component.id,
            "type": self.type
        } 