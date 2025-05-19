import pandas as pd
import os
import json
from logic.logger import Logger

class StudentManager:
    def __init__(self):
        self.classes = []  # [{'id': int, 'name': str}]
        self.students = {} # class_id: DataFrame
        self._classes_path = os.path.join('data', 'classes.json')
        self.load_classes()

    def save_classes(self):
        os.makedirs('data', exist_ok=True)
        with open(self._classes_path, 'w', encoding='utf-8') as f:
            json.dump(self.classes, f, ensure_ascii=False, indent=2)

    def load_classes(self):
        if os.path.exists(self._classes_path):
            with open(self._classes_path, 'r', encoding='utf-8') as f:
                self.classes = json.load(f)
        else:
            self.classes = []

    def add_class(self, name):
        if self.classes:
            cid = max(c['id'] for c in self.classes) + 1
        else:
            cid = 1
        self.classes.append({'id': cid, 'name': name})
        self.save_classes()

    def delete_class(self, cid):
        self.classes = [c for c in self.classes if c['id'] != cid]
        self.students.pop(cid, None)
        self.save_classes()
        path = os.path.join('data', f'students_{cid}.xlsx')
        if os.path.exists(path):
            os.remove(path)

    def get_classes(self):
        return self.classes

    def save_students(self, class_id):
        os.makedirs('data', exist_ok=True)
        df = self.students.get(class_id)
        if df is not None and not df.empty:
            df.to_excel(os.path.join('data', f'students_{class_id}.xlsx'), index=False)

    def load_students(self, class_id):
        path = os.path.join('data', f'students_{class_id}.xlsx')
        if os.path.exists(path):
            self.students[class_id] = pd.read_excel(path, dtype=str)
        else:
            self.students[class_id] = pd.DataFrame(columns=["学号", "姓名", "年级", "专业", "班级"])

    def import_students_from_excel(self, file_path, class_id):
        try:
            df = pd.read_excel(file_path, dtype=str)
            expected_cols = {'学号', '姓名', '年级', '专业', '班级'}
            if not expected_cols.issubset(set(df.columns)):
                Logger.get_logger().warning("Excel表头不正确，需包含：%s" % expected_cols)
                return 0
            self.students[class_id] = df
            self.save_students(class_id)
            Logger.get_logger().info(f"成功导入{len(df)}名学生")
            return len(df)
        except Exception as e:
            Logger.get_logger().error(f"导入学生失败：{e}")
            return 0

    def get_students(self, class_id):
        if class_id not in self.students:
            self.load_students(class_id)
        return self.students.get(class_id, pd.DataFrame(columns=["学号", "姓名", "年级", "专业", "班级"]))

    def add_student(self, class_id, student):
        if class_id not in self.students:
            self.load_students(class_id)
        df = self.students.get(class_id)
        self.students[class_id] = pd.concat([df, pd.DataFrame([student])], ignore_index=True)
        self.save_students(class_id)

    def delete_student(self, class_id, sid):
        if class_id not in self.students:
            self.load_students(class_id)
        df = self.students.get(class_id)
        df = df[df['学号'] != sid]
        self.students[class_id] = df
        self.save_students(class_id)

    def update_student(self, class_id, old_sid, new_student):
        if class_id not in self.students:
            self.load_students(class_id)
        df = self.students.get(class_id)
        idx = df[df['学号'] == old_sid].index
        if not idx.empty:
            df.loc[idx[0]] = new_student
        self.students[class_id] = df
        self.save_students(class_id)
