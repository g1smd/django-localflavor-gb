"""
GB-specific Form helpers
"""

from __future__ import absolute_import, unicode_literals

import re

from django.contrib.localflavor.gb.gb_regions import GB_NATIONS_CHOICES, GB_REGION_CHOICES
from django.forms.fields import CharField, Select
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


class GBPostcodeField(CharField):
    """
    A form field that validates its input is a UK postcode.

    The regular expression used is sourced from the schema for British Standard
    BS7666 address types: http://www.govtalk.gov.uk/gdsc/schemas/bs7666-v2-0.xsd

    The value is uppercased and a space added in the correct place, if required.
    """
    default_error_messages = {
        'invalid': _('Enter a valid postcode.'),
    }
    outcode_pattern = '[A-PR-UWYZ]([0-9]{1,2}|([A-HIK-Y][0-9](|[0-9]|[ABEHMNPRVWXY]))|[0-9][A-HJKSTUW])'
    incode_pattern = '[0-9][ABD-HJLNP-UW-Z]{2}'
    postcode_regex = re.compile(r'^(GIR 0AA|%s %s)$' % (outcode_pattern, incode_pattern))
    space_regex = re.compile(r' *(%s)$' % incode_pattern)

    def clean(self, value):
        value = super(GBPostcodeField, self).clean(value)
        if value == '':
            return value
        postcode = value.upper().strip()
        # Put a single space before the incode (second part).
        postcode = self.space_regex.sub(r' \1', postcode)
        if not self.postcode_regex.search(postcode):
            raise ValidationError(self.error_messages['invalid'])
        return postcode

class GBCountySelect(Select):
    """
    A Select widget that uses a list of UK Counties/Regions as its choices.
    """
    def __init__(self, attrs=None):
        super(GBCountySelect, self).__init__(attrs, choices=GB_REGION_CHOICES)

class GBNationSelect(Select):
    """
    A Select widget that uses a list of UK Nations as its choices.
    """
    def __init__(self, attrs=None):
        super(GBNationSelect, self).__init__(attrs, choices=GB_NATIONS_CHOICES)






/**



  ## GB telephone numbers:




  //  MAIN FUNCTIONALITY

    if valid_gb_phone_number(phonenumber):
        format_gb_phone_number(phonenumber)
    else:
        raise error





  //  CHECK IF INPUT FORMAT IS VALID THEN CHECK IF RANGE IS VALID

def valid_gb_phone_number(phonenumber):
    # Check if number entered matches a valid format
    if (!valid_gb_phone_pattern(phonenumber)):
        return FALSE;
    else:
        # Extract number parts: prefix, NSN, extension
        phonenumberPartsArray = (extract_gb_phone_parts(phonenumber));
        if (empty(phonenumberPartsArray)):
            return FALSE;
        else:
            phonenumberNSN = phonenumberPartsArray['NSN'];
            # Check if NSN entered is in a valid range
            if (!valid_gb_phone_range(phonenumberNSN)):
                return FALSE
            else:
                return TRUE





  //  FORMAT GB PHONE NUMBER

def format_gb_phone_number(phonenumber):
    phonenumberPrefix = ''
    phonenumberNSNraw = ''
    phonenumberNSNformatted = ''
    phonenumberExtension = ''

    # Extract optional country prefix, NSN, and optional extension
    phonenumberPartsArray = extract_gb_phone_parts(phonenumber)
    if (!empty(phonenumberPartsArray)):
        # Grab the NSN part of GB number
        phonenumberNSN = phonenumberPartsArray['NSN'];
        if (phonenumberNSN == null):
            return phonenumber

        # Remove spaces, hyphens, and brackets from NSN part of GB number
        arrayReplace = array(")", "-", " ");
        phonenumberNSN = trim(str_replace(arrayReplace, "", phonenumberNSN))
        # Format NSN part of GB number
        phonenumberNSNformatted = format_gb_nsn(phonenumberNSN)

        # Set prefix (will be +44 or 0)
        if (isset(phonenumberPartsArray['prefix']) && phonenumberPartsArray['prefix'] != null):
            phonenumberPrefix = phonenumberPartsArray['prefix'];

        # Grab extension and trim it
        phonenumberHasExtension = false
        phonenumberExtension = null
        if (isset(phonenumberPartsArray['extension']) && phonenumberPartsArray['extension'] != null):
            phonenumberHasExtension = true
            phonenumberExtension = " " + trim(phonenumberPartsArray['extension'])

        # Add prefix back on to NSN
        phonenumber = phonenumberPrefix + phonenumberNSNformatted

        # Add extension back on to number
        if (phonenumberHasExtension):
            phonenumber += phonenumberExtension

    return phonenumber








  //  VALID INPUT FORMAT (CHECKS ONLY FORMAT, NOT NUMBER RANGE):

def valid_gb_phone_pattern(phonenumber):
    validGBpattern = re.compile(r"^
    (?:
        (?:\(?(?:0(?:0|11)\)?\s?\(?|\+)44\)?\s?(?:\(?0\)?\s?)?)   # leading 00, 011 or + before 44 with optional (0); parentheses and spaces optional
        |
        (?:\(?0)                                 # leading (0, 0
    )
    (?:
        (?:\d{5}\)?\s?\d{4,5})                   # [5+4][5+5]
        |
        (?:\d{4}\)?\s?(?:\d{5}|\d{3}\s?\d{3}))   # [4+5][4+6]
        |
        (?:\d{3}\)?\s?\d{3}\s?\d{3,4})           # [3+6][3+7]
        |
        (?:\d{2}\)?\s?\d{4}\s?\d{4})             # [2+8]
        |
        (?:8(?:00\s?11\s?11|45\s?46\s?4\d))      # [0+7]
    )
    (?:
        (?:\s?\#\d+)?                            # optional extension number shown with a hash divider
    )
    $", re.X)

    # Test number entered for matching format
    if (!re.search(validGBpattern, phonenumber)):
        return FALSE
    else:
        return TRUE





  //  EXTRACT GB NUMBER PARTS:

def extract_gb_phone_parts(phonenumber):
    patternGBnumberparts = re.compile(r"^
    (\(?(?:0(?:0|11)\)?\s?\(?|\+)(44)\)?\s?)?\(?0?(?:\)\s?)?   # country or trunk prefix
    (
        [1-9]\d{1,4}\)?[\s\d]+                                 # NSN
    )
    (\#\d+)?                                                   # optional extension
    $", re.X)

    #  $2 contains "44" or NULL depending on whether number entered in international or national format
    #  $3 contains NSN
    #  $4 contains extension

    m = (re.search(patternGBnumberparts, phonenumber))
    if m.group:
        # Extract NSN part of GB number
        if m.group(3):
            phonenumberNSNraw = m.group(3)
            # Trim NSN and remove space, hyphen or ')' if present
            arrayReplace = array(")", "-", " ")
            phonenumberNSN = trim(str_replace(arrayReplace, "", phonenumberNSNraw))

            # Extract 44 prefix if present and set prefix as 0 or as +44 and space
            if (m.group(2) && m.group(2) == '44'):
                phonenumberPrefix = '+44 '
            else:
                phonenumberPrefix = '0'

            // Extract extension
            phonenumberExtension = null
            if m.group(4):
                phonenumberExtension = m.group(4)

    phonenumberPartsArray = array(
            'NSN'       => phonenumberNSN,
            'prefix'    => phonenumberPrefix,
            'extension' => phonenumberExtension,
        )

    return phonenumberPartsArray





  //  TEST THE NSN TO SEE IF NUMBER IS IN A VALID RANGE WITH RIGHT NUMBER OF DIGITS:

def valid_gb_phone_range(phonenumberNSN):
    patternGBvalidrange = re.compile(r"^
    (         # 2d with 10 digits [2+8] Landlines
        2(?:0[01378]|3[0189]|4[017]|8[0-46-9]|9[012])\d{7}
        |     # 11d, 1d1 with 10 digits [3+7] Landlines
        1(?:(?:1(?:3[0-48]|[46][0-4]|5[012789]|7[0-49]|8[01349])|21[0-7]|31[0-8]|[459]1\d|61[0-46-9]))\d{6}
        |     # 1ddd (and 1dddd) with 10 digits [4+6][5+5] Landlines
        1(?:2(?:0[024-9]|2[3-9]|3[3-79]|4[1-689]|[58][02-9]|6[0-4789]|7[013-9]|9\d)|3(?:0\d|[25][02-9]|3[02-579]|[468][0-46-9]|7[1235679]|9[24578])|4(?:0[03-9]|2[02-5789]|[37]\d|4[02-69]|5[0-8]|[69][0-79]|8[0-5789])|5(?:0[1235-9]|2[024-9]|3[0145689]|4[02-9]|5[03-9]|6\d|7[0-35-9]|8[0-468]|9[0-5789])|6(?:0[034689]|2[0-689]|[38][013-9]|4[1-467]|5[0-69]|6[13-9]|7[0-8]|9[0124578])|7(?:0[0246-9]|2\d|3[023678]|4[03-9]|5[0-46-9]|6[013-9]|7[0-35-9]|8[024-9]|9[02-9])|8(?:0[35-9]|2[1-5789]|3[02-578]|4[0-578]|5[124-9]|6[2-69]|7\d|8[02-9]|9[02569])|9(?:0[02-589]|2[02-689]|3[1-5789]|4[2-9]|5[0-579]|6[234789]|7[0124578]|8\d|9[2-57]))\d{6}
        |     # 1ddd with 9 digits [4+5] Landlines
        1(?:2(?:0(?:46[1-4]|87[2-9])|545[1-79]|76(?:2\d|3[1-8]|6[1-6])|9(?:7(?:2[0-4]|3[2-5])|8(?:2[2-8]|7[0-4789]|8[345])))|3(?:638[2-5]|647[23]|8(?:47[04-9]|64[015789]))|4(?:044[1-7]|20(?:2[23]|8\d)|6(?:0(?:30|5[2-57]|6[1-8]|7[2-8])|140)|8(?:052|87[123]))|5(?:24(?:3[2-79]|6\d)|276\d|6(?:26[06-9]|686))|6(?:06(?:4\d|7[4-79])|295[567]|35[34]\d|47(?:24|61)|59(?:5[08]|6[67]|74)|955[0-4])|7(?:26(?:6[13-9]|7[0-7])|442\d|50(?:2[0-3]|[3-68]2|76))|8(?:27[56]\d|37(?:5[2-5]|8[239])|84(?:3[2-58]))|9(?:0(?:0(?:6[1-8]|85)|52\d)|3583|4(?:66[1-8]|9(?:2[01]|81))|63(?:23|3[1-4])|9561))\d{3}
        |     # 1ddd with 9 digits [4+5] Landlines (special case)
        176888[234678]\d{2}
        |     # 1dddd with 9 digits [5+4] Landlines
        16977[23]\d{3}
        |     # 7ddd (including 7624) (not 70, 76) with 10 digits [4+6] Mobile phones
        7(?:[1-4]\d\d|5(?:0[0-8]|[13-9]\d|2[0-35-9])|624|7(?:0[1-9]|[1-7]\d|8[02-9]|9[0-689])|8(?:[014-9]\d|[23][0-8])|9(?:[04-9]\d|1[02-9]|2[0-35-9]|3[0-689]))\d{6}
        |     # 76 (excluding 7624) with 10 digits [2+8] Pagers
        76(?:0[012]|2[356]|4[0134]|5[49]|6[0-369]|77|81|9[39])\d{6}
        |     # 800 with 9 or 10 digits, 808 with 10 digits, 500 with 9 digits [3+7][3+6] Freephone
        80(?:0\d{6,7}|8\d{7})|500\d{6}
        |     # 871, 872, 873, 90d, 91d, 980, 981, 982, 983 with 10 digits [3+7] Premium rate
        (?:87[123]|9(?:[01]\d|8[0-3]))\d{7}
        |     # 842, 843, 844, 845, 870 with 10 digits [3+7] Business rate
        8(?:4[2-5]|70)\d{7}
        |     # 70 with 10 digits [2+8] Personal numbers
        70\d{8}
        |     # 56 with 10 digits [2+8] LIECS/VoIP
        56\d{8}
        |     # 30d, 33d, 34d, 37d, 55 with 10 digits [3+7] UAN and [2+8] Corporate
        (?:3[0347]|55)\d{8}
        |     # 800 1111, 845 46 4d with 7 digits [3+4] Freephone helplines
        8(?:001111|45464\d)
    )
    $", re.X)

    # Test NSN to see if it matches a valid number range
    if (!re.match(patternGBvalidrange, phonenumberNSN)):
        return FALSE
    else:
        return TRUE





  //  FORMAT GB NUMBER BY INITIAL DIGITS AND LENGTH:

def format_gb_nsn(phonenumberNSN):
    phonenumberNSNLength = len(phonenumberNSN)
    # RegEx patterns to define formatting by length and initial digits
    # [2+8] 2d, 55, 56, 70, 76 (not 7624) with 10 digits
    pattern28 = re.compile(r"^(?:2|5[56]|7(?:0|6(?:[013-9]|2[0-35-9])))")
    capture28 = re.compile(r"^(\d{2})(\d{4})(\d{4})$")
    # [3+7] 11d, 1d1, 3dd, 80d, 84d, 87d, 9dd with 10 digits
    pattern37 = re.compile(r"^(?:1(?:1|\d1)|3|8(?:0[08]|4[2-5]|7[0-3])|9[018])")
    capture37 = re.compile(r"^(\d{3})(\d{3})(\d{4})$")
    # [5+5] 1dddd (12 areas) with 10 digits
    pattern55 = re.compile(r"^(?:1(?:3873|5(?:242|39[456])|697[347]|768[347]|9467))")
    capture55 = re.compile(r"^(\d{5})(\d{5})")
    # [5+4] 1ddd (1 area) with 9 digits
    pattern54 = re.compile(r"^(?:16977[23])")
    capture54 = re.compile(r"^(\d{5})(\d{4})$")
    # [4+6] 1ddd, 7ddd (inc 7624) (not 70, 76) with 10 digits
    pattern46 = re.compile(r"^(?:1|7(?:[1-5789]|624))")
    capture46 = re.compile(r"^(\d{4})(\d{6})$")
    # [4+5] 1ddd (40 areas) with 9 digits
    pattern45 = re.compile(r"^(?:1(?:2(?:0[48]|54|76|9[78])|3(?:6[34]|8[46])|4(?:04|20|6[01]|8[08])|5(?:27|6[26])|6(?:06|29|35|47|59|95)|7(?:26|44|50)|8(?:27|37|84)|9(?:0[05]|35|49|63|95)))")
    capture45 = re.compile(r"^(\d{4})(\d{5})$")
    # [3+6] 500, 800 with 9 digits
    pattern36 = re.compile(r"^(?:[58]00)")
    capture36 = re.compile(r"^(\d{3})(\d{6})$")
    # [3+4] 8001111, 845464d with 7 digits
    pattern34 = re.compile(r"^(?:8(?:001111|45464\d))")
    capture34 = re.compile(r"^(\d{3})(\d{4})$")
    # Format numbers by leading digits and length
    if (phonenumberNSNLength == 10 && re.match(pattern28, phonenumberNSN)):
        m = (re.search(capture28, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2) + " " + m.group(3)
    elif (phonenumberNSNLength == 10 && re.match(pattern37, phonenumberNSN)):
        m = (re.search(capture37, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2) + " " + m.group(3)
    elif (phonenumberNSNLength == 10 && re.match(pattern55, phonenumberNSN)):
        m = (re.search(capture55, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2)
    elif (phonenumberNSNLength == 9  && re.match(pattern54, phonenumberNSN)):
        m = (re.search(capture54, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2)
    elif (phonenumberNSNLength == 10 && re.match(pattern46, phonenumberNSN)):
        m = (re.search(capture46, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2)
    elif (phonenumberNSNLength == 9  && re.match(pattern45, phonenumberNSN)):
        m = (re.search(capture45, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2)
    elif (phonenumberNSNLength == 9  && re.match(pattern36, phonenumberNSN)):
        m = (re.search(capture36, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2)
    elif (phonenumberNSNLength == 7  && re.match(pattern34, phonenumberNSN)):
        m = (re.search(capture34, phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2)
    elif (phonenumberNSNLength > 5):
        # Default format for non-valid numbers (shouldn't ever get here)
        m = (re.search("^(\d)(\d{4})(\d*)$", phonenumberNSN))
        if m.group:
            phonenumberNSN = m.group(1) + " " + m.group(2) + " " + m.group(3)

    return phonenumberNSN


**/
