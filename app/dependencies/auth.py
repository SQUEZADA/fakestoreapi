from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(lambda: AuthService()),
    user_service: UserService = Depends(lambda: UserService())
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = auth_service.verify_token(token)
    if token_data is None:
        raise credentials_exception
        
    user = user_service.get_user_by_id(int(token_data.user_id))
    if user is None:
        raise credentials_exception
        
    return user 