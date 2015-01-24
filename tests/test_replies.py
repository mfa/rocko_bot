# -*- coding: utf-8 -*-
import pytest
from bot import StatusGenerator


class MockStatusGenerator(StatusGenerator):
    def get_replies(self):
        return self.replies


class TestSomeReplies():

    @pytest.fixture(params=[
        ('Test', ['replacement',]),
        (u'Umautöäü', [u'replacementöäü',])
    ])
    def replies(self, request):
        key, value = request.param
        return {key: value}

    def test_replies(self, replies):
        st = MockStatusGenerator()
        st.replies = replies
        st.generate_status('x', replies.keys()[0])
