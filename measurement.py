import falcon

from db import MeasurementEntry


class MeasurementRoutes:
    def _to_dict(self, measurement: MeasurementEntry):
        return {
            "id": measurement.id,
            "type": measurement.type,
            "measure_date": measurement.measure_date,
            "measurement": measurement.measurement(),
            "meta": measurement.meta(),
            "ref": measurement.ref(),
        }

    def on_get(self, req, resp):
        session = req.context.db_session
        measurement_entries = session.query(MeasurementEntry).all()
        resp.media = [self._to_dict(entry) for entry in measurement_entries]
