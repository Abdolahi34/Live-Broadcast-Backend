from django.shortcuts import render


def status_code_403_forbidden(request, exception=None):
    return render(request, 'RadioRahh/403.html', status=403)


def status_code_404_not_found(request, exception=None):
    return render(request, 'RadioRahh/404.html', status=404)


def status_code_500_internal_server_error(request, exception=None):
    return render(request, 'RadioRahh/500.html', status=500)
