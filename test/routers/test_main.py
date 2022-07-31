import asynctest
import httpx
import pytest

from fastapi import status

from app.models import Restaurant
from app.schemas.restaurant import BaseRestaurantSchema
from app.server import app

from app.services.crud_db import create_new_restaurant


class IndexTest(asynctest.TestCase):
    async def test_get_to_index(self):
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.get('/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class RestaurantTest(asynctest.TestCase):

    @pytest.mark.asyncio
    async def test_post_to_restaurant_endpoint(self):
        payload = {
          'name': 'XYZ Restaurant',
          'location': 'Lagos, Nigeria'
        }
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.post('/restaurant', json=payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('id', response.text)


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

    @pytest.mark.asyncio
    async def test_post_to_employee_endpoint(self):
        payload = {
          'first_name': 'Marco',
          'last_name': 'Polo',
          'restaurant_id': str(self.restaurant_id)
        }
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.post('/employee', json=payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('id', response.text)


class MenuTest(asynctest.TestCase):

    @pytest.fixture(scope="class", autouse=True)
    def setup_db_data(self, test_db_session):
        """Set up all the data before each test"""
        new_restaurant = {
            'name': 'CDE Restaurant',
            'location': 'NG'
        }
        restaurant = create_new_restaurant(test_db_session, BaseRestaurantSchema(**new_restaurant))
        self.restaurant_id = restaurant.id

    @pytest.mark.asyncio
    async def test_post_to_menu_endpoint(self):
        payload = {
            'content': {
                'appetizer': ['oranges', 'pawpaw'],
                'main_course': ['butter chicken', 'jollof rice', 'yam pottage'],
                'desert': ['ice-cream']
            },
            'restaurant_id': str(self.restaurant_id)
        }
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.post('/menu', json=payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('id', response.text)
