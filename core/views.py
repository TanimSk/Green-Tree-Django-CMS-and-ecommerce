from .models import Post, OrderList, PlacedOrder, Comment
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from core.forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from core.tokens import account_activation_token

# Sign Up View


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'commons/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(
                request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')


# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'


# Post Handling


def create_post(req):
    if req.user.is_authenticated:

        if req.method == 'POST':
            user_id = req.user.id
            category = req.POST['category']
            title = req.POST['title']
            description = req.POST['description']

            try:
                vacancy = int(req.POST['vacancy'])
            except ValueError:
                print("not an integer")
                return redirect('create_post')

            img = req.FILES.get('img', False)

            print(
                user_id, category, title, img, description, vacancy
            )

            Post(
                user=user_id, category=category,
                title=title, img=img, description=description,
                vacancy=vacancy
            ).save()

            return redirect('home')

        return render(req, "post_form.html")
    else:
        return redirect('login')


def home(req, category=''):
    if req.user.is_authenticated:
        if category != "":
            return render(req, "home.html", {
                'posts': Post.objects.filter(category=category),
                'titles': Post.objects.all()
            })
        return render(req, "home.html", {'posts': Post.objects.all(), 'titles': Post.objects.all()})
    else:
        return redirect('login')


def query(req, category=''):
    if req.user.is_authenticated:
        if category != "":
            return render(req, "home.html", {'posts': Post.objects.filter(title=category), 'titles': Post.objects.all()})
        return render(req, "home.html", {'posts': Post.objects.all(), 'titles': Post.objects.all()})
    else:
        return redirect('login')


def show_post(req, id):
    if req.user.is_authenticated:

        if req.method == 'POST':
            comment = req.POST['cmnt']
            if comment == '': comment = 'No Comment'
            Comment(post_id=id, comment=comment, name=req.user.username).save()
            return redirect('show_post', id=id)
            
        return render(req, "post.html", {'content': Post.objects.get(id=id), 'url': id, 'comments': Comment.objects.filter(post_id=id)})
    else:
        return redirect('login')


def delete_post_page(req):
    if req.user.is_authenticated:
        return render(req, 'delete_post_page.html', {'posts': Post.objects.filter(user=req.user.id)})
    else:
        return redirect('login')


def delete_post(req, id):
    if req.user.is_authenticated:
        Post.objects.get(id=id).delete()
        return redirect('home')
    else:
        return redirect('login')


#########################-  product order  -#########################

def order_list(req, id=None):
    if req.user.is_authenticated:
        if id is not None:
            if Post.objects.get(id=id).vacancy == 0:
                return redirect('home')

            if not OrderList.objects.filter(user=req.user.id, product_id=id):
                OrderList(
                    user=req.user.id,
                    product_id=id
                ).save()

        product_list = []

        for product in OrderList.objects.filter(user=req.user.id):
            product_list.append(product.product_id)

        return render(req, 'orders/order_list.html', {'contents': Post.objects.filter(id__in=product_list)})
    else:
        return redirect('login')


def place_order(req):
    if req.user.is_authenticated:

        if req.method == 'POST':
            name = req.POST['name']
            address = req.POST['address']
            phone_no = req.POST['phone_no']

            product_list = []

            for product in OrderList.objects.filter(user=req.user.id):
                product_list.append(product.product_id)

            obj = Post.objects.filter(id__in=product_list)
            product_list = []

            for i in obj:
                product_list.append(i.title)
                i.vacancy -= 1
                i.save()

            PlacedOrder(
                name=name, address=address, phone_no=phone_no,
                products=','.join(product_list)
            ).save()

            OrderList.objects.filter(user=req.user.id).delete()

            return redirect('success')

        return render(req, 'orders/place_order.html')
    else:
        return redirect('login')


def success(req):
    if req.user.is_authenticated:
        return render(req, 'orders/success.html')
    else:
        return redirect('login')

def handle_orders(req):
    if req.user.is_authenticated:
        if req.user.is_superuser:
            if req.method == 'POST':
                my_id = req.POST['id']
                PlacedOrder.objects.get(id=my_id).delete()
                return redirect('handle_orders')

            return render(req, 'orders/handle_orders.html', {'contents': PlacedOrder.objects.all()})
        else:
            return redirect('admin:index')
    else:
        return redirect('login')

