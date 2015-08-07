from dryorm.models import BaseModel
from dryorm.psql.mixin import PsqlMixin


class PsqlModel(BaseModel,PsqlMixin):
	pass
