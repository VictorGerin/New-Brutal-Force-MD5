
import sys
import os
import sqlite3 as lite
from md5 import MD5

class sql(object):

    con = None

    numInsert = 0
    numInsertToCommit = 50000
    
    @classmethod
    def startCon(cls, db):
        cls.con = lite.connect(db)

    @classmethod
    def createTables(cls):
        if cls.con:
            cls.con.cursor().execute('CREATE  TABLE  IF NOT EXISTS "main"."keys" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "key" VARCHAR NOT NULL  UNIQUE , "hash" VARCHAR NOT NULL )')#, "type" INTEGER NOT NULL )')
            cls.con.commit()

    @classmethod
    def verificaKey(cls, key):
        if cls.con:
            cur = cls.con.cursor()
            cur.execute('SELECT * FROM keys WHERE hash = :key ', {'key':key})
            return cur.fetchone()

    @classmethod
    def close(cls):
        if cls.con:
            cls.commit()
            if cls.query_yes_no('Gostaria de copiar o banco de dados para outro lugar ?', 'no'):
                sys.stdout.write('Digite o nome do arquivo : ')
                cls.copyTo(raw_input().lower())
            if cls.getDbToMemory and cls.query_yes_no('Gostaria voltar o banco de dados para o arquivo original ?'):
                os.unlink(cls.getDbToMemory)
                cls.copyTo(cls.getDbToMemory)
            cls.con.close()
            cls.con = None

    @classmethod
    def commit(cls):
        if cls.con:
            cls.con.commit()

    @classmethod
    def loadFrom(cls, fromDB):
        if cls.con:
            cls.copyFromTo(lite.connect(fromDB), cls.con)

    @classmethod
    def copyTo(cls, newDb):
        if cls.con:
            cls.copyFromTo(cls.con, lite.connect(newDb))

    @classmethod
    def copyFromTo(cls, db1, db2):
        dump = db1.iterdump()
        print 'copiando isso pode demorar um pouco por favor nao finalize isso pode significar perda de dados'
        i = 1
        for line in dump:
            db2.executescript(line)
            if i % cls.numInsertToCommit == 0:
                db2.commit()
            i += 1

    @classmethod
    def addDataBase(cls, md5):
        if cls.con:
            cur = cls.con.cursor()
            cur.execute('INSERT INTO "main"."keys" ("key","hash") VALUES (?,?)', (md5.key, md5.calc()))
            cls.numInsert += 1
            if cls.numInsert % cls.numInsertToCommit == 0:
                cls.commit()

    @classmethod
    def query_yes_no(cls, question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.
    
        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)
    
        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")
