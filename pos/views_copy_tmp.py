from datetime import datetime
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template, Context

from BusinessApp.function import *
from expenses.models import Expenses
from inventory.models import Inventory
from invoice.models import Invoice, Sale
from pos.models import Cash_Counter, Print_Template
from purchase.models import Stock, Payment
from django.http import JsonResponse
from django.core import serializers
from setting.models import Setting
from django.views import View

from supplier.models import Supplier, Bundle

from django.db.models import Q


class Pos_Supplier_payment(View):

    def get(self, request):

        supplier_list = Supplier.objects.filter(company_id=request.COOKIES.get('company_id'))

        payment_list=Payment.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, transaction_date=datetime.today().date())

        total_amount=payment_list.aggregate(total_amount=Sum('amount', default=0))

        total_amount=total_amount.get('total_amount')

        form_start_date = datetime.today().strftime('%d/%m/%Y')
        form_end_date = datetime.today().strftime('%d/%m/%Y')

        context={

            "supplier_list": supplier_list,
            "payment_list": payment_list,
            "total_amount": total_amount,
            "form_start_date": form_start_date,
            "form_end_date": form_end_date,

        }

        print(datetime.today())

        return render(request, 'supplier_payment.html', context)

    def post(self, request):

        if 'start_date' in request.POST and 'end_date' in request.POST:
            form_start_date = request.POST['start_date']
            start_date = request.POST['start_date'].replace("/", "-")
            start_date = datetime.strptime(start_date, "%d-%m-%Y")
            form_end_date = request.POST['end_date']
            end_date = request.POST['end_date'].replace("/", "-")
            end_date = datetime.strptime(end_date, "%d-%m-%Y")

            supplier_list = Supplier.objects.filter(company_id=request.COOKIES.get('company_id'))

            payment_list = Payment.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                                  transaction_date__gte=start_date,
                                                  transaction_date__lte=end_date)

            total_amount = payment_list.aggregate(total_amount=Sum('amount', default=0))

            total_amount = total_amount.get('total_amount')

            context = {

                "supplier_list": supplier_list,
                "payment_list": payment_list,
                "total_amount": total_amount,
                "form_start_date": form_start_date,
                "form_end_date": form_end_date,

            }

            print(datetime.today())

            return render(request, 'supplier_payment.html', context)

        if 'amount' in request.POST:
            Payment(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                    supplier_id=request.POST["supplier_id"],
                    transaction_date=datetime.today(), description='CASH PAID BY CASH COUNTER',
                    paid_by='CASH',
                    amount=request.POST['amount']).save()



            return redirect('pos_supplier_payment')


class Pos_Bundle(View):
    def get(self,request):

        bundle_list = Bundle.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                            entry_date__date=datetime.today().date())

        total_amount = bundle_list.aggregate(total_transport_charge=Sum('transport_charge', default=0),
                                             total_service_charge=Sum('service_charge', default=0))

        total_amount['total'] = total_amount.get("total_transport_charge") + total_amount.get(
            "total_service_charge")

        form_start_date = datetime.today().strftime('%d/%m/%Y')
        form_end_date = datetime.today().strftime('%d/%m/%Y')

        tran_del = request.GET.get('tran_del')
        if tran_del:
            bundle_transport = setting_value(request, "bundle_transport")
            bundle_transport = bundle_transport.replace(f"{tran_del};", "")
            setting_update(request, "bundle_transport", bundle_transport)
            return redirect('pos_bundle')

        bundle_transport = setting_value(request, "bundle_transport")
        print(bundle_transport, "yes'")
        bundle_transport = bundle_transport.split(";")
        bundle_transport = list(filter(None, bundle_transport))




        supplier_list=Supplier.objects.filter(company_id=request.COOKIES.get('company_id'))



        context={
            "bundle_transport":bundle_transport,
            "supplier_list": supplier_list,
            "bundle_list": bundle_list,
            "total_amount": total_amount,
            "form_start_date": form_start_date,
            "form_end_date": form_end_date,

        }

        print(context)
        return render(request, 'bundle.html', context)


    def post(self,request):

        if 'start_date' in request.POST and 'end_date' in request.POST:
            form_start_date = request.POST['start_date']
            start_date = request.POST['start_date'].replace("/", "-")
            start_date = datetime.strptime(start_date, "%d-%m-%Y")
            form_end_date = request.POST['end_date']
            end_date = request.POST['end_date'].replace("/", "-")
            end_date = datetime.strptime(end_date, "%d-%m-%Y")

            bundle_list = Bundle.objects.filter(
                company_id=request.COOKIES.get('company_id'),
                user_id=request.user.id,
                entry_date__date__gte=start_date,
                entry_date__date__lte=end_date
            )

            total_amount = bundle_list.aggregate(total_transport_charge=Sum('transport_charge', default=0),
                                                 total_service_charge=Sum('service_charge', default=0))

            total_amount['total'] = total_amount.get("total_transport_charge") + total_amount.get(
                "total_service_charge")


            bundle_transport = setting_value(request, "bundle_transport")
            print(bundle_transport,"yes'")
            bundle_transport = bundle_transport.split(";")
            bundle_transport = list(filter(None, bundle_transport))

            supplier_list = Supplier.objects.filter(company_id=request.COOKIES.get('company_id'))

            context = {
                "bundle_transport": bundle_transport,
                "supplier_list": supplier_list,
                "bundle_list": bundle_list,
                "total_amount": total_amount,
                "form_start_date": form_start_date,
                "form_end_date": form_end_date,

            }

            # print(context)
            return render(request, 'bundle.html', context)

        bundle_transport = setting_value(request, "bundle_transport")


        print(request.POST)

        try:
            if request.POST["add_transport"]:
                bundle_transport=f"{bundle_transport}{request.POST['add_transport']};"
                setting_update(request, "bundle_transport", bundle_transport)
        except:
            pass

        try:
            if request.POST["supplier_id"]:
                Bundle(user_id=request.user.id, company_id=request.COOKIES.get('company_id'), qty=request.POST["qty"], supplier_id=request.POST["supplier_id"], transport_charge=request.POST["transport_charge"],
                       service_charge=request.POST["service_charge"],transport=request.POST["transport"]).save()
        except:
            pass


        return redirect('pos_bundle')
        # return render(request, 'bundle.html', context)






def pos_statement_update(request):

    stand_by_qty = request.POST.getlist("stand_by_qty[]")
    cash_taken_qty = request.POST.getlist("cash_taken_qty[]")

    currency_denomination=setting_value(request, "currency_denomination").split(";")

    x=0
    stand_by=''
    cash_taken=''
    for denomination in currency_denomination:
        stand_by+=f"{denomination}:{stand_by_qty[x]};"
        cash_taken += f"{denomination}:{cash_taken_qty[x]};"
        x+=1

    entry_date=request.POST.get('statement_date')
    entry_date = entry_date.replace("/", "-")
    entry_date= datetime.strptime(entry_date, "%d-%m-%Y").date()


    print(datetime.today().strftime('%d/%m/%Y'))
    print(datetime.today().date())

    if Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, entry_date=entry_date).exists():
        Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, entry_date=entry_date).update(stand_by=stand_by, cash_taken=cash_taken)

    else:
        Cash_Counter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, entry_date=entry_date, stand_by=stand_by, cash_taken=cash_taken).save()

    print(stand_by)

    context={
        "test": "okok"
    }

    return HttpResponse(json.dumps(context), content_type='application/json')

def pos_bill_list(request):

    form_invoice_date=datetime.today().strftime('%d/%m/%Y')
    invoice_date=datetime.today().date()
    if request.method=='POST':
        form_invoice_date=request.POST['invoice_date']
        invoice_date = request.POST['invoice_date'].replace("/", "-")
        invoice_date = datetime.strptime(invoice_date, "%d-%m-%Y").date()

    bill_list=Invoice.objects.filter(company_id=request.COOKIES.get('company_id'),
                                     user_id=request.user.id,invoice_date__date=invoice_date).order_by("id")

    total_amount=bill_list.aggregate(payable=Sum('total_amount', default=0),
                                     discount=Sum('discount_value', default=0),
                                     round_off=Sum('round_off', default=0),
                                     card=Sum('card', default=0),
                                     upi=Sum('upi', default=0),
                                     credit=Sum('credit', default=0))

    try:
        expenses=Expenses.objects.filter(entry_date__date=invoice_date, company_id=request.COOKIES.get('company_id'), user_id=request.user.id).aggregate(
            expenses=Sum('amount', default=0))
    except:
        expenses=None

    if expenses.get('expenses') is None:
        expenses=0
    else:
        expenses=expenses.get('expenses')

    context={
        "bill_list":bill_list,
        "form_invoice_date": form_invoice_date,
        "total_amount": total_amount,
        "total": total_amount.get("payable")+total_amount.get("discount")+total_amount.get("round_off"),
        "expenses": expenses,
        "cash_total": total_amount.get("payable")-total_amount.get("card")-total_amount.get("upi")-total_amount.get("credit")
    }


    return render(request,'bill_list.html',context)

def pos_expenses(request):



    finish=0
    if Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                   entry_date__date=datetime.today().date(), finish=1).exists():
        finish=1
    if 'amount' in request.POST:
       if finish==0:
            Expenses(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, description=request.POST['description'],
                 amount=request.POST['amount']).save()


    # Initialize
    expenses = []
    balance = 0

    if 'start_date' in request.POST and 'end_date' in request.POST:
        form_start_date = request.POST['start_date']
        start_date = request.POST['start_date'].replace("/", "-")
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        form_end_date = request.POST['end_date']
        end_date = request.POST['end_date'].replace("/", "-")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        # Get expenses safely
        expenses_list = Expenses.objects.filter(
            entry_date__date__gte=start_date, entry_date__date__lte=end_date,
            company_id=request.COOKIES.get('company_id'),
            user_id=request.user.id
        )

    else:
        # Get expenses safely
        expenses_list = Expenses.objects.filter(
            entry_date__date=datetime.today(),
            company_id=request.COOKIES.get('company_id'),
            user_id=request.user.id
        )

        form_start_date = datetime.today().strftime('%d/%m/%Y')
        form_end_date = datetime.today().strftime('%d/%m/%Y')

    # Loop through and calculate running balance
    for data in expenses_list:
        balance += data.amount or 0  # Ensure amount isn't None
        expenses.append({
            "entry_date": data.entry_date,
            "description": data.description,
            "amount": data.amount,
            "balance": balance,
        })


    print(expenses)

    context={
        "expenses_list": expenses,
        "finish": finish,
        "form_start_date": form_start_date,
        "form_end_date": form_end_date,
    }


    return render(request, 'expenses.html', context)



def pos_statement(request):

    if request.POST.get("finish_count"):
        finish_count = int(request.POST.get("finish_count"))
        finish_count+=1
    else:
        finish_count=0


    form_statement_date=datetime.today().strftime('%d/%m/%Y')
    statement_date=datetime.today().date()
    if request.POST.get('statement_date'):
        form_statement_date=request.POST['statement_date']
        statement_date = request.POST['statement_date'].replace("/", "-")
        statement_date = datetime.strptime(statement_date, "%d-%m-%Y").date()

        shortage = request.POST.get('shortage','')


        print(shortage)
        print(finish_count)
        print(request.POST.get('finish'))

        if request.POST.get('finish')=='1' and (int(finish_count)>=3 or (float(shortage)<=10 and float(shortage)>=-10 and shortage!='')):
            print("jjjjjjjjjjj")
            if Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                           entry_date__date=statement_date).exists():
                data=Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                                           entry_date__date=statement_date)
                data.update(finish='1', shortage=float(request.POST['shortage']),
                            stand_by_total=float(request.POST['stand_by_total']),
                            cash_taken_total=float(request.POST['cash_taken_total']))


    try:
        invoice = Invoice.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,invoice_date__date=statement_date).aggregate(total_sale=Sum('total_amount', default=0),
               card=Sum('card', default=0),upi=Sum('upi', default=0),credit=Sum('credit', default=0),
                round_off=Sum('round_off', default=0),discount=Sum('discount_value', default=0))
    except:
        invoice=None

    total_cancel_amount = 0
    try:
        cancel_bill=Invoice.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,invoice_date__date=statement_date).exclude(cancel_no=None)
        for data in cancel_bill:
            total_cancel_amount += Invoice.objects.filter(company_id=request.COOKIES.get('company_id'),
                                                          invoice_number=data.cancel_no,
                                                          invoice_date__date=statement_date).latest('id').total_amount
    except:
        cancel_bill=None

    try:
        total_return_amount=Invoice.objects.filter(company_id=request.COOKIES.get('company_id'),user_id=request.user.id,total_amount__lt=0, invoice_date=statement_date, invoice_date__date=statement_date).aggregate(total_return_amount=Sum('total_amount'))
    except:
        total_return_amount=None

    try:
        expenses=Expenses.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,entry_date__date=statement_date).aggregate(
            expenses=Sum('amount', default=0))
    except:
        expenses=None

    if expenses.get('expenses') is None:
        expenses=0
    else:
        expenses=expenses.get('expenses')

    bundle_charge=0
    try:
        bundle_list=Bundle.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, entry_date__date=datetime.today().date())

        total_amount=bundle_list.aggregate(total_transport_charge=Sum('transport_charge', default=0), total_service_charge=Sum('service_charge', default=0))

        bundle_charge=total_amount.get("total_transport_charge")+total_amount.get("total_service_charge")
    except:
        pass


    try:
        payment_list=Payment.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, transaction_date=datetime.today().date())
        supplier_payment=payment_list.aggregate(total_amount=Sum('amount', default=0))
        supplier_payment=supplier_payment.get('total_amount')
    except:
        pass



    cash_counter_data=None
    cash_counter_status=0
    if Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id, entry_date=statement_date).exists():
        cash_counter=Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                    entry_date=statement_date).latest('id')
        cash_counter_status=cash_counter.finish
        stand_by=cash_counter.stand_by.split(";")
        cash_taken = cash_counter.cash_taken.split(";")

        cash_counter_data=[]
        for i in range(len(stand_by)-1):
            stand_by_data=stand_by[i].split(":")
            cash_taken_data = cash_taken[i].split(":")

            datax={
                "denomination":stand_by_data[0],
                "stand_by": stand_by_data[1],
                "cash_taken": cash_taken_data[1]
            }
            cash_counter_data.append(datax)

    else:
        currency_denomination = setting_value(request, "currency_denomination").split(";")
        cash_counter_data = []
        for denomination in currency_denomination:
            datax = {
                "denomination": denomination,
                "stand_by": '',
                "cash_taken": ''
            }
            cash_counter_data.append(datax)


    ### LAST CASH COUNTER STANDBY
    cash_counter_stand_by = 0
    cash_counter_queryset = Cash_Counter.objects.filter(
        company_id=request.COOKIES.get('company_id'),
        user_id=request.user.id,
        finish=1,
        entry_date__date__lt=statement_date
    )

    if cash_counter_queryset.exists():
        cash_counter_stand_byx = cash_counter_queryset.latest('id')  # Get the latest entry

        stand_by=cash_counter_stand_byx.stand_by.split(";")


        for i in range(len(stand_by)-1):
            stand_by_data=stand_by[i].split(":")
            if stand_by_data[1]!='':
                cash_counter_stand_by += int(stand_by_data[0])*int(stand_by_data[1])


    print(cash_counter_stand_by,"YYY")





    total_sale=invoice.get('total_sale')+invoice.get('round_off')+invoice.get('discount')

    cash_balance=(cash_counter_stand_by+total_sale)-(expenses+supplier_payment+bundle_charge+invoice.get('discount')+invoice.get('card')+invoice.get('upi')+invoice.get('credit'))

    context={
        "user": request.user.username,
        "total_sale": total_sale,
        "invoice": invoice,
        "total_cancel_amount": total_cancel_amount,
        "total_return_amount": total_return_amount.get('total_return_amount'),
        "form_statement_date": form_statement_date,
        "expenses": expenses,
        "cash_balance": cash_balance,
        "cash_counter": cash_counter_data,
        "cash_counter_status":cash_counter_status,
        "bundle_charge": bundle_charge,
        "supplier_payment": supplier_payment,
        "cash_counter_stand_by": cash_counter_stand_by,
        "finish_count": finish_count

    }


    return render(request, 'pos_statement.html',context)

def pos(request):

    inventory_list=Inventory.objects.filter(company_id=request.COOKIES.get('company_id'))
    finish=0
    if Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                   entry_date__date=datetime.today().date(), finish=1).exists():
        finish=1

    context={
        "inventory_list":inventory_list,
        "finish": finish
    }

    return render(request, 'pos.html', context)

def pos_bill_copy(request):

    recent_invoice = Invoice.objects.filter(
        company_id=request.COOKIES.get('company_id'),
        user_id=request.user.id
    ).order_by('-id')[:10]

    try:
        invoice = Invoice.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id).latest('id')
        context = {
            "invoice_date": invoice.invoice_date.strftime('%d/%m/%Y'),
            "invoice_number": invoice.invoice_number,
            "recent_invoice": recent_invoice
        }
    except:
        context = {
            "invoice_number": 0
        }

    if "cash_data_id" in request.POST:
        invoice_id = request.POST.get("cash_data_id")
        invoice = Invoice.objects.get(id=invoice_id)

        def none_if_empty(val):
            return val if val.strip() else None

        invoice.cash = none_if_empty(request.POST.get("cash", ""))
        invoice.card = none_if_empty(request.POST.get("card", ""))
        invoice.upi = none_if_empty(request.POST.get("upi", ""))

        invoice.save()

    return render(request, 'bill_copy.html', context)

def pos_print_bill(request):
    context={}
    if request.method == "POST":
        invoice_date = request.POST['bill_date'].replace("/", "-")
        invoice_date = datetime.strptime(invoice_date, "%d-%m-%Y").date()
        if Invoice.objects.filter(user_id=request.user.id, company_id=request.COOKIES.get('company_id'), invoice_date__date=invoice_date, invoice_number=request.POST['bill_number']).exists():
            invoice_id=Invoice.objects.filter(company_id=request.COOKIES.get('company_id'), invoice_date__date=invoice_date, invoice_number=request.POST['bill_number']).latest('id').id
            context=print_invoice_context(invoice_id)
        elif Invoice.objects.filter(user_id=request.user.id, company_id=request.COOKIES.get('company_id'), invoice_number=request.POST['bill_number']).exists():
            invoice_id = Invoice.objects.filter(company_id=request.COOKIES.get('company_id'),
                                                invoice_number=request.POST['bill_number']).latest('id').id
            context = print_invoice_context(invoice_id)
        else:
            context = {}


    if datetime.today().date()==invoice_date:
        context["finish"]=0
    else:
        context["finish"] = 1
    if Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                   entry_date__date=invoice_date, finish=1).exists():
        context["finish"]=1


    return HttpResponse(json.dumps(context), content_type='application/json')

def pos_cancel_bill(request):
    context = {}
    if request.method == "POST":
        invoice_data=Invoice.objects.get(id= request.POST['invoice_id'])
        master_id=invoice_data.id
        cancel_no=invoice_data.invoice_number

        invoice_data.pk = None

        invoice_data.save()

        cancel_invoice_id=invoice_data.id

        Invoice.objects.filter(id=cancel_invoice_id).update(cancel_no=cancel_no, invoice_number=new_invoice_number(request), total_amount=F('total_amount')*-1)

        sale_data=Sale.objects.filter(invoice_id=master_id)

        for data in sale_data:
            data.pk = None
            data.save()
            Sale.objects.filter(id=data.id).update(invoice_id=cancel_invoice_id, qty=F('qty')*-1)

        context = print_invoice_context(master_id)

    return HttpResponse(json.dumps(context), content_type='application/json')

def new_invoice_number(request):
    # NEW INVOICE NUMBER GENERATOR
    if datetime.now() < datetime(datetime.now().year, 4, 1):
        account_year = datetime(datetime.now().year - 1, 4, 1)
    else:
        account_year = datetime(datetime.now().year, 4, 1)

    if Invoice.objects.filter(company_id=request.COOKIES.get('company_id'), invoice_date__gte=account_year,
                              invoice_date__lte=datetime.now()).exists():
        invoice_number = Invoice.objects.filter(company_id=request.COOKIES.get('company_id'),
                                                invoice_date__gte=account_year,
                                                invoice_date__lte=datetime.now()).latest(
            'invoice_number').invoice_number
        invoice_number = 1 + invoice_number

    else:
        invoice_number = 1
    # END NEW INVOICE NUMBER GENERATOR

    return invoice_number

def add_new_invoice(request):

    if request.method=="POST":
        result=1
        inventory=request.POST.getlist("inventory[]")
        inventory_id = request.POST.getlist("inventory_id[]")
        unit = request.POST.getlist("unit[]")
        qty = request.POST.getlist("qty[]")
        price = request.POST.getlist("price[]")
        stock_id = request.POST.getlist("stock_id[]")
        tax_rate = request.POST.getlist("tax_rate[]")
        row_discount = request.POST.getlist("row_discount[]")

        # NEW INVOICE NUMBER GENERATOR
        invoice_number = new_invoice_number(request)
        # END NEW INVOICE NUMBER GENERATOR

        cash_balance=request.POST['cash_balance']
        card_balance = request.POST['card_balance']
        upi_balance = request.POST['upi_balance']
        credit_balance = request.POST['credit_balance']
        round_off=request.POST['round_off']
        over_all_discount_value=request.POST['over_all_discount_value']

        if not request.POST['cash_balance']:
            cash_balance=None
        if not request.POST['card_balance']:
            card_balance=None
        if not request.POST['upi_balance']:
            upi_balance=None
        if not request.POST['credit_balance']:
            credit_balance=None
        if not request.POST['round_off']:
            round_off=None
        if request.POST['over_all_discount_value']=='0':
            over_all_discount_value=None






        Invoice(user_id=request.user.id, round_off=round_off, total_amount=request.POST['total_amount'], headline=request.POST['headline'], cash=cash_balance, card=card_balance,
                upi=upi_balance, credit=credit_balance, discount_value=over_all_discount_value, discount=request.POST['discount'],company_id=request.COOKIES.get('company_id'),
                invoice_number=invoice_number).save()

        invoice=Invoice.objects.filter(company_id=request.COOKIES.get('company_id')).latest('id')

        exchange_value = 0
        for x in range(len(inventory)):

            if unit[x]!='':
                Sale(discount=row_discount[x], tax_rate=tax_rate[x], invoice_id=invoice.id,stock_id=stock_id[x],unit=unit[x],qty=qty[x],sale_price=price[x],inventory_id=inventory_id[x]).save()

                if float(qty[x])<0:
                    exchange_value+=float(price[x])*float(unit[x])*float(qty[x])

        if exchange_value!=0:
            invoice.exchange_value=exchange_value
            invoice.save()

        return invoice.id

def print_invoice_context(invoice_id):



    invoice = Invoice.objects.get(id=invoice_id)

    if invoice.user.pos_template is None:
        template = Print_Template.objects.filter(pk=1).first()
        template_string = template.template if template else ''
    else:
        template = Print_Template.objects.filter(pk=invoice.user.pos_template.id).first()
        template_string = template.template if template else ''




    invoice_cancelled = 0
    if Invoice.objects.filter(cancel_no=invoice.invoice_number, invoice_date=invoice.invoice_date).exists():
        invoice_cancelled = 1


    sale_datax = Sale.objects.filter(invoice_id=invoice.id)
    total_unit = sum(sale_datax.values_list('unit', flat=True))
    total_qty = sum(sale_datax.values_list('qty', flat=True))

    sale_data = []
    total_amount = 0
    total_gross_amount = 0
    total_tax_amount = 0


    for data in sale_datax:
        sale_price = data.sale_price

        if "%" in data.discount:
            discount = data.discount.replace("%", "")
            sale_price = data.sale_price - (data.sale_price * float(discount) / 100)
        else:
            if data.discount:
                sale_price = data.sale_price - float(data.discount)

        amount = (data.unit * data.qty * sale_price)
        gross_sale_price = sale_price / ((data.tax_rate / 100) + 1)
        gross_amount = (data.unit * data.qty * gross_sale_price)
        tax_amount = sale_price - gross_sale_price

        sale_dataz = {
            "inventory_name": data.inventory.inventory_name,
            "unit": data.unit,
            "qty": data.qty,
            "sale_price": data.sale_price,
            "amount": amount,
            "tax_rate": data.tax_rate,
            "tax_amount": ("%.2f" % tax_amount),
            "gross_sale_price": ("%.2f" % gross_sale_price),

        }
        total_gross_amount += gross_amount
        total_tax_amount += tax_amount
        total_amount += (data.unit * data.qty * sale_price)
        sale_data.append(sale_dataz)

    total_discount = 0
    total_discount_percent = 0
    if invoice.discount:
        if "%" in invoice.discount:
            total_discount_percent = invoice.discount.replace("%", "")
            total_discount = (total_amount * (float(total_discount_percent) / 100))
        else:
            total_discount = float(invoice.discount)
            total_discount_percent = abs(float(
                ((float(total_amount) - float(total_discount)) / (float(total_amount)) * 100)) - 100)

    total_gross_amount = total_gross_amount - total_gross_amount * (float(total_discount_percent) / 100)
    total_tax_amount = total_tax_amount - total_tax_amount * (float(total_discount_percent) / 100)

    import string
    def to_alpha(data):
        alphabet = list(string.ascii_lowercase)
        if data <= 25:
            return alphabet[data]
        else:
            dividend = data + 1
            alpha = ""
            while dividend > 0:
                modulo = (dividend - 1) % 26
                alpha = alphabet[modulo] + alpha
                dividend = (dividend - modulo) // 26
            return alpha.upper()

    qr_code_data=f"{invoice.company.id}-0-{to_alpha(invoice.invoice_number)}"

    print(qr_code_data,"YESSS")

    context={
        "pos_header": Setting.objects.get(setting="pos_header", company_id=invoice.user.company.id).value,
        "pos_footer": Setting.objects.get(setting="pos_footer", company_id=invoice.user.company.id).value
    }

    if template_string:
        template_str = template_string

        # Render it safely
        rendered_template = Template(template_str).render(Context(context))

        print(rendered_template)


    context = {
        "sale_data": sale_data,
        "total_unit": total_unit,
        "total_qty": total_qty,
        "total_amount": decimal_value(total_amount),
        "invoice_number": invoice.invoice_number,
        "invoice_date": invoice.invoice_date.strftime("%d/%m/%Y %H:%M:%S"),
        "total_gross_amount": decimal_value(total_gross_amount),
        "total_tax_amount": decimal_value(total_tax_amount),
        "total_discount": total_discount,
        "total_discount_percent": total_discount_percent,
        "cash": invoice.cash,
        "card": invoice.card,
        "upi": invoice.upi,
        "username": invoice.user.username,
        "credit": invoice.credit,
        "payable": decimal_value(total_amount - total_discount),
        "headline": invoice.headline,
        "round_off": invoice.round_off,
        "invoice_total_amount": invoice.total_amount,
        "invoice_id": invoice.id,
        "invoice_cancelled":invoice_cancelled,
        "cancel_no": invoice.cancel_no,
        "qrcode_data": qr_code_data,
        "pos_template": rendered_template

    }



    return context

def complete(request):

    if Cash_Counter.objects.filter(company_id=request.COOKIES.get('company_id'), user_id=request.user.id,
                                   entry_date__date=datetime.today().date(), finish=1).exists():
        return

    invoice = Invoice.objects.get(id=add_new_invoice(request))

    context=print_invoice_context(invoice.id)

    return HttpResponse(json.dumps(context), content_type='application/json')

def barcode_query(request):
    company_id = request.COOKIES.get('company_id')
    user_id = request.user.id
    today = datetime.today().date()

    # Check if the cash counter is finished
    if Cash_Counter.objects.filter(company_id=company_id, user_id=user_id, entry_date__date=today, finish=1).exists():
        return JsonResponse({}, status=204)  # No Content Response

    if request.method == 'GET':
        query = request.GET.get('q', '')

        if not query or query == '0':
            return JsonResponse({}, status=400)  # Bad Request



        # Get barcode method
        barcode_setting = Setting.objects.filter(company_id=company_id, setting="barcode_method").order_by('-id').first()
        barcode_method = barcode_setting.value if barcode_setting else ''

        barcode_key = barcode_method.replace('{YEAR}', '').replace('{ID}', '') if barcode_method else ''
        barcode_q = query.upper().replace(barcode_key.upper(), '') if barcode_key and barcode_key.upper() in query.upper() else query

        try:
            barcode_q = int(barcode_q)  # Convert if it's a valid number
        except (ValueError, TypeError):
            barcode_q = None  # Set to None if conversion fails

        context = None

        if barcode_q and len(str(barcode_q)) > 2:
            try:
                # print(barcode_q,"ggfgf")
                stock = Stock.objects.get(barcode=barcode_q)  # Direct lookup using primary key-like behavior




                context = {
                    'inventory_id': stock.inventory.id,
                    'description': stock.inventory.inventory_name,
                    'tax_id': stock.inventory.tax_code.id,
                    'tax_rate': stock.inventory.tax_code.tax_rate,
                    'unit_enabled': stock.inventory.unit_enabled,
                    'stock_id': stock.id,
                    'price': stock.sale_price,
                    'mrp': None


                }
            except Stock.DoesNotExist:
                pass

        if context is None:
            try:

                inventory = Inventory.objects.get(
                    Q(inventory_name__iexact=query) | Q(shortcode__iexact=query),
                    company_id=company_id
                )



                context = {
                    'inventory_id': inventory.id,
                    'description': inventory.inventory_name,
                    'tax_id': inventory.tax_code.id,
                    'tax_rate': inventory.tax_code.tax_rate,
                    'unit_enabled': inventory.unit_enabled,
                    'price': inventory.default_price if inventory.default_price else None,
                    'mrp': None
                }

                # inventory = Inventory.objects.get(inventory_name__iexact=query, company_id=company_id)

            except Inventory.DoesNotExist:
                pass  # No inventory found, keep context as None

        if context is None and len(str(query)) > 2:
            try:
                stock = Stock.objects.filter(pre_barcode__iexact=query).latest("id")


                ###### MRP ########
                mrp=[]
                from django.db.models import Max

                # Step 1: Get latest stock ID per MRP for a specific pre_barcode
                latest_per_mrp = (
                    Stock.objects
                    .filter(pre_barcode=query)
                    .values('mrp')
                    .annotate(latest_id=Max('id'))
                )

                # Step 2: Fetch related stock entries using latest IDs and sort by latest_id descending
                mrpx = (
                    Stock.objects
                    .filter(id__in=[item['latest_id'] for item in latest_per_mrp])
                    .values('mrp', 'id', 'sale_price')  # id is the latest_id here
                    .order_by('-id')[:5]
                )

                # Optional: Rename 'id' to 'latest_id' if needed
                mrp = [
                    {
                        'mrp': s['mrp'],
                        'stock_id': s['id'],
                        'sale_price': s['sale_price']
                    }
                    for s in mrpx
                ]

                print(mrp)

                ###### END MRP ########


                context = {
                    'inventory_id': stock.inventory.id,
                    'description': stock.inventory.inventory_name,
                    'tax_id': stock.inventory.tax_code.id,
                    'tax_rate': stock.inventory.tax_code.tax_rate,
                    'unit_enabled': stock.inventory.unit_enabled,
                    'stock_id': stock.id,
                    'price': stock.sale_price,
                    'mrp': mrp
                }
            except Stock.DoesNotExist:
                pass

        if context is None:
            context = {"error": 1}


        print(context)
        return JsonResponse(context)


