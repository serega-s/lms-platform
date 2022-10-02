from fastapi import HTTPException, status


def HTTP400Exception():
    """
        Raise exception if bad request
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Bad Request'
    )


def HTTP401Exception():
    """
        Raise exception if wrong auth credentials
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={
            'WWW-Authenticate': "Bearer"
        })


def HTTP403Exception():
    """
        Raise exception if wrong object owner
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Wrong object owner'
    )


def HTTP404Exception():
    """
        Raise exception if object not found
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Object not found'
    )


def HTTP409Exception():
    """
        Raise exception if object already exists
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Object alredy exists'
    )


def HTTP500Exception():
    """
        Raise exception if internal server error
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Something went wrong'
    )
