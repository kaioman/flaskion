from marshmallow import Schema, fields, validate

class SignupRequestSchema(Schema):
    """
    サインアップリクエストのバリデーションスキーマ
    """
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=8)
    )
    
class SignupResponseSchema(Schema):
    """
    サインアップ成功時のレスポンススキーマ
    """
    id = fields.UUID(required=True)
    email = fields.Email(required=True)
    is_active = fields.Boolean(required=True)
    created_at = fields.DateTime(required=True) # ISO8601(UTC)
    updated_at = fields.DateTime(required=True) # ISO8601(UTC)

class SigninRequestSchema(Schema):
    """
    サインインリクエストのバリデーションスキーマ
    """
    email  = fields.Email(required=True)
    password = fields.String(required=True)

class SigninResponseSchema(Schema):
    """
    サインイン成功時のレスポンススキーマ
    """
    access_token = fields.String(required=True)
    token_type = fields.String(required=True, dump_default="Bearer")
    