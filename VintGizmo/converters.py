from django.urls import register_converter
from decimal import Decimal

class DecimalConverter:
    regex = r'\d+\.\d+|\d+'

    def to_python(self, value):
        return Decimal(value)

    def to_url(self, value):
        return str(value)

# Register the converter
register_converter(DecimalConverter, 'decimal')
