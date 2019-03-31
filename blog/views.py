from django.shortcuts import render, HttpResponse, redirect
from blog.models import BlogPost
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

def homeview(request):
	posts =BlogPost.objects.all()
	return render(request, 'index.html',{"posts" : posts})

def blogPageView(request, pk):
	post = get_object_or_404(BlogPost,pk=pk)
	return render(request, 'blogdetails.html', {"post":post})

def signin(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			return HttpResponse("Please enter username or password correctly")
	return render(request, 'signin.html')

def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		user_exists = User.objects.filter(username=username).exists()
		if not user_exists:
			user = User.objects.create_user(username=username, password=password, email=email)
			login(request, user)
			return HttpResponse(user)
		else:
			return HttpResponse("User already exists")
	return render(request, 'signup.html')

def create_post(request):
	if request.method == 'POST':
		title = request.POST['title']
		body = request.POST['body']
		blog = BlogPost.objects.create(author=request.user,title=title, body=body)
		return redirect('/')
	return render(request, 'createpost.html')

def logout_user(request):
	logout(request)
	return redirect('/')

def delete_post(request,pk):
	if request.user.is_authenticated:
		post= BlogPost.objects.get(pk=pk)
		if post.author == request.user:
			post.delete()
			return HttpResponse("Blog Post has been deleted Successfully")
		else:
			return HttpResponse("You are not authorized for deleting this post")

def edit_post(request,pk):
	post = BlogPost.objects.get(pk=pk)
	if post.author == request.user:
		print(post) 

		if request.method == 'POST':
			title = request.POST.get('title')
			body = request.POST.get('body')
			post.title = title
			post.body = body
			post.save()
			return redirect(f'/post/{post.pk}')
	else:
		response=HttpResponse('You are not authorized to edit this blog')
		response.status_code = 404
		return response

	return render(request, 'editblog.html',{"post":post})


