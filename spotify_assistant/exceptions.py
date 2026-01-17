class CSVError(Exception):
    """Base exception for CSV operations."""


class CSVFormatError(CSVError):
    """Raised when CSV file has invalid format or headers."""


class DuplicateTrackPairError(CSVError):
    """Raised when attempting to add a duplicate track pair."""
