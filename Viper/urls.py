from django.conf.urls import url, include
from rest_framework import routers

from Core.views import BaseAuthView, CurrentUserView, NoticesView, SettingView, HostView
from Core.views import NetworkTopologyView, NetworkSearchView
from Lib.montior import MainMonitor
from Msgrpc.views import LazyLoaderView, LazyLoaderInterfaceView
from Msgrpc.views import ServiceStatusView, PayloadView, JobView, HandlerView, SessionView, SessionIOView, RouteView
from Msgrpc.views import SocksView, TransportView, FileMsfView, FileSessionView, PortFwdView, HostFileView
from PostLateral.views import PortServiceView, CredentialView, VulnerabilityView
from PostModule.views import PostModuleConfigView, PostModuleActuatorView, PostModuleResultView
from PostModule.views import PostModuleResultHistoryView

router = routers.DefaultRouter()
router.register(r'api/v1/core/baseauth', BaseAuthView, basename="BaseAuth")
router.register(r'api/v1/core/currentuser', CurrentUserView, basename="CurrentUser")
router.register(r'api/v1/core/notices', NoticesView, basename="Notice")
router.register(r'api/v1/core/setting', SettingView, basename="Setting")
router.register(r'api/v1/core/host', HostView, basename="Host")

router.register(r'api/v1/core/networktopology', NetworkTopologyView, basename="NetworkTopology")
router.register(r'api/v1/core/networksearch', NetworkSearchView, basename="NetworkSearch")
router.register(r'api/v1/msgrpc/servicestatus', ServiceStatusView, basename="ServiceStatus")
router.register(r'api/v1/msgrpc/payload', PayloadView, basename="Payload")
router.register(r'api/v1/msgrpc/job', JobView, basename="Job")
router.register(r'api/v1/msgrpc/handler', HandlerView, basename="Handler")
router.register(r'api/v1/msgrpc/session', SessionView, basename="Session")
router.register(r'api/v1/msgrpc/sessionio', SessionIOView, basename="SessionIO")
router.register(r'api/v1/msgrpc/route', RouteView, basename="Route")
router.register(r'api/v1/msgrpc/socks', SocksView, basename="Socks")
router.register(r'api/v1/msgrpc/portfwd', PortFwdView, basename="PortFwd")
router.register(r'api/v1/msgrpc/transport', TransportView, basename="Transport")
router.register(r'api/v1/msgrpc/filemsf', FileMsfView, basename="FileMsfView")
router.register(r'api/v1/msgrpc/filesession', FileSessionView, basename="FileSessionView")
router.register(r'api/v1/msgrpc/lazyloader', LazyLoaderView, basename="LazyLoaderView")

router.register(r'api/v1/postlateral/portservice', PortServiceView, basename="PortServiceView")
router.register(r'api/v1/postlateral/credential', CredentialView, basename="CredentialView")
router.register(r'api/v1/postlateral/vulnerability', VulnerabilityView, basename="VulnerabilityView")
router.register(r'api/v1/postmodule/postmoduleconfig', PostModuleConfigView, basename="PostModuleConfig")
router.register(r'api/v1/postmodule/postmoduleactuator', PostModuleActuatorView, basename="PostModuleActuator")
router.register(r'api/v1/postmodule/postmoduleresult', PostModuleResultView, basename="PostModuleResult")
router.register(r'api/v1/postmodule/postmoduleresulthistory', PostModuleResultHistoryView,
                basename="PostModuleResultHistoryView")

# 无需认证的api
router.register(r'api/v1/d', HostFileView, basename="HostFileView")
router.register(r'api/v1/c', LazyLoaderInterfaceView, basename="LazyLoaderInterfaceView")

urlpatterns = [
    url(r'^', include(router.urls)),
]

MainMonitor().start()
