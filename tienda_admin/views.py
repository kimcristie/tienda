from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from datetime import datetime
from django.contrib.auth.models import User
from .models import Customer, Payment, Product, DailyInput, IncomeOutcome
from django.db.models import Sum
from decimal import *
import traceback
import xlwt
from bs4 import BeautifulSoup
from django.http import HttpResponse

from .forms import SignUpForm, CustomerRegistrationForm, PaymentRegistrationForm, ProductRegistrationForm, DailyInputForm, IncomeOutcomeForm

from django.contrib.auth import login,authenticate


def home(request):
    now = datetime.now()
    inputs_diario = DailyInput.objects.filter(create_date=now).order_by('-update_date')
    expositores = Customer.objects.values('store_name').distinct()
    products = Product.objects.values('name').distinct()
    product_colours = Product.objects.values('colour').distinct()
    payment_types = Payment.objects.values('name').distinct()


    form = DailyInputForm()
    if request.method == 'POST':

		#ver se ja tem na database, se tiver é update
        if 'btn_edit_input' in request.POST:

            try:
                input_id = int(request.POST['modal_edit_id'])
                input_object = DailyInput.objects.get(id=input_id)

                input_expositor = (request.POST['modal_edit_expositor_hidden'])
                if input_expositor:
                    input_expositor_object = Customer.objects.get(store_name=input_expositor)

                input_payment = (request.POST['modal_edit_payment_hidden'])
                if input_payment:
                    input_payment_object = Payment.objects.get(name=input_payment)

                if input_expositor == "Katifa":
                    input_product_colour = (request.POST['modal_edit_colour'])
                    if input_product_colour:
                        input_product_colour_object = Product.objects.get(colour=input_product_colour)
                else:
                    input_product_colour_object = None

                input_product = (request.POST['modal_edit_product_hidden'])
                if input_product:
                    input_product_object = Product.objects.get(name=input_product)

                input_create_date = request.POST['modal_edit_date']
                input_un_price = float((request.POST['modal_edit_price_un']).replace(",",".")) #QUANDO DECIMAL FAZER ISSO NO EDITAR PRA ADC NO BANCO
                input_obs = request.POST['modal_edit_obs']

                input_qtd = int(request.POST['modal_edit_qtd'])
                calc_final_price = (input_un_price * input_qtd)
    
                if ('is_troca' in request.POST):
                    input_is_troca = bool(request.POST['modal_edit_troca'])
                else:
                    input_is_troca = False

                input_user = request.user

                input_object.create_date = datetime.strptime(input_create_date, "%Y-%m-%d")

                input_object.updated_by = input_user
                input_object.customer = input_expositor_object
                input_object.payment_type = input_payment_object
                input_object.product_type = input_product_object
                input_object.product_colour = input_product_colour_object
                input_object.qtd = input_qtd
                input_object.obs = input_obs
                input_object.is_troca = input_is_troca
                input_object.un_price = input_un_price
                input_object.final_price = calc_final_price

                input_object.save()
                return redirect('home')

            except Exception:
                traceback.print_exc()
                #pass
        elif 'btn_create_input' in request.POST:

            input_expositor = (request.POST['selected-dropdown-expositor'])
            if input_expositor:
                input_expositor_object = Customer.objects.get(store_name=input_expositor)

            input_payment = (request.POST['selected-dropdown-payment'])
            if input_payment:
                input_payment_object = Payment.objects.get(name=input_payment)

            if input_expositor == "Katifa":
                input_product_colour = (request.POST['selected-dropdown-product-colour'])
                if input_product_colour:
                    input_product_colour_object = Product.objects.get(colour=input_product_colour)
            else:
                input_product_colour_object = None

            input_product = (request.POST['selected-dropdown-product'])
            if input_product:
                input_product_object = Product.objects.get(name=input_product)

            input_create_date = (request.POST['create_date'])
            input_un_price = float(request.POST['un_price'])
            input_obs = (request.POST['obs'])
            input_qtd = int(request.POST['qtd'])
            calc_final_price = (input_un_price * input_qtd)

            if ('is_troca' in request.POST):
                input_is_troca = bool(request.POST['is_troca'])
            else:
                input_is_troca = False

            input_user = request.user

            input_object = DailyInput(create_date=input_create_date , updated_by=input_user , customer=input_expositor_object, payment_type=input_payment_object , product_type=input_product_object , product_colour=input_product_colour_object , qtd=input_qtd , obs=input_obs , is_troca=input_is_troca ,un_price=input_un_price , final_price=calc_final_price )

            input_object.save()#force_insert=True)
            return redirect('home')
    else:


        form = DailyInputForm()
    return render(request, 'home.html', {'form': form, 'inputs_diario': inputs_diario, 'expositores': expositores, 'products': products, 'product_colours':product_colours, 'payment_types':payment_types})



def signup(request):
    #pra visualizar os usuarios ja cadastrados
    usuarios = User.objects.all()


    form = SignUpForm()
    if request.method == 'POST':

		#ver se ja tem na database, se tiver é update

        if 'btn_edit_user' in request.POST:

            try:
                usuario_id = int(request.POST['modal_edit_id'])
                user_object = User.objects.get(id=usuario_id)
                usuario_username = (request.POST['modal_edit_username'])
                usuario_email = (request.POST['modal_edit_email'])

                if ('modal_edit_active' in request.POST):
                    usuario_ativo = bool(request.POST['modal_edit_active'])
                else:
                    usuario_ativo = False

                user_object.username = usuario_username
                user_object.email = usuario_email
                user_object.is_active = usuario_ativo

                user_object.save()

                return redirect('signup')

            except:
                pass
            #form = EditUserForm(**kwargs)

            #print("O QUE VEM NO SIGNUPFORM KWARSGS")
            #print(EditUserForm(**kwargs))
            #if form.is_valid():

                #print("FORMULARIO EH VALIDO SALVA ESSA PORRA SERA")
                #user = form.save()
                #return redirect('home')

        elif 'btn_signup' in request.POST:

            form = SignUpForm(request.POST)

            if form.is_valid():
                form.save()
	        #username = form.cleaned_data.get('username')
	        #raw_password = form.cleaned_data.get('password1')
	        #user = authenticate(username=username, password=raw_password)
	        #login(request, user)
                return redirect('signup')
    else:


        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'usuarios': usuarios})


def customer_registration(request):

    #pra visualizar os usuarios ja cadastrados
    expositores = Customer.objects.all()

    expositores_owners = Customer.objects.values('owner').distinct()

    #exemplo pra deletar
    #Customer.objects.filter(id=3).delete()

    form  = CustomerRegistrationForm()
    if request.method == 'POST':
        if 'btn_edit_user' in request.POST:

            try:
                customer_id = int(request.POST['modal_edit_id'])
                customer_object = Customer.objects.get(id=customer_id)
                #pega o input de dono mas se tiver o radio estiver sim e NAO nulo, pega o valor do dropdown
                customer_owner = (request.POST['modal_edit_owner'])

                customer_store_name = (request.POST['modal_edit_store_name'])
                customer_store_phone = (request.POST['modal_edit_store_phone'])
                customer_email = (request.POST['modal_edit_email'])
                customer_store_address = (request.POST['modal_edit_store_address'])
                customer_rent = int(request.POST['modal_edit_rent'])
                customer_perc_commission = int(request.POST['modal_edit_perc_commission'])

                if ('modal_edit_active' in request.POST):
                    customer_ativo = bool(request.POST['modal_edit_active'])
                else:
                    customer_ativo = False

                customer_object.owner = customer_owner
                customer_object.store_name = customer_store_name
                customer_object.email = customer_email
                customer_object.store_phone = customer_store_phone
                customer_object.store_address = customer_store_address
                customer_object.rent = customer_rent
                customer_object.perc_commission = customer_perc_commission
                customer_object.is_active = customer_ativo

                customer_object.save()

                return redirect('customer_registration')

            except:
                pass

        elif 'btn_signup' in request.POST:

            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('customer_registration')
    else:
        return render(request, 'customer_registration.html', {'form': form, 'expositores':expositores, 'expositores_owners':expositores_owners})


def product_registration(request):

    #ProductRegistrationForm
    #pra visualizar os produtos ja cadastrados
    produtos = Product.objects.exclude(name="") # pra aparecer somente produtos
    produtos_cor = Product.objects.exclude(colour="") # pra aparecer somente cores

    form = ProductRegistrationForm()

    if request.method == 'POST':

		#ver se ja tem na database, se tiver é update
        if 'btn_edit_product' in request.POST:

            try:
                product_id = int(request.POST['modal_edit_id'])
                product_object = Product.objects.get(id=product_id)
                product_name = (request.POST['modal_edit_product_name'])
                product_colour = (request.POST['modal_edit_product_colour'])
                product_colour_price = float((request.POST['modal_edit_product_colour_price']).replace(",","."))

                product_object.name = product_name
                product_object.colour = product_colour
                product_object.colour_price = product_colour_price

                product_object.save()

                return redirect('product_registration')

            except:
                pass
        elif 'btn_new_product' in request.POST:

            form = ProductRegistrationForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('product_registration')
    else:


        form = ProductRegistrationForm()
    return render(request, 'product_registration.html', {'form': form, 'produtos': produtos, 'produtos_cor':produtos_cor})


def payment_registration(request):
    #PaymentRegistrationForm Payment
    #pra visualizar os produtos ja cadastrados , 
    pagamentos = Payment.objects.all()
    form = PaymentRegistrationForm()

    if request.method == 'POST':

		#ver se ja tem na database, se tiver é update
        if 'btn_edit_payment' in request.POST:

            try:
                payment_id = int(request.POST['modal_edit_id'])
                payment_object = Payment.objects.get(id=payment_id)
                payment_name = (request.POST['modal_edit_payment_name'])

                payment_object.name = payment_name

                payment_object.save()

                return redirect('payment_type_registration')

            except:
                pass
        elif 'btn_new_payment' in request.POST:

            form = PaymentRegistrationForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('payment_type_registration')
    else:


        form = PaymentRegistrationForm()
    return render(request, 'payment_type_registration.html', {'form': form, 'pagamentos': pagamentos})


def income_outcome_registration(request):
    today = datetime.now().date()
    income_outcomes_range_date = "" #IncomeOutcome.objects.filter(create_date__range=(start_date, end_date))
    start_date = ""
    end_date = ""
    income_outcomes = IncomeOutcome.objects.filter(create_date=today)
    form = IncomeOutcomeForm()

    if request.method == 'POST':
        if 'btn_search_dates' in request.POST:
            start_date = (request.POST['input_date_begin'])
            end_date = (request.POST['input_date_end'])
            income_outcomes_range_date = IncomeOutcome.objects.filter(create_date__range=(start_date, end_date))

		#ver se ja tem na database, se tiver é update
        if 'btn_edit' in request.POST:

            try:
                income_outcome_id = int(request.POST['modal_edit_id'])
                income_outcome_object = IncomeOutcome.objects.get(id=income_outcome_id)
                income_outcome_create_date = (request.POST['modal_edit_create-date'])
                income_outcome_desc = (request.POST['modal_edit_description'])
                income_outcome_value = float((request.POST['modal_edit_income-value']).replace(",","."))

                if ('modal_edit_is-income' in request.POST):
                    is_income = bool(request.POST['modal_edit_is-income'])
                else:
                    is_income = False

                if ('modal_edit_is-outcome' in request.POST):
                    is_outcome = bool(request.POST['modal_edit_is-outcome'])
                else:
                    is_outcome = False


                income_outcome_object.create_date = datetime.strptime(income_outcome_create_date, "%Y-%m-%d")
                income_outcome_object.description = income_outcome_desc
                income_outcome_object.value = income_outcome_value
                income_outcome_object.is_income = is_income
                income_outcome_object.is_outcome = is_outcome

                income_outcome_object.save()

                return redirect('income_outcome_registration')

            except:
                pass
        elif 'btn_new' in request.POST:

            form = IncomeOutcomeForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('income_outcome_registration')
    else:


        form = IncomeOutcomeForm()
    return render(request, 'income_outcome_registration.html', {'form': form,'income_outcomes_range_date':income_outcomes_range_date, 'income_outcomes':income_outcomes, 'start_date':start_date, 'end_date':end_date})

#################################################################################################################### reports e excel
####################################### daily report

def report_daily(request):
    inputs_diarios = ""
    date_input = "" #PASSO NO RENDER PRA PODER PEGAR NO URL EXPORTAR
    list_customer = None
    list_products = None
    expositores = Customer.objects.values('store_name').distinct()
    products = Product.objects.values('name').distinct()


    #DailyInput.objects.filter(id=21).delete()

    if request.method == 'POST':

        date_input = request.POST['input_date']

        if('select_dropdown_list_customer' in request.POST):
            list_customer = request.POST.getlist('select_dropdown_list_customer') #PARA PEGAR CUSTOMER DROPDOWN
        if('select_dropdown_list_products' in request.POST):
            list_products = request.POST.getlist('select_dropdown_list_products')


        if list_customer == None and list_products == None:
            inputs_diarios = DailyInput.objects.filter(create_date=date_input).order_by('update_date')
        else:
            if list_customer != None and list_products != None:
                inputs_diarios = DailyInput.objects.filter(create_date=date_input, customer__in = Customer.objects.filter(store_name__in=list_customer), product_type__in = Product.objects.filter(name__in=list_products)).order_by('update_date')
            elif list_customer != None and list_products == None:
                inputs_diarios = DailyInput.objects.filter(create_date=date_input, customer__in = Customer.objects.filter(store_name__in=list_customer)).order_by('update_date')
            elif list_products != None and list_customer == None:
                inputs_diarios = DailyInput.objects.filter(create_date=date_input, product_type__in = Product.objects.filter(name__in=list_products)).order_by('update_date')

    return render(request, 'report_daily.html', {'inputs_diarios': inputs_diarios, 'date_input':date_input, 'expositores':expositores, 'products':products})








#######################################customer report 

def report_customer(request):
    inputs_diarios = ""
    date_input_inicio = ""
    date_input_final = ""
    list_customer = None
    list_products = None
    input_customer = None
    expositores = Customer.objects.values('owner').distinct()#ESPOSITOR OWNERS
    products = Product.objects.values('name').distinct()

    total_cartoes = ""
    total_dinheiro = ""
    total_maq_loja = ""
    comissao_tienda = ""
    taxa_maquina_da_loja = ""
    texto_valor_a_pagar = ""
    valor_aluguel = ""
    valor_total = ""
    valor_a_pagar = ""
    total_vendas_Tienda = ""
    total_vendas_Tienda_brecho = ""
    total_vendas_Katifa = ""
    total_vendas_Tienda_Katifa = ""


    if request.method == 'POST':
        date_input_inicio = request.POST['input_date_inicio']
        date_input_final = request.POST['input_date_final']

        input_customer = request.POST['select_dropdown_list_customer'] #PARA PEGAR owner

        if input_customer == "Katifa":
        #verde, amarelo, vermelho, azul, laranja, preto
            query_vendas_Katifa = DailyInput.objects.filter(create_date__range=(date_input_inicio, date_input_final), customer__in = Customer.objects.filter(owner=input_customer))

            if query_vendas_Katifa.exists():
                somas_total_vendas_Katifa = 0
                somas_total_vendas_Tienda_Katifa = 0
                #se tiver cor, colocar colour_price na tabela
                for somar_total in query_vendas_Katifa:
                    somas_total_vendas_Katifa = somas_total_vendas_Katifa + somar_total.product_colour.colour_price
                    somas_total_vendas_Tienda_Katifa = somas_total_vendas_Tienda_Katifa + somar_total.final_price

                total_vendas_Katifa = Decimal(somas_total_vendas_Katifa)
                total_vendas_Tienda_Katifa = Decimal(somas_total_vendas_Tienda_Katifa)


        elif input_customer == "Tienda":
            query_vendas_Tienda = DailyInput.objects.filter(create_date__range=(date_input_inicio, date_input_final), customer__in = Customer.objects.filter(owner=input_customer))
            if query_vendas_Tienda.exists():
                somas_total_vendas_Tienda = 0
                somas_total_vendas_Tienda_brecho = 0
                for somar_total in query_vendas_Tienda:
                    if somar_total.customer.store_name == "Tienda":
                        somas_total_vendas_Tienda = somas_total_vendas_Tienda + somar_total.final_price
                    elif somar_total.customer.store_name == "Tienda Brechó":
                        somas_total_vendas_Tienda_brecho = somas_total_vendas_Tienda_brecho + somar_total.final_price
                total_vendas_Tienda = Decimal(somas_total_vendas_Tienda)
                total_vendas_Tienda_brecho = Decimal(somas_total_vendas_Tienda_brecho)
        else:
            total_vendas_Tienda = 0.00
            total_vendas_Tienda_brecho = 0.00




            total_cartoes_query = DailyInput.objects.filter(create_date__range=(date_input_inicio, date_input_final), customer__in = Customer.objects.filter(owner=input_customer), payment_type__in = Payment.objects.filter(name__in=['cartão', 'crédito', 'débito']))

            if total_cartoes_query.exists():
                somas_cartoes = 0
                for somar_total_cartoes in total_cartoes_query:
                    somas_cartoes = somas_cartoes + somar_total_cartoes.final_price
                total_cartoes = Decimal(somas_cartoes)
            else:
                total_cartoes = 0.00



            total_dinheiro_query = DailyInput.objects.filter(create_date__range=(date_input_inicio, date_input_final), customer__in = Customer.objects.filter(owner=input_customer), payment_type__in = Payment.objects.filter(name='dinheiro'))
            if total_dinheiro_query.exists():
                somas_dinheiro = 0
                for somar_total in total_dinheiro_query:
                    somas_dinheiro = somas_dinheiro + somar_total.final_price
                total_dinheiro = Decimal(somas_dinheiro)
            else:
                total_dinheiro = 0.00


            customer_objeto = Customer.objects.filter(store_name=input_customer) # store name pra pegar só os dados de aluguel etc do dono
            percentagem = customer_objeto[0].perc_commission

            if total_cartoes:
                comissao_tienda = Decimal(int(percentagem) * Decimal(total_cartoes)) / Decimal(100.0)
            else:
                comissao_tienda = 0


            total_maq_loja_query = DailyInput.objects.filter(create_date__range=(date_input_inicio, date_input_final), customer__in = Customer.objects.filter(owner=input_customer), payment_type__in = Payment.objects.filter(name='máquina da loja'))

            if total_maq_loja_query.exists():
                somas_maq_loja = 0
                for somar_total in total_maq_loja_query:
                    somas_maq_loja = somas_maq_loja + somar_total.final_price
                total_maq_loja = Decimal(somas_maq_loja)

                taxa_maquina_da_loja = Decimal(5 * Decimal(total_maq_loja) ) / Decimal(100.0)
            else:
                total_maq_loja = 0.00
                taxa_maquina_da_loja = 0.00


        
            valor_aluguel = Decimal(customer_objeto[0].rent)

            valor_total_a = Decimal(comissao_tienda) + Decimal(taxa_maquina_da_loja) + Decimal(valor_aluguel)
            valor_total_b = Decimal(total_dinheiro) + Decimal(total_maq_loja)

            valor_total = Decimal(total_cartoes) + Decimal(total_dinheiro) + Decimal(total_maq_loja)

            if valor_total_a > valor_total_b:
                valor_a_pagar = Decimal(valor_total_a) - Decimal(valor_total_b)
                texto_valor_a_pagar = "Total "+ input_customer +" pagar para Tienda:"
            else:
                valor_a_pagar =  Decimal(valor_total_b) - Decimal(valor_total_a)
                texto_valor_a_pagar = "Total Tienda pagar para "+ input_customer +":"


        inputs_diarios = DailyInput.objects.filter(create_date__range=(date_input_inicio, date_input_final), customer__in = Customer.objects.filter(owner=input_customer)).order_by('customer__store_name','update_date')

    return render(request, 'report_customer.html', {'inputs_diarios': inputs_diarios, 'date_input_inicio':date_input_inicio, 'date_input_final':date_input_final, 'expositores':expositores, 'owner_name':input_customer, 'total_cartoes':total_cartoes, 'total_dinheiro':total_dinheiro, 'total_maq_loja':total_maq_loja, 'comissao_tienda':comissao_tienda, 'taxa_maquina_da_loja':taxa_maquina_da_loja, 'texto_valor_a_pagar':texto_valor_a_pagar,'valor_a_pagar':valor_a_pagar, 'valor_aluguel':valor_aluguel, 'valor_total':valor_total, "total_vendas_Tienda":total_vendas_Tienda, "total_vendas_Tienda_brecho":total_vendas_Tienda_brecho, "total_vendas_Katifa":total_vendas_Katifa, "total_vendas_Tienda_Katifa":total_vendas_Tienda_Katifa})











def report_income_outcome_registration(request):
    income_outcomes_range_date = "" #IncomeOutcome.objects.filter(create_date__range=(start_date, end_date))
    start_date = ""
    end_date = ""
    start_date_date = ""
    end_date_date = ""
    total_vendas_receita_total = 0
    total_comissao_tienda = 0
    total_aluguel_expositores = 0
    total_saidas = 0
    total_entradas = 0
    total_receita_final = 0

    if request.method == 'POST':
        start_date = (request.POST['input_date_begin'])
        end_date = (request.POST['input_date_end'])
        income_outcomes_range_date = IncomeOutcome.objects.filter(create_date__range=(start_date, end_date))
        #somar no daily input todos final price do periodo QUE EH RECEITA TOTAL

        start_date_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_date = datetime.strptime(end_date, "%Y-%m-%d")

        total_vendas_receita_total_query = DailyInput.objects.filter(create_date__range=(start_date, end_date))

        if total_vendas_receita_total_query.exists():
            somas = 0
            soma_comissao_tienda = 0
            list_customers_to_distinct = []
            for valor in total_vendas_receita_total_query:
                somas = somas + valor.final_price

                #somar no daily input todas comissoes
                if valor.payment_type.name in ['cartão', 'débito', 'crédito']:
                    soma_comissao_tienda = Decimal(soma_comissao_tienda) + (Decimal((int(valor.customer.perc_commission) * Decimal(valor.final_price)) / Decimal(100.0)))

                #checar se cusotmer ja tem na lista pra usar depois como distinct pro aluguel
                if valor.customer.owner not in list_customers_to_distinct:
                    list_customers_to_distinct.append(str(valor.customer.owner))


            total_vendas_receita_total = Decimal(somas)
            total_comissao_tienda = Decimal(soma_comissao_tienda)
        else:
            total_vendas_receita_total = 0.00
            total_comissao_tienda = 0.00
        #ENTRADAS
        
        #somar todos alugueis dos que venderem no periodo // distinct no customer owner do daily input dai essa lista buscar no Customer o aluguel
        #somar todos alugueis dos que venderem no periodo
        #VER O QUE RETORNA DESSA QUERY AQUI!!!!!
        total_alugueis_query = Customer.objects.filter(owner__in=list_customers_to_distinct)
        soma_aluguel_expositores = 0
        for alug in total_alugueis_query:
            if alug.rent > 0:
                soma_aluguel_expositores = soma_aluguel_expositores + alug.rent
        total_aluguel_expositores = soma_aluguel_expositores

        soma_saida_value = 0
        soma_entrada_value = 0
        for valor in income_outcomes_range_date:
            if valor.is_outcome is True:
                soma_saida_value = soma_saida_value + Decimal(valor.value)
            if valor.is_income is True:
                soma_entrada_value = soma_entrada_value + Decimal(valor.value)

        total_saidas = Decimal(soma_saida_value)
        total_entradas = Decimal(soma_entrada_value) + Decimal(total_aluguel_expositores) + Decimal(total_comissao_tienda)

        total_receita_final = Decimal(total_entradas) - Decimal(total_saidas)

    return render(request, 'report_income_outcome_registration.html', {'income_outcomes_range_date':income_outcomes_range_date, 'start_date':start_date, 'end_date':end_date, 'start_date_date':start_date_date, 'end_date_date':end_date_date ,'total_vendas_receita_total':total_vendas_receita_total,'total_vendas_receita_total':total_vendas_receita_total, 'total_comissao_tienda':total_comissao_tienda, 'total_aluguel_expositores':total_aluguel_expositores, 'total_saidas':total_saidas, 'total_entradas': total_entradas, 'total_receita_final':total_receita_final})




def report_customer_comparation(request):
#report_customer_comparation
    report_customer = ""
    start_date = ""
    end_date = ""
    start_date_date = ""
    end_date_date = ""

    if request.method == 'POST':
        start_date = (request.POST['input_date_inicio'])
        end_date = (request.POST['input_date_final'])

        report_customer = DailyInput.objects.filter(create_date__range=(start_date, end_date)).values('customer__store_name').annotate(final_price = Sum('final_price')).order_by('-final_price')

        start_date_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_date = datetime.strptime(end_date, "%Y-%m-%d")

    return render(request, 'report_customer_comparation.html', {'report_customer':report_customer, 'start_date':start_date, 'end_date':end_date, 'start_date_date':start_date_date, 'end_date_date':end_date_date})






def report_comparation(request):
#report_customer_comparation
    input_customer = None
    expositores = Customer.objects.values('owner').distinct()#ESPOSITOR OWNERS'owner_name':input_customer
    report_customer_inicio = ""
    report_customer_final = ""
    start_date = ""
    end_date = ""
    start_date_date = ""
    end_date_date = ""
    date_inicio_ano = ""
    date_inicio_mes = ""
    date_final_ano = ""
    date_final_mes = ""
    soma_total_mes_inicio = 0
    soma_total_mes_final = 0

    if request.method == 'POST':
        start_date = (request.POST['input_date_inicio'])
        end_date = (request.POST['input_date_final'])

        if 'select_dropdown_list_customer' in request.POST:
            input_customer = request.POST['select_dropdown_list_customer'] #PARA PEGAR owner

        #buscar todos do mes e ano e agrupar o final_price por dia
        start_date_date = datetime.strptime(start_date.replace("/","-"), "%m-%Y")
        end_date_date = datetime.strptime(end_date.replace("/","-"), "%m-%Y")

        if input_customer:
            report_customer_inicio = DailyInput.objects.filter(create_date__year=start_date_date.year, create_date__month=start_date_date.month, customer__owner=input_customer).values('create_date').annotate(final_price = Sum('final_price')).order_by('create_date')


            report_customer_final = DailyInput.objects.filter(create_date__year=end_date_date.year, create_date__month=end_date_date.month, customer__owner=input_customer).values('create_date').annotate(final_price = Sum('final_price')).order_by('create_date')

        else:

            report_customer_inicio = DailyInput.objects.filter(create_date__year=start_date_date.year, create_date__month=start_date_date.month).values('create_date').annotate(final_price = Sum('final_price')).order_by('create_date')

            report_customer_final = DailyInput.objects.filter(create_date__year=end_date_date.year, create_date__month=end_date_date.month).values('create_date').annotate(final_price = Sum('final_price')).order_by('create_date')


        #para pegar total do mês
        soma_mes_inicio = 0
        for loop_soma_inicio in report_customer_inicio:
            soma_mes_inicio = soma_mes_inicio + loop_soma_inicio['final_price']
        soma_total_mes_inicio = soma_mes_inicio


        #para pegar total do mês
        soma_mes_final = 0
        for loop_soma_final in report_customer_final:
            soma_mes_final = soma_mes_final + loop_soma_final['final_price']
        soma_total_mes_final = soma_mes_final


        date_inicio_ano = start_date_date.year
        date_inicio_mes = start_date_date.month

        date_final_ano = end_date_date.year
        date_final_mes = end_date_date.month




    return render(request, 'report_comparation.html', {'input_customer':input_customer, 'expositores':expositores, 'report_customer_inicio':report_customer_inicio, 'report_customer_final':report_customer_final,'start_date':start_date, 'end_date':end_date, 'start_date_date':start_date_date, 'end_date_date':end_date_date,'date_inicio_ano':date_inicio_ano, 'date_inicio_mes':date_inicio_mes, 'date_final_ano':date_final_ano, 'date_final_mes':date_final_mes, 'soma_total_mes_final':soma_total_mes_final, 'soma_total_mes_inicio':soma_total_mes_inicio})



        

################################################################################################################################### xls 
def export_xls(request):
    try:
        report_name = request.GET.get('report_name')
        filename_name = request.GET.get('filename_name')
        sheet_name = request.GET.get('sheet_name')
        
        response = HttpResponse(content_type='application/ms-excel')

        #QUANDO O RELATORIO EH MENSAL
        if report_name == "report_daily":
            date_input = date=request.GET.get('date_input','')#"2018-12-04"

            #response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="'+ filename_name + date_input + '.xls"' # 'attachment; filename="venda_diario.xls"'

        elif report_name =='report_customer':
            date_input_inicio = date=request.GET.get('date_input_inicio','')
            date_input_final = date=request.GET.get('date_input_final','')
            owner_name = request.GET.get('owner_name')

            #response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="'+ filename_name + "_" + owner_name + "_" + date_input_inicio + "_" + date_input_final+'.xls"'

        elif report_name =='report_income_outcome':
            date_input_inicio = date=request.GET.get('date_input_inicio','')
            date_input_final = date=request.GET.get('date_input_final','')
            
            response['Content-Disposition'] = 'attachment; filename="'+ filename_name + date_input_inicio + "_" + date_input_final+'.xls"'

        elif report_name =='report_customer_comparation':
            date_input_inicio = date=request.GET.get('date_input_inicio','')
            date_input_final = date=request.GET.get('date_input_final','')
            
            response['Content-Disposition'] = 'attachment; filename="'+ filename_name + date_input_inicio + "_" + date_input_final+'.xls"'
        elif report_name == 'report_comparation':
            date_input_inicio = date=request.GET.get('date_input_inicio','')
            date_input_final = date=request.GET.get('date_input_final','')

            #response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="'+ filename_name + "_" + date_input_inicio + "_" + date_input_final+'.xls"'




        html_table_inputs_diario = request.GET.get('obj_html')#PARA VIR OBJETO TABELA ver o template

        #comparacao anual tem dois htmls
        if report_name == 'report_comparation':
            html_table_inputs_diario2 = request.GET.get('obj_html2')

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheet_name)#(sheet_name)#('Users')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ""
        if report_name == "report_daily":
            columns = ['Data','Expositor','Quantidade','Produto','Observação','Cor','É troca?', 'Preço (un)','Tipo Pagamento','Preço Total','Usuário',]

        elif report_name =='report_customer':
            if owner_name == "Katifa":
                columns = ['Data','Expositor','Quantidade','Produto','Observação','Cor','É troca?', 'Preço (un)','Tipo Pagamento','Preço Cor','Preço Total',]
            else:
                columns = ['Data','Expositor','Quantidade','Produto','Observação','Cor','É troca?', 'Preço (un)','Tipo Pagamento','Preço Total',]

        elif report_name =='report_income_outcome':
            columns = ['Data', 'Descrição', 'Valor', 'É Entrada?','É Saída?',]

        elif report_name =='report_customer_comparation':
            columns = ['Expositor', 'Valor Venda Total',]

        elif report_name == 'report_comparation':
	        columns = [date_input_inicio, '', date_input_final, '',]


        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)


        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        soup = BeautifulSoup(html_table_inputs_diario, 'lxml')

        table = soup.find("table")
        rows = table.findAll("tr")

        for row in rows: 
            row_num += 1   
            cols = row.findAll("td")
            if not cols:
                continue
            col_num = 0
            for td in cols:
                text_bu = td.text
                text_bu = text_bu.encode('utf-8')
                text_bu = text_bu.strip()

                ws.write(row_num, col_num, td.text, font_style)
                col_num = col_num + 1


        #comparacao anual tem dois htmls
        if report_name == 'report_comparation':
            #pra ter o total do inicio, na primeira coluna e com o row que tava no primeiro objeto html pq abaixo nesse segundo html o rows zera pra colocar a coluna do lado
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            soma_total_mes_inicio = request.GET.get('soma_total_mes_inicio')
            ws.write(row_num+1, 0, "Total mês", font_style)
            ws.write(row_num+1, 1, soma_total_mes_inicio)



            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            soup = BeautifulSoup(html_table_inputs_diario2, 'lxml')
            table = soup.find("table")
            rows = table.findAll("tr")
            row_num = 0 #pra colocar a essa tabela do lado da outra
            for row in rows: 
                row_num += 1   
                cols = row.findAll("td")
                if not cols:
                    continue
                col_num = 2
                for td in cols:
                    text_bu = td.text
                    text_bu = text_bu.encode('utf-8')
                    text_bu = text_bu.strip()

                    ws.write(row_num, col_num, td.text, font_style)
                    col_num = col_num + 1

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            soma_total_mes_final = request.GET.get('soma_total_mes_final')
            ws.write(row_num+1, 2, "Total mês", font_style)
            ws.write(row_num+1, 3, soma_total_mes_final)




        if report_name =='report_income_outcome':
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            total_vendas_receita_total = request.GET.get('total_vendas_receita_total')
            total_comissao_tienda = request.GET.get('total_comissao_tienda')
            total_aluguel_expositores = request.GET.get('total_aluguel_expositores')
            total_saidas = request.GET.get('total_saidas')
            total_entradas = request.GET.get('total_entradas')
            total_receita_final = request.GET.get('total_receita_final')

            ws.write(row_num+1, 0, "Receita Total", font_style)
            ws.write(row_num+1, 1, total_vendas_receita_total)
            ws.write(row_num+2, 0, "Total Comissão", font_style)
            ws.write(row_num+2, 1, total_comissao_tienda)
            ws.write(row_num+3, 0, "Total Aluguel", font_style)
            ws.write(row_num+3, 1, total_aluguel_expositores)
            ws.write(row_num+4, 0, "Total Entradas", font_style)
            ws.write(row_num+4, 1, total_entradas)
            ws.write(row_num+5, 0, "Total Saídas", font_style)
            ws.write(row_num+5, 1, total_saidas)
            ws.write(row_num+6, 0, "Receita da Loja", font_style)
            ws.write(row_num+6, 1, total_receita_final)

        elif report_name =='report_customer':
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if owner_name != "Katifa" and owner_name != "Tienda":
                total_cartoes = request.GET.get('total_cartoes')
                total_dinheiro = request.GET.get('total_dinheiro')
                total_maq_loja = request.GET.get('total_maq_loja')
                valor_total = request.GET.get('valor_total')
                comissao_tienda = request.GET.get('comissao_tienda')
                taxa_maquina_da_loja = request.GET.get('taxa_maquina_da_loja')
                valor_aluguel = request.GET.get('valor_aluguel')
                texto_valor_a_pagar = request.GET.get('texto_valor_a_pagar')
                valor_a_pagar = request.GET.get('valor_a_pagar')

                ws.write(row_num+1, 0, "Total Cartões", font_style)
                ws.write(row_num+1, 1, total_cartoes)
                ws.write(row_num+2, 0, "Total Dinheiro", font_style)
                ws.write(row_num+2, 1, total_dinheiro)
                ws.write(row_num+3, 0, "Total Máquina da loja", font_style)
                ws.write(row_num+3, 1, total_maq_loja)
                ws.write(row_num+4, 0, "Valor Total", font_style)
                ws.write(row_num+4, 1, valor_total)
                ws.write(row_num+5, 0, "Comissão Tienda", font_style)
                ws.write(row_num+5, 1, comissao_tienda)
                ws.write(row_num+6, 0, "Taxa máquina da loja", font_style)
                ws.write(row_num+6, 1, taxa_maquina_da_loja)
                ws.write(row_num+7, 0, "Aluguel", font_style)
                ws.write(row_num+7, 1, valor_aluguel)
                ws.write(row_num+8, 0, texto_valor_a_pagar, font_style)
                ws.write(row_num+8, 1, valor_a_pagar)

            elif owner_name == "Katifa":
                total_vendas_Katifa = request.GET.get('total_vendas_Katifa')
                total_vendas_Tienda_Katifa = request.GET.get('total_vendas_Tienda_Katifa')

                ws.write(row_num+1, 0, "Total Katifa(cores)", font_style)
                ws.write(row_num+1, 1, total_vendas_Katifa)
                ws.write(row_num+2, 0, "Total Tienda", font_style)
                ws.write(row_num+2, 1, total_vendas_Tienda_Katifa)

            elif owner_name == "Tienda":
                total_vendas_Tienda = request.GET.get('total_vendas_Tienda')
                total_vendas_Tienda_brecho = request.GET.get('total_vendas_Tienda_brecho')

                ws.write(row_num+1, 0, "Total Tienda", font_style)
                ws.write(row_num+1, 1, total_vendas_Tienda)
                ws.write(row_num+2, 0, "Total Tienda Brechó", font_style)
                ws.write(row_num+2, 1, total_vendas_Tienda_brecho)





        wb.save(response)

    except Exception:
        traceback.print_exc()
    return response



################################################################################################################################################
#def logout(request):
#    logout(request)
#    return redirect('login.html')

#def login():
#    def get(request):
#        return render(request, 'login.html', {})
#    def post(request):
#        return render(request, 'login.html', {})




