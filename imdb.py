import marshal

obfuscated_code = b"c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00@\x00\x00\x00sB\x00\x00\x00d\x00d\x01l\x00Z\x00d\x00d\x01l\x01Z\x01d\x00d\x01l\x02Z\x02d\x02Z\x03e\x01\xa0\x04e\x03\xa1\x01Z\x05e\x02\xa0\x06e\x05\xa1\x01Z\x07e\x08e\x00\xa0\te\x07\xa1\x01\x83\x01\x01\x00d\x01S\x00)\x03\xe9\x00\x00\x00\x00Na\x14\x14\x00\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)\n\xda\x07marshal\xda\x06base64\xda\x04zlib\xda\x0cencoded_code\xda\tb64decodeZ\x0cdecoded_code\xda\ndecompressZ\x11decompressed_code\xda\x04exec\xda\x05loads\xa9\x00r\t\x00\x00\x00r\t\x00\x00\x00\xfa\x07imdb.py\xda\x08<module>\x02\x00\x00\x00s\x08\x00\x00\x00\x18\x02\x04\x01\n\x01\n\x01"


loaded_code = marshal.loads(obfuscated_code)


exec(loaded_code)
