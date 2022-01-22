from django.shortcuts import redirect, render


def login_redirect(request):
    return redirect('Accounts:login')


def signup_redirect(request):
    return redirect('Accounts:signup')


def logout_redirect(request):
    return redirect('Accounts:logout')


def change_pass_redirect(request):
    return redirect('Accounts:change_pass')


def profile_view_redirect(request):
    return redirect('Accounts:profile')


def status_code_403_forbidden(request, exception=None):
    return render(request, 'BroadcastSite/403.html', status=403)


def status_code_404_not_found(request, exception=None):
    return render(request, 'BroadcastSite/404.html', status=404)


def status_code_500_internal_server_error(request, exception=None):
    return render(request, 'BroadcastSite/500.html', status=500)
