import magic
from rest_framework.exceptions import ValidationError


def obtain_file_buffer(file_buffer):
    """
    Args:
        file_buffer: file buffer.

    Returns:
        the bytes of the file.
    """
    file_buffer.seek(0)
    return file_buffer.read()


def validate_file_buffer(file_buffer, expected_files_types):
    """
    Validates the file type according to the list of reported types.

    Args:
        file_buffer: file buffer.
        expected_files_types: list of types.

    Returns:
        bool

    Raises:
        ValidationError
    """
    file_type = magic.from_buffer(file_buffer, mime=True)

    if file_type not in expected_files_types:
        raise ValidationError(
            f'Invalid file type. Expected {", ".join(expected_files_types)} file types, got {file_type}.')

    return True
