from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Task


class TaskTests(APITestCase):
    def setUp(self):
        """
        Set up the test environment.
        This method creates a test user and logs them in using the APIClient.
        It also creates an initial task for testing purposes.
        """
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title='Initial Task',
            description='This is an initial task'
        )

    def test_create_task(self):
        """
        Test the creation of a new task.
        This test ensures that a new task can be created successfully by sending a POST request
        to the 'create_task' endpoint with the necessary data. It verifies that the response
        status code is HTTP 201 Created, and checks that the response data contains the expected
        message and task details.
        Steps:
        1. Authenticate the client with a user.
        2. Send a POST request to the 'create_task' endpoint with task data.
        3. Verify that the response status code is 201 Created.
        4. Verify that the response contains the expected success message.
        5. Verify that the response contains the correct task title and description.
        """
        
        url = reverse('create_task')
        data = {
            'title': 'New Task',
            'description': 'This is a new task'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'New task has been added')
        self.assertEqual(response.data['data']['Task'], 'New Task')
        self.assertEqual(response.data['data']['Description'], 'This is a new task')

    def test_create_task_bad_format(self):
        """
        Test case for creating a task with bad format data.
        This test ensures that when a task is created with invalid data (e.g., an empty title),
        the API responds with a 400 Bad Request status and appropriate error messages.
        Steps:
        1. Define the URL for creating a task.
        2. Prepare the data with an empty title to simulate bad format.
        3. Authenticate the client with a valid user.
        4. Send a POST request to the create task endpoint with the invalid data.
        5. Assert that the response status code is 400 Bad Request.
        6. Assert that the response contains the expected error messages.
        """
        
        url = reverse('create_task')
        data = {
            'title': '',  # Invalid data
            'description': 'This is a new task'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Error')
        self.assertEqual(response.data['data'], 'Bad format')

    def test_update_task(self):
        """
        Test the update_task API endpoint.
        This test ensures that a task can be successfully updated with new data.
        It verifies that the response status code is HTTP 200 OK, the response 
        message indicates a successful update, and the task's title in the response 
        data matches the updated title.
        Steps:
        1. Construct the URL for the update_task endpoint.
        2. Create a data dictionary with the task ID, updated title, and description.
        3. Authenticate the client with a user.
        4. Send a PUT request to the update_task endpoint with the data.
        5. Assert that the response status code is 200 OK.
        6. Assert that the response message indicates the task has been updated.
        7. Assert that the task's title in the response data matches the updated title.
        """
        
        url = reverse('update_task')
        data = {
            'id': self.task.id,
            'title': 'Updated Task',
            'description': 'This is an updated task'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Task has been updated')
        self.assertEqual(response.data['data']['title'], 'Updated Task')

    def test_delete_task(self):
        """
        Test case for deleting a task.

        This test ensures that a task can be successfully deleted by sending a DELETE request
        to the 'delete_task' endpoint. It verifies that the response status code is 204 NO CONTENT
        and that the task is removed from the database.

        Steps:
        1. Authenticate the client with a user.
        2. Send a DELETE request to the 'delete_task' endpoint with the task ID.
        3. Check that the response status code is 204 NO CONTENT.
        4. Verify that the task is no longer present in the database.
        """
        url = reverse('delete_task')
        data = {
            'id': self.task.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=self.task.id).count(), 0)
    