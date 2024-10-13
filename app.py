from flask import Flask, request, render_template, session, redirect, url_for
from jsw import recommend_similar_foods
from yjs import refrigerator

app = Flask(__name__)
app.secret_key = 'jsw_key'

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/jsw')
def jsw():
    return render_template('jsw.html')

@app.route('/yjs')
def yjs():
    return render_template('yjs.html')

@app.route('/jsw_result', methods=['POST'])
def jsw_result():
    if request.method == 'POST':
        text_data = request.form.get('food', '')
        selected_foods = [food.strip() for food in text_data.split() if food.strip()]

        all_results = recommend_similar_foods(selected_foods)

        if 'current_index' not in session:
            session['current_index'] = 0

        start_index = session['current_index']
        end_index = start_index + 4
        result1 = all_results[start_index:end_index]

        session['current_index'] = end_index

        if session['current_index'] >= len(all_results):
            session['current_index'] = 0

        return render_template('jsw_result.html', result1=result1)

@app.route('/yjs_result',methods=['POST']) # yjs.html에서 '/yjs_result'로 보낸 값을 가져옴
def yjs_result():
    if request.method=='POST':
        materials = request.form.getlist('select')
                
        result2 = refrigerator(materials)

    return render_template('yjs_result.html', result2=result2)

@app.route('/reset')
def reset_index():
    session['current_index'] = 0
    return redirect(url_for('jsw'))
    # 다시 입력으로 넘어갈시 인덱스 초기화하고 jsw.html로 이동

if __name__ == "__main__":
    app.run(debug=True) # 웹 앱 실행