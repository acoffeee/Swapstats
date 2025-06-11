import Fastapi, jsonify, request

app = Flask(__name__)

employees = [
    {'id': 1, 'name': 'Ashley'},
    {'id': 2, 'name': 'Kate'},
    {'id': 3, 'name': 'Joe'}
]

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = next((emp for emp in employees if emp['id'] == id), None)
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400
    
    new_employee = {'id': len(employees) + 1, 'name': data['name']}
    employees.append(new_employee)
    return jsonify(new_employee), 201

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = next((emp for emp in employees if emp['id'] == id), None)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400
    
    employee['name'] = data['name']
    return jsonify(employee)

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    global employees
    employees = [emp for emp in employees if emp['id'] != id]
    return jsonify({'message': 'Employee deleted'})

if __name__ == '__main__':
    app.run(debug=True)
