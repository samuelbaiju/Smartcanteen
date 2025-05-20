from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required,user_passes_test#for importing the username into the home page
from .models import MenuItem, Bill, BillItem
from django.http import Http404
from django.views.decorators.http import require_POST

@login_required
def home(request):
    return render(request, 'inhome.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful signup
            login(request, user)
            return redirect('inhome')  # Redirect to inhome
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

def inhome_view(request):
    # Fetch all menu items
    menu_items = MenuItem.objects.all()

    # Retrieve the cart from session
    cart = request.session.get('cart', {})

    # Prepare cart items and total
    cart_items = []
    total = 0

    for item_id, qty in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            subtotal = item.price * qty
            cart_items.append({
                'item': item,
                'qty': qty,
                'subtotal': subtotal
            })
            total += subtotal
        except MenuItem.DoesNotExist:
            continue  # Skip if item no longer exists

    return render(request, 'inhome.html', {
        'menu_items': menu_items,
        'cart_items': cart_items,
        'cart_total': total
    })
@require_POST
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('inhome')

@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect('inhome')


def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

#menu section
def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def add_menu_item(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description', '')  # Optional field
        image = request.FILES.get('image')  # Optional field

        # Check if the required fields are provided
        if name and price:
            MenuItem.objects.create(name=name, price=price, description=description, image=image)
            return redirect('inhome')
        else:
            return render(request, 'add_menu.html', {'error': 'Name and price are required!'})

        # Save the menu item to the database
        MenuItem.objects.create(
            name=name,
            price=price,
            description=description,
            image=image
        )
        return redirect('inhome')  # Redirect to the inhome page after adding the item

    return render(request, 'add_menu_item.html')
#menu section end
@user_passes_test(is_staff_user)
def edit_menu(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)  # Manually fetch the object
    except MenuItem.DoesNotExist:
        raise Http404("Menu item not found")  # Raise a 404 error if the item does not exist
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        if request.FILES.get('image'):
            item.image = request.FILES['image']
        item.save()
        return redirect('inhome')
    return render(request, 'menu/edit_menu.html', {'item': item})

@user_passes_test(is_staff_user)
def delete_menu(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)  # Manually fetch the object
    except MenuItem.DoesNotExist:
        raise Http404("Menu item not found")  # Raise a 404 error if the item does not exist
    if request.method == 'POST':
        item.delete()
        return redirect('inhome')
    return render(request, 'menu/confirm_delete.html', {'item': item})

def bill_summary_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for item_id, qty in cart.items():
        item = MenuItem.objects.get(id=item_id)
        subtotal = item.price * qty
        cart_items.append({'item': item, 'qty': qty, 'subtotal': subtotal})
        cart_total += subtotal

    cash_message = None  # Initialize the message

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        table_number = request.POST.get('table_number')

        if payment_method == 'cash':
            # Set the message for cash payment
            cash_message = "Pay at the reception table."

        bill = Bill.objects.create(
            user=request.user,
            table_number=table_number,
            payment_method=payment_method,
            total_amount=cart_total
        )
        for cart_item in cart_items:
            BillItem.objects.create(
                bill=bill,
                item=cart_item['item'],
                quantity=cart_item['qty']
            ) 
        # Clear the cart after confirming the order
        request.session['cart'] = {}

        return redirect('inhome')

        # Redirect to the inhome page or pass the message to the template
        return render(request, 'bill_summary.html', {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'tables': [{'number': i} for i in range(1, 11)],
            'cash_message': cash_message,
        })

    # Example table data (replace with actual table data from your database)
    tables = [{'number': i} for i in range(1, 11)]

    return render(request, 'bill_summary.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tables': tables,
    })

@login_required
def view_bills(request):
    bills = Bill.objects.filter(user=request.user).order_by('-created_at')  # Fetch bills for the logged-in user
    return render(request, 'view_bills.html', {'bills': bills})