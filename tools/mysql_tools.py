import os

from mysql.connector import connect

from utils.logger_utils import logger


def get_db_config():
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),  # 主机号
        "port": int(os.getenv("MYSQL_PORT", "3306")),  # 端口号
        "user": os.getenv("MYSQL_USER"),  # 用户名
        "password": os.getenv("MYSQL_PASSWORD"),  # 密码
        "database": os.getenv("MYSQL_DATABASE"),  # 数据库名
        "charset": os.getenv("MYSQL_CHARSET", "utf8mb4"),  # 字符集
        "autocommit": True,  # 自动提交事务
    }
    # 过滤掉值None的项
    config = {k: v for k,v in config.items() if v is not None}
    # 检查是否缺少必要配置项，如果缺少，抛出错误
    required_keys = ["user", "password", "database"]
    missing_keys = [k for k in required_keys if k not in config]
    if missing_keys:
        raise ValueError(f"缺少必要配置项: {','.join(missing_keys)}")
    # 返回配置
    return config

_db_config = get_db_config()


def list_sql_tables()->str:
    """
            列出数据库中所有可用的表
        :return:   有表： 可用的表：a,b,c  没表：没有可用的表
    """
    logger.info("----正在查询数据库中的表名...")
    try:
        with connect(**_db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                rows = cursor.fetchall()
                if not rows:
                    return "没有可用表"
                result = ",".join([item[0] for item in rows])
                logger.info(f"可用的表：{result}")
                return f"可用的表：{result}"
    except Exception as e:
        return f"连接数据库失败：{str(e)}"

def get_table_data(table_name:str)->str:
    """
        获取指定表名的前至多100条数据列表，同时带字段名列表
        :param table_name: 表名
        :return:

         表数据
        id   name    age
        1  二狗子    18
        2  驴蛋蛋    19

        返回的结果数据： "id,name,age\n1,二狗子,1\n2,驴蛋蛋,19"
    """
    logger.info(f"----正在查询{table_name}表的数据...")
    try:
        with connect(**_db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
                rows = cursor.fetchall()
                if not rows:
                    return "没有可用数据"
                column_names_str = ','.join(cursor.column_names)
                row_values_str = "\n".join([",".join(map(str, row)) for row in rows])
                result = column_names_str + "\n" + row_values_str

                logger.info(f"查询{table_name}的数据列表：{result}")
                return result
    except Exception as e:
        return f"连接数据库失败：{str(e)}"


def execute_sql_query(sql)->str:
    """
       根据指定sql执行，返回查询的结果
       :param sql: 由大模型生成的sql
       :return:  字段列表和数据列表的字符串
    """
    logger.info(f"----正在执行{sql}...")
    try:
        with connect(**_db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"{sql}")
                rows = cursor.fetchall()
                if not rows:
                    return f"执行语句{sql},结果没有数据"
                column_names_str = ','.join(cursor.column_names)
                row_values_str = "\n".join([",".join(map(str, row)) for row in rows])
                result = column_names_str + "\n" + row_values_str

                logger.info(f"执行{sql}的结果：{result}")
                return result
    except Exception as e:
        return f"连接数据库失败：{str(e)}"