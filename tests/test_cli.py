# tests/test_cli.py
from unittest import TestCase, mock
from task_manager.cli import main
from task_manager.models import Task, TaskNotFoundError
from datetime import datetime

from task_manager import storage

class TestCLI(TestCase):
    def setUp(self):
        self.mock_load_patch = mock.patch.object(storage, '_load_tasks_from_json', autospec=True)
        self.mock_save_patch = mock.patch.object(storage, '_save_tasks_to_json', autospec=True)
        self.mock_load = self.mock_load_patch.start()
        self.mock_save = self.mock_save_patch.start()
        self.addCleanup(self.mock_load_patch.stop)
        self.addCleanup(self.mock_save_patch.stop)
        
        storage._tasks_in_memory = []
        storage._next_id = 1


    @mock.patch("builtins.print")
    @mock.patch("task_manager.cli.add_task")
    def test_add_command(self, mock_add, mock_print):
        fixed_time = datetime(2024, 6, 1, 10, 0, 0)
        mock_add.return_value = Task(id=1, title="Test", description=None, status="todo", created_at=fixed_time)

        with mock.patch('sys.argv', ['cli.py', 'add', '--title', 'Test']):
            main()
            mock_add.assert_called_once()
            args, kwargs = mock_add.call_args
            self.assertIn('title', args[0])
            self.assertEqual(args[0]['title'], 'Test')
            self.assertIn('description', args[0])
            self.assertIsNone(args[0]['description'])
            self.assertNotIn('due_date', args[0])
        
        mock_add.reset_mock()
        mock_print.reset_mock()

        with mock.patch('sys.argv', ['cli.py', 'add', '--title', 'Full Task', '--description', 'Desc', '--due-date', '2025-01-01T12:00:00']):
            mock_add.return_value = Task(id=2, title="Full Task", description="Desc", due_date=datetime(2025, 1, 1, 12, 0, 0), status="todo", created_at=fixed_time)
            main()
            mock_add.assert_called_once()
            args, kwargs = mock_add.call_args
            self.assertEqual(args[0]['title'], 'Full Task')
            self.assertEqual(args[0]['description'], 'Desc')
            self.assertEqual(args[0]['due_date'], datetime(2025, 1, 1, 12, 0, 0))


    @mock.patch("builtins.print")
    @mock.patch("task_manager.cli.get_all_tasks")
    def test_list_command(self, mock_get_all, mock_print):
        fixed_time = datetime(2024, 6, 1, 10, 0, 0)
        mock_get_all.return_value = [
            Task(id=1, title="Task A", status="todo", created_at=fixed_time, due_date=None),
            Task(id=2, title="Task B", status="done", created_at=fixed_time, due_date=datetime(2024, 7, 1))
        ]

        with mock.patch('sys.argv', ['cli.py', 'list']):
            main()
            mock_get_all.assert_called_once()
            
            mock_print.assert_any_call(f"{'ID':<4} {'Title':<30} {'Status':<15} {'Due Date':<20} {'Created At':<20}")
            mock_print.assert_any_call("-" * 90)
            
            expected_task_a_due_date = "N/A"
            expected_task_a_created_at = fixed_time.strftime("%Y-%m-%d %H:%M")
            mock_print.assert_any_call(
                f"{1:<4} {'Task A':<30} {'todo':<15} {expected_task_a_due_date:<20} {expected_task_a_created_at:<20}"
            )

            expected_task_b_due_date = datetime(2024, 7, 1).strftime("%Y-%m-%d %H:%M")
            expected_task_b_created_at = fixed_time.strftime("%Y-%m-%d %H:%M")
            mock_print.assert_any_call(
                f"{2:<4} {'Task B':<30} {'done':<15} {expected_task_b_due_date:<20} {expected_task_b_created_at:<20}"
            )
        
        mock_get_all.reset_mock()
        mock_print.reset_mock()

        with mock.patch('sys.argv', ['cli.py', 'list', '--status', 'todo']):
            main()
            mock_get_all.assert_called_once()
            mock_print.assert_any_call(
                f"{1:<4} {'Task A':<30} {'todo':<15} {expected_task_a_due_date:<20} {expected_task_a_created_at:<20}"
            )
            self.assertFalse(any('Task B' in call.args[0] for call in mock_print.call_args_list))


    @mock.patch("builtins.print")
    @mock.patch("task_manager.cli.update_task")
    def test_update_command(self, mock_update, mock_print):
        fixed_time = datetime(2024, 6, 1, 10, 0, 0)
        mock_update.return_value = Task(id=1, title="Test", status="done", created_at=fixed_time, due_date=None) 

        with mock.patch('sys.argv', ['cli.py', 'update', '--id', '1', '--status', 'done']):
            main()
            mock_update.assert_called_once_with(1, status='done')
            mock_print.assert_called_with(f"Task {mock_update.return_value.id} updated: Status='{mock_update.return_value.status}', Due Date='None'")


        mock_update.reset_mock()
        mock_print.reset_mock()

        with mock.patch('sys.argv', ['cli.py', 'update', '--id', '1', '--due-date', '2025-07-07T10:00:00']):
            fixed_due_date = datetime(2025, 7, 7, 10, 0, 0)
            mock_update.return_value = Task(id=1, title="Test", status="todo", created_at=fixed_time, due_date=fixed_due_date)
            main()
            mock_update.assert_called_once_with(1, due_date=fixed_due_date)
            expected_due_date_str = fixed_due_date.strftime("%Y-%m-%d %H:%M") 
            mock_print.assert_called_with(f"Task {mock_update.return_value.id} updated: Status='{mock_update.return_value.status}', Due Date='{expected_due_date_str}'")

    @mock.patch("builtins.print")
    @mock.patch("task_manager.cli.delete_task")
    def test_delete_command(self, mock_delete, mock_print):
        with mock.patch('sys.argv', ['cli.py', 'delete', '--id', '1']):
            main()
            mock_delete.assert_called_once_with(1)
            mock_print.assert_called_with("Task with ID 1 deleted successfully.")

        mock_delete.reset_mock()
        mock_print.reset_mock()

        mock_delete.side_effect = TaskNotFoundError("Task not found")
        with mock.patch('sys.argv', ['cli.py', 'delete', '--id', '999']):
            main()
            mock_delete.assert_called_once_with(999)
            mock_print.assert_called_with("Error: Task with ID 999 not found.")