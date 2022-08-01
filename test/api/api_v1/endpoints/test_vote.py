import asynctest
import httpx
import pytest

from fastapi import status

from app.auth.jwt import create_access_token
from app.schemas.employee import BaseEmployeeSchema
from app.schemas.menu import BaseMenuSchema
from app.schemas.restaurant import BaseRestaurantSchema
from app.schemas.vote import BaseVoteSchema
from app.server import app
from app.services.crud_db import create_new_restaurant, create_new_employee, create_new_menu, create_new_vote


class VoteTest(asynctest.TestCase):

    @pytest.fixture(scope="class", autouse=True)
    def setup_db_data(self, test_db_session):
        """Set up all the data before each test"""
        new_restaurant = {
            'name': 'ABC Restaurant',
            'location': 'NG'
        }
        restaurant = create_new_restaurant(test_db_session, BaseRestaurantSchema(**new_restaurant))

        new_employee = {
            'first_name': 'Marco',
            'last_name': 'Polo',
            'restaurant_id': str(restaurant.id)
        }
        self.employee = create_new_employee(test_db_session, BaseEmployeeSchema(**new_employee))

        new_menu = {
            'content': {
                'appetizer': ['oranges', 'pawpaw'],
                'main_course': ['butter chicken', 'jollof rice', 'yam pottage'],
                'desert': ['ice-cream']
            },
            'restaurant_id': str(restaurant.id)
        }
        self.menu = create_new_menu(test_db_session, BaseMenuSchema(**new_menu))
        self.user_access = create_access_token({'sub': 'aubrey@gmail.com'})

    @pytest.mark.asyncio
    async def test_post_to_vote_endpoint(self):
        payload = {
            'employee_id': str(self.employee.id),
            'menu_one_id': str(self.menu.id)
        }

        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.post(
                '/api/v1/vote', json=payload, headers={'Authorization': f'Bearer {self.user_access}'}
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('id', response.text)


class ResultTest(asynctest.TestCase):

    @pytest.fixture(scope="class", autouse=True)
    def setup_db_data(self, test_db_session):
        """Set up all the data before each test"""
        first_restaurant = {
            'name': 'BCD Restaurant',
            'location': 'NG'
        }
        restaurant = create_new_restaurant(test_db_session, BaseRestaurantSchema(**first_restaurant))

        first_employee = {
            'first_name': 'Marco',
            'last_name': 'Polo',
            'restaurant_id': str(restaurant.id)
        }
        self.employee = create_new_employee(test_db_session, BaseEmployeeSchema(**first_employee))

        first_menu = {
            'content': {
                'appetizer': ['oranges', 'pawpaw'],
                'main_course': ['butter chicken', 'jollof rice', 'yam pottage'],
                'desert': ['ice-cream']
            },
            'restaurant_id': str(restaurant.id)
        }
        self.control_menu = create_new_menu(test_db_session, BaseMenuSchema(**first_menu))
        self.user_access = create_access_token({'sub': 'aubrey@gmail.com'})

        for count in range(20):
            """
            Have other employees vote both the control_menu (intermittently; every second pass of the for-loop) 
            and other menus. The names don't matter and ID's are unique
            """
            new_restaurant = {
                'name': f'OPQ Restaurant{count}',
                'location': 'NG'
            }
            variant_restaurant = create_new_restaurant(test_db_session, BaseRestaurantSchema(**new_restaurant))

            new_employee = {
                'first_name': f'Marco{count}',
                'last_name': f'Polo{count}',
                'restaurant_id': str(variant_restaurant.id)
            }
            variant_employee = create_new_employee(test_db_session, BaseEmployeeSchema(**new_employee))

            new_menu = {
                'content': {
                    'appetizer': [f'a{count}', f'b{count}'],
                    'main_course': ['bc', 'jr', 'yc'],
                    'desert': ['ic']
                },
                'restaurant_id': str(variant_restaurant.id)
            }
            variant_menu = create_new_menu(test_db_session, BaseMenuSchema(**new_menu))

            # Vote the variant; but... for every other count, vote the control
            menu_one_id = str(variant_menu.id)
            if count % 2:
                # Vote the control menu
                menu_one_id = str(self.control_menu.id)

            vote = {
                'employee_id': str(variant_employee.id),
                'menu_one_id': menu_one_id
            }
            create_new_vote(test_db_session, BaseVoteSchema(**vote))

    @pytest.mark.asyncio
    async def test_get_result(self):
        async with httpx.AsyncClient(app=app, base_url='http://test') as async_client:
            response = await async_client.get(
                '/api/v1/vote/result', headers={'Authorization': f'Bearer {self.user_access}'}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(10, response.json()[0].values())
