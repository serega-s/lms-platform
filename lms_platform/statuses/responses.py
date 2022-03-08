from fastapi import Response, status


def HTTP200Response():
    return Response(
        status_code=status.HTTP_200_OK
    )


def HTTP204Response():
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
