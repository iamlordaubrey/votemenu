import random

import asynctest
import httpx
import pytest

from fastapi import status

from app.schemas.employee import BaseEmployeeSchema
from app.schemas.menu import BaseMenuSchema
from app.schemas.restaurant import BaseRestaurantSchema
from app.server import app
from app.services.crud_db import create_new_restaurant, create_new_employee, create_new_menu


class VoteTest(asynctest.TestCase):

    @pytest.fixture(scope="class", autouse=True)
    def setup_db_data(self, test_db_session):
        """Set up all the data before each test"""
        new_restaurant = {
            'name': 'BCD Restaurant',
            'location': 'NG'
        }
        restaurant = create_new_restaurant(test_db_session, BaseRestaurantSchema(**new_restaurant))

        new_employee = {
            'first_name': 'Marco',
            'last_name': 'Polo',
            'restaurant_id': str(restaurant.id)
        }
        employee = create_new_employee(test_db_session, BaseEmployeeSchema(**new_employee))

        new_menu = {
            'content': {
                'appetizer': ['oranges', 'pawpaw'],
                'main_course': ['butter chicken', 'jollof rice', 'yam pottage'],
                'desert': ['ice-cream']
            },
            'restaurant_id': str(restaurant.id)
        }
        menu = create_new_menu(test_db_session, BaseMenuSchema(**new_menu))

        self.employee_id = employee.id
        self.menu_id = menu.id

    @pytest.mark.asyncio
    async def test_post_to_vote_endpoint(self):
        payload = {
          'employee_id': str(self.employee_id),
          'menu_one_id': str(self.menu_id),
        }
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.post('/api/v1/vote', json=payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('id', response.text)
