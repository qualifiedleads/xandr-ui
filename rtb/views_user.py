from django.contrib.sites import requests
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie

@csrf_exempt
@api_view(['POST'])
def login_api(request):
    """
    Login specifed user
    Return permission for that user and auth token

## Url format: /api/v1/login

    + email(String) - email of user to login
    + password(String) - password for that user

    """
    # user = authenticate(username='john', password='secret')
    if 'username' not in request.data:
        mail = request.data["email"]
        uname = User.objects.values_list('username', flat=True).get(email=mail)
        request.data['username'] = uname
        # request.data.pop("email", None)
    user = authenticate(**request.data)
    if user:
        if user.is_active:
            login(request, user)
            return Response({
                "id": user.pk,
                # "permission": "adminfull", #types of permission: "adminfull", "adminread", "userfull", "userread"
                "permission": user.frameworkuser.permission,
                "token": request.session.session_key
            })
        else:
            return Response({'error': "User disabled"}, status=401)
    else:
        return Response({'error': "Not authentificated"}, status=401)

@api_view(['POST'])
def logout_api(request):
    """
    Logout specifed user
    Return status {"status":"ok"} or {"status":"error"}

## Url format: /api/v1/logout
    """
    try:
        logout(request)
        return Response({"status":"ok"})
    except Exception as e:
        return Response({"status":"error", "error":e.message})


