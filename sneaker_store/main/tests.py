from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.utils.html import format_html

from .models import ShoeModel
from .admin import ShoeModelAdmin

class MockRequest:
    pass

class ShoeModelAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_image_tag(self):
        obj = ShoeModel(image='path/to/image.jpg')
        admin = ShoeModelAdmin(ShoeModel, self.site)
        self.assertEqual(
            admin.image_tag(obj),
            format_html('<img src="{}" width="70" height="50" />', obj.image.url)
        )

        obj_no_image = ShoeModel()
        self.assertEqual(
            admin.image_tag(obj_no_image),
            format_html('<span class="no-image">No Image</span>')
        )
