import asynctest
import httpx
import pytest

from fastapi import status

from app.auth.jwt import create_access_token
from app.schemas.restaurant import BaseRestaurantSchema
from app.server import app

from app.services.crud_db import create_new_restaurant


class EmployeeTest(asynctest.TestCase):

    @pytest.fixture(scope="class", autouse=True)
    def setup_db_data(self, test_db_session):
        """Set up all the data before each test"""
        new_restaurant = {
            'name': 'BCD Restaurant',
            'location': 'NG'
        }
        restaurant = create_new_restaurant(test_db_session, BaseRestaurantSchema(**new_restaurant))
        self.restaurant_id = restaurant.id

        self.user_access = create_access_token({'sub': 'aubrey@gmail.com'})

    @pytest.mark.asyncio
    async def test_post_to_employee_endpoint(self):
        payload = {
          'first_name': 'Marco',
          'last_name': 'Polo',
          'restaurant_id': str(self.restaurant_id)
        }
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.post(
                '/api/v1/employee', json=payload, headers={'Authorization': f'Bearer {self.user_access}'}
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('id', response.text)
