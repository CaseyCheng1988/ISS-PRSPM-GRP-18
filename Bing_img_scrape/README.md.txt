## Scrape Images Using Bing Search v7.0 API

1. Sign up for Microsoft Azure account
2. Look for 7-day free trial of Bing Image Search under Azure Cognitive Services. [Click here](https://azure.microsoft.com/en-us/services/cognitive-services/)
3. Under the free pricing tier, maximum 3000 calls are allowed per month and 3 calls per second.
4. Get your API keys. There should be two of them.
5. The following python libraries need to be installed:
   - requests, time, os, argparse, datetime, matplotlib, PIL, io and numpy
6. In your command window, run 
   - python bing.py -k "<Your API key>" -q "<Search term>" -t <number of images required> -r <optional: number of images per API call, by default 150> -i <optional: starting index of image, by default 1>
7. Example:
   - python bing.py -k "835f2c6d22ff41518938455c80a7862b" -q "watermelon" -t 1000 
8. A log file and a subfolder containing the images will be generated as output.
9. The total number of saved images will be slightly more than the total number specified in the command as the final API call will generate extra images.

