# ERAT 实验报告缺交统计系统

## 项目简介

**ERAT（Experiment Report Attendance Tracker）** 是一个基于 Flask、Pandas 和 Excel 的实验报告统计与可视化系统，适用于高校教师管理课程实验报告的收交情况。  
系统支持班级/课程/学生的增删改查、实验报告目录自动初始化、缺交统计、提交率折线图分析和一键导出结果，极大提升实验管理效率。

---

## 项目结构

ERAT_web-master/
├── app.py
├── logic/
│ ├── init.py
│ ├── student_manager.py
│ ├── course_manager.py
│ ├── report_parser.py
│ ├── stat_exporter.py
│ └── logger.py
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── class_manage.html
│ ├── course_manage.html
│ ├── student_manage.html
│ ├── student_edit.html
│ ├── stat_manage.html
│ ├── init_exp_dir.html
├── static/
│ └── style.css
├── uploads/
├── data/

---

## 快速上手

1. **克隆或下载本项目**
2. **安装依赖**

   ```bash
   pip install Flask pandas openpyxl matplotlib
3. **运行主程序**
   ```bash
   python app.py
4. **浏览器访问**
   http://127.0.0.1:5000
