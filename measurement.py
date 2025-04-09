import falcon

from db import MeasurementEntry


class MeasurementRoutes:
    def _to_dict(self, measurement: MeasurementEntry):
        return {
            "id": measurement.id,
            "type": measurement.type,
            "measurement": measurement.measurement(),
            "meta": measurement.meta()
        }

    def on_get(self, req, resp):
        session = req.context.db_session
        measurement_entries = session.query(MeasurementEntry).all()
        resp.media = [self._to_dict(entry) for entry in measurement_entries]
