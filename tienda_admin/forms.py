from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Product, Payment, DailyInput, IncomeOutcome
from django.forms import SelectDateWidget


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=254, label='Usuario')
    email = forms.EmailField(max_length=254, required=False, help_text='Obrigatório. Informe um e-mail válido', label='E-mail')
    is_active = forms.BooleanField(label='É ativo?')

    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'password1', 'password2')

class CustomerRegistrationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['owner'].label = "Dono (expositor)"
        self.fields['store_name'].label = "Expositor"
        self.fields['store_phone'].label = "Contato"
        self.fields['store_address'].label = "Endereço"
        self.fields['rent'].label = "Aluguel"
        self.fields['perc_commission'].label = "Comissão %"
        self.fields['is_active'].label = "É ativo?"
        self.fields['email'].label = "E-mail"


        self.fields['owner'].help_text = "ex: Cleo, Anna British"
        self.fields['store_name'].help_text = "ex: Divina Rosa, Cleo"
        self.fields['store_phone'].help_text = "ex: (48) 99989898"
        self.fields['store_address'].help_text = "ex: Servidão Sete Mares, 133, Lagoa da Conceição, Florianopolis, Brasil."
        self.fields['rent'].help_text = "ex: 400"
        self.fields['perc_commission'].help_text = "ex: 35"
        self.fields['is_active'].help_text = "Expositor esta ativo?"
        self.fields['email'].help_text = "ex: expositor@gmail.com"

    class Meta:
        model = Customer
        fields = ('store_name', 'owner', 'rent', 'perc_commission', 'email', 'store_phone', 'store_address', 'is_active')

class ProductRegistrationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Nome do Produto."
        self.fields['colour'].label = "Cor do Produto"
        self.fields['colour_price'].label = "Preço da Cor"

        self.fields['name'].help_text = "ex: jaqueta. OBS: quando for cor do produto, deixar este campo em branco"
        self.fields['colour'].help_text = "ex: amarelo (casos da loja Katifa), senão deixar em branco"
        self.fields['colour_price'].help_text = "ex: 39 (casos da loja Katifa), senão deixar em branco"

    class Meta:
        model = Product
        fields = ('name', 'colour', 'colour_price')

class PaymentRegistrationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PaymentRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Tipo de Pagamento"

        self.fields['name'].help_text = "ex: máquina da loja"

    class Meta:
        model = Payment
        fields = ('name',)

class DailyInputForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DailyInputForm, self).__init__(*args, **kwargs)

        self.fields['create_date'].label = "Data"
        self.fields['customer'].label = "Expositor"
        self.fields['qtd'].label = "Quantidade"
        self.fields['product_type'].label = "Produto"
        self.fields['obs'].label = "Observação"
        self.fields['product_colour'].label = "Cor"
        self.fields['is_troca'].label = "É troca?"
        self.fields['un_price'].label = "Preço Unitário"
        self.fields['payment_type'].label = "Tipo de Pagamento"
        self.fields['final_price'].label = "Preço Total"

        self.fields['product_colour'].help_text = "caso como Katifa"

        self.fields['qtd'].widget.attrs['style'] = "width:50px"
        self.fields['un_price'].widget.attrs['style'] = "width:80px"
        self.fields['obs'].widget.attrs['style'] = "width:150px"


    class Meta:
        model = DailyInput
        fields = ('create_date','customer','qtd','product_type','obs','product_colour','is_troca','un_price','payment_type','final_price',)


class IncomeOutcomeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(IncomeOutcomeForm, self).__init__(*args, **kwargs)

        self.fields['create_date'].label = "Data"
        self.fields['description'].label = "Descrição"
        self.fields['value'].label = "Valor"
        self.fields['is_income'].label = "Entrada"
        self.fields['is_outcome'].label = "Saída"

        self.fields['description'].help_text = "ex: aluguel, àgua para consumo"
        self.fields['value'].help_text = "ex: 4500"



    class Meta:
        model = IncomeOutcome
        fields = ('create_date','description','value','is_income','is_outcome')





########### not used
#class EditUserForm(UserCreationForm):
#    email = forms.EmailField(max_length=254, required=False)
#    is_active = forms.BooleanField(required=False)
#    username = forms.CharField(max_length=254,required=False)
 
#    class Meta:
#        model = User
#        fields = ('username', 'email', 'is_active')
####################


