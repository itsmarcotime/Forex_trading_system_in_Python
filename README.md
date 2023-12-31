# Forex Trading System in Python
Built by Marco Mata

## Table of Contents
1. [Description](#description)
2. [Contribution](#contribution)
3. [Built-with](#built-with)
5. [Questions](#questions)

## Description
<h1 align="center">Welcome. :shipit:</h1> 

![image](https://github.com/itsmarcotime/Forex_trading_system_in_Python/assets/101440634/f1491383-0ea3-4972-818a-ea4a7e5841d7)

<p>
    The Python Forex Trading System is a robust python based event driven and live trading application for backtesting forex trading data from a Demo Oanda API using trading strategies coded from scratch into the program itself. Requirements to run the code are, of course, you must have Python3 installed on your local machine, an IDE of your choosing (I personally use VScode but there are many other options), and an Oanda account which I will go over in the 'Environment Setup' below.
</p>

<h3 align="center">Evironment Setup</h3><br />

First things first, if you want get anything working you will need to set up a trading account with Oanda. After thats set up you will then have to create your own .env file using your own Oanda credentials. This readme will help you get the .env set up. Without a broker account with api access to trading data it will be very hard to retrieve timely forex data. I went with the Oanda firm because they cater more towards the algorithmic trading scene, but if you know of another firm with api access feel free to use it. A link to the offical Oanda website will be right <a href="https://help.oanda.com/us/en/home.htm#">HERE</a>. **WARNING**: Oanda is setup to work with most countries around the world, but not all of them. Please make sure the country you reside in has all the necessary access to the Oanda Api before moving further. You can check the Oanda documentation for more information on your countries eligibility access to the Oanda Api. Once you have your Oanda account set up(it may take some time to have your account approved possibly more than 24hrs), navigate around the website until you are able to enter the Demo Mode set up. To find the 'Switch to Demo' button look on the top right corner, click the drop down, and located the 'Switch to Demo' button.  


![image](https://github.com/itsmarcotime/Forex_trading_system_in_Python/assets/101440634/158e8a3a-df9d-43ae-8a53-6aaaa86ce7df)


Once you are in the demo mode environment you will need to generate an Oanda API key. At the top of the Oanda webpage in the same navigation bar you found the 'demo mode' button you will also find a button named 'Tools' click on it and generate an API key yourself. DO NOT show this key to anyone else as it is your own personal api key that will go into your .env file to retrieve your own personal data. Now, create a '.env' in the root directory of the project and set up your api key like this:

```
    API_KEY='YOUR_API_KEY_HERE'
```

<br />
<p>
    Make sure to replace the 'YOUR_API_KEY_HERE' text with your own personally generated API key from Oanda. Next, we will need to locate your demo account ID. This part won't be that hard. Navigate back to the Oanda home page and login if you have not done so. Again, make sure that you are in the 'Demo mode' version of your Oanda account. WARNING: If you use your LIVE primary account ID you could accidently place live trades so be sure you are in Demo Mode. Once prompted to the home page of demo mode Oanda should automatically displace the dashboard with all of its different features. You want to look on the left hand side of the page for an "Accounts" option. Click on it.
</p>

![OANDA Hub (1)](https://github.com/itsmarcotime/Forex_trading_system_in_Python/assets/101440634/fcc0dea8-3b89-4b1c-a731-4a3b0d547049)


As shown in the image above, we are inside the 'Accounts' tab on the left side. You will find your demo account ID under the "Primary" title as circled in red on the image above. Copy the account Id number and head on back to your .env file. Directly under where you set up your api key place your acount Id in a similar fashion like so:

```
    ACCOUNT_ID='YOUR_ACCOUNT_ID_HERE'
```

<br />
Now, all you need for the .env is the a oanda url. The url provided in this readme is used to retrieve all your data for TESTING purposes. I will not provide the url for live trading data in this readme for the safety of the user. However, if you really understand what is going on I highly recommend you look through Oanda documention for the live url. The practive url will go into your .env like so:

```
    OANDA_URL=https://api-fxpractice.oanda.com/v3
```

<br />
Thats it! You're ready to start backtesting your strategies on years worth of trading data. Happy Trading!

<h3 align="center">**DISCLAIMER**</h3><br />

This is a tool. Not the holy grail. Everything you will find in this repository is for educational purposes only, and is NOT any type of investment advise whatsoever. Any live trading done by a user with the code from this repository is the USER'S responsibility. This trading system is made purely for educational purposes to practice with historical data, and should not be used to make any final finacial decisions.

## Contribution
I intend for the code of this application to be completey open sourced here on GitHub. If you discover a bug or have an enhancement in mind, please don't hesitate to open an issue. Once the issue is approved and assigned to you, fork the application over onto your local machine and create a pull request when finished. Your input and insight is always greatly appreciated.

## Built-with
This application has been build heavily on Python3 as well as many other packages that are included in the python library such as Pandas, Plotly, and Datetime. Another important tool used to build the application was Jupyter Notebook. 

## Questions
Questions? <br /> 
<a href="https://www.linkedin.com/in/marco-mata-8165bb175/">LinkedIn</a><br />
mmata3309@gmail.com