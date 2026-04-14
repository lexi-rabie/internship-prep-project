from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------
# Load data directly from BOC Valet API
# skiprows=27 skips the metadata header section
# -----------------------------
df = pd.read_csv(
    "https://www.bankofcanada.ca/valet/observations/group/bond_yields_all/csv",
    skiprows=27,
    index_col=False
)

# Melt wide format to long format so each row is one bond/date observation
df_long = df.melt(
    id_vars=["date"],
    var_name="bond_name",
    value_name="yield"
)

df_long["yield"] = pd.to_numeric(df_long["yield"], errors="coerce")
df_long["date"] = pd.to_datetime(df_long["date"])

# Current benchmark bond details sourced from BOC benchmark PDF (last page)
bond_details = {
    "BD.CDN.2YR.DQ.YLD":  {"coupon": 0.0225, "maturity": "2028-02-01"},
    "BD.CDN.3YR.DQ.YLD":  {"coupon": 0.0325, "maturity": "2028-09-01"},
    "BD.CDN.5YR.DQ.YLD":  {"coupon": 0.0275, "maturity": "2030-09-01"},
    "BD.CDN.7YR.DQ.YLD":  {"coupon": 0.0250, "maturity": "2032-12-01"},
    "BD.CDN.10YR.DQ.YLD": {"coupon": 0.0325, "maturity": "2035-12-01"},
    "BD.CDN.LONG.DQ.YLD": {"coupon": 0.0350, "maturity": "2057-12-01"},
    "BD.CDN.RRB.DQ.YLD":  {"coupon": 0.0050, "maturity": "2050-12-01"},
}

# Human-readable labels for UI display
bond_name_map = {
    "CDN.AVG.1YTO3Y.AVG": "1–3 Year Avg Yield",
    "CDN.AVG.3YTO5Y.AVG": "3–5 Year Avg Yield",
    "CDN.AVG.5YTO10Y.AVG": "5–10 Year Avg Yield",
    "CDN.AVG.OVER.10.AVG": "10+ Year Avg Yield",
    "BD.CDN.2YR.DQ.YLD": "2 Year Bond Yield",
    "BD.CDN.3YR.DQ.YLD": "3 Year Bond Yield",
    "BD.CDN.5YR.DQ.YLD": "5 Year Bond Yield",
    "BD.CDN.7YR.DQ.YLD": "7 Year Bond Yield",
    "BD.CDN.10YR.DQ.YLD": "10 Year Bond Yield",
    "BD.CDN.LONG.DQ.YLD": "Long-Term Bond Yield",
    "BD.CDN.RRB.DQ.YLD": "Real Return Bond Yield"
}

def get_latest_yield(bond):
    filtered = df_long[df_long["bond_name"] == bond]
    return filtered.sort_values("date").iloc[-1]

def get_bond_info(bond):
    return bond_details.get(bond, None)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Bond Dashboard"),

    dcc.Dropdown(
        id="bond-dropdown",
        options=[
            {"label": bond_name_map.get(b, b), "value": b}
            for b in df_long["bond_name"].unique()
        ],
        value=df_long["bond_name"].unique()[0],
        clearable=False
    ),

    html.Br(),
    html.Div(id="bond-info"),
    dcc.Graph(id="yield-chart")
])

@app.callback(
    Output("bond-info", "children"),
    Output("yield-chart", "figure"),
    Input("bond-dropdown", "value")
)
def update_info(selected_bond):
    latest = get_latest_yield(selected_bond)
    bond_info = get_bond_info(selected_bond)

    # Average yield series don't have coupon/maturity
    if selected_bond.startswith("BD.") and bond_info is not None:
        coupon = f"{bond_info['coupon']*100:.2f}%"
        maturity = bond_info["maturity"]
    else:
        coupon = "Not applicable (average yield)"
        maturity = "Not applicable (average yield)"

    filtered = df_long[df_long["bond_name"] == selected_bond]
    fig = px.line(
        filtered,
        x="date",
        y="yield",
        title=bond_name_map.get(selected_bond, selected_bond)
    )

    return html.Div([
        html.H3(bond_name_map.get(selected_bond, selected_bond)),
        html.P(f"Yield: {latest['yield']:.2f}%"),
        html.P(f"Price: N/A"),  # BOC dataset is yield-only, no price available
        html.P(f"Coupon: {coupon}"),
        html.P(f"Maturity: {maturity}"),
        html.P(f"Date: {latest['date'].date()}")
    ]), fig

if __name__ == "__main__":
    app.run(debug=True)