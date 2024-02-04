from src.api.exceptions import UndefinedSerializerException
from src.api.serializers import serializers
from src.utils import sys_args, CryptionMode

if __name__ == '__main__':
    args = sys_args()

    try:
        serializer = serializers[args.serializer]
    except KeyError:
        raise UndefinedSerializerException(serializer=str(args.serializer))

    kwargs = dict(path=args.input_file, password=args.password)

    if args.mode == CryptionMode.encrypt:
        data = serializer.serialize(**kwargs)
        serializer.loader.write(data, args.output_file + '_encoded')
    elif args.mode == CryptionMode.decrypt:
        data = serializer.deserialize(**kwargs)
        serializer.loader.write_deserialized(
            data=data,
            path=args.output_file + '_decoded'
        )
