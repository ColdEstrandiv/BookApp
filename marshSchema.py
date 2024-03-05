from marshmallow import Schema, fields, validate

class IdJsonValidation(Schema):
    id = fields.Int(required=True)

class CreateUserJsonValidation(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class UserBookIdJsonValidation(Schema):
    userId = fields.Int(required=True)
    bookId = fields.Int(required=True)

class UserReadJsonValidation(Schema):
    id = fields.Int(required=True)
    timeFrame = fields.Str(required=True,
                           validate=validate.OneOf(["week", "month", "all"])
                        )

class CreateUserReadJsonValidation(Schema):
    id = fields.Int(required=True)
    pageCount = fields.Int(required=True)
    readTime = fields.Str(required=True)

class CreateLibraryJsonValidation(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

class LibraryBookIdJsonValidation(Schema):
    libraryId = fields.Int(required=True)
    bookId = fields.Int(required=True)

class CreateBookJsonValidation(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    pageCount = fields.Int(required=True)

class CreateReviewJsonValidation(Schema):
    userId = fields.Int(required=True)
    bookId = fields.Int(required=True)
    content = fields.Str(required=True,
                        validate=validate.Length(min= 10, max= 250)
                        )