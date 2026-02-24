
## 06/23/25

### Problem
Something is wrong somewhere in the data retrieval. In the requestHistoricalData function for a
futures contract client Class. When ever I change the bar size setting to anything bigger than 
a minute, the dates are off. Im sure that the dates are off because the prices that they display are
way higher than what the price should be in 1970... they are prices that we'll see in Todays time.

### Solution
The 1970 thing was very telling. This is the epoch time. I think it's because different things get
returned based on what I ask for. Ex. If I ask for 1 min candles I get epoch time. But if I ask for
daily I get a string like "20120321". I have to make sure that I write functions where if Im pulling
for shorter granularity, it treats the time differently than longer granularity. 



## 06/25/25 

### Problem

Im at a point where I can get data. However now I want to make sure that I am doing the right thing
with the data. One of things that I need to tackle is how do I structure these dataframes. What
operations can I do with them. What statistics do I need to learn? How can I formulate ideas?




### Things that I have found out

You can treat columns as a vector in pandas. Meaning that I can do something like:

``` python
    
    # 1) compute the raw price change per candle
df['oc_change'] = df['close'] - df['open']

# 2a) cumulative (from the start through each candle) standard deviation
df['oc_change_std_cum'] = df['oc_change'].expanding(min_periods=1).std()

# 2b) or, if you prefer a 20-day rolling std dev of those changes:
df['oc_change_std_20d'] = df['oc_change'].rolling(window=20, min_periods=1).std()

```

See you can use the columns to make new columns and then you can aggregate column information to
make new columns with that. I might need to look at the documentation for more understanding. 



## 07/29/2025 

One of things that I think that I need to do more is make tests. A test suite will allow me to not
have to write a lot of tests in the code. Basically one of the main things that take a lot of my
time is the fact that I have to write tests in the code and see what works and then I don't focus on
writing coherent code. This is why I'm stuck. If I write test cases I can save the "recipes" for how
I do things and then I can focus on combining all the functions Im writing to do something
productive. Then you can always reference the test cases to see what functions were used to do
certain things.  


## 02/21/26
I have found that a lot of the things that I was doing in this code base is wrong. Not wrong for some
arbitrary reason. This project got really far away from me as far as being able to manage whats going
on and making changes. This happened before I even had ANY working features. So here are some of the
problems that I faced.

1) Everything does not need to be a class from the very inception. You should make good functions and 
maybe incorporate some functional programming to begin. Why? Because functional programming makes 
things easier to test. Pure functions makes everything clear as to what is going on. There are 3 key 
things to do  to make functional programming projects:
    - Functions don't mutate existing data.
    - Functions always return an object. 
    - Functions only use the parameters given to perform a task. 

This comes from Grokking Functional Programming. I believe that starting out purely functional will 
allow me to be able to get working functionality a lot faster, especially in the beginning of a project. 


2) Make use of fake data. This allows you to be able to get data pipelines and flow mapped before having 
to also get real data by way of some function later. This relates to this project so well because, I have 
to request the data from some source where I know what it will look like but I haven't made a way to get 
the data reliably. 

3) Composition, use it!!! This means if a function or class has to do something that another object can
already do use that other damn object.

4) You need more abstraction in your programs. I have to separate concerns better and make more modular
code to abstract away a lot of details.

5) DRY also means don't repeat your intentions as well as just don't repeat the same lines of code. This 
comes from the book, Pragmatic Programmer. An example that currently exists in this code base is that we 
are using the database class, we are having functions that execute individual sql queries. That is a
misuse of the class. It should just pass a valid sql query to the data base and return the results.
Another class should have all the details of whats going on and should be tested, that we aren't repeating
the intent of making queries to the database.
