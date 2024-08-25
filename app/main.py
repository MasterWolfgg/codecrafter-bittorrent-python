import json
import sys
import bencodepy

# import bencodepy - available if you need it!
# import requests - available if you need it!

# Examples:
#
# - decode_bencode(b"5:hello") -> b"hello"
# - decode_bencode(b"10:hello12345") -> b"hello12345"
# def decode_bencode(bencoded_value):
#     def extract_string(data):
#         length, rest = data.split(b":",1)
#         length = int(length)
#         return rest[:length] , rest[length:]
#     # recursive decoding 
#     def decode (data):
#         if data[0:1].isdigit() :
#             decoded_str, rest = extract_string(data)
#             return decoded_str, rest
#         elif data.startswith(b'i'):
#             end=data.index(b'e')
#             return int(data[1:end]), data[end+1:]
#         elif data.startswith(b'l'):
#             data=data[1:]
#             result=[]
#             while not data.startswith(b'e'):
#                 item, data=decode(data)
#                 result.append(item)
#             return result, data[1:]
#         else :
#             raise ValueError("Unsupported or invalid bencode value ")
bc = bencodepy.Bencode(encoding="utf-8")
def decode_bencode(bencoded_value):
    return bc.decode(bencoded_value)
    

    
    # decoded_value, _ = decode(bencoded_value)
    # return decoded_value

# def extract_torrent_info(torrent_file):
#     with open (torrent_file,'rb') as tf:
#         cont=tf.read()
#     decode=decode_bencode(cont)
#     if 'announce' not in decode or 'info' not in decode:
#         raise ValueError("Invalid torrent file")
#     tracker_url= decode['announce'].decode('utf-8')
#     length= decode['info']['length']
#     return tracker_url, length

def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")
    # elif command =="info":
    #     torrent_file=sys.argv[2]
    #     tracker_url, file_length =extract_torrent_info(torrent_file)
    #     print(f"Tracker URL:{tracker_url} ")
    #     print(f"Length:{file_length} ")
    
        # Uncomment this block to pass the first stage
        print(json.dumps(decode_bencode(bencoded_value), default=bytes_to_str))
    
    elif command == "info":
        file_name = sys.argv[2]
        with open(file_name, "rb") as torrent_file:
            bencoded_content = torrent_file.read()
        torrent = decode_bencode(bencoded_content)
        print("Tracker URL:", torrent["announce"].decode())
        print("Length:", torrent["info"]["length"])
    
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
