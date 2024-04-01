from django.shortcuts import redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .utilities import utilities 
from hiring_app.model.monitoring_contract_request_model import MonitoringContractRequest
from hiring_app.model.contract_request_snapshot_model import ContractRequestSnapshot
from hiring_app.model.user_model import CustomUser
from django.urls import reverse
from django.http import HttpResponseRedirect

class ChangeStateView(View):
    def post(self, request, idContract):
        contract_request = utilities.getContract(idContract)
        new_state = request.POST.get('state')

        state_actions = {
            'incomplete': {
                'error_message': 'Debe ingresar un motivo para los documentos faltantes.',
                'email_function': self.sendEmailFile
            },
            'cancelled': {
                'error_message': 'Debe ingresar un motivo para la cancelacion.',
                'email_function': self.sendEmailRequest
            },
            'filed': {
                'error_message': None,
                'email_function': self.sendEmailSuccess
            }
        }

        action = state_actions.get(new_state)

        if not action:
            action = {'error_message': None, 'email_function': None} 
                    
        reason = request.POST.get('reason')
        if not contract_request.is_valid_transition(new_state):
            request.session['error_message'] = "This option is unable"
            return HttpResponseRedirect(reverse('hiring_app:info', kwargs={'idContract': idContract}))

        if action and (not reason and action['error_message']):
            request.session['error_message'] = action['error_message']
            return HttpResponseRedirect(reverse('hiring_app:info', kwargs={'idContract': idContract}))

        if action:
            contract_request.transition_to_state(new_state)
            contract_request.state = new_state
            contract_request.save()
            if action['email_function']:
                action['email_function'](contract_request, reason)

        return HttpResponseRedirect(reverse('hiring_app:info', kwargs={'idContract': idContract}))


    def sendEmailRequest(self, contract_request, reason):
        content = f'Estimado/a {contract_request.created_by.first_name},\n\nLamentamos informarle que su solicitud ha sido cancelada. El motivo proporcionado es: {
            reason}. \n \n Por favor, no dude en ponerse en contacto con nosotros si tiene alguna pregunta.\n\nAtentamente,\nTu aplicación'

        message = EmailMultiAlternatives('Solicitud cancelada',
                                         content,
                                         settings.EMAIL_HOST_USER,
                                         [contract_request.created_by.email])

        message.attach_alternative(content, 'text/html')
        message.send()

    def sendEmailFile(self, contract_request, reason):
        content = f'Estimado/a {contract_request.created_by.first_name},\n\nLe informamos que hemos identificado documentos faltantes en su solicitud. El motivo proporcionado es: {reason}.\n\nPor favor, proporcione la documentación faltante lo antes posible para continuar con el proceso.\n\nSi tiene alguna pregunta o necesita ayuda, no dude en ponerse en contacto con nosotros.\n\nAtentamente,\nTu aplicación'

        message = EmailMultiAlternatives('Solicitud de documentación faltante',
                                        content,
                                        settings.EMAIL_HOST_USER,
                                        [contract_request.created_by.email])

        message.attach_alternative(content, 'text/html')
        message.send()

    def sendEmailSuccess(self, contract_request, reason=""):
        content = f'Estimado/a {contract_request.created_by.first_name},\n\nNos complace informarle que su solicitud ha sido completada exitosamente.\n\nPor favor, no dude en ponerse en contacto con nosotros si tiene alguna pregunta o necesita asistencia adicional.\n\nAtentamente,\nTu aplicación'

        message = EmailMultiAlternatives(
            'Solicitud completada exitosamente',
            content,
            settings.EMAIL_HOST_USER,
            [contract_request.created_by.email]
        )

        message.attach_alternative(content, 'text/html')
        message.send()