import uuid

from fastapi import APIRouter, UploadFile

from Services.file_service import FileServ
from Services.inspection_form_service import FormServ
from dtos.form import FormRes

router = APIRouter(
    prefix='/api/v1/form',
    tags=['form']
)

@router.post('/{form_id}/image')
async def upload_image(form_id: int, image: UploadFile, file_service: FileServ):
    random_name = str(uuid.uuid4())
    random_name += '.png'
    with open(f'static/images/{random_name}', 'wb') as file:
        file.write(await image.read())
    file_service.upload(form_id, original_name=image.filename, random_name=random_name)
    return True


@router.get('/{form_id}', response_model=FormRes)
async def get_form(form_id: int, service: FormServ):
    form = service.get_by_id(form_id)
    return {'form': form}
