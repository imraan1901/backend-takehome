from flask_restful import Api
from internal.transport.resource import resource


def register_handlers(api: Api) -> None:
    api.add_resource(resource.Data, '/data')
    # add other handlers here
