# from psycopg2.extensions import cursor
import psycopg2
from flask import Flask, render_template, request
from psycopg2.extras import RealDictCursor
from util import safe_int, safe_sort_by, safe_sort_dir
from sets import count_sets, search_sets
import math
conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)

app = Flask(__name__)

# TODO: create /sets HTML endpoint
@app.route("/sets")
def search_sets_html():
    queryCounter = 0
    nameOfChoices = request.args.get('nameOfChoices', '')
    choiceData = request.args.get('choiceData', '')
    selectedNumTimes = request.args.get('selectedNumTimes',5)
    page = safe_int(request.args.get('page'), 1)
    limit = safe_int(request.args.get('results_per_page'),50)
    offset =  (page -1) * limit
    sort_by = safe_sort_by(request.args.get('sort_by'), 'set_name')
    sort_dir  = safe_sort_dir(request.args.get('sort_dir'), 'asc')


    # TODO: rest of the parameters
    with conn.cursor() as cur:
        count = count_sets(cur, nameOfChoices_contains=nameOfChoices,
                           choiceData_contains=choiceData)
        results = search_sets(cur, nameOfChoices_contains=nameOfChoices, choiceData_contains= choiceData,
                              limit=limit, offset=offset, sort_by= sort_by, sort_dir=sort_dir)
        queryCounter +=1
        page_count  = int(math.round(count/limit))
        return render_template('sets.html', count=count, results=results, nameOfChoices=nameOfChoices, choiceData = choiceData,
        page=page, limit=limit, sort_by = sort_by, sort_dir=sort_dir, page_count = page_count)

# valid sort params for search_sets function
SORT_BY_PARAMS = set(["nameOfChoices", "choiceData",
                     "selectedNumTimes"])
# valid sort direction parameters for search_sets function
SORT_DIR_PARAMS = set(["asc", "desc"])


def update_select(cur:cursor,
                nameOfChoices:str,
                choiceData:str,
    cur.execute(f"""
        SELECT @n := @n + 1 n,
        nameOfChoices, 
        choiceData
        FROM choiceTable, (SELECT @n := 0) m
        ORDER BY nameOfChoices, choiceData
    """)
)

def search_sets(cur: cursor,
                nameOfChoices_contains: str,
                choiceData_contains: str,
                selectedNumTimes: int,
                limit: int,
                offset: int,
                sort_by: str,
                sort_dir: str) -> list[dict[str, str]]:
    """
    Search the sets table with the given parameters
    """

    # these values can't easily be parameterized into the sql query, so we need to sanitize them
    # before interoplating them to protect against SQL injection
    assert int(limit) >= 0
    assert int(offset) >= 0
    assert sort_by in SORT_BY_PARAMS
    assert sort_dir in SORT_DIR_PARAMS

    cur.execute(f"""
select s.nameOfChoices as nameOfChoices,
    s.choiceData as choiceData,
from set s
    inner join choiceData d on s.nameOfChoices = d.id
where lower(s.nameOfChoices) like lower(%(nameOfChoices_param)s)
    and lower(d.choiceData) like lower(%(choiceData_param)s)
order by {sort_by} {sort_dir}
limit {limit}
offset {offset}
    """, {
        'nameOfChoices_param': f"%{nameOfChoices_contains or ''}%",
        'choiceData_param': f"%{choiceData_contains or ''}%",
    })
    return list(cur)



def count_sets(cur: cursor,
               nameOfChoices: str,
               choiceData: str,
    cur.execute("""
select count(*)
from set s
    inner join choiceData d on s.nameOfChoices = d.id
where lower(s.nameOfChoices) like lower(%(nameOfChoices_param)s)
    and lower(t.nameOfChoices) like lower(%(choiceData_param)s)
    """, {
        'nameOfChoices_param': f"%{nameOfChoices_contains or ''}%",
        'choiceData_param': f"%{choiceData_contains or ''}%",
    })
    return cur.fetchone()['count']


