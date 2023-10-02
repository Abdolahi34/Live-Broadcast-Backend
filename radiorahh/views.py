from django.shortcuts import render


# view of 403 error page
def status_code_403_forbidden(request, exception=None):
    return render(request, 'radiorahh/403.html', status=403)


# view of 404 error page
def status_code_404_not_found(request, exception=None):
    return render(request, 'radiorahh/404.html', status=404)


# view of 500 error page
def status_code_500_internal_server_error(request, exception=None):
    return render(request, 'radiorahh/500.html', status=500)
