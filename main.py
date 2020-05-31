from flask import request
from flask_api import FlaskAPI, status
from classes import BashCommand, ListPackages

app = FlaskAPI(__name__, static_url_path='', static_folder='static')


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return app.send_static_file('index.html')


@app.route("/packages", methods=['GET'])
def list_installed_packages():
    """
    List installed packages.
    """
    if request.method == 'GET':
        installed_packages = ListPackages('--installed').run_command()
        return installed_packages


@app.route("/packages/all", methods=['GET'])
def list_all_packages():
    """
    List all packages.
    """
    if request.method == 'GET':
        all_packages = ListPackages().run_command()
        return all_packages


@app.route("/packages/<string:package_name>", methods=['GET', 'POST', 'DELETE'])
def install_or_remove_app(package_name):
    """
    Show app details or install or remove it.
    """
    installed_packages = ListPackages('--installed').run_command()

    if request.method == 'POST':
        if package_name in installed_packages:
            return f"Package '{package_name}' already installed", status.HTTP_200_OK
        update_cache = BashCommand(f'sudo apt update')
        update_cache.run_command()
        install_app = BashCommand(f'sudo apt install -y {package_name}')
        rc = install_app.run_command()
        return {"return_code": rc}, status.HTTP_201_CREATED

    elif request.method == 'DELETE':
        if package_name not in installed_packages:
            return f"Package '{package_name}' is not installed", status.HTTP_404_NOT_FOUND
        delete_app = BashCommand(f'sudo apt remove -y {package_name}')
        rc = delete_app.run_command()
        autoremove = BashCommand('sudo apt -y autoremove')
        autoremove.run_command()
        return {"return_code": rc}, status.HTTP_204_NO_CONTENT

    elif request.method == 'GET':
        if package_name in installed_packages:
            package_version = installed_packages[package_name]
            return {package_name: {"version": package_version}}
        else:
            return f"Package '{package_name}' is not installed"


if __name__ == "__main__":
    app.run(debug=True)
