from flask import Blueprint
from blueprints.admin.cat_admin.classes import *

from .category_admin import *

cat_admin_blueprint = Blueprint("cat_admin", __name__)
cat_admin_blueprint.register_blueprint(class_admin_blueprint, url_prefix="/classes")