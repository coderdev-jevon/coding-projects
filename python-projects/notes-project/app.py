import bleach
from flask import Flask, render_template, url_for, redirect, request, Response
import markdown as md
import os
import re
import shutil

# the base path for the notes
FOLDER_BASE = os.path.abspath(os.path.dirname(__file__))

INVALID_NAME_PATTERN = re.compile(r'[\\/:*?"<>|]|\.\.')

app = Flask(__name__)

def join_path(sub_path: str) -> str | None:
    # First get the url base for the notes folder

    # Join the base with sub_path
    joined_path = os.path.abspath(os.path.join(FOLDER_BASE, sub_path))
    # If the parent of both path isn't equal to the base of the notes folder, then travesal attack detected
    if os.path.commonpath([FOLDER_BASE, joined_path]) != FOLDER_BASE:
        return None
    return joined_path

def list_folder(path: str) -> tuple:
    folders_list = []
    files_list = []
    # Use scandir to differentiate folders and files easily
    try: 
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    folders_list.append(entry.name)
                elif entry.is_file() and entry.name.endswith(".md"):
                    files_list.append(entry.name)
        return folders_list, files_list, True
    except (FileNotFoundError, PermissionError):
        return folders_list, files_list, False

def get_parent_path(path: str) -> str:
    if not path:
        return ""
    # Remove trailing / to not include unnecessary item and split by /
    parts = path.rstrip("/").split("/")
    if len(parts) <= 1:
        return ""
    # Remove the last segment
    parts.pop()
    return "/".join(parts)

# Created this function to get out from the open file
def get_folder_path(file_path: str) -> str:
    if not file_path:
        return ""
    parts = file_path.split("/")
    if len(parts) <= 1:
        return ""

    parts.pop()
    return "/".join(parts)

def is_valid_item_name(name: str) -> bool:
    if not name.strip():
        return False
    if INVALID_NAME_PATTERN.search(name):
        return False
    return True


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<path:sub_path>")
def notes(sub_path):
    full_path = join_path(sub_path)
    if full_path is None:
        return Response("Traversal Attack Detected", 403)
    folders_list, files_list, ok = list_folder(full_path)
    if not ok:
        return Response("File Error", 403)
    # Get back path from the URL for going back purpose
    back_path = get_parent_path(sub_path)

    return render_template("notes.html", sub_path=sub_path, back_path=back_path, folders=folders_list, files=files_list)

@app.route("/view/<path:sub_path>", methods=["GET", "POST"])
def view_notes(sub_path):
    if request.method == "POST":
        text_content = request.form.get("text_content").strip()

        # Doesn't accept empty text
        if not text_content:
            return redirect(url_for("view_notes", sub_path=sub_path))

        # Get full path
        full_path = join_path(sub_path)
        if full_path is None:
            return Response("Traversal Attack Detected", 403)

        # Rewrite file_content
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(text_content)
        except Exception as e:
            return Response(f"Error Detected {e}", 403)

        return redirect(url_for("view_notes", sub_path=sub_path))

    file_path = join_path(sub_path)
    if file_path is None:
        return Response("Traversal Attack Detected", 403)

    if not os.path.isfile(file_path):
        return Response("File Not Found", 403)

    if not file_path.endswith(".md"):
        return Response("Only md file can be viewed", 403)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            md_text = f.read()
    except Exception as e:
        return Response(f"Cannot read file {e}", 403)

    # Convert md -> html
    raw_html = md.markdown(md_text, extensions=["extra"])
    safe_html = bleach.clean(raw_html) # Prevent attack in html tags

    # Create path to return to the folder page
    back_path = get_folder_path(sub_path)
    return render_template("view.html", content_html=safe_html, back_path=back_path)
    

@app.route("/createfile/<path:sub_path>", methods=["GET", "POST"])
def create_file(sub_path):
    if request.method == "GET":
        return render_template("createfile.html")
    else:
        name = request.form.get("name")
        if not name:
            return Response("Failed to create file", 403)
        # Join sub_path with file name
        if not name.endswith(".md"):
            sub_file_path = f"{sub_path}/{name}.md"
        else:
            sub_file_path = f"{sub_path}/{name}"

        full_path = join_path(sub_file_path)
        # join_path returns None if traversal attack detected
        if full_path is None:
            return Response("Traversal Attack Detected", 403)

        # Check if file already exists
        if os.path.exists(full_path):
            return Response("File exists", 403)

        # Write the file
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write("")
        except (FileNotFoundError, PermissionError) as e:
            return Response(f"Error Detected: {e}", 403)
        
        return redirect(url_for("notes", sub_path=sub_path))

@app.route("/createfolder/<path:sub_path>", methods=["GET", "POST"])
def createfolder(sub_path):
    if request.method == "GET":
        return render_template("createfolder.html")
    else:
        name = request.form.get("name").strip()
        if not name:
            return Response("Invalid foder name", 403)
        if "/" in name or "\\" in name:
            return Response("Invalid folder name", 403)

        # Join to create full path
        sub_folder_path = f"{sub_path}/{name}"
        full_path = join_path(sub_folder_path)

        if full_path is None:
            return Response("Traversal Attack Detected", 403)

        if os.path.exists(full_path):
            return Response("Folder already exists", 403)

        try:
            os.makedirs(full_path)
        except Exception as e:
            return Response(f"Error: {e}", 403)

        return redirect(url_for("notes", sub_path=sub_path))

@app.route("/delete/<path:sub_path>")
def delete(sub_path):
    full_path = join_path(sub_path)
    if full_path is None:
        return Response("Traversal Attack Detected", 403)

    # Check file or folder, because each has different deleting method
    if os.path.isdir(full_path):
        try:    
            shutil.rmtree(full_path)
        except Exception as e:
            return Response(f"Error Detected: {e}", 403)
    elif os.path.isfile(full_path):
        try:
            os.remove(full_path)
        except Exception as e:
            return Response(f"Error Detected: {e}", 403)

    back_path = get_folder_path(sub_path)
    return redirect(url_for("notes", sub_path=back_path))

@app.route("/edit/<path:sub_path>", methods=["GET", "POST"])
def edit(sub_path):
    if request.method == "GET":
        full_path = join_path(sub_path)
        # Check if targeted path is a folder or a file
        if os.path.isdir(full_path):
            type = "folder"
        elif os.path.isfile(full_path):
            type = "file"
        return render_template("edit.html", type=type)
    else:
        name = request.form.get("name").strip()
        type = request.form.get("type")
        if not name or not is_valid_item_name(name):
            return Response("New name is not valid", 403)

        # Get folder path of the targetted file or folder
        if type == "file":
            folder_path = get_folder_path(sub_path)
            name = name + ".md"
        elif type == "folder":
            folder_path = get_parent_path(sub_path)

        # Get new old path and new path
        old_path = join_path(sub_path)
        new_path = join_path(f"{folder_path}/{name}")

        # Renaming
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            return Response(f"Renaming failed: {e}", 403)

        return redirect(url_for('notes', sub_path=folder_path))
        
    
        
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)