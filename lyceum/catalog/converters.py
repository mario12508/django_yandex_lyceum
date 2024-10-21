class PositiveIntegerConverter:
    regex = r"0*[1-9]\d*"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return str(value)


__all__ = ["PositiveIntegerConverter"]
