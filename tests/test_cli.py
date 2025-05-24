import pytest
import json
from unittest import mock
from task_manager.cli import main

class TestCLI:
    # Інтеграційні тести (другий PR)
    @pytest.fixture(autouse=True)
    
    def setup(self, tmp_path):
        self.tmp_json = tmp_path / "tasks.json"
        self.tmp_json.write_text("[]")

    @pytest.mark.integration
    def test_add_command_with_storage(self):
        with mock.patch('task_manager.storage.JSON_FILE', new=self.tmp_json):
            with mock.patch('sys.argv', ['cli.py', 'add', '--title', 'Test']):
                main()
        data = json.loads(self.tmp_json.read_text())
        assert len(data) == 1

 
    # Юніт-тести (перший PR)
    @pytest.mark.unit
    @mock.patch("task_manager.cli.add_task")  # Изменяем путь мока
    def test_add_command_mocked(self, mock_add):
        with mock.patch('sys.argv', ['cli.py', 'add', '--title', 'Mocked']):
            main()
        mock_add.assert_called_once()

    @pytest.mark.unit
    @mock.patch("task_manager.cli.delete_task")  # Изменяем путь мока
    def test_delete_command_mocked(self, mock_delete):
        with mock.patch('sys.argv', ['cli.py', 'delete', '--id', '1']):
            main()
        mock_delete.assert_called_once_with(1)