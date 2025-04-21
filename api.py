#!/usr/bin/env python3

import argparse
import falcon
import json
import logging
import multiprocessing
import bjoern
import werkzeug

from functools import partial

import auth
import config
import cors
import db
import measurement
import user
import utils


logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)
logger.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


def create_falcon_app(cfg: config.Config):
    db_session = db.create_session(cfg.db.db_url)
    app = falcon.App(middleware=[cors.CorsMiddleware(), db.DBMiddleware(db_session)])

    json_handler = falcon.media.JSONHandler(
        dumps=partial(json.dumps, default=utils.json_serialize, sort_keys=True),
        loads=partial(json.loads),
    )
    extra_handlers = {"application/json": json_handler}
    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)
    app.add_route(
        "/measurement",
        measurement.MeasurementRoutes(cfg.measurement.validation.path_to_public_key),
    )
    app.add_route(
        "/user",
        user.UserRoutes(),
    )

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=6543)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--productive", type=bool, default=False)
    parser.add_argument("--cfg", default=None)

    parsed_args = parser.parse_args()
    port = parsed_args.port
    workers = parsed_args.workers
    prod = parsed_args.productive
    cfg = config.make_config_obj(parsed_args.cfg)

    app = create_falcon_app(cfg)

    if cfg.server.authentication_service.authentication_provider == "firebase":
        auth.init_firebase(cfg.server.authentication_service.path_to_authentication_provider_config)
    else:
        raise NotImplemented(f"{cfg.server.authentication_service.authentication_provider=} unknown")

    if prod:
        logger.info("RUNING IN PRODUCTION")

        def serve():
            bjoern.run(app, "localhost", port, reuse_port=True)

        for _ in range(workers - 1):
            proc = multiprocessing.Process(target=serve)
            proc.start()
        try:
            serve()
        except KeyboardInterrupt:
            logger.info("Terminating due to KeyboardInterrupt")
    else:
        logger.info("RUNING NON-PRODUCTIVE")
        werkzeug.serving.run_simple(
            "localhost",
            port=port,
            application=app,
            use_reloader=True,
            use_debugger=True,
        )


if __name__ == "__main__":
    main()
