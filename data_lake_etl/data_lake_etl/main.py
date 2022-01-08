# TODO: 테이블에서 필터링 후에 select all 버튼이 원하는대로 작동하지 않는 것 개선

from dateutil import parser as dateparser

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd

import pymongo
from dotenv import dotenv_values


config = dotenv_values("../.env")
mongo_uri = f"mongodb://{config['MONGO_INITDB_ROOT_USERNAME']}:{config['MONGO_INITDB_ROOT_PASSWORD']}@{config['MONGO_HOST']}:{config['MONGO_PORT']}/"
page_size = 10


def get_db_list():
    client = pymongo.MongoClient(mongo_uri)
    all_db = client.list_database_names()
    client.close()
    db_list = [
        {"label": db, "value": db}
        for db in all_db
        if not db in ["admin", "local", "config"]
    ]
    if db_list == []:
        return [{"label": "No DB found", "value": "None"}]
    else:
        return db_list


def get_collection_list(db_name):
    client = pymongo.MongoClient(mongo_uri)
    try:
        db = client[db_name]
    except:
        return [{"label": "No DB found", "value": "None"}]
    all_collection = db.list_collection_names()
    client.close()
    collection_list = [
        {"label": collection, "value": collection} for collection in all_collection
    ]
    if collection_list == []:
        return [{"label": "No Collection found", "value": "None"}]
    else:
        return collection_list


def get_document_records(db_name, collection_name):
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    all_document = list(collection.find({}, {"_id": 0}))
    client.close()
    df = pd.DataFrame(all_document)
    df.acq_time = df.acq_time.apply(
        lambda x: dateparser.parse(x).strftime("%Y-%m-%d %H:%M:%S.%f")
    )
    records = df.to_dict("records")
    return records


sample_column = [{"name": "Select DB and Collection First", "id": "None"}]
sample_records = []


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Data Lake ETL"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Database"),
                        dcc.Dropdown(
                            id="DB_list_input",
                            options=get_db_list(),
                            placeholder="Select DB",
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "width": "45%",
                        "vertical-align": "bottom",
                    },
                ),
                html.Div(
                    [
                        html.Label("Collection"),
                        dcc.Dropdown(
                            id="collection_list_input",
                            placeholder="Select Collection",
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "width": "45%",
                        "vertical-align": "bottom",
                    },
                ),
                html.Button(
                    "Refresh",
                    id="refresh_button",
                    style={
                        "display": "inline-block",
                        "width": "10%",
                        "height": "36px",
                        "vertical-align": "bottom",
                    },
                ),
            ],
            style={"display": "inline-block", "width": "100%"},
        ),
        html.Div(
            [
                html.H3(id="DB_collection_name"),
                html.Div(
                    [
                        html.Button(
                            "Select All in this Page",
                            id="select_all_page_button",
                            style={
                                "height": "36px",
                                "display": "inline-block",
                            },
                        ),
                        html.Button(
                            "Select All",
                            id="select_all_button",
                            style={
                                "height": "36px",
                                "display": "inline-block",
                            },
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "width": "100%",
                    },
                ),
                dash_table.DataTable(
                    id="document_dataframe",
                    columns=sample_column,
                    data=sample_records,
                    page_current=0,
                    page_size=page_size,
                    page_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    filter_action="native",
                    row_selectable="multi",
                    selected_rows=[],
                ),
            ],
        ),
        html.Div(
            [
                html.Code(id="get_code", lang="python"),
                dcc.Clipboard(target_id="get_code"),
            ]
        ),
    ],
)


@app.callback(
    Output("collection_list_input", "options"),
    Input("DB_list_input", "value"),
)
def update_collection_list(db_name):
    if db_name is None:
        raise PreventUpdate
    collection_list = get_collection_list(db_name)
    return collection_list


@app.callback(
    Output("document_dataframe", "data"),
    Output("document_dataframe", "columns"),
    Input("refresh_button", "n_clicks"),
    Input("DB_list_input", "value"),
    Input("collection_list_input", "value"),
)
def update_document_table(refresh, db_name, collection_name):
    if db_name is None or collection_name is None:
        raise PreventUpdate

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered == "refresh_button":
            records = get_document_records(db_name, collection_name)
            columns = [{"name": i, "id": i} for i in records[0].keys()]
            return records, columns
        else:
            raise PreventUpdate


@app.callback(
    Output("DB_collection_name", "children"),
    Input("DB_list_input", "value"),
    Input("collection_list_input", "value"),
    Input("document_dataframe", "derived_virtual_selected_rows"),
)
def update_db_collection_name(db_name, collection_name, selected_rows):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        if db_name is None:
            raise PreventUpdate
        elif db_name is not None and collection_name is None:
            return f"DB: {db_name}, Select Collection"
        elif db_name is not None and collection_name is not None:
            if selected_rows == []:
                return_str = f"DB: {db_name}, Collection: {collection_name}"
            else:
                return_str = f"DB: {db_name}, Collection: {collection_name}, Selected rows: {selected_rows.__len__()}"
            return return_str


@app.callback(
    Output("document_dataframe", "selected_rows"),
    Input("select_all_page_button", "n_clicks"),
    Input("select_all_button", "n_clicks"),
    Input("document_dataframe", "data"),
    Input("document_dataframe", "selected_rows"),
    Input("document_dataframe", "page_current"),
)
def sellect_all_in_page(page_button, all_button, data, selected_rows, page_current):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered == "select_all_page_button":
        selected_rows_set = set(selected_rows)
        new_rows = set(range(page_current * page_size, (page_current + 1) * page_size))
        if new_rows.issubset(selected_rows_set):
            new_selected_rows = selected_rows_set.difference(new_rows)
        else:
            new_selected_rows = selected_rows_set.union(new_rows)
        return list(new_selected_rows)
    elif triggered == "select_all_button":
        selected_rows_set = set(selected_rows)
        new_rows = set(range(len(data)))
        if new_rows.issubset(selected_rows_set):
            new_selected_rows = selected_rows_set.difference(new_rows)
        else:
            new_selected_rows = selected_rows_set.union(new_rows)
        return list(new_selected_rows)
    else:
        raise PreventUpdate


@app.callback(
    Output("get_code", "children"),
    Input("document_dataframe", "derived_virtual_data"),
    Input("document_dataframe", "columns"),
)
def get_code(selected_data, columns):
    if selected_data is None or columns is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(selected_data)
    return f"{df}"


if __name__ == "__main__":
    app.run_server(debug=True)
