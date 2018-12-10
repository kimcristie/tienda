from django.contrib.auth.models import User
from django.db import models

#perguntar Tienda
#Comissao Tienda (35% ou 40%) é feito sobre que valor? Venda total ou somente cartão do expositor?

#expositor
class Customer(models.Model):
    create_date = models.DateTimeField(max_length=100, auto_now_add=True)
    update_date = models.DateTimeField(max_length=100, auto_now=True)
    owner = models.CharField(max_length=200)
    store_name = models.CharField(max_length=200)
    store_phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, default="expositor@expositor.com")
    store_address = models.CharField(max_length=200)
    rent = models.IntegerField(default=0)
    perc_commission = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

#tipo de produto #TODO COLOCAR PRECO POR CAUSA DAS CORES DAI NO TEMPLATE APARECER PRIMEIRO AS CORES E DPS O RESTO DOS PRODUTOS
class Product(models.Model):
    create_date = models.DateTimeField(max_length=100, auto_now_add=True)
    update_date = models.DateTimeField(max_length=100, auto_now=True)
    name = models.CharField(max_length=200, blank=True, default="")
    colour = models.CharField(max_length=200,blank=True,default="")
    colour_price = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True, default=0)

#tipo de pagamento
class Payment(models.Model):
    create_date = models.DateTimeField(max_length=100, auto_now_add=True)
    update_date = models.DateTimeField(max_length=100, auto_now=True)
    name = models.CharField(max_length=200)

#entrada diaria
class DailyInput(models.Model):
    create_date = models.DateField(max_length=100)#, auto_now_add=True)
    update_date = models.DateTimeField(max_length=100, auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) #linka com o store_name
    payment_type = models.ForeignKey(Payment, on_delete=models.CASCADE) #linka com o name
    product_type = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'product_name', blank=True) #linka com o name
    product_colour = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'product_colour', blank=True, null=True) # on_delete=models.SET_NULLlinka com a colour #caso valido pra Katifa
    qtd = models.IntegerField(default=1)
    obs = models.CharField(max_length=200, blank=True)#para adc referencia, ou seila pagamento em duas vezes
    is_troca = models.BooleanField(default=False) #se eh TROCA
    un_price = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True, default=0)
    final_price = models.DecimalField(max_digits=50, decimal_places=2,null=True, blank=True, default=0)


class IncomeOutcome(models.Model):
    create_date = models.DateField(max_length=100)
    update_date = models.DateTimeField(max_length=100, auto_now=True)
    description = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    is_income = models.BooleanField(default=False)
    is_outcome = models.BooleanField(default=False)

###### reports save //quando mostrar o que salva, procurar periodo de 
#class report_customer(models.Model):
#    date_month_reference = models.DateField(max_length=100)
#    update_date = models.DateTimeField(max_length=100, auto_now=True)
#    total_cartao = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    total_maq_loja = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    total_dinheiro = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    total_geral = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    total_comissao_tienda = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    total_taxa_maq_loja = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    total_aluguel = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    total_a_pagar = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
#    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) #linka com o store_name




#fazer model dos relatorios que tem que ter todos os campos de daily e MAS LEMBRAR QUE ELE SO SALVA SE O USUARIO GRAVAR O RELATORIO

#class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)



















