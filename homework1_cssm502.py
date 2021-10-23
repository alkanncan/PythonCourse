# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 22:22:34 2021

@author: Alkan
"""
import random
class Portfolio:
    def __init__(self):
        
        self.cash=0
        self.portfolio={"Cash($)":[self.cash],"Stocks":{}, "Mutualfunds":{}}
        self.hist=("PORTFOLIO HISTORY: \n")
        self.sellprice={} #for stocks
    
    
    def history(self):
        return print(self.hist)
    
    def __repr__(self):
        return str(self.portfolio)
    
      
    def addcash(self,amount):
        self.cash+=amount
        self.hist+=("The customer added $"+str(amount)+ " to portfolio\n")
    
    def withdrawcash(self,amount):
        self.cash-=amount
        self.hist+=("The customer withdrew $"+str(amount)+ " from portfolio")
    
    
    
    def buystock(self,share,n):
        if self.cash>=share*n.price: #to check if there is enough money
            self.cash-=share*n.price
            self.portfolio["Cash($)"]=self.cash           
            if n.symbol not in self.portfolio["Stocks"]:
                self.portfolio["Stocks"][n.symbol]=share
                self.sellprice[n.symbol]=random.uniform(0.5*n.price, 1.5*n.price) #to save the sell price of the purchased stock
            else:
                self.portfolio["Stocks"][n.symbol]+=share
            self.hist+=("The customer purchased "+ str(share)+ " shares of stock " + n.symbol+" for $"+str(n.price)+"/share."+"\n")
        else:
            print("Insufficient funds!")
    
    def buyMutualFund(self,share,n):
        if self.cash>=share*n.price: 
            self.cash-=share*n.price
            self.portfolio["Cash($)"]=self.cash           
            if n.symbol not in self.portfolio["Mutualfunds"]:
                self.portfolio["Mutualfunds"][n.symbol]=share
            else:
                self.portfolio["Stocks"][n.symbol]+=share
            self.hist+=("The customer purchased "+ str(share)+ " shares of " + n.symbol+" for $"+str(n.price)+"/share."+"\n")
        else:
            print("Insufficient funds!")
    
    
    
    def sellstock(self,symbol,share):
        
        if symbol in self.portfolio["Stocks"] and self.portfolio["Stocks"][symbol]>=share:
            sellprice=self.sellprice[symbol] #calling the previously saved sell price
            self.cash+=sellprice*share
            self.portfolio["Cash($)"]=self.cash
            self.portfolio["Stocks"][symbol]-=share
            self.hist+=("The customer sold "+ str(share)+ " shares of stock " +symbol+" for $"+str(sellprice)+"/share."+"\n")
            if self.portfolio["Stocks"][symbol]==0:
                del self.portfolio["Stocks"][symbol]
        elif symbol not in self.portfolio["Stocks"]:
            print("You have no share of stock "+symbol+ " to sell")
        else:
            print("You don't have enough shares of stock "+symbol+ " to sell")
    
    def sellMutualFund(self,symbol,share):
        if symbol in self.portfolio["Mutualfunds"] and self.portfolio["Mutualfunds"][symbol]>=share:
            mfsellprice=random.uniform(0.9, 1.2)
            self.cash+=mfsellprice*share
            self.portfolio["Cash($)"]=self.cash
            self.portfolio["Mutualfunds"][symbol]-=share
            self.hist+=("The customer sold "+ str(share)+ " shares of " + symbol+" for $"+str(mfsellprice)+"/share."+"\n")
            if self.portfolio["Mutualfunds"][symbol]==0:
                del self.portfolio["Mutualfunds"][symbol]
        elif symbol not in self.portfolio["Mutualfunds"]:
            print("You have no share of "+symbol+ " to sell")
        else:
            print("You don't have enough shares of "+symbol+ " to sell")
        
        
        
class Stock:
    def __init__(self,price,symbol):
        self.price=price
        self.symbol=symbol
        
   
        
       
   

class MutualFund():
    def __init__(self, symbol):
        self.symbol=symbol
        self.price=1
        


portfolio=Portfolio()
portfolio.addcash(300.5)
s=Stock(20,"HFH")
portfolio.buystock(5, s)
mf1=MutualFund("BRT")
mf2=MutualFund("GHT")
portfolio.buyMutualFund(10.3, mf1)
portfolio.buyMutualFund(2, mf2)
print(portfolio)
portfolio.sellMutualFund("BRT",3)
portfolio.sellstock("HFH", 1)
portfolio.withdrawcash(50)
print(portfolio)
portfolio.history()



