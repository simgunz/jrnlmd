import os
import subprocess
import tempfile

EXTERNAL_COMMAND = "bat -l markdown --pager=never --style=plain"


def print_with_external(text: str) -> None:
    try:
        subprocess.run(EXTERNAL_COMMAND.split(), input=text, encoding="utf-8")
    except Exception:
        print(text)


def input_from_editor():
    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call([editor, tf.name])
        tf.seek(0)
        return tf.read().decode("utf-8")
