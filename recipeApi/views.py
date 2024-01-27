from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from recipeApi.models import Recipe
from django.contrib import messages

from django.core.mail import send_mail
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

# Create your views here.


@login_required(login_url="/login/")
def recipes(request):
    if request.method == 'POST':
        data = request.POST
        recipeImg = request.FILES.get('recipeImg')
        recipeName = data.get('recipeName')
        recipeDescrip = data.get('recipeDescrip')
        Recipe.objects.create(
            user=request.user,
            recipeName=recipeName,
            recipeDescrip=recipeDescrip,
            recipeImg=recipeImg
        )
        return redirect('/recipes')
        # print(name)
        # print(description)
        # print(images)
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(
            recipeName__icontains=request.GET.get('search'))
        return render(request, 'recipes/recipes.html', {'recipes': queryset})

    return render(request, 'recipes/recipes.html', {'recipes': queryset})


def deteleRecipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes')


def updateRecipe(request, id):
    queryset = Recipe.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        recipeImg = request.FILES.get('recipeImg')
        recipeName = data.get('recipeName')
        recipeDescrip = data.get('recipeDescrip')
        queryset.recipeName = recipeName
        queryset.recipeDescrip = recipeDescrip
        if recipeImg:
            queryset.recipeImg = recipeImg
        queryset.save()
        return redirect('/recipes')

    return render(request, "recipes/updateRecipe.html", {'recipes': queryset})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            # user = User.objects.filter(username = username)
            messages.error(request, 'Invalid username')
            return redirect('/login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipes/')
    return render(request, 'recipes/login.html')


def registerPage(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "Username already exists.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Register succesfully.")
        return redirect('/register/')

    return render(request, 'recipes/register.html')


def logout_page(request):
    logout(request)
    return redirect('/login')
