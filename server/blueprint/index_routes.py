from server.blueprint import bp
from server.enums import Rule, Status


@bp.route(Rule.INDEX)
def index():
    return {"status": Status.OK}


@bp.route(Rule.HEALTH)
def health():
    return {"status": Status.OK}
