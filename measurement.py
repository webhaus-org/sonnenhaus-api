import falcon

from db import MeasurementEntry


class MeasurementRoutes:
    def _to_dict(self, measurement: MeasurementEntry):
        return {
            "id": measurement.id,
            "type": measurement.type,
            "measure_date": measurement.measure_date,
            "data": measurement.data,
            "meta": measurement.data,
            "ref": measurement.ref,
        }

    def on_get(self, req, resp):
        session = req.context.db_session
        measurement_entries = session.query(MeasurementEntry).order_by(MeasurementEntry.measure_date.desc()).all()
        resp.media = [self._to_dict(entry) for entry in measurement_entries]
