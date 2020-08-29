## Scrape Images Using Bing Search v7.0 API

1. Sign up for Microsoft Azure account
2. Look for 7-day free trial of Bing Image Search under Azure Cognitive Services. [Click here](https://azure.microsoft.com/en-us/services/cognitive-services/)
3. Under the free pricing tier, maximum 3000 calls are allowed per month and 3 calls per second.
4. Get your API keys. There should be two of them.
5. The following python libraries need to be installed:
   - requests, time, os, argparse, datetime, matplotlib, PIL, io and numpy
6. In your command window, run 
   - python bing.py -k "**Your API key**" -q "**[Your search term]**" -t **[number of images required]** -r **[optional: number of images per API call, by default 150]** -i **[optional: starting index of image, by default 1]**
7. Example:
   - python bing.py -k "08a7dcf38a474a75a103f296885d57c8" -q "potato" -t 1000
8. A log file and a subfolder containing the images will be generated as output.
9. The total number of saved images will be slightly more than the total number specified in the command as the final API call will generate extra images.


## Removing Duplicates 
1. The following python libraries need to be installed:
   - os, argparse
6. In your command window, run
   - python remove_duplicates.py -d **[Your Image Directory Path]**
3. Example:
   $ python remove_duplicates.py -d "C:\Users\onnwe\Desktop\ISS-PRSPM-GRP-18\Bing_img_scrape\tomato"
4. Duplicated image will be removed upon confirmation


## Prefix Adder
1. The following python libraries need to be installed:
   - os, argparse
6. In your command window, run
   - python prefix_adder.py -d **[Your Image Directory Path]** -p **[Your Prefix]** -r **[Optional: To rename (1) or add a prefix (0), by default is 1 (set to 0 if you want to add a prefix)]**
3. Example:
   $ python prefix_adder.py -d "C:\Users\onnwe\Desktop\ISS-PRSPM-GRP-18\Bing_img_scrape\tomato" -p "T"
4. All files(Images) within the folder specified will have a prefix added to their existing filename
