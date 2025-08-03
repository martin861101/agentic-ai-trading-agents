from main import chart_analyst_node

# Test input
test_data = {
    "symbol": "EURUSD",
    "timeframe": "1h"
}

if __name__ == "__main__":
    result = chart_analyst_node(test_data)
    print("=== Agent Output ===")
    print(result)
