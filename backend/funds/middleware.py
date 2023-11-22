

class SimpleMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):

        response = self.get_response(request)
        print(f'mehtod: {request.method} , path: {request.path} , status_code: {response.status_code}')
        
        return response