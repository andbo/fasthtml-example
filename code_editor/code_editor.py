# AUTOGENERATED! DO NOT EDIT! File to edit: code_editor.ipynb.

# %% auto 0
__all__ = ['ace_editor', 'gridlink', 'css', 'app', 'files', 'File', 'rt', 'id_curr', 'id_list', 'js_code', 'example_code',
           'SaveFile', 'Toolbar', 'FileRow', 'Sidebar', 'CodeEditor', 'get', 'post']

# %% code_editor.ipynb 3
from fasthtml.fastapp import *

# Ace Editor (https://ace.c9.io/)
ace_editor = Script(src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.35.0/ace.min.js")
# Flexbox CSS (http://flexboxgrid.com/)
gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")

css = Style('''\
.sidebar {
    background-color: #f4f4f4;
    overflow-y: auto;
    padding: 10px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    height: calc(100vh - 40px);
}

#editor-container {
    flex: 1;
    height: calc(100vh - 40px);
}

#editor {
    height: 100%;
    width: 100%;
}

.box-row {
    border: 1px solid #ccc;
}
''')

app,rt,files, File = fast_app('data/files.db', hdrs=(ace_editor, gridlink, css), id=int, filename=str, content=str, pk='id')

id_curr = 'current-file'
id_list = 'file-list'

# %% code_editor.ipynb 5
js_code = """\
function renderEditor() {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/javascript");
}

function getFileContent() {
    var editor = ace.edit("editor");
    return editor.getValue();
}

renderEditor();
"""

example_code = """\
function foo(items) {
    var x = "All this is syntax highlighted";
    return x;
}"""

# %% code_editor.ipynb 6
def SaveFile():
    return Form(
        Input(type="text", id="filename", name="filename", placeholder="Filename", required=True),
        Button("Save", type="submit", hx_post="/save", target_id=id_list, hx_swap="beforeend", hx_vals="js:{content: getFileContent(), filename: filename.value}"),
        cls="col-xs-12"
    )
    ...
def Toolbar():
    return Div(
        Div(
            Select(
                Option("JavaScript", value="javascript"),
                Option("Python", value="python"),
                Option("HTML", value="html"),
                Option("CSS", value="css"),
                Option("Markdown", value="markdown"),
                id="language"
            ),
            Button("Run", id="run"),
            SaveFile(),
            cls="col-xs-12 toolbar"
        ),
        cls="row"
    )

# %% code_editor.ipynb 7
def FileRow(file: File):
    return Li(
        A(
            file.filename, hx_get=f'/files/{file.id}', target_id="editor-container", hx_swap="innerHTML",
            hx_on="htmx:afterSwap: renderEditor()",
          ),
        id=f'file-{file.id}'
    )

# %% code_editor.ipynb 8
def Sidebar():
    return Div(
        Div(
            Ul(*map(FileRow, files()), id=id_list), cls="sidebar"
        ),
        cls="col-xs-12 col-sm-3"
    )

# %% code_editor.ipynb 9
def CodeEditor():
    toolbar = Toolbar()
    main = Div(
        Sidebar(),
        Div(
            Div(example_code, id="editor"),
            id="editor-container", cls="col-xs-12 col-sm-9", hx_on="htmx:afterSwap: renderEditor()"
        ),
        cls="row"
    )
    return Title("Code Editor",), Div(toolbar, main, cls="container-fluid"), Script(NotStr(js_code))

# %% code_editor.ipynb 11
@rt("/")
def get():
    return CodeEditor()

# %% code_editor.ipynb 12
@rt("/files/{id}")
def get(id:int):
    return Div(files[id].content, id="editor", cls="ace_editor ace-tm")#, hx_on="htmx:afterSwap: renderEditor()"),

# %% code_editor.ipynb 13
@rt("/save")
def post(filename: str, content: str):
    file = File(filename=filename, content=content, id=len(files()) + 1)
    files.insert(file)
    return FileRow(file)
