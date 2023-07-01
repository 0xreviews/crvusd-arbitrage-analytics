import json
from flowchart.generate_flowchart import draw_graph_from_string, generate_flowchart


with open("data/detailed_trades_tokenflow_data_sFrxETH.json", "r") as f:
    trades_data = json.load(f)

    row_data = trades_data[-1]

    G_string = generate_flowchart(row_data)

    draw_graph_from_string(
        G_string,
        save_dot_dir="data/original/token_flow.dot",
        save_png_dir="data/original/token_flow.png",
    )
