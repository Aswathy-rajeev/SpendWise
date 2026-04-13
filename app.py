from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Default demo data (makes app look filled)
expenses = [
    {'name': 'Lunch', 'amount': 120, 'category': 'Food'},
    {'name': 'Bus', 'amount': 40, 'category': 'Travel'},
    {'name': 'Movie', 'amount': 200, 'category': 'Entertainment'}
]

budget = 2000

@app.route('/')
def index():
    global budget

    total = sum([e['amount'] for e in expenses])
    warning = total > budget

    # Category-wise totals
    category_total = {}
    for e in expenses:
        category_total[e['category']] = category_total.get(e['category'], 0) + e['amount']

    # Smart suggestions
    suggestion = ""

    if 'Food' in category_total and category_total['Food'] > 500:
        suggestion = "You are spending too much on food. Try reducing eating out."

    elif 'Shopping' in category_total and category_total['Shopping'] > 500:
        suggestion = "Shopping expenses are high. Avoid unnecessary purchases."

    elif 'Entertainment' in category_total and category_total['Entertainment'] > 300:
        suggestion = "Entertainment expenses are high. Try limiting subscriptions or outings."

    elif total > budget:
        suggestion = "You exceeded your budget. Try to save more."

    return render_template(
        'index.html',
        expenses=expenses,
        total=total,
        warning=warning,
        suggestion=suggestion,
        budget=budget
    )


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    amount = float(request.form['amount'])
    category = request.form['category']

    expenses.append({
        'name': name,
        'amount': amount,
        'category': category
    })

    return redirect('/')


@app.route('/delete/<int:index>')
def delete(index):
    expenses.pop(index)
    return redirect('/')


@app.route('/set_budget', methods=['POST'])
def set_budget():
    global budget
    budget = float(request.form['budget'])
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)