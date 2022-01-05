

class EmailAddress:
    """Format class for email addresses.

    This class is useful manipulate the 
    addresses in templates with minimal
    effort. More about email addresses from 
    `Wikipedia <https://en.wikipedia.org/wiki/Email_address>`_.

    Parameters
    ----------
    address : str
        Email address as string.


    """
    def __init__(self, address:str):
        self.address = address

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
        "bool: Domain of the address"
        return self.parts[1]

    @property
    def is_personal(self):
        "bool: Whether the email address seems to belong to a person"
        return len(self.local_part.split(".")) == 2

# More of typical conventions
    @property
    def top_level_domain(self):
        """Get top level domain (if possible)
        
        Ie. john.smith@en.example.com --> com"""
        domain = self.domain.split(".")
        return '.' + domain[-1] if len(domain) > 1 else None

    @property
    def second_level_domain(self):
        """Get second level domain (if possible)
        
        Ie. john.smith@en.example.com --> example"""
        domain = self.domain.split(".")
        return domain[-2] if len(domain) > 1 else None

    @property
    def full_name(self) -> str:
        """str: Full name of the address
        """
        if self.is_personal:
            return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
        else:
            return self.local_part.capitalize()

    @property
    def first_name(self) -> str:
        """str: First name of the address (if in typical form)"""
        if self.is_personal:
            return self.local_part.split(".")[0].capitalize()

    @property
    def last_name(self) -> str:
        """str: Last name of the address (if in typical form)"""
        if self.is_personal:
            return self.local_part.split(".")[1].capitalize()

# Aliases
    @property
    def organization(self) -> str:
        """str: Organization"""
        return self.second_level_domain.capitalize()