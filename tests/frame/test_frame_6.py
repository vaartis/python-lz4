import os
import pytest
import lz4.frame as lz4frame

test_data=[
    b'',
    (128 * (32 * os.urandom(32))),
    (5 * 128 * os.urandom(1024)),
]

@pytest.fixture(
    params=test_data,
    ids=[
        'data' + str(i) for i in range(len(test_data))
    ]
)
def data(request):
    return request.param

compression_levels = [
        (lz4frame.COMPRESSIONLEVEL_MIN),
        # (lz4frame.COMPRESSIONLEVEL_MINHC),
        # (lz4frame.COMPRESSIONLEVEL_MAX),
    ]
@pytest.fixture(
    params=compression_levels
)
def compression_level(request):
    return request.param


def test_lz4frame_open_write(data):
    with lz4frame.open('testfile', mode='wb') as fp:
        fp.write(data)

def test_lz4frame_open_write_read_defaults(data):
    with lz4frame.open('testfile', mode='wb') as fp:
        fp.write(data)
    with lz4frame.open('testfile', mode='r') as fp:
        data_out = fp.read()
    assert data_out == data

def test_lz4frame_open_write_read(
        data,
        compression_level,
        block_linked,
        block_checksum,
        block_size,
        content_checksum,
        auto_flush,
        store_size,
        return_bytearray):

    kwargs = {}

    if store_size is True:
        kwargs['source_size'] = len(data)

    kwargs['compression_level'] = compression_level
    kwargs['block_size'] = block_size
    kwargs['block_linked'] = block_linked
    kwargs['content_checksum'] = content_checksum
    kwargs['block_checksum'] = block_checksum
    kwargs['auto_flush'] = auto_flush
    kwargs['return_bytearray'] = return_bytearray
    kwargs['mode'] = 'wb'

    with lz4frame.open('testfile', **kwargs) as fp:
        fp.write(data)

    with lz4frame.open('testfile', mode='r') as fp:
        data_out = fp.read()

    assert data_out == data
