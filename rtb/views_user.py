from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

@api_view()
def permissionInfo(request):
    """
POST type of permission for certain user

## Url format: /api/v1/login

+ data

    + email(String) - email for getting information about users's permissions
    + password(String) - password for getting information about users's permissions

    """
    return Response({
        "id": 19,
        "permission": "adminfull", #types of permission: "adminfull", "adminread", "userfull", "userread"
        "token":"12qw34er56ty"
    })



def addUser(request):
    """
POST type for add new user

## Url format: /api/v1/user

+ data

    + email(String) - email for getting information about users's permissions
    + password(String) - password for getting information about users's permissions
    + confpassword(String) - confirm password for getting information about users's permissions
    + permission(String) - permission for role user
    + appnexususerid(integer) - ususer id from app nexus
    """
    return Response({
        "id": 19,
        "email": "newUser@user.new",
        "name": "newUser",
        "permission":"userfull",
        "appnexususerid" : 153
    })


def selectAppNexus(request):
    """
GET type for select all users from app nexus

## Url format: /api/v1/appnexus/user

    """
    return Response([{
      "id": "1",
      "login":"cnm@gmail.com",
      "name":"CNM"
    },{
      "id": "2",
      "login":"BBC@gmail.com",
      "name":"BBC"
    },{
      "id": "3",
      "login":"Discovery@gmail.com",
      "name":"Discovery"
    },{
      "id": "4",
      "login":"HTB@gmail.com",
      "name":"HTB"
    },{
      "id": "5",
      "login":"ICTV@gmail.com",
      "name":"ICTV"
    }])


def listUser(request):
    """
GET type for list user

## Url format: /api/v1/user

    """
    return Response([{
            "id": "1",
            "email":"cnm@gmail.com",
            "permission":"11111",
            "apnexusname":"CNM"
          },{
            "id": "2",
            "email":"BBC@gmail.com",
            "permission":"11111",
            "apnexusname":"BBC"
          },{
            "id": "3",
            "email":"Discovery@gmail.com",
            "permission":"11111",
            "apnexusname":"Discovery"
          },{
            "id": "4",
            "email":"HTB@gmail.com",
            "permission":"11111",
            "apnexusname":"HTB"
          },{
            "id": "5",
            "email":"ICTV@gmail.com",
            "permission":"11111",
            "apnexusname":"ICTV"
          }])


def removeUser(request):
    """
DELETE type for remove user

## Url format: /api/v1/user/:id

+ Parameters

    + id (Number) - id for remove user

ON SUCCESS: Response with status: 200 OK
ON FAILURE: Response with status: 400 Bad Request
    """
    return Response(200)



