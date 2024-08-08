import logging

import phonenumbers as py_phonenumbers

# https://github.com/daviddrysdale/python-phonenumbers

logger = logging.getLogger(__name__)

CONST_COUNTY_CODE_INDIA = 91


def is_valid_indian_number(mob_num):
    is_valid_number, parsed_e164, country_code, indian_national_number = validate_and_return_param(mob_num)
    return (is_valid_number and (country_code == CONST_COUNTY_CODE_INDIA)), parsed_e164, indian_national_number


def get_region_code_for_country_code(country_code):
    region_code = None
    if country_code:
        try:
            region_code = py_phonenumbers.COUNTRY_CODE_TO_REGION_CODE[country_code][0]
        except KeyError:
            pass
    return region_code


# Used most of the time
# if validation fails, then its  a failure
# if passes, save the parsed_e164
def validate_and_return_param(input_phonenumber: str):
    return validate_and_return_param_for_country(input_phonenumber, None)


# Ideally not required to be used directly
def validate_and_return_param_for_country(input_phonenumber: str, region_code):
    is_valid_number = parsed_e164 = country_code = national_number = None
    try:
        # People were sending spaces and then we were rejecting it.
        input_phonenumber = input_phonenumber.strip()
        logger.debug(input_phonenumber)
        if len(input_phonenumber) == 11 and (input_phonenumber.startswith("0")):
            # If people sending landline/phone number starting with zero, then removing that 0
            input_phonenumber = input_phonenumber[1:]
        if len(input_phonenumber) == 10 and (not input_phonenumber.startswith("+")):
            # If a simple indian number is entered, it will be just 10 digits hence we come in
            # if a full indian num is entered, it will be 12 digit so we wont do anything
            # a foreign num may come in, in that case it will have a + but not 10 digit, we wont come in
            input_phonenumber = "+" + str(CONST_COUNTY_CODE_INDIA) + input_phonenumber
        if not input_phonenumber.startswith("+"):
            input_phonenumber = "+" + input_phonenumber
        phonenumber_instance = py_phonenumbers.parse(input_phonenumber, region_code)

        logger.debug(str(phonenumber_instance))
        is_valid_number = py_phonenumbers.is_valid_number(phonenumber_instance)
        if is_valid_number:
            parsed_e164 = py_phonenumbers.format_number(phonenumber_instance, py_phonenumbers.PhoneNumberFormat.E164)
            country_code = phonenumber_instance.country_code
            national_number = phonenumber_instance.national_number
    except py_phonenumbers.phonenumberutil.NumberParseException as e:
        logger.warning(f"Invalid number passed - {input_phonenumber}, {e}")
        is_valid_number = False
    return is_valid_number, parsed_e164, country_code, national_number
