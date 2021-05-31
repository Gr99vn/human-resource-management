from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls.base import reverse

# Create your views here.
def register(request):
  if request.method == "GET":
    context = {
      "form": UserCreationForm,
    }
    return render(request, "register.html", context)
  elif request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect(reverse("home"))