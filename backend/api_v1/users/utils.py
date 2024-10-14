from fastapi import UploadFile
import os
import aiofiles
import shutil

from backend.config.settings import IMAGE_URL


async def upload_file(file: UploadFile,
                      login: str,
                      ) -> str:
    file_name = file.filename.replace(' ', '').replace('/', '')
    file_location = IMAGE_URL(login)
    try:
        async with aiofiles.open(f'{file_location}/{file_name}', 'wb') as file_object:
            connect = await file.read()
            await file_object.write(connect)
    finally:
        await file.close()
    return file_name


async def rm_save_upload_file(old: str,
                              file: UploadFile,
                              login: str,
                              ) -> str:
    """
    Удаление и сохранение нового файла
    """
    if old:
        old_location = IMAGE_URL(login, old)
        os.remove(old_location)
    file_save = await upload_file(
        file=file,
        login=login
    )
    return file_save


def rename_dir_of_login(old: str,
                        new: str,
                        ) -> None:
    """
    Переименование папки
    """
    if not old == new:
        old_location = IMAGE_URL(old)
        new_location = IMAGE_URL(new)
        os.rename(old_location, new_location)


def make_image_directory(dir_name: str) -> None:
    """
    Создание папки для изобращений
    """
    try:
        file_path = IMAGE_URL(dir_name)
        os.mkdir(file_path)
    except FileExistsError:
        return


def delete_dir(dir_name: str) -> None:
    """
    Удаление папки
    """
    dir_path = IMAGE_URL(dir_name)
    shutil.rmtree(dir_path, ignore_errors=True)
