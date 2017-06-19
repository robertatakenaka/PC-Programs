# coding=utf-8

from ws import ws_requester
from ws import institutions_service
from ws import proxy
from app import app_texts
from config import app_config


_ = app_texts.get_texts('../locale')

app_config = app_config.AppConfiguration()
proxy_info = proxy.ProxyInfo(app_config.web_access_proxy_server_and_port)
app_ws_requester = ws_requester.WebServicesRequester(
    is_enabled=app_config.is_web_access_enabled,
    proxy_info=proxy_info)
institutions_manager = institutions_service.InstitutionsManager()
