from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.views import View
from django.utils import timezone

from .models import Profile, Post, Products
from .forms import PostForm, FeedbackForm
from datetime import datetime

import pytz
# Create your views here.

def index(request):
    return render(request, "index.html",{})

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")
# Display all alumni except the current logged in user
def displayAlumni(request):
    if request.user.is_authenticated:   
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "alumni_list.html",{"profiles":profiles})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('/')
def displayUserProfile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user__id= pk)
        return render(request, "user_profile.html",{"profile":profile}) 
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('/')
def editUserProfile(request, pk):
    if request.user.is_authenticated:
        # Redirect to original profile user 
        if pk != request.user.id:
            return redirect(f'/edit_profile/{request.user.id}')
            
        # Get profile object
        profile = Profile.objects.get(user__id= pk)
        
        if request.method == 'POST':
            names = request.POST['fullName'].split()
            print(names)
            profile.user.first_name = names[0]
            profile.user.last_name  = " ".join(names[1:])
            profile.user.email = request.POST['email']
            profile.avatar = request.FILES.get('avatar',None)
            profile.save()
            profile.user.save()
            messages.success(request, "Changes saved, successfully!")
        return render(request, "user_profile_edit.html",{"profile":profile}) 
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('/')

class PostListView( View ):
    
   def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-publish_date").filter(publish_date__lte=timezone.now().astimezone(pytz.utc))
        print(posts[0].created_at)
        print(posts[0].publish_date)
        print(timezone.now().astimezone(pytz.utc))
        print(len(posts))
        
        form = PostForm()
        return render(request, 'post_list.html', {'post_list' : posts, 'form':form})
   def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-created_at")
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
        return render(request, 'post_list.html', {'post_list' : posts, 'form':form})

class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = FeedbackForm()
        return render(request, 'post_detail.html',{'post':post, 'form':form})
    
class PostCreateView(View):
   def get(self, request, *args, **kwargs):
        form = PostForm(request.POST) 
        return render(request, 'add_post.html', {'form':form})
   def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
        return render(request, 'add_post.html', {'form':form})
 
# Products/Services
class ServiceListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'products.html',{}) 
    
class CartListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "cart.html", {})
    

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard\dashboard.html", {})


class ProductAdd(View):
    def get(self, request, *args, **kwargs):
    
        return render(request, 'dashboard\dashboard_product_add.html')
    def post(self,request,*args, **kwargs):
            if request.method == "POST" :
                data = request.POST
                product_name = data.get('product_name')
                product_category = data.get('product_category')
                product_subcategory = data.get('product_subcategory')
                product_price = data.get('product_price')
                product_desc = data.get('product_desc')
                product_image = request.FILES.get('product_image')
                Products.objects.create(
                    product_name = product_name,
                    product_category = product_category,
                    product_subcategory = product_subcategory,
                    product_price = product_price,
                    product_desc = product_desc,
                    product_image = product_image,
                )
                return redirect('/dashboard/dashboard_products')

class ProductDelete(View): 
    def get (self,request, id,):           
       products = Products.objects.get(id=id)
       products.delete()
       return redirect('/dashboard/dashboard_products')
class ProductUpdate(View):
    def get(self, request, id):
          products = Products.objects.get(id=id)
          context = {'products' : products}
          return render(request, 'dashboard\dashboard_product_edit.html',context)
    
    def post(self,request,*args, **kwargs):
        
         if request.method == "POST" :
              data = request.POST
              product_id = data.get('product_id')
              product_name = data.get('product_name')
              product_category = data.get('product_category')
              product_subcategory = data.get('product_subcategory')
            #   product_price = data.get('product_price')
              product_desc = data.get('product_desc')
              product_image = request.FILES.get('product_image')

              products = Products.objects.get(id=product_id)

              products.product_name = product_name
              products.product_category = product_category,
              products.product_subcategory = product_subcategory,
            #   products.product_price = product_price,
              products.product_desc = product_desc,
              if product_image:
                  products.product_image = product_image,
         products.save()
         return  redirect('/dashboard/dashboard_products')
        
                
class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        print(products)
        return render(request, 'dashboard\dashboard_product.html',{'products':products})
    
    def editProduct(request, id):
        products = Products.objects.get(id = id)
        return render(request, 'dashboard/dashborad_product_edit.html', {'products':products})
    
    def product_update(request, id):
        products = Products.objects.get(id=id)
        form = ProductsForm(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            form = ProductsForm(instance=products)
            return render(request, 'dashboard/dashborad_product_edit.html', {'form': form})
        
    def product_destroy(request, id):
         products = Products.objects.get(id=id)
         products.delete()
         return redirect
