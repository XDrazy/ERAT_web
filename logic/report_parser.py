import os
import re
from collections import defaultdict
from logic.logger import Logger

class ReportParser:
    def __init__(self, student_manager, course_manager):
        self.sm = student_manager
        self.cm = course_manager

    def parse_reports(self, root_dir, class_id, course_id):
        students_df = self.sm.get_students(class_id)
        if students_df.empty:
            Logger.get_logger().warning("该班级无学生名单，请先导入。")
            return {}, {}
        class_name = next((c['name'] for c in self.sm.get_classes() if c['id'] == class_id), '')
        course_name = next((c['name'] for c in self.cm.get_courses() if c['id'] == course_id), '')
        base_path = os.path.join(root_dir, course_name, class_name)
        if not os.path.isdir(base_path):
            Logger.get_logger().warning(f"目录不存在：{base_path}")
            return {}, {}

        student_stat = defaultdict(lambda: {"缺交次数": 0, "缺交实验": []})
        exp_stat = defaultdict(list)

        for exp_dir in os.listdir(base_path):
            exp_path = os.path.join(base_path, exp_dir)
            if not os.path.isdir(exp_path): continue
            submitted = set()
            for file in os.listdir(exp_path):
                m = re.match(r"(.+?)_(\d+?)_(.+?)\.docx?$", file)
                if not m:
                    Logger.get_logger().warning(f"文件名不规范: {file}")
                    continue
                _, sid, name = m.groups()
                if not ((students_df["学号"] == sid) & (students_df["姓名"] == name)).any():
                    Logger.get_logger().warning(f"名单中未找到: {sid} {name} ({file})")
                    continue
                submitted.add((sid, name))
            for _, row in students_df.iterrows():
                sid, name = str(row["学号"]), row["姓名"]
                if (sid, name) not in submitted:
                    student_stat[(sid, name)]["缺交次数"] += 1
                    student_stat[(sid, name)]["缺交实验"].append(exp_dir)
                    exp_stat[exp_dir].append((sid, name))
        return student_stat, exp_stat

    def visualize_submit_rate(self, root_dir, class_id, course_id):
        import matplotlib.pyplot as plt
        import uuid
        import matplotlib

        # 设置支持中文显示
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']   # 中文字体，Windows 默认
        matplotlib.rcParams['axes.unicode_minus'] = False     # 负号显示

        students_df = self.sm.get_students(class_id)
        if students_df.empty:
            return None
        class_name = next((c['name'] for c in self.sm.get_classes() if c['id'] == class_id), '')
        course_name = next((c['name'] for c in self.cm.get_courses() if c['id'] == course_id), '')
        base_path = os.path.join(root_dir, course_name, class_name)
        if not os.path.isdir(base_path):
            return None
        exp_names = []
        submit_rates = []
        for exp_dir in sorted(os.listdir(base_path)):
            exp_path = os.path.join(base_path, exp_dir)
            if not os.path.isdir(exp_path): continue
            exp_names.append(exp_dir)
            total = len(students_df)
            submitted = set()
            for file in os.listdir(exp_path):
                m = re.match(r"(.+?)_(\d+?)_(.+?)\.docx?$", file)
                if not m: continue
                _, sid, name = m.groups()
                if ((students_df["学号"] == sid) & (students_df["姓名"] == name)).any():
                    submitted.add((sid, name))
            submit_rates.append(len(submitted) / total if total else 0)
        plt.figure(figsize=(6, 4))
        plt.plot(exp_names, submit_rates, marker='o')
        plt.xlabel("实验编号", fontsize=12)
        plt.ylabel("提交率", fontsize=12)
        plt.ylim(0, 1)
        plt.title("实验提交率折线图", fontsize=14)
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        plt.tight_layout()
        img_path = os.path.join("static", f"submit_rate_{uuid.uuid4().hex[:8]}.png")
        plt.savefig(img_path)
        plt.close()
        return img_path
