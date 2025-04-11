from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_volume_percentage(value):
    """
    Validate that volume percentage is between 0 and 100.
    
    Args:
        value (float): The volume percentage to validate
        
    Raises:
        ValidationError: If the value is less than 0 or greater than 100
    """
    if value < 0:
        raise ValidationError(
            _('%(value)s is less than 0. Volume percentage must be non-negative.'),
            params={'value': value},
        )
    if value > 100:
        raise ValidationError(
            _('%(value)s is greater than 100. Volume percentage cannot exceed 100%.'),
            params={'value': value},
        )

