from flask import Flask, request, jsonify
from models.task import Task


app = Flask(__name__)


tasks = []
task_id_control = 1

@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(
        id=task_id_control,
        title=data.get("title"),
        description=data.get("description", "")
    )
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({ "mensagem": "Nova tarefa criada com sucesso" })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }

    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
        
    return jsonify({ "message": "Não foi possível encontrar a atividade" }), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task_to_update = None
    for task in tasks:
        if task.id == id:
            task_to_update = task
            break

    if task_to_update == None:
        return jsonify({ "message": "Não foi possível encontrar a atividade" }), 404
    
    data = request.get_json()
    task_to_update.title = data["title"]
    task_to_update.description = data["description"]
    task_to_update.completed = data["completed"]

    return jsonify({ "message": "Tarefa atualizada com sucesso" })


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task_to_delete = None
    for task in tasks:
        if task.id == id:
            task_to_delete = task
            break

    if not task_to_delete:
        return jsonify({ "message": "Não foi possível encontrar a atividade" }), 404
    
    tasks.remove(task_to_delete)

    return jsonify({ "message": "Tarefa removida com sucesso" })


# Para execução manual (local)
if __name__ == "__main__":
    app.run(debug=True)