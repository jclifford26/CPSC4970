class IdentifiedObject:

    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        if self is other:
            return True
        return isinstance(other, type(self)) and self.oid == other.oid

    def __hash__(self):
        return hash(self.oid)

    def __str__(self):
        return f"IdentifiedObject(oid={self.oid})"


class DuplicateOid(Exception):

    def __init__(self, oid):
        self.oid = oid
        super().__init__(f"Duplicate OID: {oid}")

    def __str__(self):
        return f"Duplicate OID: {self.oid}"


class DuplicateEmail(Exception):

    def __init__(self, email):
        self.email = email
        super().__init__(f"Duplicate Email: {email}")

    def __str__(self):
        return f"Duplicate Email: {self.email}"
