from django.core.management.base import BaseCommand

import requests
import os
import subprocess


class Command(BaseCommand):
    help = 'Registers a deploy event'

    def rollbar_record_deploy(self):
        access_token = 'eb67f32be84f4e93a903a79bde5e8378'
        environment = 'production'
        git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
        revision = os.environ.get('HEROKU_SLUG_COMMIT') or git_hash

        local_username = 'Auto Deploy'

        resp = requests.post('https://api.rollbar.com/api/1/deploy/', {
            'access_token': access_token,
            'environment': environment,
            'revision': revision,
            'local_username': local_username,
        }, timeout=3)

        if resp.status_code == 200:
            print "Deploy recorded successfully."
        else:
            print "Error recording deploy:", resp.text

    def handle(self, *args, **options):
        self.rollbar_record_deploy()
