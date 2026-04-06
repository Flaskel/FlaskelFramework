import click
import inflect
import os

p = inflect.engine()

@click.command('make:model')
@click.option("--name", prompt="Model name")
def make_model(name):

    model_name = name.capitalize()
    model_name_lower = name.lower()
    table_name = p.plural(model_name_lower)

    # ------------------ MODEL ------------------
    with open("app/Stub/Model.stub") as f:
        stub = f.read()

    model_code = stub.replace("{model_name}", model_name)\
        .replace("{table_name}", table_name)\
        .replace("{model_name_lower}", model_name_lower)

    with open(f"app/Models/{model_name}.py", "w") as f:
        f.write(model_code)


    # ------------------ CONTROLLER ------------------
    with open("app/Stub/Controller.stub") as f:
        stub = f.read()

    controller_code = stub.replace("{model_name}", model_name)\
        .replace("{table_name}", table_name)\
        .replace("{model_name_lower}", model_name_lower)

    with open(f"app/Controller/{model_name}Controller.py", "w") as f:
        f.write(controller_code)


    # ----------------- AUTO IMPORT IN __init__.py -------------------  
    import_line = f"from .{model_name} import {model_name}\n"
    
    init_file_path = "app/Models/__init__.py"

    if not os.path.exists(init_file_path):
        with open(init_file_path, "w") as f:
            f.write(import_line)
    else:
        with open(init_file_path, "r") as f:
            content = f.read()

        if import_line not in content:
            with open(init_file_path, "a") as f:
                f.write(import_line)

    # ------------------ CREATE MIGRATION -------------------
    try:
        migration_message = f"create_table_{model_name_lower}"

        os.system(f'flask db migrate -m "{migration_message}"')

        click.echo(f"✅ Migration created: {migration_message}")

    except Exception as e:
        click.echo("❌ Migration failed")
        click.echo(str(e))