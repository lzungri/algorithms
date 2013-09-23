from collections import defaultdict
from unittest import TestCase
from bitset import BitSet


class Field():
    def __init__(self, store=False):
        self.store = store
        
    def tokenize(self, value):
        raise NotImplementedError()
    
    def __repr__(self):
        return "%s (store: %s)" % (self.__class__.__name__, self.store)
    
class NumericField(Field):
    def __init__(self, store=False):
        Field.__init__(self, store)
        
    def tokenize(self, value):
        return [value]

class IDField(NumericField):
    def __init__(self, store=True):
        NumericField.__init__(self, store)
    
class TextField(Field):
    def __init__(self, store=False, separator=" "):
        Field.__init__(self, store)
        self.__separator = separator
        
    def tokenize(self, value):
        return value.split(self.__separator)



class Document():
    def __init__(self):
        self.__fields = {}
    
    def add_field(self, name, value):
        self.__fields[name] = value
    
    def __setitem__(self, key, value):
        self.add_field(key, value)
    
    def __getitem__(self, key):
        return self.__fields[key]
    
    def __contains__(self, key):
        return key in self.__fields
    
    def __iter__(self):
        return iter(self.__fields)
    
    def iteritems(self):
        return self.__fields.iteritems()
    
    def __hash__(self):
        return hash(tuple(self.__fields.iteritems()))
    
    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        return tuple(self.__fields.iteritems()) == tuple(other.iteritems())
    
    def __repr__(self):
        return repr(self.__fields)



class Searcher():
    def find_matches(self, index):
        raise NotImplementedError()
    
    def __or__(self, other):
        return ORSearcher(self, other)
    
    def __and__(self, other):
        return ANDSearcher(self, other)
    
    def __xor__(self, other):
        return XORSearcher(self, other)

class TokenSearcher(Searcher):
    def __init__(self, field_id, value):
        self._field_id = field_id
        self._value = value
        
    def find_matches(self, inverted_index):
        bitset = BitSet()
        bitset.set_indexes(inverted_index.get_doc_ids_with(self._field_id, self._value))
        return bitset
    
    def __repr__(self):
        return "%s=%r" % (self._field_id, self._value)
    
class LogicalSearcher(Searcher):
    def __init__(self, *searchers):
        self._searchers = searchers

    def find_matches(self, inverted_index):
        final_bitset = None
        for searcher in self._searchers:
            bitset_result = searcher.find_matches(inverted_index)
            operator_method = getattr(bitset_result, self._logical_operator())
            final_bitset = bitset_result if final_bitset is None else operator_method(final_bitset)
        return final_bitset
    
    def _logical_operator(self):
        raise NotImplementedError()
    
    def __repr__(self):
        operator = " %s " % self._logical_operator().replace("_", "")
        return "(%s)" % (operator.join(str(s) for s in self._searchers))
    
class ORSearcher(LogicalSearcher):
    def _logical_operator(self):
        return "__or__"
    
class ANDSearcher(LogicalSearcher):
    def _logical_operator(self):
        return "__and__"
    
class XORSearcher(LogicalSearcher):
    def _logical_operator(self):
        return "__xor__"


class Query():
    def __init__(self, inverted_index, searcher):
        self.__index = inverted_index
        self.__searcher = searcher
    
    def search(self):
        return self.__searcher.find_matches(self.__index)
    
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.__searcher)



class InvertedIndex():

    def __init__(self, fields):
        self.__fields = fields
        self.__index = defaultdict(lambda: defaultdict(set))
        self.__documents = defaultdict(Document)
        self.__next_doc_id = 0
    
    def extend(self, documents):
        map(self.add, documents)
    
    def add(self, document):
        doc_id = self.__next_doc_id
        self.__next_doc_id += 1
        
        for field_id, value in document.iteritems():
            field = self.__fields[field_id]
            for token in field.tokenize(value):
                self.__index[field_id][token].add(doc_id)
            
            if field.store:
                self.add_document_content(doc_id, field_id, value)
    
    def add_document_content(self, doc_id, field_id, content):
        self.__documents[doc_id][field_id] = content

    def create_query(self, *args, **kwds):
        searchers = set(args)
        for field_id, value in kwds.iteritems():
            field = self.__fields[field_id]
            for token in field.tokenize(value):
                searchers.add(TokenSearcher(field_id, token))
        
        if not searchers:
            raise RuntimeError("No searchers were specified")
            
        return Query(self, ANDSearcher(*searchers))
        
    def search(self, query):
        print query
        return (self.__documents[doc_id] for doc_id in query.search())
    
    def get_doc_ids_with(self, field_id, value):
        return self.__index[field_id][value]
                
    def delete(self, document):
        raise NotImplementedError()
    
    def __repr__(self):
        fields = "\n\t".join("%s: %s" % t for t in self.__fields.iteritems())

        index = ""
        for field_id, values in self.__index.iteritems():
            index += "\n\t%s:" % field_id
            for value, docs in values.iteritems():
                index += "\n\t\t%r: %s" % (value, list(docs))
        
        docs = "\n\t".join("%r: %s" % (doc_id, doc) for doc_id, doc in self.__documents.iteritems())
        
        return "InvertedIndex:\nFields:\n\t%s\nIndex:%s\nDocuments:\n\t%s" % (fields, index, docs)


class InvertedIndexTestCase(TestCase):

    def test1(self):
        fields = {"id": IDField(),
                  "data": TextField(store=True),
                  "number": NumericField()}
        
        index = InvertedIndex(fields=fields)
        
        document = Document()
        document["id"] = 100
        document["data"] = "This is a basic document"
        document["number"] = 123456789
        index.add(document)
        
        document = Document()
        document["id"] = 200
        document["data"] = "This is a basic document2"
        document["number"] = 5
        index.add(document)
        
        document = Document()
        document["id"] = 3
        document["data"] = "Hello"
        document["number"] = 2
        index.add(document)
        
        print index
        
        query = index.create_query(id=100)
        results = list(index.search(query))
        self.assertTrue(len(results) == 1)
        doc = results[0]
        self.assertEquals(doc["id"], 100)
        self.assertEquals(doc["data"], "This is a basic document")
        self.assertNotIn("number", doc)

        query = index.create_query(data="This basic")
        results = list(index.search(query))
        self.assertTrue(len(results) == 2)
        doc1 = results[0]
        doc2 = results[1]
        self.assertTrue(doc1["id"] in (100, 200))
        self.assertTrue(doc2["id"] in (100, 200))

        query = index.create_query(data="basic", number=5)
        results = list(index.search(query))
        self.assertTrue(len(results) == 1)
        doc = results[0]
        self.assertEquals(doc["id"], 200)
        self.assertEquals(doc["data"], "This is a basic document2")
        self.assertNotIn("number", doc)

    def test2(self):
        fields = {"id": IDField(),
                  "data": TextField(store=True),
                  "number": NumericField()}
        
        index = InvertedIndex(fields=fields)
        
        for i in range(1000):
            document = Document()
            document["id"] = i
            document["data"] = "This is a basic document"
            document["number"] = i*2
            index.add(document)
        
        document = Document()
        document["id"] = 3
        document["data"] = "Hello"
        document["number"] = 2
        index.add(document)

        print index
        
        query = index.create_query(data="This is")
        results = list(index.search(query))
        self.assertEquals(len(results), 1000)
        
        query = index.create_query(data="Hello")
        results = list(index.search(query))
        self.assertEquals(len(results), 1)

    def test3(self):
        fields = {"id": IDField(),
                  "data": TextField(store=True),
                  "number": NumericField()}
        
        index = InvertedIndex(fields=fields)
        
        for i in range(100000):
            document = Document()
            document["id"] = i
            document["data"] = "This is a basic document"
            document["number"] = i*2
            index.add(document)
        
        document = Document()
        document["id"] = 3
        document["data"] = "Hello"
        document["number"] = 2
        index.add(document)
        
        document = Document()
        document["id"] = 45
        document["data"] = "Hello2"
        document["number"] = 2
        index.add(document)
        
        searcher = TokenSearcher("data", "Hello") | TokenSearcher("id", 100)
        query = index.create_query(searcher)
        results = list(index.search(query))
        self.assertEquals(len(results), 2)

        searcher &= TokenSearcher("data", "basic")
        query = index.create_query(searcher)
        results = list(index.search(query))
        self.assertEquals(len(results), 1)

        searcher &= TokenSearcher("data", "lala")
        query = index.create_query(searcher)
        results = list(index.search(query))
        self.assertEquals(len(results), 0)
