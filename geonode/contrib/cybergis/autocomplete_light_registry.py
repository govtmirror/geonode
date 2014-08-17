import autocomplete_light
from models import CyberGISClient

autocomplete_light.register(
    CyberGISClient,
    search_fields=['^title'],
    autocomplete_js_attributes={
        'placeholder': 'CyberGIS Client name..',
    },
)
