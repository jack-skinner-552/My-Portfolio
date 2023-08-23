# RickRoll Selenium Project
The "RickRoll" project is a Python script that uses the Selenium library to perform an automated action of "Rickrolling" someone on YouTube by redirecting them to the official music video of "Never Gonna Give You Up" by Rick Astley.

## Description
The "RickRoll" project utilizes Selenium, a web testing framework, to automate the process of searching for the "Never Gonna Give You Up" music video on YouTube and clicking on the correct video to initiate the "Rickroll." The script launches a Chrome browser and performs the following steps:

1. Launch Chrome browser using the ChromeDriver.
2. Navigate to YouTube's homepage.
3. Search for "Never Gonna Give You Up."
4. Click on the correct music video.
5. Print a message indicating that the user has been "Rickrolled."
6. Wait for 70 seconds (length of the song).
7. Quit the Chrome browser.
## Requirements
* Python
* Selenium library
* ChromeDriver executable (Make sure to provide the correct path to the ChromeDriver executable in the script)
* Chrome browser
## Usage
1. Clone or download the repository to your local machine.
2. Install the Selenium library if you haven't already:
```sh
pip install selenium
```
3. Make sure you have the correct path to the ChromeDriver executable set in the script (**'System.setProperty("webdriver.chrome.driver", "/Users/Jack/Downloads/Driver/chromedriver.exe")'**).
4. Run the script:
```sh
python main.py
```
5. The script will open a Chrome browser, perform the "Rickroll" action, and print the corresponding message.
**Note:** Be cautious when running automated scripts on websites, and use them responsibly and with permission.