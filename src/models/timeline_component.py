class TimelineComponent:
    def __init__(self, id: str, title: str, importance: str = "MEDIUM"):
        self.id = id
        self.title = title
        self._importance = None
        self.importance = importance  # Using the setter

    @property
    def importance(self) -> str:
        return self._importance

    @importance.setter
    def importance(self, value: str):
        valid_importance = ["HIGH", "MEDIUM", "LOW"]
        if value.upper() not in valid_importance:
            raise ValueError(f"Importance must be one of {valid_importance}")
        self._importance = value.upper()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "importance": self.importance
        } 