Welcome to our project (If it has been finished)!

#BACKGROUND

For this Hack112, we envisioned an application that could help options traders make informed investment decisions using one of the most well-known but complex mathematical models offered in quantitative analysis—the Black-Scholes Model. This model is defined by a second-order parabolic partial differential equation; the solution to which we mapped in a 3-Dimensional graph which gives information regarding the optimal pricing for call options given any potential stock price and time remaining for maturity. We additionally plotted a 2-Dimensional graph using the given maturity date for the options contract chosen.

SPEAKING OF WHICH: "How are users able to input a contract option??!!?!?!" You may ask. Alongside plotting multiple graphs with complex mathematical models, we also created a CMU-Graphics-based graphical user interface (GUI) that conveniently gives consumers all of the dates of upcoming options contracts directly to their fingertips. Using just a few clicks, they can access any of the TENS OF THOUSANDS of stock options that we have web-scraped and extrapolated immediately into the user interface.

FURTHERMORE, after processing the vast amounts of data, we then send the data directly to our algorithm, which crunches the numbers, and produces the vital information necessary to make an educated options purchase prediction and decision.


#Instructions

To USE THIS MASTERPIECE OF A PROGRAM, all you must do is run UI.py and either input your stock ticker into the text box or choose one of the five MARVELOUS stocks that we have provided at your disposal. Once you have chosen a stock, press the corresponding "Go!" button to load the maturity dates available for that stock. From there, you can choose a date by scrolling using the up and down arrows and clicking whatever date you wish followed by the corresponding "Go!" button. Finally, you can repeat this process to choose a specific options contract, after which another screen will pop up which will display the corresponding graphs. 


#Dependencies

This application uses selenium, pandas, numpy, scipy, lxml, cmu graphics, and matplotlib for its functionality.


#Citations

Python Programming and Numerical Methods book A guide for engineers and scientists - Berkeley University —> was used for 3D plotting

Investopedia —> used for financial information

ChatGPT —> Used for debugging and learning new packages