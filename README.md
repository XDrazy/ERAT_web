# ERAT 实验报告缺交统计系统

## 项目简介

**ERAT（Experiment Report Attendance Tracker）** 是一款基于 Flask、Pandas 和 Excel 的高校实验报告缺交统计与可视化系统。  
本系统支持班级、课程和学生名单管理，自动统计缺交实验报告情况，生成可视化提交率曲线，并一键导出统计结果，大幅提升教师实验管理效率。

---

## 项目结构

```text
your_project/
├── app.py
├── logic/
│   ├── __init__.py
│   ├── student_manager.py
│   ├── course_manager.py
│   ├── report_parser.py
│   ├── stat_exporter.py
│   └── logger.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── class_manage.html
│   ├── course_manage.html
│   ├── student_manage.html
│   ├── student_edit.html
│   ├── stat_manage.html
│   ├── init_exp_dir.html
├── static/
│   └── style.css
├── uploads/
├── data/
```

---
## 快速上手
1. **克隆或下载本项目**
2. **安装依赖**

   ```bash
   pip install Flask pandas openpyxl matplotlib
   ```
3. **运行主程序**
   ```bash
   python app.py
   ```
4. **浏览器访问**
   http://127.0.0.1:5000
