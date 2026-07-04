from io import BytesIO
from urllib.parse import urlparse
import os
import shutil
from flask import session

from flask import (
    Flask,
    render_template,
    request,
    flash,
    send_file,
    redirect,
    url_for
)

from config import Config
from models import db, ScriptHistory
from script_generator import generate_script

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


def is_valid_github_url(url):

    try:

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        if parsed.netloc.lower() != "github.com":
            return False

        path = parsed.path.strip("/")

        if len(path.split("/")) < 2:
            return False

        return True

    except Exception:
        return False


@app.route("/", methods=["GET", "POST"])
def home():

    generated_script = ""

    try:
        db.session.execute(db.text("SELECT 1"))
        database_status = "Connected Successfully"

    except Exception as error:

        database_status = f"Connection Failed: {error}"

    if request.method == "POST":

        project_name = request.form.get(
            "project_name",
            ""
        ).strip()

        github_url = request.form.get(
            "github_url",
            ""
        ).strip()

        docker_image = request.form.get(
            "docker_image",
            ""
        ).strip()

        docker_container = request.form.get(
            "docker_container",
            ""
        ).strip()

        port = request.form.get(
            "port",
            ""
        ).strip()

        if not project_name:

            flash(
                "Project Name is required.",
                "danger"
            )

            return render_template(
                "index.html",
                generated_script="",
                database_status=database_status
            )

        if not github_url:

            flash(
                "GitHub Repository URL is required.",
                "danger"
            )

            return render_template(
                "index.html",
                generated_script="",
                database_status=database_status
            )

        if not is_valid_github_url(github_url):

            flash(
                "Please enter a valid GitHub repository URL.",
                "danger"
            )

            return render_template(
                "index.html",
                generated_script="",
                database_status=database_status
            )

        if not docker_image:

            flash(
                "Docker Image Name is required.",
                "danger"
            )

            return render_template(
                "index.html",
                generated_script="",
                database_status=database_status
            )

        if not docker_container:

            flash(
                "Docker Container Name is required.",
                "danger"
            )

            return render_template(
                "index.html",
                generated_script="",
                database_status=database_status
            )

        try:

            port_number = int(port)

            if port_number < 1 or port_number > 65535:
                raise ValueError

        except ValueError:

            flash(
                "Port Number must be between 1 and 65535.",
                "danger"
            )

            return render_template(
                "index.html",
                generated_script="",
                database_status=database_status
            )

        try:

            generated_script = generate_script(
                request.form
            )

            history = ScriptHistory(
                project_name=project_name,
                github_url=github_url,
                generated_script=generated_script
            )

            db.session.add(history)

            db.session.commit()

            flash(
                "Jenkins Freestyle Script generated successfully.",
                "success"
            )

        except Exception as error:

            db.session.rollback()

            flash(
                f"Database Error: {error}",
                "danger"
            )

    return render_template(
        "index.html",
        generated_script=generated_script,
        database_status=database_status
    )

@app.route("/history")
def history():

    scripts = ScriptHistory.query.order_by(
        ScriptHistory.id.desc()
    ).all()

    total_scripts = len(scripts)

    return render_template(
        "history.html",
        scripts=scripts,
        total_scripts=total_scripts
    )

@app.route("/clear-history", methods=["POST"])
def clear_history():
    """
    Delete all saved script history.
    """

    try:
        deleted = ScriptHistory.query.delete()
        db.session.commit()

        flash(
            f"Successfully deleted {deleted} history record(s).",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        flash(
            f"Unable to clear history: {error}",
            "danger"
        )

    return redirect(
        url_for("history")
    )

@app.route("/clear-cache", methods=["POST"])
def clear_cache():
    """
    Clear Flask session and temporary generated files.
    """

    try:

        # Clear Flask session
        session.clear()

        # Folder containing generated files
        generated_folder = "generated_scripts"

        if os.path.exists(generated_folder):

            for filename in os.listdir(generated_folder):

                filepath = os.path.join(
                    generated_folder,
                    filename
                )

                try:

                    if os.path.isfile(filepath):
                        os.remove(filepath)

                    elif os.path.isdir(filepath):
                        shutil.rmtree(filepath)

                except Exception:
                    pass

        flash(
            "Application cache cleared successfully.",
            "success"
        )

    except Exception as error:

        flash(
            f"Unable to clear cache: {error}",
            "danger"
        )

    return redirect(
        url_for("history")
    )

@app.route("/delete-history/<int:history_id>", methods=["POST"])
def delete_history(history_id):
    """
    Delete one history record.
    """

    try:

        history = ScriptHistory.query.get_or_404(
            history_id
        )

        db.session.delete(history)

        db.session.commit()

        flash(
            "History record deleted.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        flash(
            f"Unable to delete history: {error}",
            "danger"
        )

    return redirect(
        url_for("history")
    )

@app.route("/download/sh", methods=["POST"])
def download_sh():

    script = request.form.get(
        "generated_script",
        ""
    )

    return send_file(
        BytesIO(
            script.encode("utf-8")
        ),
        as_attachment=True,
        download_name="jenkins_build.sh",
        mimetype="text/x-shellscript"
    )


@app.route("/download/txt", methods=["POST"])
def download_txt():

    script = request.form.get(
        "generated_script",
        ""
    )

    return send_file(
        BytesIO(
            script.encode("utf-8")
        ),
        as_attachment=True,
        download_name="jenkins_build.txt",
        mimetype="text/plain"
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0", port=5000, debug=True
    )
