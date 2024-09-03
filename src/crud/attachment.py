from crud.async_crud import BaseAsyncCRUD
from models import Attachment
from schemas.attachment import AttachmentCreateDB, AttachmentUpdate


class AttachmentCRUD(
    BaseAsyncCRUD[Attachment, AttachmentCreateDB, AttachmentUpdate]
):
    pass


attachment_crud = AttachmentCRUD(Attachment)
