import pytest
from unittest.mock import patch, MagicMock
from main import CurrencyList, JSONDecorator, CSVDecorator, show_currencies


# Фикстура для создания объекта CurrencyList
@pytest.fixture
def currency_list():
    return CurrencyList()


# Тест с фикстурой: проверка, что метод get_currencies возвращает правильные данные
def test_get_currencies(currency_list):
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(text="<ValCurs><Valute ID='R01239'><Value>75.00</Value><Name>USD</Name></Valute></ValCurs>")
        result = currency_list.get_currencies(['R01239'])
        assert 'R01239' in result
        assert result['R01239'] == ('75.00', 'USD')


# Тест без фикстуры: проверка работы JSONDecorator
def test_json_decorator(currency_list):
    json_decorator = JSONDecorator(currency_list)
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(text="<ValCurs><Valute ID='R01239'><Value>75.00</Value><Name>USD</Name></Valute></ValCurs>")
        result = json_decorator.get_currencies(['R01239'])
        assert isinstance(result, str)
        assert '"R01239": [' in result
        assert '"USD"' in result


# Тест без фикстуры: проверка работы CSVDecorator
def test_csv_decorator(currency_list):
    csv_decorator = CSVDecorator(currency_list)
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(text="<ValCurs><Valute ID='R01239'><Value>75.00</Value><Name>USD</Name></Valute></ValCurs>")
        result = csv_decorator.get_currencies(['R01239'])
        assert isinstance(result, str)
        assert "ID;Rate;Name" in result
        assert "R01239;75.00;USD" in result


# Тест без фикстуры: проверка работы метода show_currencies
def test_show_currencies(currency_list, capsys):
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(text="<ValCurs><Valute ID='R01239'><Value>75.00</Value><Name>USD</Name></Valute></ValCurs>")
        show_currencies(currency_list)
        captured = capsys.readouterr()
        assert 'USD' in captured.out
        assert '75.00' in captured.out
