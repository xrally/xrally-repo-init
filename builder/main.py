"""
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""

import os
import shutil

import click
import jinja2


@click.command()
@click.option("--name",
              prompt="Package name", help="Project name")
@click.option("--platform",
              prompt="Platform name", help="xRally platform name")
@click.option("--path", default="./", help="Root directory of new project.")
@click.option("--existing/--no-existing", default=False)
def cli(name, platform, path, existing):
    skeleton = "existing_platform" if existing else "new_platform"
    shutil.copytree(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "skeletons", skeleton),
        path
    )
    render_path(path, name)
    render_content(path, name, platform)


def render_path(path, name):
    for p in os.listdir(path):
        full_path = os.path.join(path, p)

        if os.path.isfile(full_path):
            shutil.move(
                full_path,
                full_path.replace("{project}", name).replace(".j2", "")
            )

        elif os.path.isdir(full_path):
            new_path = full_path.replace("{project}", name)
            shutil.move(full_path, new_path)
            render_path(new_path, name)


def render_content(path, name, platform):

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(path), encoding="utf8"))

    for root, dirs, files in os.walk(path):
        for file_name in files:
            with open(os.path.join(root, file_name), "r+") as f:
                template = f.read()
                content = env.from_string(template).render(
                    name=name, platform=platform)
                f.seek(0)
                f.write(content)
                f.truncate()


def main():
    cli()


if __name__ == "__main__":
    main()
