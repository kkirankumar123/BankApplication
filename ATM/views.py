from ctypes.wintypes import PINT
from django.shortcuts import render
from django.http import HttpResponse
from ATM.models import ATM_Details
from Bank.models import Bank_Details, Transact_Details
import random

# Create your views here.
def home(request):
    return render(request,'ATM/Home.html')
def generatePin(request):
    if request.method=='POST':
        ac=request.POST.get('account')
        mb=request.POST.get('mobile')
        ot=request.POST.get('otp')
        data1=Bank_Details.objects.all()
        data2=ATM_Details.objects.all()
        for ea in data2:
            if(ea.Account_Number==ac):
                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application</h3>
                <h3>Sorry, your ATM Pin Number generated already . Please check</h3>
                <br><br><a href="/atm/generatePin" style="margin-left:250px;">Back</a>''')  
        for acno in data1:
            if(ac==acno.Account_Number):
                if(int(mb)==acno.Mobile):
                    pinnum=random.randint(1000,10000)
                    tamt=acno.Amount
                    ATM_Details.objects.create(Account_Number=ac,Pin_Number=pinnum,Mobile=mb,Amount=tamt)
                    Transact_Details.objects.filter(Account=ac).update(Pin=pinnum)
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                    width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                    <h3 style='text-align:center;background-color:purple; color:white'>
                    Welcome in my ATM Application</h3>
                    <h3>ATM Pin generate Successfully</h3>
                    <table style="margin:auto;font-size:25px">
                    <tr><th>Account Number :</th><td>{ac}</td></tr>
                    <tr><th>Total Amount :</th><td>{tamt}</td></tr>
                    <tr><th>Pin Number :</th><td>{pinnum}</td></tr>
                    </table><br><br><a href="/atm/generatePin" style="margin-left:250px;">Back</a>''')
                else:
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application</h3>
                <h3>Sorry, your Mobile number is not exists in your Bank A/C. Please check</h3>
                <br><br><a href="/atm/generatePin" style="margin-left:250px;">Back</a>''')
            
                    
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application</h3>
                <h3>Sorry, your A/C number is not exists in Bank. Please check</h3>
                <br><br><a href="/atm/generatePin" style="margin-left:250px;">Back</a>''')
                                  
    else:
        sotp=random.randint(100000,1000000)
    
        return render(request,'ATM/GeneratePin.html',{'sotp':sotp})
def withdraw(request):
    if request.method=='POST':
        pn=request.POST.get('pin')
        amt=request.POST.get('amount')
        data=ATM_Details.objects.all()
        for acno in data:
            if(int(pn)==acno.Pin_Number):
                if(int(amt)+1000<=acno.Amount):
                    ac=acno.Account_Number
                    tamt=acno.Amount-int(amt)
                    ATM_Details.objects.filter(Pin_Number=pn).update(Amount=tamt)
                    Bank_Details.objects.filter(Account_Number=ac).update(Amount=tamt)
                    Transact_Details.objects.create(Account=ac,Pin=int(pn),Amount=int(amt),Debit_Credit='Debit')
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application</h3>
                 <h3>Withdraw Successfully from Your A/C</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>Withdraw Amount :</th><td>{amt}</td></tr>
                <tr><th>Total Amount :</th><td>{tamt}</td></tr>
            </table><br><br><a href="/atm/withdraw" style="margin-left:250px;">Back</a>''')
                
                else:
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application</h3>
                <h3>Sorry, You do not have enough balence in your A/C. Please check</h3>
                <br><br><a href="/atm/withdraw" style="margin-left:250px;">Back</a>''')
                

        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your Pin number is wrong. Please check</h3>
                <br><br><a href="/atm/withdraw" style="margin-left:250px;">Back</a>''')
                
    else:
        return render(request,'ATM/Withdraw.html')
def deposit(request):
    if request.method=='POST':
        amt=request.POST.get('amount')
        pn=request.POST.get('pin')
        data=ATM_Details.objects.all()
        for acno in data:
            if(int(pn)==acno.Pin_Number):
                tamt=acno.Amount+int(amt)
                ac=acno.Account_Number
                ATM_Details.objects.filter(Pin_Number=pn).update(Amount=tamt)
                Bank_Details.objects.filter(Account_Number=ac).update(Amount=tamt)
                Transact_Details.objects.create(Account=ac,Pin=int(pn),Amount=int(amt),Debit_Credit='Credit')
                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application </h3>
                 <h3>Your Amount Deposit Successfully into A/C</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>Deposit Amount :</th><td>{amt}</td></tr>
                <tr><th>Total Amount :</th><td>{tamt}</td></tr>
            </table><br><br><a href="/atm/deposit" style="margin-left:250px;">Back</a>''')
                
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application</h3>
                <h3>Sorry, your ATM number is wrong. Please check</h3>
                <br><br><a href="/atm/deposit" style="margin-left:250px;">Back</a>''')
            
        
    else:
        return render(request,'ATM/Deposit.html')

def balanceEnq(request):
    if request.method=='POST':
        pn=request.POST.get('pin')
        data=ATM_Details.objects.all()
        for acno in data:
            if(int(pn)==acno.Pin_Number):
                amt=acno.Amount
                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my ATM Application</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th> Total Amount :</th><td>{amt}</td></tr>
            </table><br><br><a href="/atm/balanceEnq" style="margin-left:250px;">Back</a>''')
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your ATM Pin number is wrong. Please check</h3>
                <br><br><a href="/atm/balanceEnq" style="margin-left:250px;">Back</a>''')
            
    else:
        return render(request,'ATM/BalanceEnq.html')
def transaction(request):
    if request.method=='POST':
        pn=request.POST.get('pin')
        mb=request.POST.get('mobile')
        data=Transact_Details.objects.all()
        for acno in data:
            if(int(pn)==acno.Pin):
                info=Transact_Details.objects.filter(Pin=int(pn))
                return render(request,'ATM/Passbook.html',{'info':info})
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your ATM Pin number is wrong. Please check</h3>
                <br><br><a href="/atm/transaction" style="margin-left:250px;">Back</a></div>''')                                 
                
    else:
        return render(request,'ATM/Transaction.html')

def about(request):
    return render(request,'ATM/About.html')

def other(request):
    return render(request,'ATM/Other.html')