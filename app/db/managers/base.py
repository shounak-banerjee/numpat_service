import boto3
from abc import ABC
from typing import Dict, Any

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')

class BaseManager(ABC):
    def __init__(self, table_name: str) -> 'BaseManager':
        self.table = dynamodb.Table(table_name)

    async def get_by_id(self, _id: str) -> Any:
        response = self.table.get_item(Key={'id': _id})
        return response.get('Item')

    async def create_one(self, item: Dict[str, Any]) -> Any:
        response = self.table.put_item(Item=item)
        return response

    async def delete_by_id(self, _id: str) -> None:
        response = self.table.delete_item(Key={'id': _id})
        return response