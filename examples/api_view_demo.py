# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2022/10/18 9:00
from typing import Optional

from flask.views import MethodView
from pydantic import BaseModel, Field

from flask_openapi3 import OpenAPI, Tag, Info, HTTPBearer
from flask_openapi3.view import APIView

jwt = HTTPBearer()
security_schemes = {"jwt": jwt}
info = Info(title='book API', version='1.0.0')
app = OpenAPI(__name__, info=info, security_schemes=security_schemes)

security = [{"jwt": []}]

api_view = APIView(url_prefix="/api/v1", view_tags=[Tag(name="book")], view_security=security)


class BookQuery(BaseModel):
    age: Optional[int] = Field(None, description='Age')


class BookBody(BaseModel):
    age: Optional[int] = Field(..., ge=2, le=4, description='Age')
    author: str = Field(None, min_length=2, max_length=4, description='Author')


@api_view.route("/book")
class BookListAPIView(MethodView):
    a = 1

    @api_view.doc(summary="get book list")
    def get(self, query: BookQuery):
        print(self.a)
        return query.json()

    @api_view.doc(summary="create book")
    def post(self, body: BookBody):
        """description for create book"""
        return body.json()


@api_view.route("/book/<id>")
class BookAPIView:
    @api_view.doc(summary="get book", deprecated=True)
    def get(self):
        return "get"

    @api_view.doc(summary="update book")
    def put(self):
        return "put"

    @api_view.doc(summary="delete book")
    def delete(self):
        return "delete"


app.register_api_view(api_view)

if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True)
