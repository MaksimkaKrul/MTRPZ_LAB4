from unittest import TestCase, mock
from task_manager.cli import main

class TestCLI(TestCase):
    @mock.patch("task_manager.cli.add_task")
    def test_add_command(self, mock_add):
        with mock.patch('sys.argv', ['cli.py', 'add', '--title', 'Test']):
            main()
            mock_add.assert_called_with({"title": "Test", "description": None})
    
    @mock.patch("task_manager.cli.delete_task")
    def test_delete_command(self, mock_delete):
        with mock.patch('sys.argv', ['cli.py', 'delete', '--id', '1']):
            main()
            mock_delete.assert_called_with(1)