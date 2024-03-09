from marshmallow import Schema, fields, validate

class CreateUserJsonValidation(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class UserReadJsonValidation(Schema):
    timeFrame = fields.Str(required=True,
                           validate=validate.OneOf(["week", "month", "all"])
                        )

class CreateUserReadJsonValidation(Schema):
    pageCount = fields.Int(required=True)
    readTime = fields.Str(required=True)

class CreateLibraryJsonValidation(Schema):
    name = fields.Str(required=True)

class CreateBookJsonValidation(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    pageCount = fields.Int(required=True)

class CreateReviewJsonValidation(Schema):
    content = fields.Str(required=True,
                        validate=validate.Length(min= 10, max= 250)
                        )
    
class adminToggleJsonValidation(Schema):
    userId = fields.Int(required=True)
    password = fields.Str(required=True)