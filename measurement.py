import falcon

from db import MeasurementEntry


class MeasurementRoutes:
    def _to_dict(self, measurement: MeasurementEntry):
        return {
            "id": measurement.id,
            "type": measurement.type,
            "measure_date": measurement.measure_date,
            "measurement": measurement._measurement,
            "meta": measurement._meta,
            "ref": measurement._ref,
        }

    def on_get(self, req, resp):
        session = req.context.db_session
        measurement_entries = session.query(MeasurementEntry).all()
        resp.media = [self._to_dict(entry) for entry in measurement_entries]
