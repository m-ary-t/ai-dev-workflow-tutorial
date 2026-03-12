import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2024-01-15", "2024-01-22", "2024-02-10", "2024-02-18",
                    "2024-03-05", "2024-03-14", "2024-04-02", "2024-04-20",
                    "2024-05-08", "2024-05-25",
                ]
            ),
            "order_id": [f"ORD-{i:03d}" for i in range(1, 11)],
            "product": [
                "Laptop", "Headphones", "Smartwatch", "Keyboard",
                "Speaker", "Tablet", "Earbuds", "Monitor",
                "Fitness Band", "Smart Hub",
            ],
            "category": [
                "Electronics", "Audio", "Wearables", "Accessories",
                "Audio", "Electronics", "Audio", "Electronics",
                "Wearables", "Smart Home",
            ],
            "region": [
                "North", "South", "East", "West",
                "North", "East", "South", "West",
                "North", "East",
            ],
            "quantity": [1, 2, 1, 3, 1, 1, 2, 1, 2, 1],
            "unit_price": [999.99, 49.99, 299.99, 79.99, 149.99, 599.99, 39.99, 399.99, 89.99, 129.99],
            "total_amount": [999.99, 99.98, 299.99, 239.97, 149.99, 599.99, 79.98, 399.99, 179.98, 129.99],
        }
    )
