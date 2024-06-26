from django.urls import include, path
from hiring_app.views import *
from hiring_app.views.request_hiring.assign_manager import AssignManagerView
from hiring_app.views.request_hiring.request_hiring_view import RequestHiringView
from hiring_app.views.request_hiring.change_state import ChangeStateView
from hiring_app.views.request_hiring.snapshot_view import SnapshotsView
from hiring_app.views.request_creation.cex_contract_request_view import download_rut_file
from hiring_app.views.request_creation.pos_contract_request_view import POSContractRequestView
from hiring_app.views.request_creation.additional_pos_fields_view import get_additional_fields
from hiring_app.views.control_board.administrator_user_list_view import AdministratorUserListView
from hiring_app.views.control_board.add_user_view import AddUserView
from hiring_app.views.statistical_registers.statistics_view import StatisticsView
from hiring_app.views.control_board.export_requests_view import ExportRequestsView

app_name = 'hiring_app'

urlpatterns = [
    path('external_user_dashboard/', ExternalUserDashboardView.as_view(),
         name='external_user_dashboard'),
    path('administrator_dashboard/', AdministratorDashboardView.as_view(),
         name='administrator_dashboard'),
    path('administrator_dashboard/user_list/',
         AdministratorUserListView.as_view(), name='administrator_user_list'),
    path('administrator_dashboard/user_list/add_user/',
         AddUserView.as_view(), name='administrator_add_user'),
    path('leader_dashboard/', LeaderDashboardView.as_view(),
         name='leader_dashboard'),
    path('manager_dashboard/', ManagerDashboardView.as_view(),
         name='manager_dashboard'),
    path('info/<str:idContract>/', RequestHiringView.as_view(), name='info'),
    path('info/snapshots/<str:idContract>/',
         SnapshotsView.as_view(), name='snapshots'),
    path('info/change_state/<str:idContract>/',
         ChangeStateView.as_view(), name='change_state'),
    path('info/assign_manager/<str:idContract>/',
         AssignManagerView.as_view(), name='assign_manager'),
    path('info/assign_leader/<str:idContract>/',
         AssignLeaderView.as_view(), name='assign_leader'),
    path('request_creation/cex/', CEXContractRequestView.as_view(), name='cex',),
    path('request_creation/monitoring/',
         MonitoringContractRequestView.as_view(), name='monitoring',),
    path('request_creation/pos/', POSContractRequestView.as_view(), name='pos',),
    path('fields/', get_additional_fields, name='pos_fields',),
    path('download_rut/<str:idContract>/',
         download_rut_file, name='download_rut'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('export_requests/', ExportRequestsView.as_view(), name='export_requests')
]

