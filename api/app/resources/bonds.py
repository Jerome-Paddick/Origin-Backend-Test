from .auth import AuthenticatedRestfulResource
from flask import request
from flask_restful import reqparse, Resource
from flask_restful_swagger import swagger
from flask_restful import fields, inputs
from ..utils.legal_entity_identifier import legal_entity_identiy_request
from ..models.core import db
from ..models.bonds import Bonds
import datetime

@swagger.model
class BondsNestedResponse:
    resource_fields = {
        "id": fields.Integer,
        "isin": fields.String,
        "size": fields.Integer,
        "currency": fields.String,
        "maturity": fields.DateTime,
        "legal_name": fields.String,
    }
    required=["id", "isin", "size", "currency", "maturity", "legal_name"]
@swagger.model
@swagger.nested(data=BondsNestedResponse.__name__)
class BondsResponse:
    resource_fields = {
        "status": fields.String,
        "data": fields.List(fields.Nested(BondsNestedResponse.resource_fields))
    }
    required=["status", "data"]

@swagger.model
class BondsRequest:
    resource_fields = {
        "isin": fields.String,
        "size": fields.Integer,
        "currency": fields.String,
        "maturity": fields.DateTime,
        "lei": fields.String,
    }
    required = ["isin", "size", "currency", "maturity", "lei"]

@swagger.model
class GenericResponse:
    resource_fields = {
        "status": fields.String,
        "message": fields.String
    }
    required = ['status', 'message']


class BondsResource(AuthenticatedRestfulResource):
    @swagger.operation(
        responseClass=BondsResponse.__name__,
        parameters=[{
                "name": "legal_name", "description": "legal_name filter", "required": False,
                "dataType": "string", "paramType": "query",
            },{
                "name": "api_key", "description": "JWT Token", "required": True,
                "dataType": "string", "paramType": "query",
            }],
        responseMessages=[
            {"code": 200, "message": "Successful Request"},
            {"code": 500, "message": "Unexpected error"},
        ]
    )
    def get(self):
        try:
            bonds_query = Bonds.query.filter(Bonds.user_id==self.user_id)

            legal_name_filter = request.args.get('legal_name')
            if legal_name_filter:
                bonds_query = bonds_query.filter(Bonds.legal_name==legal_name_filter)

            data = [{
                'id': bond.id,
                'isin': bond.isin,
                'size': bond.size,
                'currency': bond.currency,
                'maturity': bond.maturity.strftime('%Y-%m-%d'),
                'legal_name': bond.legal_name,
            } for bond in bonds_query.all()]

            return {'status': 'ok',
                    'data': data}, 200

        except Exception as ex:
            return {'status': 'error',
                    'message': f'Unexpected Error in {self.__class__.__name__} get',
                    'error': str(ex)}, 500

    @swagger.operation(
        responseClass=GenericResponse.__name__,
        parameters=[{
                "name": "api_key", "description": "JWT Token", "required": True,
                "dataType": "string", "paramType": "query",
            },{
                "dataType": BondsRequest.__name__,
                "name": "payload", "required": True, "allowMultiple": False, "paramType": "body",
            }],
        responseMessages=[
            {"code": 200, "message": "Successful Request"},
            {"code": 500, "message": "Unexpected error"},
        ]
    )
    def post(self):
        """ Gets List of gifts on list """
        # "isin": "FR0000131104",
        # "size": 100000000,
        # "currency": "EUR",
        # "maturity": "2025-02-28",
        # "lei": "R0MUWSFPU8MPRO8K5P83"
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("lei", type=str, required=True)
            parser.add_argument("isin", type=str, required=True)
            parser.add_argument("size", type=int, required=True)
            parser.add_argument("currency", type=str, required=True)
            parser.add_argument("maturity", type=str, required=True)
            args = parser.parse_args()
        except:
            return {'status': 'invalid_request', 'message': 'parameters not provided'}, 400
        try:
            lei = args.get('lei')
            legal_entity_name, lei_error = legal_entity_identiy_request(lei)
            if lei_error:
                return {'status': 'lei_error', 'error': lei_error}, 400

            try:
                maturity = datetime.date.fromisoformat(args.get("maturity"))
            except ValueError:
                return {'status': 'invalid_request', 'message': 'Invalid maturity timestamp, please use ISO format'}, 400

            bond = Bonds(
                isin=args.get("isin"),
                size=args.get("size"),
                currency=args.get("currency"),
                maturity=maturity,
                legal_name=legal_entity_name,
                user_id=self.user_id,
            )
            db.session.add(bond)
            db.session.commit()

            return {'status': 'entity_added', 'message': 'Entity added to database'}, 200

        except Exception as ex:
            return {'status': 'error',
                    'message': f'Unexpected Error in {self.__class__.__name__} post',
                    'error': str(ex)}, 500