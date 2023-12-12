from flask import Blueprint, request


bms_route = Blueprint("Book Management Service", __name__)

@bms_route.post("books/create")
def create()