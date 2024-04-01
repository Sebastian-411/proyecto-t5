from django.http import Http404, HttpResponse
from django.views.generic import CreateView
from hiring_app.forms import CEXContractRequestForm
from hiring_app.model import CEXContractRequest
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from .utilities import utilities
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

class CEXContractRequestView(CreateView):
    model = CEXContractRequest
    form_class = CEXContractRequestForm
    success_url = reverse_lazy('hiring_app:cex')
    template_name = 'request_creation/cex_request_form.html'

    def form_valid(self, form):
        # Assign created_by and estimated_completion_date fields
        current_user = self.request.user
        estimated_completion_date = datetime.now() + timedelta(days=30)
        form.instance.estimated_completion_date = estimated_completion_date
        form.instance.created_by = current_user

        cex_contract_request = form.save(commit=False)
        cex_contract_request.create_snapshot()
        cex_contract_request.save()
        utilities.sendEmailSuccess(current_user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
def download_rut_file(request, idContract, *args, **kwargs):
    # Get the rut and send it as a file
    model_instance = get_object_or_404(CEXContractRequest, id=idContract)
    if not request.user.has_perm('your_app.view_cexcontractrequest'):
        raise PermissionDenied("You don't have permission to download this file.")

    if not model_instance.rut:
        raise Http404("The requested file does not exist.")
    try:
        rut_file_data = model_instance.rut
    except IOError as e:
        raise IOError(f"Error reading file: {e}")

    response = HttpResponse(rut_file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{model_instance.rut.name}"'
    return response