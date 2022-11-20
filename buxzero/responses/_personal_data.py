from ._response import Response

class PersonalData(Response):
    """
    Personal Data endpoint of bux. Storing private account login data.
    """
    @property
    def email(self) -> str:
        return self['email']

    @property
    def first_name(self) -> str:
        return self['firstName']

    @property
    def last_name(self) -> str:
        return self['lastName']