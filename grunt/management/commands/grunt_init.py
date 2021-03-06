from __future__ import unicode_literals

import os.path, shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from grunt.conf import settings as grunt_settings


def default_staticfiles_dir():
    staticfiles_dirs = getattr(settings, "STATICFILES_DIRS", ())
    if len(staticfiles_dirs) == 0:
        return None
    return staticfiles_dirs[0]


class Command(BaseCommand):

    help = (
        "Copies the base gruntfile.js file and package.json into your STATICFILES_DIRS.\n\n"
    )

    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--force",
            action = "store_true",
            dest = "force",
            default = False,
            help = "Overwrite existing files if found."
        )
        parser.add_argument(
            "-d",
            "--dir",
            action = "store",
            dest = "dir",
            help = "Copy files into the named directory. Defaults to the first item in your STATICFILES_DIRS setting."
        )

    def handle(self, **options):
        verbosity = int(options.get("verbosity", 1))
        # Calculate the destination dir.
        dst_dir = options["dir"] or default_staticfiles_dir()
        if not dst_dir:
            raise CommandError("settings.STATICFILES_DIRS is empty, and no --dir option specified")
        # Handle destination directory tuples.
        if isinstance(dst_dir, (list, tuple)):
            dst_dir = dst_dir[1]  # Could do something more intelligent here with matching prefixes, but is it worth it?
        # Calculate paths.
        resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "resources"))
        resources = [
            "Gruntfile.js",
            "package.json",
        ]

        # Check if the file exists.
        for resource_name in resources:
            dst_path = os.path.abspath(os.path.join(dst_dir, grunt_settings.REQUIRE_BASE_URL, resource_name))
            if os.path.exists(dst_path) and not options["force"]:
                if verbosity > 0:
                    self.stdout.write("{} already exists, skipping.\n".format(dst_path))
            else:
                dst_dirname = os.path.dirname(dst_path)
                if not os.path.exists(dst_dirname):
                    os.makedirs(dst_dirname)
                shutil.copyfile(os.path.join(resources_dir, resource_name), dst_path)
                if verbosity > 0:
                    self.stdout.write("Copied {} to {}.\n".format(resource_name, dst_path))