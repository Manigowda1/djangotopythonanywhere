from django.shortcuts import render, redirect,HttpResponseRedirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Orders
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .templatetags import cart
from django.http import HttpResponse
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator


class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        # print( request.session['cart'])
        return redirect('homepage')

    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart']= {}
        # request.session.get('cart').clear()
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()
        context = {'products': products, 'categories': categories}
        # print(request.session.get('customer_email'))
        return render(request, 'index.html', context)

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        post_data = request.POST
        name = post_data.get('name')
        email = post_data.get('email')
        password = post_data.get('password')
        # validation
        value = {'name': name, 'email': email}
        customer = Customer(name=name, email=email, password=password)
        error_message = self.validateCustomer(customer)  # Validation call
        # saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()  # register call
            return redirect('homepage')
        else:
            data = {'error': error_message, 'values': value}

            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.name:
            error_message = "Name missing!! "
        elif not customer.email:
            error_message = "email missing!!"
        elif not customer.password:
            error_message = "password missing!!"
        elif customer.isExists():
            error_message = "Email already exists"
        return error_message

class Login(View): #class based view
    return_url= None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request,'login.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        print(customer.name)
        # print(request.session.customer.name)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            # print(customer.password)
            # print(password)
            # print(flag)
            if flag:
                request.session['customer'] = customer.id
                request.session['customer_name'] = customer.name
                # request.session['customer_email'] = customer.email
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url= None
                    return redirect('homepage')

            else:
                error_message = "Password is incorrect, Please check and Retry"

        else:
            error_message = "Email or password is incorrect"
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

class Cart(View): #class based view
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        # print(list(request.session.get('cart').keys()))
        products = Product.get_products_by_id(ids)
        # print(products)
        context = {'products':products}

        return render(request,'cart.html', context)

class Checkout(View): #class based view
    def post(self,request):
      address = request.POST.get('address')
      phone = request.POST.get('phone')
      customer = request.session.get('customer')
      cart = request.session.get('cart')
      products = Product.get_products_by_id(list(cart.keys()))




      print(address,phone,customer,cart,products)
      for product in products:
          key = ' ' + str(product.id)



          order = Orders(customer = Customer(id = customer), product= product,quantity = cart.get(key),price = product.price,address = address,phone = phone)

          print(order.placeorder())
      request.session['cart'] = {}


      return redirect('cart')

class OrderView(View): #class based view

    def get(self,request):
        customer = request.session.get('customer')
        orders = Orders.get_orders_by_customer(customer)
        print(orders)
        orders = orders.reverse()
        return render(request,'orders.html',{'orders': orders})




