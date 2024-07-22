from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User

def who_are_you(method):
    def wrapper(self,request, *args, **kwargs):
        try:
            user_id = request.session['user']
            user = User.objects.get(id=int(user_id))
        except:
            user = None
        user = user if user else request.user
        
        if not user.is_staff:
            messages.add_message(request, messages.WARNING, "Sizda ushbu amalni amalga oshirish uchun ruxsat yo'q !")
            return redirect("profil:verification")
        return method(self, request, *args, **kwargs)
    return wrapper
