from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate


SESSION_EXPIRATION_TIME = 0


def view_login_page(request):
    if request.user.is_authenticated():
        return redirect('main')
    else:
        return render(request, 'security/login.html')


def handle_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    error_msg = None
    if user is not None:
        if user.is_active:
            request.session.set_expiry(SESSION_EXPIRATION_TIME)
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            error_msg = 'Account is disabled'
    else:
        # Return an 'invalid login' error message.
        error_msg = 'Invalid login'

    if error_msg:
        return render(request,
                      'security/login.html',
                      {'error_msg': error_msg})
    else:
        return HttpResponseRedirect(reverse('login'))


def handle_logout(request):
    logout(request)
    return redirect('login')
