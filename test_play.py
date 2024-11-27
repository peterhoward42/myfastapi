def test_something():
        assert 3 == 3

class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_plain_fn_arguments(self):
        def fn(name, age):
            return (age,name)
         
        assert(fn('peter', 42) == (42, 'peter'))

    def test_starargs_fn_arguments(self):
        def fn(*args):
            return args
        # Provided discrete args are harvested and delivered to *args as a single tuple.
        assert(fn('peter', 42) == ('peter', 42))

    def test_starstartargs_fn_arguments(self):
        def fn(**kwargs):
            return kwargs
        assert(fn(name='peter', age=42) == {'age': 42, 'name': 'peter'})