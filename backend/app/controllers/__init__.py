# Import controllers
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.career_controller import CareerController
from app.controllers.document_controller import DocumentController

__all__ = ['AuthController', 'UserController', 'CareerController', 'DocumentController']
