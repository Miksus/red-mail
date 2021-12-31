

class EmailAddress:
    """Utility class to represent email
    address and access the organization/
    names in it.

    https://en.wikipedia.org/wiki/Email_address
    """
    def __init__(self, address:str):
        self.address = address


    def organization(self):
        return self.address.split("@")

    def __str__(self):
        return self.address

# From official specs
    @property
    def parts(self):
        return self.address.split("@")

    @property
    def local_part(self):
        return self.parts[0]

    @property
    def domain(self):
        return self.parts[1]

# Checks
    @property
    def is_personal(self):
        "Whether the email address seems to belong to a person"
        return len(self.local_part.split(".")) == 2

# More of typical conventions
    @property
    def top_level_domain(self):
        """Get top level domain (if possible)
        
        Ie. john.smith@en.example.com --> com"""
        domain = self.domain.split(".")
        return domain[-1] if len(domain) > 1 else None

    @property
    def second_level_domain(self):
        """Get second level domain (if possible)
        
        Ie. john.smith@en.example.com --> example"""
        domain = self.domain.split(".")
        return domain[-2] if len(domain) > 1 else None

    @property
    def full_name(self):
        """Get full name of the sender (if possible)
        
        Ie. john.smith@en.example.com --> 'john smith'"""
        if self.is_personal:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.local_part.capitalize()

    @property
    def first_name(self):
        """Get first name of the sender (if possible)
        
        Ie. john.smith@en.example.com --> John"""
        if self.is_personal:
            return self.local_part.split(".")[0].capitalize()

    @property
    def last_name(self):
        """Get last name of the sender (if possible)
        
        Ie. john.smith@en.example.com --> Smith"""
        if self.is_personal:
            return self.local_part.split(".")[1].capitalize()

# Aliases
    @property
    def organization(self):
        """This is alias for second level domain."""
        return self.second_level_domain