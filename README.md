# MOPITT V10 Validation
Code developed for this project includes algorithms to validate version 10 MOPITT carbon monoxide (CO) retrievals against aircraft-measured profiles.

To cite this codebase, please use:
  * TBD

Latest version: TBD

Aircraft profiles are from NOAA, HIPPO and ATom. * Add data DOI.

## Methodology

Data processing and analysis is separated into several sections.

| Name | description | folder |
|---------:|:------------|:----:|
| plotting | Folder containing code for generalized plotting. |  [plotting]() |
| sample_data | Folder containing sample aircraft measurements from NOAA, HIPPO1 and ATom-1. |  [sample_data](https://github.com/rrbuchholz/mopittv10/tree/main/sample_data) |
| sample_pairing | Folder containing sample aircraft measurements from NOAA, HIPPO1 and ATom-1. |  [sample_pairing](https://github.com/rrbuchholz/mopittv10/tree/main/sample_pairing) |
| validation | Folder containing code to perform validation. |  [validation](https://github.com/rrbuchholz/mopittv10/tree/main/validation) |


Validation code description.

| Name | description | location |
|---------:|:------------|:----:|
| original_IDL | Folder: IDL code for test stations used for converting to python framework (val_L2_v10_noaa_test.pro, distance.pro). This location also houses a folder containing a subfolder called SOFTWARE, that archives original IDL code used to validate previous versions of MOPITT. |  [original_IDL](https://github.com/rrbuchholz/mopittv10/tree/main/validation/original_IDL) |
| copilot_transformed | Folder: Copilot transformation of IDL code as a starting point for refactoring code. |  [copilot_transformed](https://github.com/rrbuchholz/mopittv10/tree/main/validation/copilot_transformed) |
