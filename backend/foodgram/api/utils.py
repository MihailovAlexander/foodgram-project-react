
from rest_framework import status
from rest_framework.response import Response


def create_record(obj_class, user, recipe, serializer):
    already_existed, created = obj_class.objects.get_or_create(
        user=user,
        recipe=recipe
    )
    if not created:
        return Response(
            {'errors': 'Ошибка при создании записи.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        serializer(recipe).data,
        status=status.HTTP_201_CREATED,
    )


def delete_record(obj_class, user, recipe):
    try:
        record = obj_class.objects.get(user=user, recipe=recipe)
    except obj_class.DoesNotExist:
        return Response(
            {'errors': 'Удаление не удалось.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    record.delete()
    return Response(
        {'detail': 'Удаление успешно.'},
        status=status.HTTP_204_NO_CONTENT,
    )
