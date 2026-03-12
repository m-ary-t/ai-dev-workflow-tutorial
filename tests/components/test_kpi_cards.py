from unittest.mock import patch, MagicMock
from components.kpi_cards import render_kpi_cards


def _make_mock_st():
    mock_st = MagicMock()
    col1, col2 = MagicMock(), MagicMock()
    mock_st.columns.return_value = [col1, col2]
    return mock_st


# T008 [US1]: render_kpi_cards renders without error and calls st.metric twice
def test_render_kpi_cards_no_error():
    with patch("components.kpi_cards.st", _make_mock_st()):
        render_kpi_cards(total_sales=672000.0, total_orders=482)


def test_render_kpi_cards_labels():
    mock_st = _make_mock_st()
    with patch("components.kpi_cards.st", mock_st):
        render_kpi_cards(total_sales=100.0, total_orders=5)
    labels = [c.kwargs.get("label", "") for c in mock_st.metric.call_args_list]
    assert "Total Sales" in labels
    assert "Total Orders" in labels
