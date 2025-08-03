import falcon

from auth import Auth
from db import MeasurementEntry
from utils import validate_payload


class MeasurementRoutes:

    def __init__(self, path_to_public_key: str):
        with open(path_to_public_key, "rb") as f:
            self.public_key = f.read()

    def _to_dict(self, measurement: MeasurementEntry):
        return {
            "id": measurement.id,
            "type": measurement.type,
            "measure_date": measurement.measure_date,
            "data": measurement.data,
            "meta": measurement.meta,
            "ref": measurement.ref,
        }

    @falcon.before(Auth.validate_permission)
    def on_get(self, req, resp):
        session = req.context.db_session
        query_params = req.params
        limit = query_params.get("limit", 60*24)
        min_measure_date = query_params.get("min_measure_date", None)
        max_measure_date = query_params.get("max_measure_date", None)
        measurement_entries = session.query(MeasurementEntry)

        if min_measure_date:
            measurement_entries = measurement_entries.filter(
                    MeasurementEntry.measure_date >= min_measure_date
                    )
        if max_measure_date:
            measurement_entries = measurement_entries.filter(
                    MeasurementEntry.measure_date <= max_measure_date
                    )

        measurement_entries = (
            measurement_entries.order_by(MeasurementEntry.measure_date.desc())
            .limit(limit)
            .all()
        )
        resp.media = [self._to_dict(entry) for entry in measurement_entries]

    def on_post(self, req, resp):
        measurement = validate_payload(self.public_key, req)
        session = req.context.db_session
        try:
            measurement_entry = MeasurementEntry(
                type=measurement["type"],
                measure_date=int(measurement["measure_date"]),
                data=measurement.get("data", None),
                meta=measurement.get("meta", None),
                ref=measurement.get("ref", None),
            )
            session.add(measurement_entry)
            session.commit()
        except KeyError:
            raise falcon.HTTPBadRequest(description="Missing required field")
        except ValueError:
            raise falcon.HTTPBadRequest(description="Value of wrong type")
        except TypeError:
            raise falcon.HTTPBadRequest(description="Measurement invalid")
        resp.media = self._to_dict(measurement_entry)
