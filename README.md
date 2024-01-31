# Finnish Passphrase Generator

This is a project in implementing exactly what it says in the title – a program for generating passphrases in Finnish. The project uses the [Kotus Finnish word list](http://kaino.kotus.fi/sanat/nykysuomi/), which contains a total of 94,110 word entries. The word list also contains morphological information on the correct consonant gradation and inflection patterns for the words. The passphrase generator leverages this information, and randomly inflects the words. Theoretically, this enables using the Finnish language's naturally complex morphology to create passphrases with more entropy. In practical terms, I have in no way verified that this is indeed the case, so as you'd do with any random program you find on the Internet, use at your own risk.

This is a work in progress. Currently, I have implemented inflection patterns 1–15 (out of 78), and the generator uses 16,457 of the 94,110 word entries.
