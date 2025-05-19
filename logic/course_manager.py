import os
import json

class CourseManager:
    def __init__(self):
        self.courses = []
        self._courses_path = os.path.join('data', 'courses.json')
        self.load_courses()

    def save_courses(self):
        os.makedirs('data', exist_ok=True)
        with open(self._courses_path, 'w', encoding='utf-8') as f:
            json.dump(self.courses, f, ensure_ascii=False, indent=2)

    def load_courses(self):
        if os.path.exists(self._courses_path):
            with open(self._courses_path, 'r', encoding='utf-8') as f:
                self.courses = json.load(f)
        else:
            self.courses = []

    def add_course(self, name):
        if self.courses:
            cid = max(c['id'] for c in self.courses) + 1
        else:
            cid = 1
        self.courses.append({'id': cid, 'name': name})
        self.save_courses()

    def delete_course(self, cid):
        self.courses = [c for c in self.courses if c['id'] != cid]
        self.save_courses()

    def get_courses(self):
        return self.courses
