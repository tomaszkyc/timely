from app.api.api_status import ApiStatusAPI
from app.api.cite import CiteAPI
from app.api.countdown_result import CountdownResultAPI
from app.api.user_status import UserStatusAPI


def api_path(path):
    return f"/api/{path}"


def initialize_routes(api_instance):
    api_instance.add_resource(CiteAPI, api_path('cite'), api_path('cite/<int:id>'))
    api_instance.add_resource(ApiStatusAPI, api_path('status'))
    api_instance.add_resource(CountdownResultAPI, api_path('countdown-result'), api_path('countdown-result/<int:id>'))
    api_instance.add_resource(UserStatusAPI, api_path('user/authenticated'))