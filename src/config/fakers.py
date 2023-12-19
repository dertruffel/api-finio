import os
import faker
import random
from faker.providers import BaseProvider

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


class StaticFileProvider(BaseProvider):
    media_file_counters = {}
    base_dir = settings.STATICFILES_DIRS[0]
    use_loop = True

    def static_image(self, from_folder=''):
        path = self._get_path(from_folder)
        filenames = self._get_filenames(path, ('.jpeg', '.jpg', '.png'))
        filename = self._select_filename(filenames, path)
        return self._to_simple_uploaded_file(path, filename)

    def static_pdf(self, from_folder=''):
        path = self._get_path(from_folder)
        filenames = self._get_filenames(path, ('.pdf',))
        filename = self._select_filename(filenames, path)
        return self._to_simple_uploaded_file(path, filename)

    def _get_path(self, folder):
        return os.path.join(self.base_dir, folder)

    def _get_filenames(self, path, extensions):
        filenames = os.listdir(path)
        return [f for f in filenames if any(f.endswith(e) for e in extensions)]

    def _select_filename(self, filenames, path):
        if self.use_loop:
            self.media_file_counters.setdefault(path, 0)
            idx = self.media_file_counters[path]
            self.media_file_counters[path] += 1
            return filenames[idx % len(filenames)]
        else:
            return random.choice(filenames)

    def _to_simple_uploaded_file(self, path, filename):
        full_path = os.path.join(path, filename)
        file = open(full_path, 'rb')
        return SimpleUploadedFile(name=filename, content=file.read(), content_type='image/jpg')


class LoremProvider(BaseProvider):
    WORDS = (
        'adipisci aliquam amet consectetur dolor dolore dolorem eius est et'
        'incidunt ipsum labore magnam modi neque non numquam porro quaerat qui'
        'quia quisquam sed sit tempora ut velit voluptatem'
    ).split()

    def lorem_sentence(self, nb_words=10):
        n = random.randint(3, nb_words)
        s = ' '.join(random.choice(self.WORDS) for _ in range(n))
        return s[0].upper() + s[1:] + '.'

    def lorem_paragraph(self, nb_sentences=10):
        n = random.randint(3, nb_sentences)
        return ' '.join(self.lorem_sentence() for _ in range(n))


fake = faker.Faker()
fake.add_provider(StaticFileProvider)
fake.add_provider(LoremProvider)
