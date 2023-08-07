from tortoise.models import Model
from tortoise import fields, Tortoise
from tortoise.validators import MaxValueValidator


class TrackCurrency(Model):
    currency = fields.CharField(max_length=50)
    value = fields.FloatField(validators=[MaxValueValidator(50)])
    base = fields.CharField(max_length=100)

    class Meta:
        table = "TrackCurrency"


class InitDatabase:
    @classmethod
    async def init_db(cls):
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['models.database.models']}
        )
        await Tortoise.generate_schemas()
