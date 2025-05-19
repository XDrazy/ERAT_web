from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os

from logic.student_manager import StudentManager
from logic.course_manager import CourseManager
from logic.report_parser import ReportParser
from logic.stat_exporter import StatExporter

def get_root_dir():
    path = os.path.join('data', 'root_dir.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def set_root_dir(new_dir):
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data', 'root_dir.txt'), 'w', encoding='utf-8') as f:
        f.write(new_dir.strip())

app = Flask(__name__)
app.secret_key = "supersecret"
app.config['REPORT_ROOT_DIR'] = get_root_dir()

sm = StudentManager()
cm = CourseManager()
report_parser = ReportParser(sm, cm)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        root_dir = request.form.get('root_dir')
        if root_dir:
            app.config['REPORT_ROOT_DIR'] = root_dir
            set_root_dir(root_dir)
            flash('实验报告根目录设置成功')
    root_dir = app.config.get('REPORT_ROOT_DIR', None)
    return render_template('index.html', root_dir=root_dir)

@app.route('/set_root_dir', methods=['POST'])
def set_root_dir_route():
    root_dir = request.form.get('root_dir')
    if root_dir:
        app.config['REPORT_ROOT_DIR'] = root_dir
        set_root_dir(root_dir)
        flash('实验报告根目录设置成功')
    return redirect(request.referrer or url_for('index'))

@app.route('/classes', methods=['GET', 'POST'])
def class_manage():
    if request.method == 'POST':
        cname = request.form['class_name']
        sm.add_class(cname)
        flash("添加班级成功")
    classes = sm.get_classes()
    return render_template('class_manage.html', classes=classes)

@app.route('/classes/delete/<int:cid>')
def delete_class(cid):
    sm.delete_class(cid)
    flash("删除班级成功")
    return redirect(url_for('class_manage'))

@app.route('/classes/import', methods=['POST'])
def import_students():
    file = request.files['student_file']
    class_id = int(request.form['class_id'])
    filename = file.filename
    save_path = os.path.join("uploads", filename)
    file.save(save_path)
    count = sm.import_students_from_excel(save_path, class_id)
    flash(f"导入{count}名学生成功")
    return redirect(url_for('class_manage'))

@app.route('/students/<int:class_id>', methods=['GET', 'POST'])
def student_manage(class_id):
    if request.method == 'POST':
        student = {
            '学号': request.form['sid'],
            '姓名': request.form['name'],
            '年级': request.form['grade'],
            '专业': request.form['major'],
            '班级': next((c['name'] for c in sm.get_classes() if c['id'] == class_id), '')
        }
        sm.add_student(class_id, student)
        flash("添加学生成功")
    students = sm.get_students(class_id).to_dict(orient='records')
    class_name = next((c['name'] for c in sm.get_classes() if c['id'] == class_id), '')
    return render_template('student_manage.html', students=students, class_id=class_id, class_name=class_name)

@app.route('/students/<int:class_id>/delete/<sid>')
def student_delete(class_id, sid):
    sm.delete_student(class_id, sid)
    flash("删除学生成功")
    return redirect(url_for('student_manage', class_id=class_id))

@app.route('/students/<int:class_id>/edit/<sid>', methods=['GET', 'POST'])
def student_edit(class_id, sid):
    df = sm.get_students(class_id)
    stu = df[df['学号'] == sid].iloc[0].to_dict()
    if request.method == 'POST':
        new_student = {
            '学号': request.form['sid'],
            '姓名': request.form['name'],
            '年级': request.form['grade'],
            '专业': request.form['major'],
            '班级': next((c['name'] for c in sm.get_classes() if c['id'] == class_id), '')
        }
        sm.update_student(class_id, sid, new_student)
        flash("修改成功")
        return redirect(url_for('student_manage', class_id=class_id))
    return render_template('student_edit.html', stu=stu, class_id=class_id)

@app.route('/courses', methods=['GET', 'POST'])
def course_manage():
    if request.method == 'POST':
        cname = request.form['course_name']
        cm.add_course(cname)
        flash("添加课程成功")
    courses = cm.get_courses()
    return render_template('course_manage.html', courses=courses)

@app.route('/courses/delete/<int:cid>')
def delete_course(cid):
    cm.delete_course(cid)
    flash("删除课程成功")
    return redirect(url_for('course_manage'))

@app.route('/stat', methods=['GET', 'POST'])
def stat_manage():
    classes = sm.get_classes()
    courses = cm.get_courses()
    result = None
    plot_url = None
    root_dir = app.config.get('REPORT_ROOT_DIR')
    if request.method == 'POST':
        class_id = int(request.form['class_id'])
        course_id = int(request.form['course_id'])
        if not root_dir:
            flash('请先设置实验报告根目录！')
            return redirect(url_for('index'))
        student_stat, exp_stat = report_parser.parse_reports(root_dir, class_id, course_id)
        result = {'student_stat': student_stat, 'exp_stat': exp_stat, 'class_id': class_id, 'course_id': course_id, 'report_root': root_dir}
        if student_stat:
            plot_url = url_for('stat_plot', class_id=class_id, course_id=course_id, report_root=root_dir)
        app.config['STAT_RESULT'] = (student_stat, exp_stat)
    return render_template('stat_manage.html', classes=classes, courses=courses, result=result, plot_url=plot_url, root_dir=root_dir)

@app.route('/stat/plot')
def stat_plot():
    class_id = int(request.args.get('class_id'))
    course_id = int(request.args.get('course_id'))
    root_dir = app.config.get('REPORT_ROOT_DIR')
    img_path = report_parser.visualize_submit_rate(root_dir, class_id, course_id)
    return send_file(img_path, mimetype='image/png')

@app.route('/stat/export')
def stat_export():
    student_stat, exp_stat = app.config.get('STAT_RESULT', ({}, {}))
    file_path = StatExporter.export(student_stat, exp_stat, "excel")
    return send_file(file_path, as_attachment=True)

@app.route('/init_exp_dir', methods=['GET', 'POST'])
def init_exp_dir():
    courses = cm.get_courses()
    classes = sm.get_classes()
    msg = ""
    root_dir = app.config.get('REPORT_ROOT_DIR')
    if request.method == 'POST':
        course_id = int(request.form['course_id'])
        class_id = int(request.form['class_id'])
        exp_name = request.form['exp_name']
        if not root_dir:
            flash('请先设置实验报告根目录！')
            return redirect(url_for('index'))
        course_name = next((c['name'] for c in courses if c['id'] == course_id), '')
        class_name = next((c['name'] for c in classes if c['id'] == class_id), '')
        dir_path = os.path.join(root_dir, course_name, class_name, exp_name)
        os.makedirs(dir_path, exist_ok=True)
        msg = f"已创建目录：{dir_path}"
    return render_template('init_exp_dir.html', courses=courses, classes=classes, msg=msg, root_dir=root_dir)

if __name__ == '__main__':
    for d in ['uploads', 'data', 'static']:
        os.makedirs(d, exist_ok=True)
    app.run(debug=True)
