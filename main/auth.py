from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        return_URL =  request.META["PATH_INFO"]
        a =request.session['user'] = 'username'
        print(f"salom--{a}")
        if  not request.session.get('user'):
            return redirect('login')
        response = get_response(request)
        return response
    
    return middleware




def auth_middleware_admin(get_response):
    def middleware(request):
        return_URL =  request.META["PATH_INFO"]
        request.session['user'] = 'username'
        if  not request.session.get('user'):
            print(request.session.get('user'))
            print("_______________________$$$$$$$$$$$$")
            return redirect('Login_admin')
        response = get_response(request)
     
        return response
    
    return middleware