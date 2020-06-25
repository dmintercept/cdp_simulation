from dash.dependencies import Input, Output, State
from app import app
from layouts import DIRECTORY, page_not_found

from pages.home import run_sim, cdp_sim, return_go,cdp_sim_ma,pairs

input_list = ['pairs-dd','strat-dd','tf-dd','period-input','R_L-input','R_T-input','R_U-input','NR_L-input','NR_T-input','NR_U-input']
@app.callback(
    [Output(f"{x}", "active") for x in DIRECTORY], [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return ["Home" == x for x in DIRECTORY]
    return [pathname == f"/{x}" for x in DIRECTORY]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return DIRECTORY["Home"]
    elif f"{pathname}"[1:] in DIRECTORY:
        return DIRECTORY[f"{pathname}"[1:]]
    else:
        return page_not_found(pathname)


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output('graph-content','children'),
    [Input(_,'value') for _ in input_list]
)
def return_graph(*args):
    print(args[0])
    sim = run_sim(strat=args[1], pair=args[0], exchange='poloniex', tf=args[2],args=args[3:])
    
    return return_go(sim)