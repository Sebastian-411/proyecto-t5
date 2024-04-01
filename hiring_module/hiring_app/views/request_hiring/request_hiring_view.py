from django.utils import timezone
from django.shortcuts import render
from django.views import View
from hiring_app.views.request_hiring.utilities import utilities
from hiring_app.model.contract_request_model import state_choices
from django.contrib.auth.models import Group
from hiring_app.model.user_model import CustomUser
from hiring_app.model.cex_contract_request_model import CEXContractRequest
from hiring_app.model.monitoring_contract_request_model import MonitoringContractRequest
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class RequestHiringView(View):
    def references(self, request, idContract):
        is_admin = any(group.name == 'admin' for group in self.request.user.groups.all())
        is_leader = any(group.name == 'leader' for group in self.request.user.groups.all())
        is_manager = any(group.name == 'manager' for group in self.request.user.groups.all())        
        groupManager = Group.objects.get(name='manager')
        groupLeader = Group.objects.get(name='leader')        
        managers = list(CustomUser.objects.filter(groups=groupManager))
        leaders = list(CustomUser.objects.filter(groups=groupLeader))
        contract_request = utilities.getContract(idContract)        
        typedContract = ("Contrato CEX" if isinstance(contract_request, CEXContractRequest) 
                        else "Contrato Monitoria" if isinstance(contract_request, MonitoringContractRequest) 
                        else "Error al obtener")
        snapshot_comment = contract_request.get_snapshots().filter(state=contract_request.state).first().comment

        days_difference = (contract_request.estimated_completion_date - timezone.now().date()).days if contract_request.estimated_completion_date else None
        return {
            'days_difference': days_difference,
            'typedContract': typedContract,
            'choices': state_choices(),
            'contract_request': contract_request,
            'managers': managers,
            'leaders': leaders,
            'error_message': request.session.pop('error_message', None),
            'user': self.request.user,
            'is_admin': is_admin,
            'is_leader': is_leader,
            'is_manager': is_manager,
            'snapshot_comment': snapshot_comment
            }

    def get(self, request, idContract):
        is_admin = any(group.name == 'admin' for group in self.request.user.groups.all())
        is_leader = any(group.name == 'leader' for group in self.request.user.groups.all())
        is_manager = any(group.name == 'manager' for group in self.request.user.groups.all())

        if not (is_admin or is_leader or is_manager):
            # Redirect to external user dashboard if user doesn't have admin, leader, or manager role
            return HttpResponseRedirect(reverse_lazy('hiring_app:external_user_dashboard'))

        return render(request, 'request_hiring.html', self.references(request, idContract))
    
    