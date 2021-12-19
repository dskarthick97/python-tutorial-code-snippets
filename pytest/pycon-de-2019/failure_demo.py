from pytest import raises
import pytest


def otherfunc(a, b):
    assert a == b


def somefunc(x, y):
    otherfunc(x, y)


def otherfunc_multi(a, b):
    assert a == b


class TestFailing(object):
    def test_simple(self):
        def f():
            return 42

        def g():
            return 43

        assert f() == g()

    def test_simple_multiline(self):
        otherfunc_multi(42, 6 * 9)

    def test_not(self):
        def f():
            return 42

        assert not f()


class TestSpecialisedExplanations(object):
    def test_eq_text(self):
        assert "spam" == "eggs"

    def test_eq_similar_text(self):
        assert "foo 1 bar" == "foo 2 bar"

    def test_eq_multiline_text(self):
        assert "foo\nspam\nbar" == "foo\neggs\nbar"

    def test_eq_long_text(self):
        a = "1" * 100 + "a" + "2" * 100
        b = "1" * 100 + "b" + "2" * 100
        assert a == b

    def test_eq_long_text_multiline(self):
        a = "1\n" * 100 + "a" + "2\n" * 100
        b = "1\n" * 100 + "b" + "2\n" * 100
        assert a == b

    def test_eq_list(self):
        assert [0, 1, 2] == [0, 1, 3]

    def test_eq_list_long(self):
        a = [0] * 100 + [1] + [3] * 100
        b = [0] * 100 + [2] + [3] * 100
        assert a == b

    def test_eq_dict(self):
        assert {"a": 0, "b": 1} == {"a": 0, "b": 2}

    def test_eq_set(self):
        assert set([0, 10, 11, 12]) == set([0, 20, 21])

    def test_eq_longer_list(self):
        assert [1, 2] == [1, 2, 3]

    def test_in_list(self):
        assert 1 in [0, 2, 3, 4, 5]

    def test_not_in_text_multiline(self):
        text = "some multiline\ntext\nwhich\nincludes foo\nand a\ntail"
        assert "foo" not in text

    def test_not_in_text_single(self):
        text = "single foo line"
        assert "foo" not in text

    def test_not_in_text_single_long(self):
        text = "head " * 50 + "foo " + "tail " * 20
        assert "foo" not in text

    def test_not_in_text_single_long_term(self):
        text = "head " * 10 + "f" * 5 + "tail " * 10
        assert "f" * 5 not in text


def test_attribute():
    class Foo(object):
        b = 1

    i = Foo()
    assert i.b == 2


def test_attribute_instance():
    class Foo(object):
        b = 1

    assert Foo().b == 2


def test_attribute_failure():
    class Foo(object):
        def _get_b(self):
            raise Exception("Failed to get attrib")

        b = property(_get_b)

    i = Foo()
    assert i.b == 2


def test_attribute_multiple():
    class Foo(object):
        b = 1

    class Bar(object):
        b = 2

    assert Foo().b == Bar().b


def globf(x):
    return x + 1


class TestRaises:
    def test_raises(self):
        s = "qwe"
        with pytest.raises(TypeError):
            int(s)

    def test_raises_doesnt(self):
        with pytest.raises(TypeError):
            int(3)

    def test_tupleerror(self):
        a, b = [1]

    def test_reinterpret_fails_with_print_for_the_fun_of_it(self):
        l = [1, 2, 3]
        print("l is %r" % l)
        a, b = l.pop()

    def func1(self):
        assert 41 == 42


class TestMoreErrors:
    def test_complex_error(self):
        def f():
            return 44

        def g():
            return 43

        somefunc(f(), g())

    def test_z1_unpack_error(self):
        l = []
        a, b = l

    def test_z2_type_error(self):
        l = 3
        a, b = l

    def test_startswith(self):
        s = "123"
        g = "456"
        assert s.startswith(g)

    def test_startswith_nested(self):
        def f():
            return "123"

        def g():
            return "456"

        assert f().startswith(g())

    def test_global_func(self):
        assert isinstance(globf(42), float)

    def test_instance(self):
        self.x = 6 * 7
        assert self.x != 42

    def test_compare(self):
        assert globf(10) < 5
