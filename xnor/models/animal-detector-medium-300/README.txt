===============================================================================
animal-detector-medium-300 for Raspberry Pi Zero
===============================================================================

Thank you for choosing Xnor.ai!

This distribution contains a single model for your use.  You can find samples
for using this model as part of the evaluation SDK, which you must download
separately at the following URL:

https://ai2go.xnor.ai/

This is a balanced model that finds bounding boxes for animals.

Installation:

 - C: Copy libxnornet.so to the same directory as your executable.
 - Python: Uninstall an existing xnornet module and install the wheel:

     python3 -m pip uninstall xnornet
     python3 -m pip install --user xnornet*.whl

Classes:
  - bird
  - cat
  - dog
  - horse
  - sheep
  - cow
  - elephant
  - bear
  - zebra
  - giraffe

Minimum effective image size: 300 x 300 pixels.

Benchmarks:
  - 1 thread:
    - Minimum measured inference latency: 2.1 s
    - Maximum measured resident set: 36.7 MB

