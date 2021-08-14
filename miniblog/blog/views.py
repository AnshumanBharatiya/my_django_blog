from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.

# home
def home(request):
	posts = Post.objects.all()
	return render(request,"blog/home.html",{'posts':posts,'home_active':'active'})

#about
def about(request):
	return render(request,"blog/about.html",{'about_active':'active'})

#contact
def contact(request):
	return render(request,"blog/contact.html",{'contact_active':'active'})

#dashboard
def dashboard(request):
	if request.user.is_authenticated:
		posts = Post.objects.all()
		user = request.user
		full_name = user.get_full_name()
		grps = user.groups.all()
		return render(request,"blog/dashboard.html",{'posts':posts,'dashboard_active':'active','full_name':full_name,'group':grps})
	else:
		return HttpResponseRedirect('/login/')

# logout
def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/login/");

#signup
def user_signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(name='Author')
			user.groups.add(group)
			messages.success(request,"Congratulations, You have become an Author")
	else:
		form = SignupForm()

	return render(request,"blog/signup.html",{'form':form,'signup_active':'active'})


#login
def user_login(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			form = LoginForm(request=request, data=request.POST)
			if form.is_valid():
				uname = form.cleaned_data["username"]
				upass = form.cleaned_data["password"]
				user = authenticate(username=uname, password=upass)
				if user is not None:
					login(request, user)
					messages.success(request,"Log in Successfully Done")
					return HttpResponseRedirect('/dashboard/')
		else:
			form = LoginForm()
		return render(request,"blog/login.html",{'form':form,'login_active':'active'})
	else:
		return HttpResponseRedirect('/dashboard/')


# add new post
def add_post(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = PostForm(request.POST)
			if form.is_valid():
				title = form.cleaned_data["title"]
				desc = form.cleaned_data["desc"]
				pst = Post(title=title,desc=desc)
				pst.save()
				messages.success(request,"You are adding a post")
				form = PostForm()
		else:
			form = PostForm()
		return render(request,"blog/addpost.html",{'form':form,'addpost_active':'active'})
	else:
		return HttpResponseRedirect('/login/')

# update post
def update_post(request, id):
	if request.user.is_authenticated:
		if request.method == 'POST':
			pi = Post.objects.get(pk=id)
			form = PostForm(request.POST, instance=pi)
			if form.is_valid():
				form.save()
				messages.success(request,"You just updated your post")
				form = PostForm()
		else:
			pi = Post.objects.get(pk=id)
			form = PostForm(instance=pi)
		return render(request,"blog/updatepost.html",{'form':form,'update_active':'active'})
	else:
		return HttpResponseRedirect('/login/')


# delete post
def delete_post(request, id):
	if request.user.is_authenticated:
		# if request.method == 'POST':
		pi = Post.objects.get(pk=id)
		pi.delete()
		return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/')