# /usr/bin/python3

import os
import dryscrape
import urllib.parse as Parser


DEFAULT_BABEL_LANGUAGE = 'en'
BABEL_FILE_NAME = 'messages.po'

# Make a dryscrape session
session = dryscrape.Session()

# This might change depending on one's location, or actually, at Google's whim
BASE_GOOGLE_TRANSLATE_URL = "https://translate.google.com/#view=home&op=translate"
TRANSLATED_TEXT_SELECTOR = "body > div.container > div.frame > div.page.tlid-homepage.homepage.translate-text > \
                            div.homepage-content-wrap > div.tlid-source-target.main-header > div.source-target-row > \
                            div.tlid-results-container.results-container > div.tlid-result.result-dict-wrapper > \
                            div.result.tlid-copy-target > div.text-wrap.tlid-copy-target > div > span.tlid-translation.translation > span"
                
# Mapping of ISO-639-1 codes as gotten from https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
ISO_639_1_CODES = dict(
    abkhazian='ab',
    afar='aa',
    akan='ak',
    albanian='sq',
    amharic='am',
    arabic='ar',
    aragones='an',
    armenian='hy',
    assamese='as',
    avaric='av',
    avestan='ae',
    aymara='ay',
    azerbaijani='az',
    bambara='bm',
    bashkir='ba',
    basque='eu',
    belarusian='be',
    bengali='bh', 
    bihari='bh',
    bislama='bi',
    bosnian='bs',
    breton='br',
    bulgarian='bg',
    burmese='my',
    catalan='ca',
    chamoro='ch',
    chechen='ce',
    chichewa='ny',
    chinese='zh',
    chuvash='cv',
    cornish='kw',
    corsican='co',
    cree='cr',
    croatian='hr',
    czech='cs',
    danish='da',
    divehi='dv',
    dutch='nl',
    dzongkha='dz',
    english='en',
    esperanto='eo',
    estonian='et',
    ewe='ee',
    faroese='fo',
    fijian='fj',
    finnish='fi',
    french='fr',
    fulah='ff',
    galician='gl',
    georgian='ka',
    german='de',
    greek='el',
    guarani='gn',
    gujarati='gu',
    haitian='ht',
    hausa='ha',
    hebrew='he',
    herero='hz',
    hindi='hi',
    hirimotu='ho',
    hungarian='hu',
    interlingua='ia',
    indonesian='id',
    interlingue='ie',
    irish='ga',
    igbo='ig',
    inupiaq='ik',
    ido='io',
    icelandic='is',
    italian='it',
    inuktitut='iu',
    japanese='ja',
    javanese='jv',
    kalaallisut='kl',
    kannada='kn',
    kanuri='kr',
    kasmiri='ks',
    kazakh='kk',
    khmer='km',
    kikuyu='ki',
    kinyarwanda='rw',
    kirghiz='ky',
    komi='kv',
    kongo='kg',
    korean='ko',
    kurdish='ku',
    kuanyama='kj',
    latin='la',
    luxembourgish='lb',
    ganda='lg',
    limburgan='li',
    lingala='ln',
    lao='lo',
    lithuanian='lt',
    luba_katanga='lu',
    latvian='lv',
    manx='gv',
    macedonian='mk',
    malagasy='mg',
    malay='ms',
    malayalam='ml',
    maltese='mt',
    maori='mi',
    marathi='mr',
    marshallese='mh',
    mongolian='mn',
    nauru='na',
    navajo='nv',
    north_ndebele='nd',
    nepali='ne',
    ndonga='ng',
    bokmal='nb',
    nynorsk='nn',
    norwegian='no',
    nuosu='ii',
    south_ndebele='nr',
    occitan='oc',
    ojibwa='oj',
    church_slavic='cu',
    oromo='om',
    oriya='or',
    osstian='os',
    punjabi='pa',
    pali='pi',
    persian='fa',
    polish='pl',
    pashto='ps',
    portuguese='pt',
    quechua='qu',
    romanish='rm',
    rundi='rn',
    roman='ro',
    russian='ru',
    sanskrit='sa',
    sardinian='sc',
    sindhi='sd',
    sarni='se',
    samoan='sm',
    sango='sg',
    serbian='sr',
    gaelic='gd',
    shona='sn',
    sinhala='si',
    slovak='sk',
    slovenian='sl',
    somali='so',
    sotho='st',
    spanish='es',
    sudanese='su',
    swahili='sw',
    swati='ss',
    swedish='sv',
    tamil='ta',
    telugu='te',
    tajik='tg',
    thai='th',
    tigrinya='ti',
    tibetan='bo',
    turkmen='tk',
    tagalog='tl',
    tswana='tn',
    tonga='to',
    turkish='tr',
    tsonga='ts',
    tatar='tt',
    twi='tw',
    tahitian='ty',
    uighur='ug',
    ukranian='uk',
    urdu='ur',
    uzbek='uz',
    venda='ve',
    vietnamese='vi',
    volapuk='vo',
    walloon='wa',
    welsh='cy',
    wolof='wo',
    frisian='fy',
    yiddish='yi',
    yoruba='yo',
    zhuang='za',
    zulu='zu'
)
         

def translate_po(folder):
    """
    Automatically updates `.po` files with their translated counterparts
    Leverages Google Translate
    """

    def _encode_query_parameters(s, d, t):
        """Utility to encode query parameters for use with Google Translate"""

        parameters = dict(sl=s, tl=d, text=t)
        return "&" + Parser.urlencode(parameters, quote_via=Parser.quote)

    # Walk through the `translations` folder
    for (dir, _, files) in os.walk(folder):
        lang = '' 
        # If a 'message.po' file
        if BABEL_FILE_NAME in files:

            # Copy contents
            with open(os.path.join(dir, BABEL_FILE_NAME)) as f:
                fc = f.readlines()

            # Rewrite
            with open(os.path.join(dir, BABEL_FILE_NAME), 'w+') as f:
                # Holder for a translated line. 
                tl = None 

                for index, line in enumerate(fc):
                    # If a translated line exists
                    # Write it and continue
                    if tl: 
                        f.write(tl)
                        f.write('\n')
                        # Reset
                        tl = None
                        continue

                    # Get language.
                    # First line of 'po' file is the language.
                    if index == 0:
                        lang = line.split(' ')[1].lower() 
                        if lang not in ISO_639_1_CODES:
                            print(f"[Warning]: Translation for {lang.capitalize()} is not supported. Skipping...")
                            break # Skip file
                        
                        # Get ISO code for language
                        # e.g french is `fr`
                        lang = ISO_639_1_CODES[lang]
                    
                    # Translate lines 
                    if line.startswith('msgid') and index != 5:

                        # Previously translated text
                        pvt = fc[index+1][7:].strip('\n').strip('"')

                        # Hasn't been previously translated
                        if pvt == '':                            
                            try:
                                # Text to translate (ttt)
                                ttt = line[6:].strip('\n').strip('"')

                                # Compose Google Translate FQ URL
                                url =  f"{BASE_GOOGLE_TRANSLATE_URL}{_encode_query_parameters(DEFAULT_BABEL_LANGUAGE, lang, ttt)}"

                                # Using Dryscrape, visit URL
                                session.visit(url)

                                # Get translated text
                                tt = session.at_css(TRANSLATED_TEXT_SELECTOR).text()

                                # Translated text
                                tl = f'msgstr "{tt}"'
                            
                            except:
                                print(f"[Warning]: Could not translate {ttt}. Defaulting to original...")
                                # Translated text is the same
                                tl = f'msgstr "{ttt}"'

                            finally:                            
                                # Write original id line
                                f.write(line)
                                continue            

                    f.write(line)


def main():
    po_folder = '/home/olumidesan/projects/python/nms/webapp/app/translations'
    if os.path.exists(po_folder):
        translate_po(po_folder)
    else:
        print(f"[Error]: Invalid path")
        exit()

main() if __name__ == "__main__" else None