"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
from google.cloud import translate_v2 as translate
translate_client = translate.Client()


# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
result = translate_client.translate(
    'ana are mere', target_language='eng', source_language='ro')

print(u'Text: {}'.format(result['input']))
print(u'Translation: {}'.format(result['translatedText']))
