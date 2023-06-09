from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, TOPSALE, Wishlist,STATE_CHOICES
from .forms import CustomerRegistrationForm
from .forms import CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Main_Category
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
import json


class ProductView(View):
    def get(self, request):
        if request.GET.get("search"):
            search = request.GET.get("search")
            search = search.lower()
            prod = Product.objects.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(brand__icontains=search)
            )
            print(prod)
            data = {
                "productData": prod,
            }

            return render(request, "app/product.html", data)
        else:
            male = Product.objects.filter(category="M")
            female = Product.objects.filter(category="W")
            shoes = Product.objects.filter(category="S")
            return render(
                request,
                "app/home.html",
                {"male": male, "female": female, "shoes": shoes},
            )


def Topsale(request):
    topsale = TOPSALE.objects.all()
    return render(request, "app/topsale.html", {"topsale": topsale})


def product(request):
    prod = Product.objects.all()
    data = {"productData": prod}
    return render(request, "app/product.html", data)


class ProductDetailsView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)
            ).exists()
        return render(
            request,
            "app/productdetail.html",
            {"product": product, "item_already_in_cart": item_already_in_cart},
        )


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 100.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
                totalamount = amount + shipping_amount

            return render(
                request,
                "app/addtocart.html",
                {"carts": cart, "totalamount": totalamount, "amount": amount},
            )
        else:
            return render(request, "app/emptycart.html")


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": amount + shipping_amount,
        }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": amount + shipping_amount,
        }
    return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        data = {"amount": amount, "totalamount": amount + shipping_amount}
    return JsonResponse(data)


def buy_now(request):
    return render(request, "app/buynow.html")

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        message = f'{product.title} has been added to your wishlist.'
    else:
        message = f'{product.title} is already in your wishlist.'

    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    product_names = wishlist_item.product.title
    wishlist_item.delete()
    message = f'{product_names} has been removed from your wishlist.'

    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})
# def profile(request):
# return render(request, 'app/profile.html')
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", {"add": add, "active": "btn-primary"})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, "app/orders.html", {"order_placed": op})


def shoe(request, data=None):
    if data == None:
        shoe = Product.objects.filter(category="S")
    elif data == "Nike" or data == "Jorden":
        shoe = Product.objects.filter(category="S").filter(brand=data)
    return render(request, "app/shoe.html", {"shoe": shoe})


def men(request, data=None):
    if data == None:
        men = Product.objects.filter(category="M")
    return render(request, "app/men.html", {"men": men})


def women(request, data=None):
    if data == None:
        women = Product.objects.filter(category="W")
    return render(request, "app/women.html", {"women": women})


def womenshoe(request, data=None):
    if data == None:
        womenshoe = Product.objects.filter(category="SW")
    return render(request, "app/womenshoe.html", {"womenshoe": womenshoe})


def menshoe(request, data=None):
    if data == None:
        menshoe = Product.objects.filter(category="SM")
    return render(request, "app/menshoe.html", {"menshoe": menshoe})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Congratulations!! Registered Successfully")
            form.save()
        return render(request, "app/customerregistration.html", {"form": form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 100.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(
        request,
        "app/checkout.html",
        {"add": add, "totalamount": totalamount, "cart_items": cart_items},
    )


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request, "app/profile.html", {"form": form,
                                          "active": "btn-primary"}
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            reg = Customer(
                user=usr, name=name, locality=locality, city=city, state=state
            )
            reg.save()
            messages.success(request, "congratulations!")
        return render(
            request, "app/profile.html", {"form": form,
                                          "active": "btn-primary"}
        )


def Home(request):
    main_category = Main_Category.objects.all()
    product = Product.objects.all()
    context = {
        "main_category": main_category,
        "product": product,
    }
    return render(request, "app/product.html", context)


@csrf_exempt
def verify_payment(request):
    data = request.POST
    product_ids = list(filter(None, data["product_identity"].strip().split(","))) # ids of all cart items
    product_names = list(filter(None, data["product_name"].strip().split(","))) # product names of all cart items
    token = data["token"]
    amount = data["amount"]

    print(product_ids)

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {"token": token, "amount": amount}
    headers = {
        "Authorization": "Key test_secret_key_73af2c8bfe754b14b2c2becac4a48a1f"}

    response = requests.request("POST", url, headers=headers, data=payload)

    response_data = json.loads(response.text)
    status_code = str(response.status_code)

    if status_code == "400":
        response = JsonResponse(
            {"status": "false", "message": response_data["detail"]}, status=500
        )
        return response

    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_data)

    # After payment is verified, save the order in database
    if response_data['idx']:
        for id in product_ids:
            order = OrderPlaced(user=request.user, customer=Customer.objects.get(user=request.user), product=Product.objects.get(id=id), quantity=1, ordered_date=datetime.datetime.now(), status='Pending')
            order.save()
        cart = Cart.objects.filter(user=request.user)
        cart.delete()

    return JsonResponse(
        f"Payment Done !! With IDX. {response_data['user']['idx']}", safe=False
    )
