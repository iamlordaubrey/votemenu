import asynctest
import httpx

from fastapi import status

from app.server import app


class IndexTest(asynctest.TestCase):
    async def test_get_to_index(self):
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.get('/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
