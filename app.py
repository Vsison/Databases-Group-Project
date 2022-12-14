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
        count = count_sets(cur, nameOfChoices = nameOfChoices, choiceData = choiceData, selectedNumTimes = selectedNumTimes
                page = page, limit = limit, offset - offset, safe_sort_by = 'set_name', safe_sort_dir = 'asc')
        results = search_sets(cur, nameOfChoices = nameOfChoices, choiceData = choiceData, selectedNumTimes = selectedNumTimes
                page = page, limit = limit, offset = offset, safe_sort_by = 'set_name', safe_sort_dir = 'asc')
        return render_template('choice_display.html', nameOfChoices = nameOfChoices, choiceData = choiceData, selectedNumTimes = selectedNumTimes
                page = page, offset = offset)


