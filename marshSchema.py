from marshmallow import Schema, fields, validate

class IdRequest(Schema):
    id = fields.Int(required=True)

class CreateUser(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class UserBookId(Schema):
    userId = fields.Int(required=True)
    bookId = fields.Int(required=True)

class UserRead(Schema):
    id = fields.Int(required=True)
    timeFrame = fields.Str(required=True,
                           validate=validate.OneOf(["week", "month", "all"])
                        )

class CreateUserRead(Schema):
    id = fields.Int(required=True)
    pageCount = fields.Int(required=True)
    readTime = fields.Str(required=True)

class CreateLibrary(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

class LibraryBookId(Schema):
    libraryId = fields.Int(required=True)
    bookId = fields.Int(required=True)

class CreateBook(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    pageCount = fields.Int(required=True)

class CreateReview(Schema):
    userId = fields.Int(required=True)
    bookId = fields.Int(required=True)
    content = fields.Str(required=True,
                        validate=validate.Length(min= 10, max= 250)
                        )