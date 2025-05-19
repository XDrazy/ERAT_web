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
## 功能特性

- 支持**班级管理、学生名单增删改查**（Excel一键导入/导出）
- 支持**课程管理**与课程下班级实验报告统计
- 支持**实验报告目录自动初始化**（一键批量创建实验文件夹）
- 自动统计每位学生缺交实验数与缺交实验列表
- 自动统计每个实验缺交学生名单
- 实验提交率**可视化折线图**
- 统计结果一键**导出 Excel**
- **全部数据持久化**，重启不丢失
- 支持中文界面，页面简洁美观
  
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
   
---
## 首次使用
- 首次启动，需设置“实验报告根目录”（如 D:/lab_reports）
- 通过导航栏管理班级/课程/学生名单（学生名单可用 Excel 模板导入）
- 实验报告应命名为 实验名_学号_姓名.docx，如 实验1_20230001_张三.docx，放在根目录下对应课程/班级/实验名文件夹
- 支持一键生成实验存放目录，快速初始化
- 统计、分析、导出均在导航栏功能页内一键完成

---
## 实验报告文件命名规范
格式：
```text
实验名_学号_姓名.docx
```
例如：
```text
实验3_20231101_李四.docx
```
必须严格与学生名单匹配（学号/姓名），否则视为未交或不计入
