import falcon
import hashlib
import hmac
import os
import subprocess

own_dir = os.path.dirname(__file__)


class GithubRoutes:
    def __init__(
        self,
        webhook_secret: str,
        service_name: str,
        update_script_path: str=os.path.join(own_dir, 'update_api.sh'),
    ):
        self.webhook_secret = webhook_secret.encode("utf-8")
        self.service_name = service_name
        self.update_script_path = update_script_path

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        hub_signature = req.get_header(
            "x-hub-signature-256",
            required=True,
            default="x-hub-signature-256 is missing"
        )

        with req.bounded_stream as rs:
            raw_body = rs.read()
        digest = hmac.new(key=self.webhook_secret, msg=raw_body, digestmod=hashlib.sha256)
        expected_signature = f"sha256={digest.hexdigest()}"
        if not hmac.compare_digest(expected_signature, hub_signature):
            raise falcon.HTTPBadRequest(
                title="Signature unmatched",
                description="Calculated and provided signature didn't match"
            )
        subprocess.Popen([self.update_script_path, self.service_name])
