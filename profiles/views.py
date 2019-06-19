from django.shortcuts import render
from django.views.generic import View

class ProfileView(View):
    def get(self,request):
        return render(request,'profiles/profile.html')
