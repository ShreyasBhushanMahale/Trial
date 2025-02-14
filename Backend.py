from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


# Database connection setup
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="BRUNO",
        database="infrastructure_db",
    )
    return conn


# Initialize the database and create a table if it doesn't exist
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            project_type VARCHAR(255),
            location VARCHAR(255),
            budget FLOAT,
            materials VARCHAR(255),
            issues TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Home route
@app.route("/")
def index():
    return render_template("index.html")


# Form submission route
@app.route("/submit", methods=["POST"])
def submit():
    project_type = request.form["project-type"]
    location = request.form["location"]
    budget = request.form["budget"]
    materials = request.form["materials"]
    issues = request.form["existing-issues"]

    # Save project data to MySQL database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO projects (project_type, location, budget, materials, issues)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (project_type, location, budget, materials, issues),
    )
    conn.commit()
    conn.close()

    # Generate project suggestions
    suggestions = generate_suggestions(
        project_type, location, budget, materials, issues
    )

    return render_template("suggestions.html", suggestions=suggestions)


# Suggestion generation logic
def generate_suggestions(project_type, location, budget, materials, issues):
    suggestions = []
    if project_type == "building":
        suggestions.append(f"For a building in {location}, consider using {materials}.")
    elif project_type == "bridge":
        suggestions.append(
            f"A bridge in {location} might need reinforced steel due to the terrain."
        )
    elif project_type == "tunnel":
        suggestions.append(
            f"Tunnels in {location} might benefit from the cut-and-cover method."
        )
    elif project_type == "dam":
        suggestions.append(
            f"Dams in {location} should use high-grade concrete for durability."
        )

    if issues:
        suggestions.append(
            f"The existing issues reported: {issues}. Maintenance is highly recommended."
        )

    suggestions.append(
        f"Estimated budget: ${budget} is sufficient for {project_type} in {location}."
    )
    return suggestions


if __name__ == "__main__":
    init_db()  # Initialize the MySQL database
    app.run(debug=True)
