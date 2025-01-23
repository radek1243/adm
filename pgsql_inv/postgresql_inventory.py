from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.inventory import BaseInventoryPlugin
import psycopg2
from ansible.errors import AnsibleParserError

DOCUMENTATION = r'''
    name: postgresql_inventory
    options:
      plugin:
        description: Plugin name
        required: True
        type: string
      db_host:
        description: IP address of database server
        required: True
        type: string
      db_user: 
        description: User with access to database
        required: True
        type: string
      db_pass:
        description: Password for database user
        required: True
        type: string
      db_name:
        description: Database name to connect to
        required: True
        type: string
      db_port:
        description: Port to connect to database
        default: 5432
        required: False
        type: integer
'''


class InventoryModule(BaseInventoryPlugin):

    NAME = 'postgresql_inventory'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def verify_file(self, path):
        ''' return true/false if this is possibly a valid file for this plugin to consume '''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(('postgresql.yaml', 'postgresql.yml', 'pgsql.yaml', 'pgsql.yml')):
                valid = True
        return valid
    

    def parse(self, inventory, loader, path, cache=False):

        # call base method to ensure properties are available for use with other helper methods
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # this method will parse 'common format' inventory sources and
        # update any options declared in DOCUMENTATION as needed
        self._read_config_data(path)
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=self.get_option('db_name'),
                user=self.get_option('db_user'),
                password=self.get_option('db_pass'),
                host=self.get_option('db_host'),
                port=self.get_option('db_port')
            )
            cur = conn.cursor()
            #pobranie wszystkich hostów
            cur.execute("select * from host")
            for host in cur.fetchall():
                self.inventory.add_host(host[1])
                self.inventory.set_variable(host[1],'ansible_host',host[2])
            #pobranie wszystkich zmiennych hostów
            cur.execute("select host.name, hostvars.name, hostvars.value from host join hostvars on host.id=hostvars.hostid")
            for hostvar in cur.fetchall():
                self.inventory.set_variable(hostvar[0],hostvar[1],hostvar[2])
            #pobranie wszystkich grup
            cur.execute('select name from "group"')
            for group in cur.fetchall():
                self.inventory.add_group(group[0])
            #pobranie wszystkich podgrup danych grup
            cur.execute('select parent.name, "group".name from "group" as parent join "group" on parent.id="group".parent_group_id')
            for parent in cur.fetchall():
                self.inventory.add_child(parent[0],parent[1])
            #pobranie zmiennych grupowych
            cur.execute('select "group".name, groupvars.name, groupvars.value from "group" join groupvars on "group".id=groupvars.groupid')
            for groupvar in cur.fetchall():
                self.inventory.set_variable(groupvar[0],groupvar[1],groupvar[2])
            #pobranie grup hostów
            cur.execute('select "group".name, host.name from host join host_group on host.id=host_group.hostid join "group" on "group".id=host_group.groupid')
            for host_group in cur.fetchall():
                self.inventory.add_child(host_group[0],host_group[1])
            cur.close()
        except(Exception,  psycopg2.DatabaseError) as error:
            #print(error)
            raise AnsibleParserError(error)
        finally:
            if conn is not None:
                conn.close()