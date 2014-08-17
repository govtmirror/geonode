from modeltranslation.translator import translator, TranslationOptions
from .models import CyberGISClient


class CyberGISClientTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'abstract',
        'purpose',
        'constraints_other',
        'supplemental_information',
        'distribution_description',
        'data_quality_statement',
    )

translator.register(CyberGISClient, CyberGISClientTranslationOptions)
