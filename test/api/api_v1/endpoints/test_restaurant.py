import asynctest
import httpx
import pytest

from fastapi import status

from app.server import app


class RestaurantTest(asynctest.TestCase):

    @pytest.mark.asyncio
    async def test_post_to_restaurant_endpoint(self):
        payload = {
          'name': 'XYZ Restaurant',
          'location': 'Lagos, Nigeria'
        }
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.post('api/v1/restaurant', json=payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('id', response.text)
