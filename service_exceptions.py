"""Base class for other exceptions"""
class Error(Exception):
    pass

"""Raised when no permissions are granted for letter soup generation"""
class NoPermissions(Error):
    pass

"""Raised when non existent soup id is used"""
class InvalidSoupId(Error):
    pass
