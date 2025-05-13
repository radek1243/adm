import psycopg2
import os
import dotenv

class DBPostgreSQL:
    def __init__(self):
        self.conn = None

    def __connect__(self):
        dotenv.load_dotenv(os.path.dirname(__file__)+"/.env.pgsql")
        if self.conn is None:
            self.conn = psycopg2.connect(database=os.getenv('DATABASE'),user=os.getenv('DBUSER'),password=os.getenv('PASSWORD'),host=os.getenv('HOST'))

    def __close__(self):
        if self.conn is not None:
            self.conn.close()

    def __commit__(self):
        if self.conn is not None:
            self.conn.commit()

    def __rollback__(self):
        if self.conn is not None:
            self.conn.rollback()

    def __get_cursor__(self):
        if self.conn is not None:
            return self.conn.cursor()

    def add_host(self, hostname: str, ip: str):
        try:
            self.__connect__()
            cur = self.__get_cursor__()
            cur.execute("insert into inv.host (name,ip) values (%s,%s)",[hostname, ip])
            self.__commit__()
            self.__close__()
            print(f"Host: {hostname} added.")
        except Exception as ex:
            print(f"Error during inserting host!\n{ex}")

    def add_host_variable(self, hostname: str, varname: str, varvalue: str | list[str]):
        try:
            tempvarvalue=''
            if isinstance(varvalue,list):
                for l in varvalue:
                    tempvarvalue+=l+','
                tempvarvalue=tempvarvalue.removesuffix(',')
            else:
                tempvarvalue=varvalue
            self.__connect__()
            cur = self.__get_cursor__()
            cur.execute('select id from inv.host where name=%s',[hostname])
            id = cur.fetchall()[0][0]
            cur.execute('insert into inv.hostvars (name,value,hostid) values (%s,%s,%s)',[varname, tempvarvalue, id])
            self.__commit__()
            self.__close__()
            print(f'Variable {varname} added to host {hostname}')
        except Exception as ex:
            print(f"Error during inserting host variable!\n{ex}")

    def add_group(self, groupname: str, parentgroup: str | None = None):
        try:
            self.__connect__()
            cur = self.__get_cursor__()
            pgid = None
            if parentgroup is not None:
                cur.execute('select id from inv.group where name=%s',[parentgroup])
                pgid=cur.fetchall()[0][0]
                cur.execute("insert into inv.group (name,parent_group_id) values (%s,%s)",[groupname, int(pgid)])
            else:
                cur.execute("insert into inv.group (name) values (%s)",[groupname])
            self.__commit__()
            self.__close__()
            print(f"Group: {groupname} added.")
        except Exception as ex:
            print(f"Error during inserting host!\n{ex}")

    def add_group_variable(self, groupname: str, varname: str, varvalue: str | list[str]):
        try:
            tempvarvalue=''
            if isinstance(varvalue,list):
                for l in varvalue:
                    tempvarvalue+=l+','
                tempvarvalue=tempvarvalue.removesuffix(',')
            else:
                tempvarvalue=varvalue
            self.__connect__()
            cur = self.__get_cursor__()
            cur.execute('select id from inv.group where name=%s',[groupname])
            id = cur.fetchall()[0][0]
            cur.execute('insert into inv.groupvars (name,value,groupid) values (%s,%s,%s)',[varname, tempvarvalue, id])
            self.__commit__()
            self.__close__()
            print(f'Variable {varname} added to group {groupname}')
        except Exception as ex:
            print(f"Error during inserting host variable!\n{ex}")

    def add_host_to_group(self, hostname: str, groupname: str):
        try:
            self.__connect__()
            cur = self.__get_cursor__()
            cur.execute('select id from inv.host where name=%s',[hostname])
            hid = cur.fetchall()[0][0]
            cur.execute('select id from inv.group where name=%s',[groupname])
            gid = cur.fetchall()[0][0]
            cur.execute('insert into inv.host_group (hostid,groupid) values (%s,%s)',[hid,gid])
            self.__commit__()
            self.__close__()
            print(f'Host {hostname} added to group {groupname}')
        except Exception as ex:
            print(f"Error during inserting host variable!\n{ex}")

    def remove_host():
        pass

    def remove_host_variable():
        pass

    def remove_group():
        pass

    def remove_host_from_group():
        pass

db = DBPostgreSQL()
db.add_host_to_group('ansible-vm','grupa3')