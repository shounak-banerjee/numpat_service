# import uuid
# from datetime import datetime
# from typing import Optional
# from sqlalchemy.ext.declarative import declared_attr
# from sqlmodel import SQLModel as _SQLModel, Field
# from pydantic import validator


# class SQLModel(_SQLModel):

#     # Generates table name automatically using model class's name
#     # it is suggested to use model class names in plural
#     @declared_attr  # type: ignore
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

# class ModelIdGenerator:
#     """
#     Id generator class for model

#     Note: Should create a id generator interface and rely on that interface instead,
#             better for future when we intend to use a new id generator
#     """

#     @classmethod
#     def generate_uuid(cls) -> str:
#         """Generates a random UUID and returns a str converted id"""

#         return str(uuid.uuid4())

# class BaseModel(SQLModel):
#     id: Optional[str] = Field(default_factory=ModelIdGenerator.generate_uuid, primary_key=True)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)
#     created_at: datetime = Field(default_factory=datetime.utcnow)

#     def __init__(self, **kwargs):
#         self.__config__.table = False
#         super().__init__(**kwargs)
#         self.__config__.table = True

#     class Config:
#         # validate_assignment = True
#         arbitrary_types_allowed = True
import uuid
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
class BaseModel:
    # You can specify table name here or when creating the table in DynamoDB
    table_name = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        # self.updated_at = kwargs.get('updated_at', datetime.utcnow().isoformat())
        # self.created_at = kwargs.get('created_at', datetime.utcnow().isoformat())

    def save(self):
        table = dynamodb.Table(self.table_name)
        table.put_item(Item=self.to_dict())

    def to_dict(self):
        return {
            "id": self.id
        }

    @classmethod
    def get_by_id(cls, id):
        table = dynamodb.Table(cls.table_name)
        response = table.get_item(Key={"id": id})
        return cls(**response['Item']) if 'Item' in response else None

        

    
    
    