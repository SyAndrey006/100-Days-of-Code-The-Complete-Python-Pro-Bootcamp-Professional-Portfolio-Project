from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_text = request.form.get("task")
        if task_text:
            tasks.append({"text": task_text, "done": False})
        return redirect(url_for("index"))

    return render_template("index.html", tasks=tasks)

@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    tasks[task_id]["done"] = not tasks[task_id]["done"]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
