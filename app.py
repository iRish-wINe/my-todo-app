from flask import Flask, render_template, request

app = Flask(__name__)

# Day 4 concept: A global Python list to store our tasks temporarily
my_tasks = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        typed_text = request.form.get("todo_item")
        
        # If the user actually typed something, add it to our list
        if typed_text:
            my_tasks.append(typed_text)
            
    # We pass our Python list into the HTML template as a variable named "tasks"
    return render_template("index.html", tasks=my_tasks)

if __name__ == "__main__":
    app.run(debug=True)
