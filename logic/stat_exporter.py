import pandas as pd
from logic.logger import Logger

class StatExporter:
    @staticmethod
    def export(student_stat, exp_stat, file_type="excel"):
        rows = []
        for (sid, name), stat in student_stat.items():
            rows.append([sid, name, stat["缺交次数"], "、".join(stat["缺交实验"])])
        df = pd.DataFrame(rows, columns=["学号", "姓名", "缺交次数", "缺交实验列表"])
        if file_type == "excel":
            path = "data/stat_result.xlsx"
            df.to_excel(path, index=False)
            Logger.get_logger().info(f"结果导出到 {path}")
            return path
        elif file_type == "csv":
            path = "data/stat_result.csv"
            df.to_csv(path, index=False)
            Logger.get_logger().info(f"结果导出到 {path}")
            return path
