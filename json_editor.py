import json

class json_editor:
    def __init__(self, path, options=None):
        self.path = path
        self.options = options or {}
        self.options.setdefault('stringify_width', 2)
        self.options.setdefault('stringify_fn', None)
        self.options.setdefault('stringify_eol', False)
        self.options.setdefault('ignore_dots', False)
        self.options.setdefault('autosave', False)
        self.data = self.read()

    def set(self, path, value, options=None):
        options = options or {}
        if isinstance(path, dict):
            for key, val in path.items():
                self._set_value(self.data, key, val, options)
        elif self.options['ignore_dots']:
            self.data[path] = value
        else:
            self._set_value(self.data, path, value, options)
        
        if self.options['autosave']:
            self.save()
        
        return self

    def get(self, path=None):
        if path:
            return self.data[path] if self.options['ignore_dots'] else self._find_value(self.data, path)
        return self.data

    def unset(self, path):
        return self.set(path, None)

    def append(self, path, value):
        data = self.get(path)
        data = data if isinstance(data, list) else []
        if not isinstance(data, list):
            raise ValueError("The data is not a list!")
        data.append(value)
        self.set(path, data)
        return self

    def pop(self, path):
        data = self.get(path)
        if not isinstance(data, list):
            raise ValueError("The data is not a list!")
        data.pop()
        self.set(path, data)
        return self

    def read(self):
        try:
            with open(self.path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def write(self, content):
        with open(self.path, 'w') as file:
            file.write(content)
        return self

    def empty(self):
        return self.write("{}")

    def save(self):
        data = json.dumps(self.data, indent=self.options['stringify_width'], default=self.options['stringify_fn'])
        if self.options['stringify_eol']:
            data += '\n'
        self.write(data)
        return self

    def _set_value(self, obj, path, value, options):
        if '.' in path and not options.get('ignore_dots'):
            keys = path.split('.')
            for key in keys[:-1]:
                obj = obj.setdefault(key, {})
            obj[keys[-1]] = value
        else:
            obj[path] = value

    def _find_value(self, obj, path):
        if '.' in path and not self.options['ignore_dots']:
            keys = path.split('.')
            for key in keys:
                if key in obj:
                    obj = obj[key]
                else:
                    return None
            return obj
        return obj.get(path, None)


def edit_json_file(path, options=None):
    return JsonEditor(path, options)
