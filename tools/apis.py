import os
from pathlib import Path

from apps.log import logger
from settings.config import Config
from tools.read_png import read
from apps.utils import timing_


class OcrKit(object):
    def __init__(self):
        pass

    @staticmethod
    def get_photos(_request):
        _request_files = _request.files
        if _request_files:
            if 'photo' not in _request_files:
                logger.info(_request_files)
                return False
            else:
                return _request_files.getlist('photo')
        else:
            return False

    def handle_photos(self, photos):
        logger.info('<<<< handle_request photos: {}'.format(photos))
        f_ls = self.save_photos(photos)
        data = []
        for _img in f_ls:
            img_path = ""
            try:
                img_path = str(Path(Config.upload_path) / _img)
                str_img = self.ocr(img_path)
                data.append((_img, str_img))
            except Exception as e:
                logger.error(e)
            finally:
                if os.path.exists(img_path):
                    os.remove(img_path)

        return data

    @staticmethod
    def save_photos(photos):
        # patch_request_class(app)
        f_ls = []
        for _img in photos:
            _img.save(str(Path(Config.upload_path) / _img.filename))
            f_ls.append(_img.filename)
        return f_ls

    @staticmethod
    @timing_
    def ocr(img):
        is_exist = Path(Config.upload_path).exists()
        if not is_exist:
            Path(Config.upload_path).mkdir(parents=True)
        try:
            ret = read(img)
            return ret
        except Exception as e:
            logger.error(e)
            return False


def my_ocr(_request):
    ocr_worker = OcrKit()
    photos = ocr_worker.get_photos(_request)
    if photos is not False:
        ret = ocr_worker.handle_photos(photos)
        if ret:
            return ret, '', 0
        else:
            return False, 'null ocr', 400
    else:
        return False, 'no photos', 400
