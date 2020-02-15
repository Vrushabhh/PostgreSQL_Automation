from Utility import establishConnection


class Test(object):

    def test_DB_Connection(self):
        assert establishConnection.database_connection('Test-01') != ""

    def test_Execute_Query(self):
        record = establishConnection.execute_query(self,'Test-02')
        assert record != ""
