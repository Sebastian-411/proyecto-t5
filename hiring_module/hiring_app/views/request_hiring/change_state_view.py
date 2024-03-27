from django.shortcuts import redirect
from django.views import View
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from hiring_app.model import CEXContractRequest
from hiring_app.model import state_choices
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class ChangeState(View):
    def get(self, request, number):
        contract_request = get_object_or_404(CEXContractRequest, id=number)
        return render(request, 'request_hiring.html', {'choices': state_choices(), 'result': contract_request.state, 'id':number})



    def post(self, request, number):
        contract_request = get_object_or_404(CEXContractRequest, id=number)
        new_state = request.POST.get('state')
        
        if new_state == 'incomplete':
            reason = request.POST.get('reason')
            if not reason:
                return render(request, 'request_hiring.html', {'choices': state_choices(), 'result': contract_request.state, 'error_message': 'Debe ingresar un motivo para los documentos faltantes.'})
            
        if contract_request.is_valid_transition(contract_request.state, new_state):
            if new_state == 'incomplete':
                reason = request.POST.get('reason')
                if not reason:
                    return render(request, 'request_hiring.html', {'choices': state_choices(), 'result': contract_request.state, 'error_message': 'Debe ingresar un motivo para los documentos faltantes.'})
                else:
                    contract_request.state = new_state
                    contract_request.save()
                    
                    self.sendEmail(contract_request, reason)
            else:
                contract_request.state = new_state
                contract_request.save()
                    


        else:
            return render(request, 'request_hiring.html', {'choices': state_choices(), 'result': contract_request.state, 'error_message': 'Invalid state transition. Unable to change state.'})
        
        return self.get(request, number) 


    def sendEmail(self, contract_request, reason):
        content = f'Estimado/a {contract_request.solicitant_name},\n\nLamentamos informarle que faltan documentos para su solicitud. El motivo proporcionado es: {reason}.\n\nPor favor, complete los documentos requeridos lo antes posible.\n\nAtentamente,\nTu aplicación'
            
        message = EmailMultiAlternatives('Documentos faltantes', 
                                            content,
                                            settings.EMAIL_HOST_USER, 
                                            ['sg5043161@gmail.com'])

        message.attach_alternative(content, 'text/html')
        message.send()

