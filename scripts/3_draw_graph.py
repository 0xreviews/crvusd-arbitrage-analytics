import json
from flowchart.generate_flowchart import generate_flowchart



with open("data/detailed_trades_tokenflow_data.json", "r") as f:
    trades_data = json.load(f)

    token_flow_list = trades_data[2]["token_flow_list"]

    G = generate_flowchart(token_flow_list)
    G.draw("data/original/file.png")