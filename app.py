import psycopg2
from flask import Flask, render_template, request
from psycopg2.extras import RealDictCursor
from util import safe_int, safe_sort_by, safe_sort_dir
from sets import count_sets, search_sets

from choices import nameOfChoices

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)
app = Flask(__name__)

# TODO: create /sets HTML endpoint
@app.route('/sets')
def search_sets_html():
    print(request.args)
    nameOfChoices = request.args.get('nameOfChoices', '')
    choiceData = request.args.get('s.choiceData', '')
    selectedNumTimes = request.args.get('selectedNumTimes', '')
    page = safe_int(request.args.get('page'), 1)
    limit = safe_int(request.args.get('results_per_page'),50)
    offset =  (page -1) * limit
    safe_sort_by = safe_sort_by(request.args.get('safe_sort_by'), 'set_name')
    safe_sort_dir  = safe_sort_dir(request.args.get('safe_sort_dir'), 'asc')
    page_count = safe_int(request.args.get('page_count', 1))
    if page_count is None:
        page_count = 1            

    with conn.cursor() as cur:
        count = count_sets(cur, nameOfChoices = nameOfChoices, choiceData = choiceData, selectedNumTimes = selectedNumTimes,
                page = page, limit = limit, offset = offset, safe_sort_by = 'set_name', safe_sort_dir = 'asc')
        results = search_sets(cur, nameOfChoices = nameOfChoices, choiceData = choiceData, selectedNumTimes = selectedNumTimes,
                page = page, limit = limit, offset = offset, safe_sort_by = 'set_name', safe_sort_dir = 'asc')
        return render_template('choice_display.html', nameOfChoices = nameOfChoices, choiceData = choiceData, selectedNumTimes = selectedNumTimes,
                page = page, offset = offset)

# TODO: create /sets HTML endpoint
@app.route('/test/info')
def instructions():
    return render_template('info_page.html')

@app.route('/test/question')
def would_you_rather():
    table_name = request.args.get('table_name', 'animals')
    row_id = request.args.get('id', 0)
    with conn.cursor() as cur:
        select = select_page_data(cur, table_name = table_name, requested_page_id = row_id)
        update = update_choice_count(cur, table_name = table_name)
        return render_template('questions_page.html', table_name = table_name, update = update, select = select)

@app.route('/test/results')
def results():
    #We may need additional query requests for the last page's question and the chosen answer to be saved
    #If so, remember to put those in the section below this, like so
    #return(render_template('q', table_name = table_name, select = select, QUERY_NAME=PUT HERE))

    table_name = request.args.get('table_name', 'animals')
    row_id = request.args.get('id', 0)
    with conn.cursor() as cur:
        select = select_page_data(cur, table_name = table_name, requested_page_id = row_id)
        return render_template('q', table_name = table_name, select = select)

def update_id(cur.cursor, nameOfChoices:str, choiceData:str,
                selectedNumTimes:int, id:int
    cur.execute(f"""
        update choiceData
        set id = id
        where id = null
    """)
)

def update_table(cur.cursor, table:str, nameOfChoices:str, 
                choiceData:str,selectedNumTimes:int,id:int
    cur.execute("""
        update table
        set column=nameOfChoices
        where column=null
    """)
)


