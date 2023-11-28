# Forex Trading System in Python
Built by Marco Mata

## Table of Contents
1. [Description](#description)
2. [Built-with](#built-with)
3. [Contribution](#contribution)
5. [Questions](#questions)

## Description
<h1 align="center">Welcome. :shipit:</h1> 


![image](https://github.com/itsmarcotime/Forex_trading_system_in_Python/assets/101440634/754accf7-842c-4092-8426-dd3811dfcd74)




<p>
    The Python Forex Trading System is a robust python based event driven and live trading application for backtesting forex trading data from a Demo Oanda API using trading strategies coded from scratch into the program itself. Requirements to run the code are, of course, you must have Python3 installed on your local machine, an IDE of your choosing (I personally use VScode but there are many other options), and an Oanda account which I will go over in the 'Environment Setup' below.
</p><br />
<h3 align="center">Evironment Setup</h3><br />
<p>
    First things first, if you want get anything working you will need to set up a trading account with Oanda. After thats set up you will then have to create your own .env file using your own Oanda credentials. This readme will help you get the .env set up. Without a broker account with api access to trading data it will be very hard to retrieve timely forex data. I went with the Oanda firm because they cater more towards the algorithmic trading scene, but if you know of another firm with api access feel free to use it. A link to the offical Oanda website will be right <a href="https://help.oanda.com/us/en/home.htm#">HERE</a>. **WARNING**: Oanda is setup to work with most countries around the world, but not all of them. Please make sure the country you reside in has all the necessary access to the Oanda Api before moving further. You can check the Oanda documentation for more information on your countries eligibility access to the Oanda Api. Once you have your Oanda account set up(it may take some time to have your account approved possibly more than 24hrs), navigate around the website until you are able to enter the Demo Mode set up. To find the 'Switch to Demo' button look on the top right corner, click the drop down, and located the 'Switch to Demo' button.  
</p>

![image](https://github.com/itsmarcotime/Forex_trading_system_in_Python/assets/101440634/158e8a3a-df9d-43ae-8a53-6aaaa86ce7df)


Once you are in the demo mode environment you will need to generate an Oanda API key. At the top in the same navigation bar you found the 'demo mode' button you will also find a button named 'Tools' click on it and generate an API key yourself. DO NOT show this key to anyone else as it is your own personal api key that will go into your .env file to retrieve your own personal data. Create a '.env' in the root directory of the project and set you the api key like this:<br />
```
    API_KEY='YOUR_API_KEY_HERE'
```




## Built-with
This application has been build heavily on Python3 as well as many other packages that are included in the python library such as Pandas, Plotly, and Datetime. Another important tool used to build the application was Jupyter Notebook. 

## Contribution
I intend for the code of this application to be completey open sourced here on GitHub. If you discover a bug or have an enhancement in mind, please don't hesitate to open an issue. Once the issue is approved and assigned to you, fork the application over onto your local machine and create a pull request when finished. Your input and insight is always greatly appreciated.

## Questions
Questions? <br /> 
<a href="https://www.linkedin.com/in/marco-mata-8165bb175/">LinkedIn</a><br />
mmata3309@gmail.com