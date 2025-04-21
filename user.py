import falcon

from auth import validate_permission
from db import UserEntry


class UserRoutes:
    def _to_dict(self, user: UserEntry):
        return {
            "id": user.id,
            "email_address": user.email_address,
            "creation_date": user.creation_date,
            "roles": user.roles
        }

    @falcon.before(validate_permission)
    def on_get(self, req, resp):
        resp.media = self._to_dict(req.context.user)

    @falcon.before(validate_permission)
    def on_post(self, req, resp):
        session = req.context.db_session
        user = req.get_media()
        try:
            user_entry = UserEntry(
                email_address=usert["email_address"],
                roles=user.get(roles, [])
            )
            session.add(user_entry)
            session.commit()
        except KeyError:
            raise falcon.HTTPBadRequest(description="Missing required field")
        except ValueError:
            raise falcon.HTTPBadRequest(description="Value of wrong type")
        except TypeError as e:
            raise falcon.HTTPBadRequest(description="User invalid")
        resp.media = self._to_dict(user_entry)
