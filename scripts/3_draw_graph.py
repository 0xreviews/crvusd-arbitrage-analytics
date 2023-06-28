import json
from flowchart.generate_flowchart import generate_flowchart



with open("data/detailed_trades_tokenflow_data_sFrxETH.json", "r") as f:
    trades_data = json.load(f)

    token_flow_list = trades_data[4]["token_flow_list"]

    G = generate_flowchart(token_flow_list)
    G.write("data/original/token_flow.dot")
    G.draw("data/original/token_flow.png")