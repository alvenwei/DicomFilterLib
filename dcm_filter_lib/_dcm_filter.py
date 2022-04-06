import argparse
import json
from json import JSONDecodeError
from typing import Tuple, Dict, List

import os
import os.path


class DCMException(Exception):
    pass


def _get_dcom_from_json_file(file) -> Dict:
    """
    Returns the dcom in dict from the json file

            Parameters:
                    file : A file with json format.
            Returns:
                    the dcom in dict format and none if file not found or cannot be decoded.
    """
    dcom = None
    try:
        with open(file, "r") as f:
            dcom = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        pass
    return dcom


def _walk_through_all_json_files(folder):
    """
    Walks through all the json files

            Parameters:
                    folder : the specified json file folder
            Returns:
                    the json files under the specified directory
            Raises:
                    DCMException: if directory doesn't exist or no json files found under directory/sub directories.
    """
    no_json_file_found = True

    if not os.path.isdir(folder):
        raise DCMException(f"'{folder}' directory doesn't exist.")

    for dir_path, dir_names, file_names in os.walk(folder):
        for filename in [f for f in file_names if f.endswith(".json")]:
            no_json_file_found = False
            file = os.path.join(dir_path, filename)
            yield file

    if no_json_file_found:
        raise DCMException(f"No json file found under '{folder}'.")


def dcm_filter(dicom: Dict, key_value_pairs: List[Tuple[str, str]]) -> bool:
    """
    File filter with the DCM

            Parameters:
                    dicom : the dict structure of the json file
                    key_value_pairs : the dicom  filtering criteria
            Returns:
                    true if they are matched otherwise false
            Raises:
                    KeyError: if the key doesn't exist in the dicom dict
                    ValueError: if the value doesnt match in the dicom dict
    """
    if not dicom:
        return False

    result = False
    try:
        for key, value in key_value_pairs:
            if value not in dicom[key]["Value"]:
                raise ValueError(f"No match for value: {value}")
            result = True
    except (KeyError, ValueError):
        result = False
    return result


def _is_matching_in_file(file, key_value_pairs: List[Tuple[str, str]]) -> bool:
    """
    Check a DCM file with the dicom filtering criteria

            Parameters:
                    file : the DCM json file
                    key_value_pairs : the DCM filtering criteria
            Returns:
                    True if they are matched otherwise false
    """
    dicom = _get_dcom_from_json_file(file)
    return dcm_filter(dicom, key_value_pairs)


def _dcm_files_filter(folder: str, key_value_pairs: List[Tuple[str, str]]) -> List[str]:
    """
    Filters all the json files that contain given all key value pairs.

            Parameters:
                    folder : the specified json file folder
                    key_value_pairs : the dicom filtering criteria
            Returns:
                    the matched json file list
    """
    match_list = []
    for file in _walk_through_all_json_files(folder):
        if _is_matching_in_file(file, key_value_pairs):
            # replace might not be necessary in file path - Windows print backslashes normally
            match_list.append(str(file).replace("\\",  '/'))
    return match_list


def _dcm_filter_printed(folder: str, key_value_pairs: List[Tuple[str, str]]) -> None:
    """
    Prints all the json files that contain given all key value pairs.

            Parameters:
                    folder : the specified json file folder
                    key_value_pairs : the dicom filtering criteria
    """
    for match in _dcm_files_filter(folder, key_value_pairs):
        print(match)


def _combine_keys_and_values(keys_comma_separated, values_comma_separated) -> List[Tuple[str, str]]:
    """
    Combines the keys and values as pairs into a dict list
            Parameters:
                    keys_comma_separated : the keys in the filtering criteria
                    values_comma_separated : the values in the filtering criteria
            Returns:The filtering key-value criteria list
            Raises:
                    DCMException: If comma separated key and value numbers do not match.
    """
    keys = [key.strip() for key in keys_comma_separated.split(",")]
    values = [value.strip() for value in values_comma_separated.split(",")]

    if len(keys) != len(values):
        raise DCMException("Keys and values length don't match.")

    return list(tuple(zip(keys, values)))


def main():
    """
    Filters all the json files with the specified dicom criteria
    """
    parser = argparse.ArgumentParser(
        description="DCM filter. Prints matching DCM json files for given keys and values.")
    parser.add_argument("--keys", action="store", required=True,  help="DCM keys to be filtered")
    parser.add_argument("--values", action="store", required=True, help="DCM values to be filtered.")
    parser.add_argument('folder', help="Directory holding DCM json files.")
    args = parser.parse_args()

    keys_comma_separated = args.keys
    values_comma_separated = args.values
    folder = args.folder

    try:
        keys_value_pairs = _combine_keys_and_values(keys_comma_separated, values_comma_separated)
        _dcm_filter_printed(folder, keys_value_pairs)
    except DCMException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
