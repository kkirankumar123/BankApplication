
from re import A
from sqlite3 import connect
from django.shortcuts import render,redirect
from django.http import HttpResponse
from Bank.models import Bank_Details,Transact_Details
from ATM.models import ATM_Details
import random

# Create your views here.
def home(request):
    return render(request,'Bank/Home.html')
def Bhome(request):
    return render(request,'Bank/bHome.html')
def Ahome(request):
    return render(request,'ATM/Home.html')
def openAC(request):
    if request.method=='POST':
        ac='283101000'
        rm=str(random.randint(10000,99999))
        Account_Number=ac+rm
        Name=request.POST.get('cname')
        Father_Name=request.POST.get('fname')
        Address=request.POST.get('address')
        City=request.POST.get('city')
        State=request.POST.get('state')
        Pin=request.POST.get('pin')
        Mobile=request.POST.get('mobile')
        DOB=request.POST.get('dob')
        Religion=request.POST.get('religion')
        Gender=request.POST.get('gender')
        Amount=request.POST.get('amount')
        data=Bank_Details.objects.all()
        for acno in data:
            if(acno.Name==Name and acno.Father_Name==Father_Name and acno.Mobile==int(Mobile) and str(acno.DOB)==DOB):
                return HttpResponse(f'''<div style="margin:auto;margin-top:50px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno.Name} in my bank A/C</h3>
                <h3>Sorry, You can't open another A/C Because you are old customer in Bank. Please check</h3>
                <br><br><a href="/openAC" style="margin-left:250px;">Back</a>''')
                
        if(int(Amount)>=1000):
            Bank_Details.objects.create(Name=Name,Father_Name=Father_Name,Account_Number=Account_Number,
                                    Amount=Amount,Mobile=Mobile,Gender=Gender,DOB=DOB,Address=Address,
                                    City=City,State=State,Pin=Pin,Religion=Religion)
            Transact_Details.objects.create(Account=Account_Number,Amount=Amount,Debit_Credit='Credit')
            
        
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:620px;height:800px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {Name} in my bank A/C</h3>
                <h3>Your A/C Open Successfully in Bank</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>Customer Name :</th><td>{Name}</td></tr>
                <tr><th>Father's Name :</th><td>{Father_Name}</td></tr>
                <tr><th>Date Of Birth :</th><td>{DOB}</td></tr>
                 <tr><th>Gender :</th><td>{Gender}</td></tr>
                <tr><th>Account No. :</th><td>{Account_Number}</td></tr>
                <tr><th>Amount :</th><td>{Amount}</td></tr>
                <tr><th>Mobile No. :</th><td>{Mobile}</td></tr>
                <tr><th>Address :</th><td>{Address}</td></tr>
                <tr><th>Customer Name :</th><td>{City}</td></tr>
                <tr><th>Father's Name :</th><td>{State}</td></tr>
                <tr><th>Account No. :</th><td>{Pin}</td></tr>
                <tr><th>Father's Name :</th><td>{Religion}</td></tr>
            </table><br><br><a href="/openAC" style="margin-left:250px;">Back</a>''')
                

    else:
        return render(request,'Bank/OpenAccount.html')
def withdraw(request):
    if request.method=='POST':
        amt=request.POST.get('amount')
        ac=request.POST.get('account')
        data=Bank_Details.objects.all()
        for acno in data:
            if(ac==acno.Account_Number):
                if(int(amt)+1000<=acno.Amount):
                    tamt=acno.Amount-int(amt)
                    inf=ATM_Details.objects.get(Account_Number=ac)
                    Bank_Details.objects.filter(Account_Number=ac).update(Amount=tamt)
                    ATM_Details.objects.filter(Account_Number=ac).update(Amount=tamt)
                    Transact_Details.objects.create(Account=acno.Account_Number,Pin=inf.Pin_Number,Amount=int(amt),Debit_Credit='Debit')
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno.Name} in my bank A/C</h3>
                 <h3>Withdraw Successfully from Your A/C</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>A/C Number :</th><td>{ac}</td></tr>
                <tr><th>Withdraw Amount :</th><td>{amt}</td></tr>
                <tr><th>Total Amount :</th><td>{tamt}</td></tr>
            </table><br><br><a href="/withdraw" style="margin-left:250px;">Back</a>''')
                
                else:
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno.Name} in my bank A/C</h3>
                <h3>Sorry, You do not have enough balence in your A/C. Please check</h3>
                <br><br><a href="/withdraw" style="margin-left:250px;">Back</a>''')
                

        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your A/C number is wrong. Please check</h3>
                <br><br><a href="/withdraw" style="margin-left:250px;">Back</a>''')
                
    else:
        return render(request,'Bank/Withdraw.html')
def deposite(request):
    if request.method=='POST':
        amt=request.POST.get('amount')
        ac=request.POST.get('account')
        data=Bank_Details.objects.all()
        for acno in data:
            if(ac==acno.Account_Number):
                tamt=acno.Amount+int(amt)
                inf=ATM_Details.objects.get(Account_Number=ac)
                Bank_Details.objects.filter(Account_Number=ac).update(Amount=tamt)
                ATM_Details.objects.filter(Account_Number=ac).update(Amount=tamt)
                Transact_Details.objects.create(Account=acno.Account_Number,Pin=inf.Pin_Number,Amount=int(amt),Debit_Credit='Credit')
                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno.Name} in my bank A/C</h3>
                 <h3>Your Amount Deposit Successfully into A/C</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>A/C Number :</th><td>{ac}</td></tr>
                <tr><th>Withdraw Amount :</th><td>{amt}</td></tr>
                <tr><th>Total Amount :</th><td>{tamt}</td></tr>
            </table><br><br><a href="/deposit" style="margin-left:250px;">Back</a>''')
                
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your A/C number is wrong. Please check</h3>
                <br><br><a href="/deposit" style="margin-left:250px;">Back</a>''')
            
        
    else:
        return render(request,'Bank/Deposit.html')
def changeMobile(request):
    if request.method=='POST':
        ac=request.POST.get('account')
        rjn=request.POST.get('reason')
        om=request.POST.get('oMobile')
        nm=request.POST.get('nMobile')
        data=Bank_Details.objects.all()
        for acno in data: 
            if(ac==acno.Account_Number): 
                if(om==nm):
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                        width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                        <h3 style='text-align:center;background-color:purple; color:white'>
                        Welcome in my bank A/C</h3>
                        <h3>Sorry, your  both Mobile number is Same. Please check</h3>
                        <br><br><a href="/changeMobile" style="margin-left:250px;">Back</a>''')
                                
                if(int(om)==acno.Mobile):
                    Bank_Details.objects.filter(Account_Number=ac).update(Mobile=int(nm))
                    ATM_Details.objects.filter(Account_Number=ac).update(Mobile=int(nm))
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno.Name} in my bank A/C</h3>
                 <h3>Your Mobile Number change Successfully in Bank</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>A/C Number :</th><td>{acno.Account_Number}</td></tr>
                <tr><th>Total Amount :</th><td>{acno.Amount}</td></tr>
                <tr><th>Mobile No. :</th><td>{acno.Mobile}</td></tr>
            </table><br><br><a href="/deposit" style="margin-left:250px;">Back</a>''')
                
                else:
                        return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                        width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                        <h3 style='text-align:center;background-color:purple; color:white'>
                        Welcome in my bank A/C</h3>
                        <h3>Sorry, This Mobile number "{om}" is not attached from your Account . Please check</h3>
                        <br><br><a href="/changeMobile" style="margin-left:250px;">Back</a>''')
                    
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your A/C number is wrong. Please check</h3>
                <br><br><a href="/changeMobile" style="margin-left:250px;">Back</a>''')
            
    else:
        return render(request,'Bank/ChangeMobileNo.html')
def balanceEnq(request):
    if request.method=='POST':
        ac=request.POST.get('account')
        data=Bank_Details.objects.all()
        for acno in data:
            if(ac==acno.Account_Number):
                amt=acno.Amount
                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno.Name} in my bank A/C</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>A/C Number :</th><td>{ac}</td></tr>
                <tr><th>Amount :</th><td>{amt}</td></tr>
            </table><br><br><a href="/balanceEnq" style="margin-left:250px;">Back</a>''')
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your A/C number is wrong. Please check</h3>
                <br><br><a href="/balanceEnq" style="margin-left:250px;">Back</a>''')
            
    else:
        return render(request,'Bank/BalanceEnq.html')
def fundTransfer(request):
    if request.method=='POST':
        ac1=request.POST.get('account1')
        ac2=request.POST.get('account2')
        am=request.POST.get('amount')
        data=Bank_Details.objects.all()
        if(ac1==ac2):
            #return HttpResponse("Your A/C Number are same")
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your both A/C number is same. Please check</h3>
                <br><br><a href="/fundTransfer" style="margin-left:250px;">Back</a>''')
            
        else:
            for acno1 in data:
                if(ac1==acno1.Account_Number):
                    for acno2 in data:
                        if(ac2==acno2.Account_Number):
                            if(int(am)+1000<=acno1.Amount):
                                tam1=acno1.Amount-int(am)
                                tam2=acno2.Amount+int(am)
                                inf1=ATM_Details.objects.get(Account_Number=ac1)
                                inf2=ATM_Details.objects.get(Account_Number=ac2)
                                Bank_Details.objects.filter(Account_Number=ac1).update(Amount=tam1)
                                Bank_Details.objects.filter(Account_Number=ac2).update(Amount=tam2)
                                ATM_Details.objects.filter(Account_Number=ac1).update(Amount=tam1)
                                ATM_Details.objects.filter(Account_Number=ac2).update(Amount=tam2)
                                Transact_Details.objects.create(Account=acno1.Account_Number,Pin=inf1.Pin_Number,Amount=int(am),Debit_Credit='Debit')
                                Transact_Details.objects.create(Account=acno2.Account_Number,Pin=inf2.Pin_Number,Amount=int(am),Debit_Credit='Credit')
                                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno1.Name} in my bank A/C</h3>
                 <h3>Your Fund transfer Successfully into A/C</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>A/C Number :</th><td>{ac1}</td></tr>
                <tr><th>Withdraw Amount :</th><td>{am}</td></tr>
                <tr><th>Total Amount :</th><td>{tam1}</td></tr>
            </table><br><br><a href="/deposit" style="margin-left:250px;">Back</a>''')
                
                            else:
                                #return HttpResponse("<h1>You do not have enough balence in your account</h1>")
                                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; 
                border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno1.Name} in my bank A/C</h3>
                <h3>Sorry, You do not have enough balence in your A/C. Please check</h3>
                <br><br><a href="/fundTransfer" style="margin-left:250px;">Back</a>''')
                
                    else:    
                        #return HttpResponse("Destination A/C does not exist") 
                        return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno1.Name} in my bank A/C</h3>
                <h3>Sorry, Destination A/C does not exists. Please check</h3>
                <br><br><a href="/fundTransfer" style="margin-left:250px;">Back</a>''')
                           
            else:
                #return HttpResponse("Sorry You are not a exists Accounter")
                return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your A/C number is not exists in Bank. Please check</h3>
                <br><br><a href="/fundTransfer" style="margin-left:250px;">Back</a>''')
            
    else:
        return render(request,'Bank/FundTransfer.html')
def closeAC(request):
    if(request.method=='POST'):
        ac=request.POST.get('account')
        rjn=request.POST.get('reason')
        mb=request.POST.get('mobile')
        data=Bank_Details.objects.all()
        for acno in data:
            if(ac==acno.Account_Number):
                if(int(mb)==acno.Mobile):
                    Bank_Details.objects.filter(Account_Number=ac).delete()
                    ATM_Details.objects.filter(Account_Number=ac).delete()
                    Transact_Details.objects.filter(Account=ac).delete()
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:620px;height:800px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome {acno.Name} in my bank A/C</h3>
                <h3>Your A/C Closed Successfully from Bank</h3>
                <table style="margin:auto;font-size:25px">
                <tr><th>Customer Name :</th><td>{acno.Name}</td></tr>
                <tr><th>Father's Name :</th><td>{acno.Father_Name}</td></tr>
                <tr><th>Date Of Birth :</th><td>{acno.DOB}</td></tr>
                 <tr><th>Gender :</th><td>{acno.Gender}</td></tr>
                <tr><th>Account No. :</th><td>{acno.Account_Number}</td></tr>
                <tr><th>Amount :</th><td>{acno.Amount}</td></tr>
                <tr><th>Mobile No. :</th><td>{acno.Mobile}</td></tr>
                <tr><th>Address :</th><td>{acno.Address}</td></tr>
                <tr><th>Customer Name :</th><td>{acno.City}</td></tr>
                <tr><th>Father's Name :</th><td>{acno.State}</td></tr>
                <tr><th>Account No. :</th><td>{acno.Pin}</td></tr>
                <tr><th>Father's Name :</th><td>{acno.Religion}</td></tr>
            </table><br><br><a href="/closeAC" style="margin-left:250px;">Back</a>''')
            
                else:
                    return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                        width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                        <h3 style='text-align:center;background-color:purple; color:white'>
                        Welcome in my bank A/C</h3>
                        <h3>Sorry, This Mobile number "{mb}" is not attached from your Account . Please check</h3>
                        <br><br><a href="/closeAC" style="margin-left:250px;">Back</a>''')
                    
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your A/C number is wrong. Please check</h3>
                <br><br><a href="/closeAC" style="margin-left:250px;">Back</a>''')
            
                
    else:
        return render(request,'Bank/CloseBank.html')
def transaction(request):
    if request.method=='POST':
        ac=request.POST.get('account')
        mb=request.POST.get('mobile')
        data=Transact_Details.objects.all()
        for acno in data:
            if(ac==acno.Account):
                info=Transact_Details.objects.filter(Account=ac)
                return render(request,'Bank/Passbook.html',{'info':info})
        else:
            return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                <h3 style='text-align:center;background-color:purple; color:white'>
                Welcome in my bank A/C</h3>
                <h3>Sorry, your A/C number is wrong. Please check</h3>
                <br><br><a href="/transaction" style="margin-left:250px;">Back</a></div>''')                                 
                
    else:
        return render(request,'Bank/Transaction.html')
    
