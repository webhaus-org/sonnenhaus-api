class CorsMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header(
            'Access-Control-Allow-Headers',
            ','.join((
                'Content-Type',
                'Authorization',
                '*',
            ))
        )
        resp.set_header(
            'Access-Control-Allow-Methods',
            ','.join((
                'DELETE',
                'GET',
                'HEAD',
                'POST',
                'PATCH',
                'PUT',
            )),
        )

        if req.method == 'OPTIONS':
            resp.complete = True
