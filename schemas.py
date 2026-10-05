from marshmallow import Schema, fields, validate


class StoreSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    location = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    price = fields.Float(
        required=True,
        validate=validate.Range(min=0)
    )

    store_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )