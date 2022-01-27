from flask import Flask

def home_route(app: Flask):
    @app.post('/series')
    def create_serie():
        from app.controllers.user_controller import create
        return create()

    @app.get('/series')
    def get_all_series():
        from app.controllers.user_controller import series
        return series()

    @app.get('/series/<int:serie_id>')
    def get_serie(serie_id): 
        from app.controllers.user_controller import selec_by_id
        return selec_by_id(serie_id)