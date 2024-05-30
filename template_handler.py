import json

class Template:
    def __init__(self, image_path, title):
        self.image_path = image_path
        self.title = title

    def get_image_path(self):
        return self.image_path

    def get_image_title(self):
        return self.title

class TemplateHandler:
    def __init__(self):
        self.templates = []

    def add_template(self, image_path, title):
        new_template = Template(image_path, title)
        self.templates.append(new_template)

    def save_templates(self, filename="templates.json"):
        with open(filename, 'w') as file:
            json_templates = [{'image_path': t.image_path, 'title': t.title} for t in self.templates]
            json.dump(json_templates, file)

    def load_templates(self, filename="templates.json"):
        try:
            with open(filename, 'r') as file:
                json_templates = json.load(file)
                self.templates = [Template(t['image_path'], t['title']) for t in json_templates]
        except FileNotFoundError:
            self.templates = []

    def get_templates(self):
        return self.templates
