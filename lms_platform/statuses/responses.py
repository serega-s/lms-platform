from fastapi import Response, status


def HTTP200Response():
    """
        Return response if success
    """
    return Response(
        status_code=status.HTTP_200_OK
    )


def HTTP204Response():
    """
        Return response if success but no content
    """
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
