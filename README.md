
# README

### DCM Filter

* DCM Filter to filter json files in a given folder for given comma separated key-value pairs.
---
### lib creation
    
    * create a libray dmc_filter_lib.<version>.tgz file under ./dist

    $ python setup.py sdist 

### Installation
    
    $ pip install dmc_filter_lib.<version>.tgz

### Usage
* **As a library**

    $ dcm_filter --help
    usage: dcm_filter [-h] --keys KEYS --values VALUES folder

    DCM filter. Prints matching DCM json files for given keys and values.

    positional arguments:
        folder           Directory holding DCM json files.

    optional arguments:
        -h, --help       show this help message and exit
        --keys KEYS      DCM keys to be filtered
        --values VALUES  DCM values to be filtered.

* **Command line**

    $ dcm_filter --keys="00080005,00080016" --values="ISO_IR 100,1.2.840.10008.5.1.4.1.1.1.1" ./files
    ./files/test_working.json
    ./files/sub/test_working.json
    ./files/sub/sub_sub/test_working.json


* **Import the DCM lib into the source code**

    from dcm_filter_lib import dcm_filter
    
    SAMPLE_DCM = {
      "00080005": {
          "Value": [
              "ISO_IR 100"
          ],
          "vr": "CS"
      },
      "00080008": {
          "Value": [
              "DERIVED",
              "PRIMARY"
          ],
          "vr": "CS"
      },
      "00080016": {
          "Value": [
              "1.2.840.10008.5.1.4.1.1.1.1"
          ],
          "vr": "UI"
      },
      "20500020": {
          "Value": [
              "IDENTITY"
          ],
          "vr": "CS"
      }
    }
      
    print(dcm_filter(SAMPLE_DCM, [("00080005", "ISO_IR 100"), ("00080016", "1.2.840.10008.5.1.4.1.1.1.1")]))
    print(dcm_filter(SAMPLE_DCM, [("00080005", "ISO_IR 100"), ("00080016", "1.2.840.5.1.4.1.1.1.1")]))
    
    """
    Output
    -----
    True
    False
    -----
    """